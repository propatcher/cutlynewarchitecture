from fastapi import APIRouter, Depends, HTTPException

from app.api.dependecies import get_user_service
from app.api.schemas.users_schema import UserRegisterRequest, UserResponse
from app.domain.entities.user import User
from app.services.user_services import UserService
from app.domain.exceptions.user_exceptions import UserAlreadyExists
router = APIRouter(
    prefix = "/users",
    tags=["Пользователи"]
)

@router.post("/register",
            summary="Register user",
            description="Return the access token if succes else error",
            responses={
                409: {"description": "User already exist"},
            },
            response_model=UserResponse)
async def new_user(user_data: UserRegisterRequest, user_service: UserService = Depends(get_user_service)) -> User:
    try:
        user = await user_service.register_user(
            login=user_data.login,
            email=user_data.email,
            password=user_data.password
        )
        return UserResponse(
            id=user.id,
            login=user.login,
            email=user.email,
            created_at=user.created_at
        )
    except UserAlreadyExists as e:
        raise HTTPException(status_code=409,detail=str(e))  
        


# @router.get(
#     "/me",
#     response_model=UserResponse,
#     summary="Get current user",
#     description="Returns the currently authenticated user's profile",
#     responses={
#         200: {"description": "Success"},
#         401: {"description": "Not authenticated"},
#         404: {"description": "User not found"}
#     }
# )
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user
