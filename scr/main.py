from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from .authen.base_config import auth_backend, fastapi_users
from scr.authen.models import User
from .authen.manager import get_user_manager
from .authen.schemas import UserRead, UserCreate

app = FastAPI(
    title="Web Images"
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# app.mount("/index", StaticFiles(directory="templates", html=True))
#
#
# @app.get("/root")
# async def root():
#     return RedirectResponse("/hello/{name}")
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     data = "That's new page for something"
#     return Response(content=data, media_type='text/html')
#

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"
