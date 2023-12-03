from typing import List
from pydantic import BaseModel, ConfigDict
# pydantic schemas


class ImageUpdate(BaseModel):
    image_attributes: List[str]
    image_name: str
