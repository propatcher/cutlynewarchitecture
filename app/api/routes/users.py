from datetime import timedelta
from typing import Annotated, Optional, Union
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from app.api.dependecies import get_current_user, get_user_service
from app.api.schemas.users_schema import TokenResponse, UserLoginRequest, UserRegisterRequest, UserRegisterResponse, UserResponse
from app.domain.entities.user import User
from app.services.user_services import UserService
from app.domain.exceptions.user_exceptions import UserAlreadyExists, UserWrongData
from app.settings import config
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
                422: {"description": "Validation Error"}
            },
            response_model=UserRegisterResponse)
async def new_user(user_data: UserRegisterRequest, user_service: UserService = Depends(get_user_service)) -> UserRegisterResponse:
    try:
        registed_user = await user_service.register_user(
            login=user_data.login,
            email=user_data.email,
            password=user_data.password
        )
        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(
            data={"sub": registed_user.login, "type": "access", "user_id": str(registed_user.id)}, expires_delta=access_token_expires
        )
        return UserRegisterResponse(
        user = UserResponse(
            id=registed_user.id,
            login=registed_user.login,
            email=registed_user.email,
            created_at=registed_user.created_at
        ),
        token = TokenResponse(
            access_token=access_token,
            token_type = "bearer"
        ))
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
    
@router.post("/token",             
             summary="Login user",
             description="Login user with token return",
             responses={
                422: {"description": "Validation Error"},
                
            },
             response_model=TokenResponse)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(),user_service: UserService = Depends(get_user_service)) -> TokenResponse:
    try:
        user, token = await user_service.get_token_and_authenticate_user(
            username=form_data.username,
            password=form_data.password
        )
        
        return TokenResponse(
            access_token=token,
            token_type="bearer"
            
        )
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)

@router.post("/login",
             summary="Login user",
             description="Login user with token return",
             responses={
                422: {"description": "Validation Error"},
                
            },
            response_model=UserRegisterResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),user_service: UserService = Depends(get_user_service)) -> UserRegisterResponse:
    try:
        user, token = await user_service.get_token_and_authenticate_user(username=form_data.username, password=form_data.password)
        return UserRegisterResponse(
            user = UserResponse(
                id=user.id,
                login=user.login,
                email=user.email,
                created_at=user.created_at
            ),
            token = TokenResponse(
                access_token=token,
                token_type = "bearer"
            ))
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
    
@router.patch("/me",
              summary="About me",
              description="Get info about login user",
              responses={
                  422: {"description": "Validation Error"},
              },
              response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=current_user.user.id,
        login=current_user.login,
        email=current_user.email,
        created_at=current_user.created_at  
    )
     