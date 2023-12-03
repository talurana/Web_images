from typing import List
from pydantic import BaseModel, ConfigDict
# pydantic schemas

class ImageCreate(BaseModel):
    id: int
    image_name: str
    url: str
    attributes: List[str]

    model_config = ConfigDict(from_attributes=True)


class ImageUpdate(BaseModel):
    image_attributes: List[str]
    image_name: str
