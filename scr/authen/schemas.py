from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    email: str
    name: str
    surname: str
    middle_name: str
    id: int
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    name: str
    surname: str
    middle_name: str
    password: str


class UserUpdate(schemas.BaseUser):
    email: str
    name: str
    surname: str
    middle_name: str
