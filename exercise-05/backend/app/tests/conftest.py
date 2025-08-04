import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import get_db, Base
from app.models.brand import Brand
from app.models.vehicle import Vehicle

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_brand(db_session):
    """Create a sample brand for testing"""
    brand = Brand(name="Toyota")
    db_session.add(brand)
    db_session.commit()
    db_session.refresh(brand)
    return brand


@pytest.fixture
def sample_vehicle(db_session, sample_brand):
    """Create a sample vehicle for testing"""
    vehicle = Vehicle(
        model="Camry",
        brand_id=sample_brand.id,
        color="Blue",
        year=2020,
        description="A reliable sedan",
        is_sold=False
    )
    db_session.add(vehicle)
    db_session.commit()
    db_session.refresh(vehicle)
    return vehicle


@pytest.fixture
def multiple_brands(db_session):
    """Create multiple brands for pagination testing"""
    brands = [
        Brand(name="Toyota"),
        Brand(name="Honda"),
        Brand(name="Ford"),
        Brand(name="BMW"),
        Brand(name="Mercedes"),
    ]
    for brand in brands:
        db_session.add(brand)
    db_session.commit()
    return brands


@pytest.fixture
def multiple_vehicles(db_session, sample_brand):
    """Create multiple vehicles for testing"""
    vehicles = [
        Vehicle(model="Camry", brand_id=sample_brand.id, color="Blue", year=2020, description="Sedan", is_sold=False),
        Vehicle(model="Corolla", brand_id=sample_brand.id, color="Red", year=2021, description="Compact", is_sold=True),
        Vehicle(model="Prius", brand_id=sample_brand.id, color="White", year=2022, description="Hybrid", is_sold=False),
        Vehicle(model="RAV4", brand_id=sample_brand.id, color="Black", year=2023, description="SUV", is_sold=False),
        Vehicle(model="Highlander", brand_id=sample_brand.id, color="Silver", year=2024, description="Large SUV", is_sold=True)
    ]
    for vehicle in vehicles:
        db_session.add(vehicle)
    db_session.commit()
    return vehicles


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """Clean up test database after all tests"""
    yield  # Run all tests first
    db_path = "./test.db"
    if os.path.exists(db_path):
        os.remove(db_path)