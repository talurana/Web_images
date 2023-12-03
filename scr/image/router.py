import json

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from scr.db import get_async_session
from .models import Image
from scr.auth.users import current_active_user
from .schemas import ImageUpdate
from scr.auth.models import User

# create special "url dir" where we place all.py about
image_router = APIRouter(
    prefix='/images',
    tags=['Images']
)


def get_lower_attribute_names(attribute_names: List[str]):
    return [attribute.lower() for attribute in attribute_names]


@image_router.get('/search_image')
async def get_image(
        # write params that will be in link after questtion sign : "...search_image?limit=10&offset=0"
        limit: int = Query(10, alias="limit", description="Количество элементов, которые нужно вернуть."),
        offset: int = Query(0, alias="offset", description="Номер элемента, с которого нужно начать."),
        filter_str: str = Query(None, alias="filter", description="Строковое значение для фильтрации."),
        is_marked: bool|None = Query(None, description='Есть ли маркировка у изображения'),
        # for code logic we use depedency injection: FastAPi search function that called like get_async_session
        session: AsyncSession = Depends(get_async_session)
):
    # get images from filter
    query = select(Image.image_name, Image.url, Image.attributes)
    if filter_str:
        query = query.where(Image.image_name.ilike(f"{filter_str}%"))
    if is_marked is True:
        query = query.where(Image.attributes != None)
    elif is_marked is False:
        query = query.where(Image.attributes == None)

    query = query.limit(limit).offset(offset)  # pagination
    rows = await session.execute(query)

    image_data = [
        dict(
            file_name=row[0],
            url=row[1],
            attributes=json.loads(row[2]) if row[2] else None
        ) for row in rows
    ]

    # for frontend pagination
    total_nb_query = select(func.count()).select_from(Image)
    if filter_str:
        total_nb_query = total_nb_query.where(Image.image_name.ilike(f"{filter_str}%"))
    total_nb = await session.scalar(total_nb_query)

    # return answer
    return {
        "data": image_data,
        "pagination": {
            "size": len(image_data),
            "totalNb": total_nb
        }
    }


@image_router.post('/update/{name}')
async def update_image(
        req_params: ImageUpdate,
        cur_user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    attributes_list = get_lower_attribute_names(req_params.image_attributes)

    update_image_query = (
        update(Image)
        .where(Image.image_name == req_params.image_name)
        .values(
            attributes=json.dumps(attributes_list, ensure_ascii=False),
            last_change=cur_user.email,
        )
    )

    await session.execute(update_image_query)
    await session.commit()

    return {"message": "Изображение обновлено успешно"}
