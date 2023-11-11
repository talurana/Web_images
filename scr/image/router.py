from fastapi import APIRouter, Depends, Query, HTTPException, Header
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from scr.database import get_async_session
from .models import image
from .schemas import ImageCreate

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
    columns_to_select = [image.columns.file_name, image.columns.url, image.columns.attributes]

    query = select(*columns_to_select)
    if filter_str:
        query = query.where(image.c.file_name.ilike(f"{filter_str}%"))
        total_nb_query = select(func.count()).select_from(image).where(image.c.file_name.ilike(f"{filter_str}%"))

    else:
        total_nb_query = select(func.count()).select_from(image)

    total_nb = await session.scalar(total_nb_query)

    query = query.limit(limit).offset(offset)
    rows = await session.execute(query)

    image_data = [row._asdict() for row in rows]

    pagination = {
        "size": len(image_data),
        "totalNb": total_nb
    }

    response_data = {
        "data": image_data,
        "pagination": pagination
    }

    return response_data


@router.post('/update/{name}')
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
