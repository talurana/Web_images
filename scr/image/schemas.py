from typing import List

from pydantic import BaseModel, ConfigDict


class ImageCreate(BaseModel):
    id: int
    file_name: str
    url: str
    attributes: List[str]

    model_config = ConfigDict(from_attributes=True)


class ImageUpdate(BaseModel):
    attributes: List[str]
    email: str

