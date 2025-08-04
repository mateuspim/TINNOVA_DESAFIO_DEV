# TINNOVA - Teste de Desenvolvimento Python

## 1. Introduction

This repository contains all exercises developed for the Tinnova Challenge. Each exercise is organized in its own folder.

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Technologies Used](#2-technologies-used)
- [3. Project Structure](#3-project-structure)
- [4. Setup and Installation](#4-setup-and-installation)
  - [4.1. Prerequisites](#41-prerequisites)
  - [4.2. Clone the Repository](#42-clone-the-repository)
  - [4.3. Setup Environment Variables](#43-setup-environment-variables)
  - [4.4. Setup Options](#44-setup-options)
- [5. Running the Application](#5-running-the-application)
- [6. Running Tests](#6-running-tests)

## 2. Technologies Used

- **Python** (3.12+): Programming language
- **FastAPI**: High-performance web framework for building APIs
- **Pytest**: Testing framework
- **uv**: Extremely fast Python package and project manager

## 3. Project Structure

```
.
├── exercise-01/                # Vote Counter Exercise
│   └── vote_counter.py
├── exercise-02/                # Bubble Sort Exercise
│   └── bubble_sort.py
├── exercise-03/                # Factorial Exercise
│   └── factorial.py
├── exercise-04/                # Multiples Exercise
│   └── multiples.py
└── exercise-05/                # Backend Challenge
    ├── backend/
    └── frontend/
```

`Simple structure  shown above for a more detailed walktrough, please follow the README of each exercise section`

## 4. Setup and Installation

Follow these steps to get the project up and running on your local machine.

### 4.1. Prerequisites

- Python 3.12+
- `uv` (recommended) or `pip` (Python package installer)

**For Docker:**

- Docker
- Docker Compose (optional)

### 4.2. Clone the Repository

```bash
git clone <repository_url>
cd tinnova_desafio_dev/exercise-0X
```

### 4.3 Setup the env params for backend

```bash
cp app/.env.example app/.env
```

### 4.4. Setup Options

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

#### Option C: Docker (Backend)

1. **Build the Docker image:**

   ```bash
   docker build -t tinnova-backend .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:80 tinnova-backend
   ```

## 5. Running the Application

To start the projects individually, refer to each exercise's README for more details. In general, you can run them with uv:

```bash
# For exercises
uv run python factorial.py

# For Backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 6. Running Tests

To run the entire test suite for each exercise run:

```bash
uv run pytest /tests/ -v
# or simply
uv run pytest -v
```

To run tests for a specific module:

```bash
uv run pytest app/tests/test_{file}.py
uv run pytest app/tests/test_{file}.py
```
