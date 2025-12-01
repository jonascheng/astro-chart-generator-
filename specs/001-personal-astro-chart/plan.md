# Implementation Plan: Personal Astro Chart Generator

**Branch**: `001-personal-astro-chart` | **Date**: 2025-12-01 | **Spec**: [/Users/jonas/Git/personal/astro-chart-generator/specs/001-personal-astro-chart/spec.md]

**Input**: Feature specification from `/specs/001-personal-astro-chart/spec.md`

## Summary

This plan outlines the implementation of a personal astrology natal chart generator. The primary feature allows a user to input their birth date, time, and location to generate a visual representation of their natal chart. The technical approach involves a React frontend (with Vite and Tailwind CSS) communicating with a Python backend that uses `pyswisseph` for astrological calculations. The application will be containerized with Docker for deployment, and local development will be managed using `pyenv`.

## Technical Context

**Language/Version**: Python 3.11+, Node.js 20+
**Primary Dependencies**:
- **Frontend**: React (Vite), Tailwind CSS
- **Backend**: Python, `pyswisseph`, FastAPI
**Storage**: N/A
**Testing**: Pytest (backend), Vitest/React Testing Library (frontend)
**Target Platform**: Web (Desktop & Mobile browsers)
**Project Type**: Web Application
**Performance Goals**: Chart generation under 5 seconds, Lighthouse accessibility score > 90.
**Constraints**: Adherence to the five core constitutional principles.
**DevOps**: `pyenv` for local Python version management, Docker for containerization and deployment.
**Scale/Scope**: Single-user chart generation.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [X] **I. Simplicity & Focus**: The feature adheres to the core function of generating a single natal chart.
- [X] **II. Modern Frontend Stack**: The implementation uses React, Vite, and Tailwind CSS as specified.
- [X] **III. Python-Powered Backend**: All calculation logic will be in the Python backend.
- [X] **IV. Clear API Boundary**: A well-defined API contract (`openapi.json`) has been created.
- [ ] **V. Testability**: Tests need to be written. This will be part of the implementation tasks.

## Project Structure

### Documentation (this feature)

```text
specs/001-personal-astro-chart/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── api/             # API endpoints (FastAPI)
│   ├── core/            # Core astrological calculation logic using pyswisseph
│   └── models/          # Data models (Pydantic)
└── tests/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── components/      # Reusable React components
│   ├── pages/           # Main pages/views
│   ├── services/        # API communication services
│   └── styles/          # Tailwind CSS configuration and custom styles
└── tests/
    ├── component/
    └── unit/
```

**Structure Decision**: The project follows a standard monorepo structure with a `frontend` directory for the React application and a `backend` directory for the Python API. This aligns with Principle IV (Clear API Boundary).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [Principle ID] | [Justification for deviation] | [Reasoning] |
