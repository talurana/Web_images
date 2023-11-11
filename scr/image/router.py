import json

from fastapi import APIRouter, Depends, Query, HTTPException, Header
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

    image_data = []
    for row in rows:
        row_dict = row._asdict()
        try:
            row_dict['attributes'] = json.loads(row_dict['attributes']) if row_dict['attributes'] else None
        except json.JSONDecodeError as e:
            # Log the problematic data and set 'attributes' to None
            print(f"Error decoding JSON in 'attributes' column. Data: {row_dict['attributes']}. Error: {e}")
            # row_dict['attributes'] = list(row_dict['attributes'][1:-1].split(', '))
        image_data.append(row_dict)

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
async def classify(name: str, attribute: ImageUpdate, x_user_id: str = Header(None, alias="X-User-Id"),
                   session: AsyncSession = Depends(get_async_session)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Неавторизованный запрос")

    attributes_list = attribute.attributes

    update_image = (
        update(image)
        .where(image.c.file_name == name)
        .values(
            attributes=json.dumps(attributes_list, ensure_ascii=False),
            edited_by=int(x_user_id)
        )
    )

    await session.execute(update_image)
    await session.commit()

    return {"message": "Изображение обновлено успешно"}
