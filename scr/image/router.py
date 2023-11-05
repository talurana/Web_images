from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import typing

from scr.database import get_async_session
from .models import image
from .schemas import ImageCreate

router = APIRouter(
    prefix='/image',
    tags=['Images']
)


@router.get('/')
async def get_image(session: AsyncSession = Depends(get_async_session)):
    query = select(image)
    rows = await session.execute(query)
    image_data = [row._asdict() for row in rows]

    return image_data

