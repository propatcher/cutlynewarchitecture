from typing import Optional
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response

from app.api.dependecies import get_user_service
from app.api.schemas.users_schema import UserRegisterRequest, UserResponse
from app.domain.entities.user import User
from app.services.user_services import UserService
from app.domain.exceptions.user_exceptions import UserAlreadyExists
router = APIRouter(
    prefix = "/users",
    tags=["Пользователи"]
)
from app.infra.auth.token_setter import create_access_token

@router.post("/register",
            summary="Register user",
            description="Return the access token if succes else error",
            responses={
                409: {"description": "User already exist"},
            },
            response_model=UserResponse)
async def new_user(response: Response,user_data: UserRegisterRequest, user_service: UserService = Depends(get_user_service), cutly_auth_token: Optional[str] = Cookie(None)) -> User:
    try:
        user = await user_service.register_user(
            login=user_data.login,
            email=user_data.email,
            password=user_data.password
        )
        if cutly_auth_token is None:
            access_token = create_access_token({"sub": str(user.id)})
            response.set_cookie(
            "cutly_auth_token",
            access_token,
            httponly=True,
            )
        return UserResponse(
            id=user.id,
            login=user.login,
            email=user.email,
            created_at=user.created_at
        )
    except UserAlreadyExists as e:
        raise HTTPException(status_code=409,detail=str(e))  
        