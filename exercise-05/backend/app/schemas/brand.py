from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class BrandResponse(BrandBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
