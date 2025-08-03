from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.logger import logger
from app.db.database import get_db
from app.models.vehicle import Vehicle
from app.models.brand import Brand
from app.schemas.vehicle import (
    VehicleResponse,
    VehicleCreate,
    VehicleUpdate,
    VehiclePatch,
)


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
    dependencies=[],
    responses={403: {"description": "Not enough permissions"}},
)


@router.get("/", response_model=Page[VehicleResponse])
def get_vehicles(
    year: int = Query(None, description="Query vehicle by year"),
    brand_id: int = Query(None, description="Query vehicle by brand ID"),
    color: str = Query(None, description="Query vehicle by color"),
    db: Session = Depends(get_db),
) -> Page[VehicleResponse]:
    logger.info("Starting to fetch all vehicles")
    query = db.query(Vehicle)
    if brand_id is not None:
        brand = get_brand_or_404(db, brand_id)
        if brand:
            query = query.filter(Vehicle.brand_id == brand_id)
    if year is not None:
        query = query.filter(Vehicle.year == year)
    if color is not None:
        query = query.filter(Vehicle.color == color)

    query = query.order_by(Vehicle.created_at)
    logger.info("Pagination query executed successfully")
    return paginate(db, query)


@router.get("/{id}", response_model=VehicleResponse)
def get_vehicle(id: int, db: Session = Depends(get_db)) -> VehicleResponse:
    vehicle = get_vehicle_or_404(db, id)
    logger.info(f"Vehicle with ID {id} fetched successfully")
    return vehicle


def get_brand_or_404(db: Session, id: int) -> Brand:
    brand = db.query(Brand).filter(Brand.id == id).first()
    if not brand:
        logger.warning(f"Brand with ID {id} not found")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Brand not found")
    logger.info(f"Brand with ID {id} fetched successfully")
    return brand


@router.post("/", response_model=VehicleResponse)
def create_vehicle(
    request: VehicleCreate, db: Session = Depends(get_db)
) -> VehicleResponse:
    logger.info("Starting vehicle creation")
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
        logger.info(f"Vehicle with ID {vehicle.id} created successfully")
        return vehicle
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create vehicle: {str(e)}", exc_info=True)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_vehicle_or_404(db: Session, id: int) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not vehicle:
        logger.warning(f"Vehicle with ID:{id} not found")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    logger.info(f"Vehicle with ID {id} fetched successfully")
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
        logger.info(f"Vehicle with ID {id} updated successfully")
        return vehicle
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error while updating vehicle with ID {id}: {str(e)}", exc_info=True)
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
        logger.info(f"Vehicle with ID {id} patched successfully")
        return vehicle
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error while updating vehicle with ID {id}: {str(e)}", exc_info=True)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(id: int, db: Session = Depends(get_db)):
    vehicle = get_vehicle_or_404(db, id)
    try:
        db.delete(vehicle)
        db.commit()
        logger.info(f"Vehicle with ID {id} deleted successfully")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error while deleting vehicle with ID {id}: {str(e)}", exc_info=True)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))