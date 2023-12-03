from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi import Depends
from sqlalchemy import Column, Integer, String

from scr.db import Base, get_async_session


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)  # имя
    surname = Column(String, nullable=False)  # фамилия
    middle_name = Column(String, nullable=False)  # отчество


async def get_user_db(session=Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
