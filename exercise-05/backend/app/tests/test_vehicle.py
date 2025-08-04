import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError

from app.main import app
from app.db.database import get_db
from app.models.vehicle import Vehicle
from app.models.brand import Brand
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehiclePatch

from app.tests.conftest import client, override_get_db


class TestGetVehicles:
    def test_get_vehicles_success(self, db_session, sample_vehicle):
        """Test successful retrieval of vehicles"""
        response = client.get("/api/vehicles/")

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["model"] == "Camry"
        assert data["items"][0]["id"] == sample_vehicle.id

    def test_get_vehicles_empty_list(self, db_session):
        """Test getting vehicles when none exist"""
        response = client.get("/api/vehicles/")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []

    def test_get_vehicles_filter_by_year(self, db_session, sample_vehicle):
        """Test filtering vehicles by year"""
        response = client.get("/api/vehicles/?year=2020")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["year"] == 2020

    def test_get_vehicles_filter_by_brand_id(
        self, db_session, sample_vehicle, sample_brand
    ):
        """Test filtering vehicles by brand_id"""
        response = client.get(f"/api/vehicles/?brand_id={sample_brand.id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["brand_id"] == sample_brand.id

    def test_get_vehicles_filter_by_color(self, db_session, sample_vehicle):
        """Test filtering vehicles by color"""
        response = client.get("/api/vehicles/?color=Blue")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["color"] == "Blue"

    def test_get_vehicles_filter_by_nonexistent_brand(self, db_session, sample_vehicle):
        """Test filtering by non-existent brand returns 404"""
        response = client.get("/api/vehicles/?brand_id=999")

        assert response.status_code == 404
        assert "Brand not found" in response.json()["detail"]

    def test_get_vehicles_no_results_with_filters(self, db_session, sample_vehicle):
        """Test filtering with no matching results"""
        response = client.get("/api/vehicles/?year=1999")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []


class TestGetVehicle:
    def test_get_vehicle_success(self, db_session, sample_vehicle):
        """Test successful vehicle retrieval by ID"""
        response = client.get(f"/api/vehicles/{sample_vehicle.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["model"] == "Camry"
        assert data["id"] == sample_vehicle.id

    def test_get_vehicle_not_found(self, db_session):
        """Test vehicle not found scenario"""
        response = client.get("/api/vehicles/999")

        assert response.status_code == 404
        assert "Vehicle not found" in response.json()["detail"]


class TestCreateVehicle:
    def test_create_vehicle_success(self, db_session, sample_brand):
        """Test successful vehicle creation"""
        vehicle_data = {
            "model": "Corolla",
            "brand_id": sample_brand.id,
            "color": "Red",
            "year": 2021,
            "description": "Compact car",
            "is_sold": False,
        }
        response = client.post("/api/vehicles/", json=vehicle_data)

        assert response.status_code == 200
        data = response.json()
        assert data["model"] == "Corolla"
        assert data["brand_id"] == sample_brand.id
        assert "id" in data

        # Verify vehicle was actually created in database
        created_vehicle = (
            db_session.query(Vehicle).filter(Vehicle.model == "Corolla").first()
        )
        assert created_vehicle is not None
        assert created_vehicle.model == "Corolla"

    def test_create_vehicle_invalid_brand(self, db_session):
        """Test vehicle creation with invalid brand_id"""
        vehicle_data = {
            "model": "Corolla",
            "brand_id": 999,
            "color": "Red",
            "year": 2021,
            "description": "Compact car",
            "is_sold": False,
        }
        response = client.post("/api/vehicles/", json=vehicle_data)

        assert response.status_code == 404
        assert "Brand not found" in response.json()["detail"]

    def test_create_vehicle_invalid_data(self, db_session):
        """Test vehicle creation with invalid data"""
        response = client.post("/api/vehicles/", json={})

        assert response.status_code == 422  # Validation error

    def test_create_vehicle_database_error(self, db_session, sample_brand):
        """Test database error during vehicle creation"""
        mock_session = MagicMock()
        mock_session.commit.side_effect = SQLAlchemyError("Database error")
        mock_session.add.return_value = None
        mock_session.refresh.return_value = None
        mock_session.rollback.return_value = None
        mock_session.query.return_value.filter.return_value.first.return_value = (
            sample_brand
        )

        def mock_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = mock_get_db

        try:
            vehicle_data = {
                "model": "Corolla",
                "brand_id": sample_brand.id,
                "color": "Red",
                "year": 2021,
                "description": "Compact car",
                "is_sold": False,
            }
            response = client.post("/api/vehicles/", json=vehicle_data)

            assert response.status_code == 500
            assert "Database error" in response.json()["detail"]
        finally:
            app.dependency_overrides[get_db] = override_get_db


class TestUpdateVehicle:
    def test_update_vehicle_success(self, db_session, sample_vehicle):
        """Test successful vehicle update"""
        update_data = {
            "model": "Updated Camry",
            "brand_id": sample_vehicle.brand_id,
            "color": "Green",
            "year": 2022,
            "description": "Updated description",
            "is_sold": True,
        }
        response = client.put(f"/api/vehicles/{sample_vehicle.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["model"] == "Updated Camry"
        assert data["color"] == "Green"
        assert data["year"] == 2022
        assert data["is_sold"] == True

    def test_update_vehicle_not_found(self, db_session):
        """Test updating non-existent vehicle"""
        update_data = {
            "model": "Updated Model",
            "brand_id": 1,
            "color": "Green",
            "year": 2022,
            "description": "Updated description",
            "is_sold": True,
        }
        response = client.put("/api/vehicles/999", json=update_data)

        assert response.status_code == 404
        assert "Vehicle not found" in response.json()["detail"]

    def test_update_vehicle_database_error(self, db_session, sample_vehicle):
        """Test database error during vehicle update"""
        mock_session = MagicMock()
        mock_session.commit.side_effect = SQLAlchemyError("Database error")
        mock_session.refresh.return_value = None
        mock_session.rollback.return_value = None
        mock_session.query.return_value.filter.return_value.first.return_value = (
            sample_vehicle
        )

        def mock_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = mock_get_db

        try:
            update_data = {
                "model": "Updated Model",
                "brand_id": sample_vehicle.brand_id,
                "color": "Green",
                "year": 2022,
                "description": "Updated description",
                "is_sold": True,
            }
            response = client.put(
                f"/api/vehicles/{sample_vehicle.id}", json=update_data
            )

            assert response.status_code == 500
            assert "Database error" in response.json()["detail"]
        finally:
            app.dependency_overrides[get_db] = override_get_db


class TestPatchVehicle:
    def test_patch_vehicle_success(self, db_session, sample_vehicle):
        """Test successful vehicle patch"""
        patch_data = {"color": "Yellow", "is_sold": True}
        response = client.patch(f"/api/vehicles/{sample_vehicle.id}", json=patch_data)

        assert response.status_code == 200
        data = response.json()
        assert data["color"] == "Yellow"
        assert data["is_sold"] == True
        assert data["model"] == "Camry"  # Unchanged field

    def test_patch_vehicle_not_found(self, db_session):
        """Test patching non-existent vehicle"""
        patch_data = {"color": "Yellow"}
        response = client.patch("/api/vehicles/999", json=patch_data)

        assert response.status_code == 404
        assert "Vehicle not found" in response.json()["detail"]

    def test_patch_vehicle_database_error(self, db_session, sample_vehicle):
        """Test database error during vehicle patch"""
        mock_session = MagicMock()
        mock_session.commit.side_effect = SQLAlchemyError("Database error")
        mock_session.refresh.return_value = None
        mock_session.rollback.return_value = None
        mock_session.query.return_value.filter.return_value.first.return_value = (
            sample_vehicle
        )

        def mock_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = mock_get_db

        try:
            patch_data = {"color": "Yellow"}
            response = client.patch(
                f"/api/vehicles/{sample_vehicle.id}", json=patch_data
            )

            assert response.status_code == 500
            assert "Database error" in response.json()["detail"]
        finally:
            app.dependency_overrides[get_db] = override_get_db


class TestDeleteVehicle:
    def test_delete_vehicle_success(self, db_session, sample_vehicle):
        """Test successful vehicle deletion"""
        vehicle_id = sample_vehicle.id
        response = client.delete(f"/api/vehicles/{vehicle_id}")

        assert response.status_code == 204

        # Verify vehicle was actually deleted
        deleted_vehicle = (
            db_session.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        )
        assert deleted_vehicle is None

    def test_delete_vehicle_not_found(self, db_session):
        """Test deleting non-existent vehicle"""
        response = client.delete("/api/vehicles/999")

        assert response.status_code == 404
        assert "Vehicle not found" in response.json()["detail"]

    def test_delete_vehicle_database_error(self, db_session, sample_vehicle):
        """Test database error during vehicle deletion"""
        mock_session = MagicMock()
        mock_session.commit.side_effect = SQLAlchemyError("Database error")
        mock_session.delete.return_value = None
        mock_session.rollback.return_value = None
        mock_session.query.return_value.filter.return_value.first.return_value = (
            sample_vehicle
        )

        def mock_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = mock_get_db

        try:
            response = client.delete(f"/api/vehicles/{sample_vehicle.id}")

            assert response.status_code == 500
            assert "Database error" in response.json()["detail"]
        finally:
            app.dependency_overrides[get_db] = override_get_db


class TestIntegration:
    def test_full_crud_workflow(self, db_session, sample_brand):
        """Test complete CRUD workflow"""
        # Create
        vehicle_data = {
            "model": "Prius",
            "brand_id": sample_brand.id,
            "color": "White",
            "year": 2023,
            "description": "Hybrid car",
            "is_sold": False,
        }
        create_response = client.post("/api/vehicles/", json=vehicle_data)
        assert create_response.status_code == 200
        vehicle_id = create_response.json()["id"]

        # Read (get all)
        get_all_response = client.get("/api/vehicles/")
        assert get_all_response.status_code == 200
        assert len(get_all_response.json()["items"]) == 1

        # Read (get by ID)
        get_by_id_response = client.get(f"/api/vehicles/{vehicle_id}")
        assert get_by_id_response.status_code == 200
        assert get_by_id_response.json()["model"] == "Prius"

        # Update
        update_data = {
            "model": "Prius Updated",
            "brand_id": sample_brand.id,
            "color": "Black",
            "year": 2023,
            "description": "Updated hybrid car",
            "is_sold": False,
        }
        update_response = client.put(f"/api/vehicles/{vehicle_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["model"] == "Prius Updated"

        # Patch
        patch_data = {"is_sold": True}
        patch_response = client.patch(f"/api/vehicles/{vehicle_id}", json=patch_data)
        assert patch_response.status_code == 200
        assert patch_response.json()["is_sold"] == True

        # Delete
        delete_response = client.delete(f"/api/vehicles/{vehicle_id}")
        assert delete_response.status_code == 204

        # Verify deletion
        get_after_delete_response = client.get("/api/vehicles/")
        assert len(get_after_delete_response.json()["items"]) == 0


# Additional fixtures and utilities
@pytest.fixture
def multiple_vehicles(db_session, sample_brand):
    """Create multiple vehicles for testing"""
    vehicles = [
        Vehicle(
            model="Camry",
            brand_id=sample_brand.id,
            color="Blue",
            year=2020,
            description="Sedan",
            is_sold=False,
        ),
        Vehicle(
            model="Corolla",
            brand_id=sample_brand.id,
            color="Red",
            year=2021,
            description="Compact",
            is_sold=True,
        ),
        Vehicle(
            model="Prius",
            brand_id=sample_brand.id,
            color="White",
            year=2022,
            description="Hybrid",
            is_sold=False,
        ),
        Vehicle(
            model="RAV4",
            brand_id=sample_brand.id,
            color="Black",
            year=2023,
            description="SUV",
            is_sold=False,
        ),
        Vehicle(
            model="Highlander",
            brand_id=sample_brand.id,
            color="Silver",
            year=2024,
            description="Large SUV",
            is_sold=True,
        ),
    ]
    for vehicle in vehicles:
        db_session.add(vehicle)
    db_session.commit()
    return vehicles


class TestPagination:
    def test_vehicles_pagination(self, db_session, multiple_vehicles):
        """Test pagination functionality"""
        response = client.get("/api/vehicles/?page=1&size=3")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert "total" in data
        assert data["total"] == 5
