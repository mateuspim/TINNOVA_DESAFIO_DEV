import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError

from app.main import app
from app.db.database import get_db
from app.models.brand import Brand
from app.schemas.brand import BrandCreate

from app.tests.conftest import client, override_get_db


class TestGetBrands:
    def test_get_brands_success(self, db_session, sample_brand):
        """Test successful retrieval of brands"""
        response = client.get("/api/brands/")

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Toyota"
        assert data["items"][0]["id"] == sample_brand.id

    def test_get_brands_empty_list(self, db_session):
        """Test getting brands when none exist"""
        response = client.get("/api/brands/")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []

    @patch("app.routers.brand.paginate")
    def test_get_brands_database_error(self, mock_paginate, db_session):
        """Test database error handling"""
        from sqlalchemy.exc import SQLAlchemyError

        mock_paginate.side_effect = SQLAlchemyError("Database connection failed")

        response = client.get("/api/brands/")

        assert response.status_code == 500
        assert "Database connection failed" in response.json()["detail"]


class TestGetBrandByName:
    def test_get_brand_by_name_success(self, db_session, sample_brand):
        """Test successful brand retrieval by name"""
        response = client.get("/api/brands/resolve?name=Toyota")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Toyota"
        assert data["id"] == sample_brand.id

    def test_get_brand_by_name_case_insensitive(self, db_session, sample_brand):
        """Test case-insensitive brand search"""
        response = client.get("/api/brands/resolve?name=TOYOTA")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Toyota"

    def test_get_brand_by_name_not_found(self, db_session):
        """Test brand not found scenario"""
        response = client.get("/api/brands/resolve?name=NonExistent")

        assert response.status_code == 404
        assert "Brand with name 'NonExistent' not found" in response.json()["detail"]

    def test_get_brand_by_name_missing_parameter(self, db_session):
        """Test missing name parameter"""
        response = client.get("/api/brands/resolve")

        assert response.status_code == 422  # Validation error


class TestCreateBrand:
    def test_create_brand_success(self, db_session):
        """Test successful brand creation"""
        brand_data = {"name": "Honda"}
        response = client.post("/api/brands/", json=brand_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Honda"
        assert "id" in data

        # Verify brand was actually created in database
        created_brand = db_session.query(Brand).filter(Brand.name == "Honda").first()
        assert created_brand is not None
        assert created_brand.name == "Honda"

    def test_create_brand_invalid_data(self, db_session):
        """Test brand creation with invalid data"""
        response = client.post("/api/brands/", json={})

        assert response.status_code == 422  # Validation error

    def test_create_brand_database_error(self, db_session):
        """Test database error during brand creation"""
        from unittest.mock import MagicMock
        from sqlalchemy.exc import SQLAlchemyError

        # Create a mock session whose commit raises an error
        mock_session = MagicMock()
        mock_session.commit.side_effect = SQLAlchemyError("Database error")
        mock_session.add.return_value = None
        mock_session.refresh.return_value = None
        mock_session.rollback.return_value = None

        # Override the dependency to return our mock session
        def mock_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = mock_get_db

        try:
            brand_data = {"name": "Honda"}
            response = client.post("/api/brands/", json=brand_data)

            assert response.status_code == 500
            assert "Failed to create brand" in response.json()["detail"]

            # Verify the mock was called correctly
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.rollback.assert_called_once()
        finally:
            # Clean up - restore original dependency
            app.dependency_overrides[get_db] = override_get_db


class TestDeleteBrand:
    def test_delete_brand_success(self, db_session, sample_brand):
        """Test successful brand deletion"""
        brand_id = sample_brand.id
        response = client.delete(f"/api/brands/{brand_id}")

        assert response.status_code == 204

        # Verify brand was actually deleted
        deleted_brand = db_session.query(Brand).filter(Brand.id == brand_id).first()
        assert deleted_brand is None

    def test_delete_brand_not_found(self, db_session):
        """Test deleting non-existent brand"""
        response = client.delete("/api/brands/999")

        assert response.status_code == 404  # Assuming get_brand_or_404 raises 404

    def test_delete_brand_database_error(self, db_session, sample_brand):
        """Test database error during brand deletion"""
        from unittest.mock import MagicMock, patch
        from sqlalchemy.exc import SQLAlchemyError

        # Create a mock session whose commit raises an error
        mock_session = MagicMock()
        mock_session.commit.side_effect = SQLAlchemyError("Database error")
        mock_session.delete.return_value = None
        mock_session.rollback.return_value = None

        # Override the dependency to return our mock session
        def mock_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = mock_get_db

        # Mock get_brand_or_404 to return our sample brand
        with patch("app.routers.brand.get_brand_or_404") as mock_get_brand:
            mock_get_brand.return_value = sample_brand

            try:
                brand_id = sample_brand.id
                response = client.delete(f"/api/brands/{brand_id}")

                assert response.status_code == 500
                assert (
                    f"Failed to delete brand with ID {brand_id}"
                    in response.json()["detail"]
                )

                # Verify the mock was called correctly
                mock_session.delete.assert_called_once()
                mock_session.commit.assert_called_once()
                mock_session.rollback.assert_called_once()
            finally:
                # Clean up - restore original dependency
                app.dependency_overrides[get_db] = override_get_db


class TestIntegration:
    def test_full_crud_workflow(self, db_session):
        """Test complete CRUD workflow"""
        # Create
        brand_data = {"name": "Nissan"}
        create_response = client.post("/api/brands/", json=brand_data)
        assert create_response.status_code == 200
        brand_id = create_response.json()["id"]

        # Read (get all)
        get_all_response = client.get("/api/brands/")
        assert get_all_response.status_code == 200
        assert len(get_all_response.json()["items"]) == 1

        # Read (get by name)
        get_by_name_response = client.get("/api/brands/resolve?name=Nissan")
        assert get_by_name_response.status_code == 200
        assert get_by_name_response.json()["name"] == "Nissan"

        # Delete
        delete_response = client.delete(f"/api/brands/{brand_id}")
        assert delete_response.status_code == 204

        # Verify deletion
        get_after_delete_response = client.get("/api/brands/")
        assert len(get_after_delete_response.json()["items"]) == 0


# Additional fixtures and utilities
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


class TestPagination:
    def test_brands_pagination(self, db_session, multiple_brands):
        """Test pagination functionality"""
        response = client.get("/api/brands/?page=1&size=3")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert "total" in data
        assert data["total"] == 5
