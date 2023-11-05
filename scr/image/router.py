from fastapi import APIRouter, Depends, Query, HTTPException, Header
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

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


@router.post('/update/{image.id}')
async def classify(name: str, attribute: str, x_user_id: str = Header(None, alias="X-User-Id"),
                   session: AsyncSession = Depends(get_async_session)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Неавторизованный запрос")

    update_image = (
        update(image)
        .where(image.c.file_name == name)
        .values(
            attributes=attribute,
            edited_by=int(x_user_id)
        )
    )

    await session.execute(update_image)
    await session.commit()

    return {"message": "Изображение обновлено успешно"}