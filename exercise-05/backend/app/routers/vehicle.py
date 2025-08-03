from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
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
