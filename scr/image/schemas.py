from typing import Optional

from pydantic import BaseModel, ConfigDict


class ImageCreate(BaseModel):
    id: int
    file_name: str
    url: str
    attributes: Optional[str]

    model_config = ConfigDict(from_attributes=True)



