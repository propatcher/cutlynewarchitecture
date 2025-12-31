from fastapi import APIRouter, Depends

from app.domain.entities.user import User

router = APIRouter(
    prefix = "/users",
    tags=["users"]
)

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Returns the currently authenticated user's profile",
    responses={
        200: {"description": "Success"},
        401: {"description": "Not authenticated"},
        404: {"description": "User not found"}
    }
)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
