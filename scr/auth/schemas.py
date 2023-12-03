from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Pydatic model for UserRead"""
    middle_name: str
    name: str
    surname: str


class UserCreate(schemas.BaseUserCreate):
    """Pydatic model for UserCreate"""
    middle_name: str
    name: str
    surname: str


class UserUpdate(schemas.BaseUserUpdate):
    """Pydatic model for UserUpdate"""
    pass
