from fastapi import APIRouter, Depends

from app.api.schemas.users_schema import SUserRegistration
from app.domain.entities.user import User
from app.services.user_services import UserService
router = APIRouter(
    prefix = "/users",
    tags=["users"]
)

@router.post("/register",
            summary="Register user",
            description="Return the access token if succes else error",
            responses={
                200: {"description": "Success"},
                409: {"description": "User already exist"},
            })
async def new_user(user_data: SUserRegistration) -> User:
    return await UserService.register_user(login = user_data.login, email = user_data.email, password = user_data.password)


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
