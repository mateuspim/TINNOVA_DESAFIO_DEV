from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base
from models.vehicle import Vehicle


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, unique=True)

    vehicles = relationship(
        "Vehicle", back_populates="brand", cascade="all, delete-orphan"
    )
