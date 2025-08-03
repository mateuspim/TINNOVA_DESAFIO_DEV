from pydantic import BaseModel
from datetime import datetime


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class BrandResponse(BrandBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
