from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, Query
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db, SessionLocal
from app.models.vehicle import Vehicle
from app.models.brand import Brand
from datetime import datetime
from app.schemas.vehicle import (
    VehicleResponse,
    VehicleCreate,
    VehicleUpdate,
    VehiclePatch,
)
from typing import List


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
    dependencies=[],
    responses={403: {"description": "Not enough permissions"}},
)


@router.get("", response_model=Page[VehicleResponse])
def get_vehicles(
    year: int = Query(None),
    brand_id: int = Query(None),
    color: str = Query(None),
    db: Session = Depends(get_db),
) -> Page[VehicleResponse]:
    query = db.query(Vehicle)
    if brand_id is not None:
        query = query.filter(Vehicle.brand_id == brand_id)
    if year is not None:
        query = query.filter(Vehicle.year == year)
    if color is not None:
        query = query.filter(Vehicle.color == color)

    query = query.order_by(Vehicle.created_at)
    return paginate(db, query)


@router.get("/{id}", response_model=VehicleResponse)
def get_vehicle(id: int, db: Session = Depends(get_db)) -> VehicleResponse:
    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(404, detail="Vehicle not found")

    return vehicle
