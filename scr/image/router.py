import json

from fastapi import APIRouter, Depends, Query, HTTPException, Header, status
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from scr.database import get_async_session
from .models import image
from .schemas import ImageUpdate

router = APIRouter(
    prefix='/image',
    tags=['Images']
)


@router.get('/search_image')
async def get_image(
        limit: int = Query(10, alias="limit", description="Количество элементов, которые нужно вернуть."),
        offset: int = Query(0, alias="offset", description="Номер элемента, с которого нужно начать."),
        filter_str: str = Query(None, alias="filter", description="Строковое значение для фильтрации."),
        session: AsyncSession = Depends(get_async_session)):

    query = select(
        image.columns.file_name,
        image.columns.url,
        image.columns.attributes
    )
    total_nb_query = select(func.count()).select_from(image)
    if filter_str:
        query = query.where(image.c.file_name.ilike(f"{filter_str}%"))
        total_nb_query = total_nb_query.where(image.c.file_name.ilike(f"{filter_str}%"))


    total_nb = await session.scalar(total_nb_query)

    query = query.limit(limit).offset(offset)
    rows = await session.execute(query)


    image_data = [
        dict(
            file_name=row[0],
            url=row[1],
            attributes=json.loads(row[2]) if row[2] else None
        ) for row in rows
    ]


    return {
        "data": image_data,
        "pagination": {
            "size": len(image_data),
            "totalNb": total_nb
        }
    }


@router.post('/update/{name}')
async def classify(name: str, attribute: ImageUpdate, x_user_id: str = Header(None, alias="X-User-Id"),
                   session: AsyncSession = Depends(get_async_session)):
    if not x_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неавторизованный запрос")

    attributes_list = attribute.attributes

    attributes_list = attribute.attributes

    update_image = (
        update(image)
        .where(image.c.file_name == name)
        .values(
            attributes=json.dumps(attributes_list, ensure_ascii=False),
            edited_by=int(x_user_id)
        )
    )
    async with session.begin():
        await session.execute(update_image)

    return {"message": "Изображение обновлено успешно"}
