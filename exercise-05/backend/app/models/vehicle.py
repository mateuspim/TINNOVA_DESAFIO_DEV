from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base
from models.brand import Brand


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(100), index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), index=True)
    color = Column(String(50), index=True)
    year = Column(Integer, index=True)
    description = Column(Text)
    is_sold = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    brand = relationship("Brand", back_populates="vehicles")
