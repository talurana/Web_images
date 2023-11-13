from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers, models
from .base_config import fastapi_users, auth_backend
from .schemas import UserCreate, UserUpdate

router = APIRouter(
    prefix="/auth",
    tags=["Dont work"],
)


@router.put("/users/me")
async def update_user(
        user: UserCreate,
        user_manager=Depends(fastapi_users.get_user_manager),
):
    current_user = await user_manager.get_current_active_user()
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await user_manager.update(current_user, user)
    return updated_user


@router.post("/forgot-password")
async def forgot_password(
    email: str,
    user_manager=Depends(fastapi_users.get_user_manager),
):
    user = await user_manager.get_by_email(email)
    if user:
        # Handle logic to send reset password email here
        # You might want to send an email with a link containing a token
        # The token can be generated using user_manager.generate_password_reset_token(user)
        pass
    return {"message": "If the email exists, a reset password email has been sent"}
