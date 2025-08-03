from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, Query, status
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import exc

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
from typing import List, Union


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


def get_brand_or_404(db: Session, id: int) -> Brand:
    brand = db.query(Brand).filter(Brand.id == id).first()
    if not brand:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return brand


@router.post("", response_model=VehicleResponse)
def create_vehicle(
    request: VehicleCreate, db: Session = Depends(get_db)
) -> VehicleResponse:
    brand = get_brand_or_404(db, request.brand_id)

    vehicle = Vehicle(
        model=request.model,
        brand_id=request.brand_id,
        color=request.color,
        year=request.year,
        description=request.description,
        is_sold=request.is_sold,
    )
    try:
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        _ = vehicle.brand
        return vehicle
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_vehicle_or_404(db: Session, id: int) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return vehicle


@router.put("/{id}", response_model=VehicleResponse)
def update_vehicle(
    request: VehicleUpdate, id: int, db: Session = Depends(get_db)
) -> VehicleResponse:
    vehicle = get_vehicle_or_404(db, id)

    for attr, value in request.dict().items():
        setattr(vehicle, attr, value)

    try:
        db.commit()
        db.refresh(vehicle)
        _ = vehicle.brand
        return vehicle
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{id}", response_model=VehicleResponse)
def patch_vehicle(
    request: VehiclePatch, id: int, db: Session = Depends(get_db)
) -> VehicleResponse:
    vehicle = get_vehicle_or_404(db, id)

    for key, value in request.dict(exclude_unset=True).items():
        setattr(vehicle, key, value)
    try:
        db.commit()
        db.refresh(vehicle)
        _ = vehicle.brand
        return vehicle
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
