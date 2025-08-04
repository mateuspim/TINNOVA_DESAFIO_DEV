# Tinnova Challenge - Backend

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange?style=for-the-badge&logo=sqlalchemy)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite)
![Pytest](https://img.shields.io/badge/Pytest-7.x-green?style=for-the-badge&logo=pytest)

## Table of Contents

- [Tinnova Challenge - Backend](#tinnova-challenge---backend)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Features](#2-features)
  - [3. Technologies Used](#3-technologies-used)
  - [4. Project Structure](#4-project-structure)
  - [5. Setup and Installation](#5-setup-and-installation)
    - [5.1. Prerequisites](#51-prerequisites)
    - [5.2. Clone the Repository](#52-clone-the-repository)
    - [5.3. Setup Env](#53-setup-the-env-params)
    - [5.4. Setup Options](#54-setup-options)
    - [5.5. Database Setup](#55-database-setup)
  - [6. Running the Application](#6-running-the-application)
  - [7. API Endpoints](#7-api-endpoints)
    - [7.1. Brands](#71-brands)
    - [7.2. Vehicles](#72-vehicles)
  - [8. Running Tests](#8-running-tests)

---

## 1. Introduction

This repository contains the backend API for the Tinnova Challenge, built with FastAPI. It provides a robust and efficient set of endpoints for managing vehicle brands and vehicles, including CRUD operations, filtering, and pagination.

## 2. Features

- **Brand Management**:
  - Create, retrieve (single, all, by name), update, and delete vehicle brands.
  - Pagination for brand listings.
- **Vehicle Management**:
  - Create, retrieve (single, all, with filters), update, patch, and delete vehicles.
  - Filtering vehicles by year, brand, color, and sold status.
  - Pagination for vehicle listings.
- **Database Integration**: Uses SQLAlchemy ORM with SQLite for data persistence.
- **API Documentation**: Automatic interactive API documentation (Swagger UI / ReDoc) via FastAPI.
- **Error Handling**: Centralized exception handling for common API errors (404 Not Found, 500 Internal Server Error).
- **Logging**: Structured logging for better observability.
- **Unit and Integration Tests**: Comprehensive test suite using Pytest.

## 3. Technologies Used

- **Python**: Programming language (3.12+)
- **FastAPI**: High-performance web framework for building APIs.
- **Pydantic**: Data validation and settings management.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapper (ORM).
- **SQLite**: Lightweight, file-based relational database.
- **Uvicorn**: ASGI server for running the FastAPI application.
- **FastAPI-Pagination**: Library for easy pagination.
- **Pytest**: Testing framework.
- **uv**: An extremely fast Python package and project manager

## 4. Project Structure

```
.
├── app/
│   ├── core/
│   │   └── logger.py           # Centralized logging configuration
│   │   └── config.py           # Core Application configuration
│   │   └── __init__.py
│   ├── db/
│   │   ├── database.py         # SQLAlchemy engine, session, and Base
│   │   └── __init__.py
│   ├── models/
│   │   ├── brand.py            # SQLAlchemy model for Brand
│   │   ├── vehicle.py          # SQLAlchemy model for Vehicle
│   │   └── __init__.py
│   ├── routers/
│   │   ├── brand.py            # API endpoints for Brands
│   │   ├── vehicle.py          # API endpoints for Vehicles
│   │   ├── logs.py             # API endpoints for Logs
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── brand.py            # Pydantic schemas for Brand
│   │   ├── vehicle.py          # Pydantic schemas for Vehicle
│   │   └── __init__.py
│   ├── tests/
│   │   ├── conftest.py         # Pytest fixtures and shared test setup
│   │   ├── test_brand.py       # Unit/Integration tests for Brand endpoints
│   │   ├── test_vehicle.py     # Unit/Integration tests for Vehicle endpoints
│   │   └── __init__.py
│   └── main.py                 # Main FastAPI application entry point
│   └── seed.py                 # Script to automate inserting brands into DB
├── .env.example                # Example environment variables file
├── .python-version             # Project python version
├── Dockerfile                  # Dockerfile for building the Docker image
├── pyproject.toml              # Project configuration
├── README.md                   # This README file
└── uv.lock                     # Python locked dependencies
```

## 5. Setup and Installation

Follow these steps to get the project up and running on your local machine.

### 5.1. Prerequisites

- Python 3.12+
- `uv` (recommended) or `pip` (Python package installer)

**For Docker:**

- Docker
- Docker Compose (optional)

### 5.2. Clone the Repository

```bash
git clone <repository_url>
cd tinnova_desafio_dev/exercise-05/backend/
```

### 5.3 Setup the env params

```bash
cp app/.env.example app/.env
```

### 5.4. Setup Options

Choose one of the following setup methods:

#### Option A: Local Development with uv (Recommended)

1. **Install uv** (if not already installed):

   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

3. **Activate the virtual environment:**

   ```bash
   # On Linux/macOS
   source .venv/bin/activate

   # On Windows
   .venv\Scripts\activate
   ```

#### Option B: Local Development with pip

1. **Create and activate virtual environment:**

   ```bash
   python -m venv .venv
   # On Linux/macOS
   source .venv/bin/activate
   # On Windows
   .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

#### Option C: Docker (Production-ready)

1. **Build the Docker image:**

   ```bash
   docker build -t tinnova-backend .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:80 tinnova-backend
   ```

### 5.5. Database Setup

This project uses SQLite, which is file-based and requires no separate server setup. The database file (`./app.db`) will be created automatically when the application runs for the first time or when migrations are applied (if you implement them).

For development, the `db_session` fixture in `app/tests/conftest.py` handles test database creation and teardown.

## 6. Running the Application

To start the FastAPI development server:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be accessible at `http://0.0.0.0:8000`.

- **Interactive API Documentation (Swagger UI)**: `http://0.0.0.0:8000/docs`
- **Alternative API Documentation (ReDoc)**: `http://0.0.0.0:8000/redoc`

## 7. API Endpoints

All endpoints are prefixed with `/api`.

### 7.1. Brands

| Method   | Endpoint              | Description                            | Request Body (JSON)  | Response (JSON)       |
| :------- | :-------------------- | :------------------------------------- | :------------------- | :-------------------- |
| `GET`    | `/api/brands/`        | Get all brands (paginated)             | `None`               | `Page[BrandResponse]` |
| `GET`    | `/api/brands/{id}`    | Get brand by ID                        | `None`               | `BrandResponse`       |
| `GET`    | `/api/brands/resolve` | Get brand by name (query param `name`) | `None`               | `BrandResponse`       |
| `POST`   | `/api/brands/`        | Create a new brand                     | `{"name": "string"}` | `BrandResponse`       |
| `PUT`    | `/api/brands/{id}`    | Update an existing brand by ID         | `{"name": "string"}` | `BrandResponse`       |
| `DELETE` | `/api/brands/{id}`    | Delete a brand by ID                   | `None`               | `204 No Content`      |

### 7.2. Vehicles

| Method   | Endpoint             | Description                                | Request Body (JSON)                                           | Response (JSON)         |
| :------- | :------------------- | :----------------------------------------- | :------------------------------------------------------------ | :---------------------- |
| `GET`    | `/api/vehicles/`     | Get all vehicles (paginated, with filters) | `None` (Query params: `year`, `brand_id`, `color`, `is_sold`) | `Page[VehicleResponse]` |
| `GET`    | `/api/vehicles/{id}` | Get vehicle by ID                          | `None`                                                        | `VehicleResponse`       |
| `POST`   | `/api/vehicles/`     | Create a new vehicle                       | `VehicleCreate` schema                                        | `VehicleResponse`       |
| `PUT`    | `/api/vehicles/{id}` | Update an existing vehicle by ID           | `VehicleUpdate` schema                                        | `VehicleResponse`       |
| `PATCH`  | `/api/vehicles/{id}` | Partially update a vehicle by ID           | `VehiclePatch` schema                                         | `VehicleResponse`       |
| `DELETE` | `/api/vehicles/{id}` | Delete a vehicle by ID                     | `None`                                                        | `204 No Content`        |

**Schema Details (for POST/PUT/PATCH):**

- `VehicleCreate`: `{"model": "string", "brand_id": int, "color": "string", "year": int, "description": "string", "is_sold": bool}`
- `VehicleUpdate`: Same as `VehicleCreate`, all fields required.
- `VehiclePatch`: All fields optional. `{"model"?: "string", "brand_id"?: int, ...}`

## 8. Running Tests

To run the entire test suite:

```bash
uv run pytest app/tests/ -v
# or simply
uv run pytest -v
```

To run tests for a specific module:

```bash
uv run pytest app/tests/test_brand.py
uv run pytest app/tests/test_vehicle.py
```
