from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
import time
from scr.auth.users import auth_backend, fastapi_users, current_active_user
from scr.auth.schemas import UserRead, UserCreate, UserUpdate
from scr.image.router import image_router

# create global app
app = FastAPI(
    title="Web Images",
    description='Swagger for backend endpoints',
    docs_url=None,  # Отключаем стандартную ручку /docs
    redoc_url=None
)

security = HTTPBasic()

# Функция для проверки пароля
def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"  # Установите имя пользователя
    correct_password = "1111"  # Установите пароль

    if credentials.username == correct_username and credentials.password == correct_password:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )

origins = [
    "http://localhost:3000",  # Adjust this to match the origin of your frontend
]

# decorators for all.py request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные методы
    allow_headers=["*"],  # Разрешенные заголовки
)

# add app logic routers
app.include_router(
    image_router
)

# add auth routers
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user=Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@app.get("/docs", include_in_schema=False)
async def custom_docs(verified: bool = Depends(verify_password)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Docs")