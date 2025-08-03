from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    vehicles = relationship(
        "Vehicle", back_populates="brand", cascade="all, delete-orphan"
    )
