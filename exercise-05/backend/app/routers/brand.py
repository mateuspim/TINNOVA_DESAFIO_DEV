from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db
from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandResponse
from app.routers.vehicle import get_brand_or_404


router = APIRouter(
    prefix="/brands",
    tags=["Brands"],
    dependencies=[],
    responses={403: {"description": "Not enough permissions"}},
)


@router.get("/", response_model=Page[BrandResponse])
def get_brands(db: Session = Depends(get_db)) -> Page[BrandResponse]:
    query = db.query(Brand).order_by(Brand.created_at)
    try:
        return paginate(db, query)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/resolve", response_model=BrandResponse)
def get_brand_id_by_name(
    name: str = Query(..., description="Query brand ID by name"),
    db: Session = Depends(get_db),
) -> BrandResponse:
    brand = db.query(Brand).filter(func.lower(Brand.name) == name.lower()).first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand with name '{name}' not found",
        )

    return brand


@router.post("/", response_model=BrandResponse)
def create_brand(
    request: BrandCreate,
    db: Session = Depends(get_db),
) -> BrandResponse:
    brand = Brand(name=request.name)
    try:
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create brand: {str(e)}",
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(id: int, db: Session = Depends(get_db)):
    brand = get_brand_or_404(db, id)
    try:
        db.delete(brand)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete brand with ID {id}: {str(e)}",
        )
