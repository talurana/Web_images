from fastapi import FastAPI

from .authen.base_config import auth_backend, fastapi_users
from .authen.schemas import UserRead, UserCreate

from .image.router import router as router_operation

app = FastAPI(
    title="Web Images"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    router_operation
)
