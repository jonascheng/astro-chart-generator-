# Research & Decisions

This document records the decisions made to resolve the "NEEDS CLARIFICATION" items from the implementation plan.

## 1. Backend Framework Selection

**Decision**: FastAPI will be used as the web framework for the Python backend.

**Rationale**:
- **Modern & Fast**: FastAPI is a high-performance web framework that aligns with the project's "Modern Frontend Stack" principle (Principle II).
- **Type-Hint Based**: It uses standard Python type hints, which leads to better editor support, code completion, and data validation (Pydantic). This improves developer productivity and code quality.
- **Automatic Documentation**: It automatically generates interactive API documentation (Swagger UI and ReDoc), which is crucial for satisfying Principle IV (Clear API Boundary).
- **Good Fit for Scope**: It is an excellent choice for building RESTful APIs, which is what is needed to connect the frontend and backend.

**Alternatives considered**:
- **Flask**: A solid and mature framework, but it requires more boilerplate and dependencies for features like data validation and async support, which are built into FastAPI.

## 2. DevOps and Deployment Strategy

**Decision**:
1.  **Local Development**: `pyenv` will be used to manage the Python version locally. A `.python-version` file will be placed in the `backend/` directory to lock the version.
2.  **Containerization**: Docker will be used to containerize both the frontend and backend services.
3.  **Orchestration**: `docker-compose.yml` will be used to define and run the multi-container application for both local development and production-like environments.

**Rationale**:
- **`pyenv`**: Ensures all developers work with the same Python version, avoiding "it works on my machine" issues related to the interpreter.
- **Docker**: Provides a consistent and isolated environment for the application, packaging all dependencies. This simplifies deployment and satisfies the user's request.
- **`docker-compose`**: Simplifies the management of multi-service applications. It allows us to define the entire application stack (frontend, backend) in a single file and run it with one command.

### Proposed Docker Setup:

**`backend/Dockerfile`**:
- A multi-stage build.
- The first stage installs dependencies (`pyswisseph`, `fastapi`, `uvicorn`, etc.) using `pip`.
- The second stage copies the application code and the installed dependencies to create a lean production image.

**`frontend/Dockerfile`**:
- A multi-stage build.
- The first stage uses a Node.js image to build the React application using `npm run build`.
- The second stage copies the built static files into a lightweight Nginx container for serving.

**`docker-compose.yml` (at the root):**
- Defines two services: `frontend` and `backend`.
- The `frontend` service builds from `frontend/Dockerfile` and exposes port 80 (or 8080).
- The `backend` service builds from `backend/Dockerfile`, exposes the API port (e.g., 8000), and uses the `.python-version` file to ensure the correct Python version is used.
- Sets up a network for the services to communicate with each other.

This approach provides a robust and reproducible development and deployment workflow.
