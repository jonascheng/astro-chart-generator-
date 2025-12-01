# Quickstart Guide

This guide provides instructions on how to set up and run the Astro Chart Generator application locally for development.

## Prerequisites

-   **Node.js**: Version 20+
-   **`pyenv`**: For managing Python versions.
-   **Docker**: For running the application services.
-   **`make`**: For using the simplified commands in the Makefile.

## 1. Environment Setup

### Frontend

The frontend is a standard Vite-based React application.

```bash
cd frontend
npm install
```

### Backend

The backend is a Python application. The required Python version is managed by `pyenv`.

```bash
cd backend
# The .python-version file will be used by pyenv automatically
pyenv install $(cat .python-version)
pip install -r requirements.txt
```

## 2. Running the Application with Docker

The easiest way to run the entire application stack is using `docker-compose`.

1.  **Build and Start Services**:
    From the project root directory, run:

    ```bash
    docker-compose up --build
    ```

    This command will:
    -   Build the Docker image for the `frontend` service.
    -   Build the Docker image for the `backend` service.
    -   Start both containers.

2.  **Accessing the Application**:
    -   **Frontend**: Open your browser and navigate to `http://localhost:5173` (or the port specified in `docker-compose.yml`).
    -   **Backend API**: The API will be available at `http://localhost:8000`. The interactive API documentation can be accessed at `http://localhost:8000/docs`.

## 3. Local Development without Docker

For more direct development (e.g., with frontend hot-reloading):

### Running the Frontend

```bash
cd frontend
npm run dev
```
The frontend will be available at `http://localhost:5173`.

### Running the Backend

```bash
cd backend
uvicorn src.api.main:app --reload
```
The backend API will be running at `http://localhost:8000`.

## 4. Running Tests

### Frontend

```bash
cd frontend
npm test
```

### Backend

```bash
cd backend
pytest
```
