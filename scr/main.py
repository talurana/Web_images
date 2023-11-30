from fastapi import FastAPI

from .authen.base_config import auth_backend, fastapi_users
from .authen.schemas import UserRead, UserCreate, UserUpdate

from .image.router import router as router_image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Web Images"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные методы
    allow_headers=["*"],  # Разрешенные заголовки
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
    router_image
)

app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

#app.include_router(fastapi_users.get_reset_password_router(UserCreate), prefix="/auth", tags=["auth"],)