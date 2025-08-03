from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.brand import BrandResponse


class VehicleBase(BaseModel):
    model: str
    brand_id: int
    color: str
    year: int
    description: Optional[str] = None
    is_sold: Optional[bool] = False


class VehicleCreate(VehicleBase):
    brand_id: int


class VehicleResponse(VehicleBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
    brand: BrandResponse


class VehicleUpdate(BaseModel):
    model: str
    color: str
    year: int
    description: Optional[str] = None
    is_sold: Optional[bool] = False
    brand_id: int


class VehiclePatch(BaseModel):
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    is_sold: Optional[bool] = None
    brand_id: Optional[int] = None
