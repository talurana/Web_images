from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Pydatic model for UserRead"""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Pydatic model for UserCreate"""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Pydatic model for UserUpdate"""
    pass
