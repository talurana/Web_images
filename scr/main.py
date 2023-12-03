from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from scr.auth.users import auth_backend, fastapi_users, current_active_user
from scr.auth.schemas import UserRead, UserCreate, UserUpdate
from scr.image.router import image_router

# create global app
app = FastAPI(
    title="Web Images",
    description='Swagger for backend endpoints'
)

# decorators for all.py request
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3000/register"],  # Разрешенные источники
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
