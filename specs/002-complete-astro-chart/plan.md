# Implementation Plan: Complete Astrological Chart and Traditional Chinese UI

**Branch**: `002-complete-astro-chart` | **Date**: 2025-12-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-complete-astro-chart/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature will enhance the astrological chart generation to match the level of detail and presentation shown in the `example-astro.png` reference image. This includes rendering a complete set of planetary bodies, houses, and aspects. A key part of this work is also to ensure the entire user interface for this feature is presented in Traditional Chinese.

The technical approach will involve using the `pyswisseph` library in the Python backend for high-precision astrological calculations and the `d3.js` library in the React frontend to render a detailed and accurate SVG-based chart. Internationalization will be handled by `react-i18next`.

## Technical Context

**Language/Version**: Python 3.11+, Node.js 20+
**Primary Dependencies**: React (Vite), Tailwind CSS, FastAPI
**New Dependencies**:
- **Backend**: `pyswisseph`
- **Frontend**: `d3`, `react-i18next`
**Storage**: N/A
**Testing**: Pytest (backend), Vitest/React Testing Library (frontend)
**Target Platform**: Web (Desktop & Mobile browsers)
**Project Type**: Web Application
**Performance Goals**: Fast-loading UI, responsive chart generation under 2 seconds.
**Constraints**:
- Adherence to the five core constitutional principles.
- The visual output of the chart must be as close as possible to `example-astro.png`.
- **Font Selection**: Traditional Chinese text uses `Source Han Serif (思源宋體)` for a traditional serif feel; Latin characters and numerals use `Source Han Sans` for readability and modern aesthetics. Both are open-source and provide full Traditional Chinese coverage.
**Scale/Scope**: Single-user chart generation.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Simplicity & Focus**: Does this feature adhere to the core function of generating a single natal chart? (Pass: It enhances the existing core function.)
- [x] **II. Modern Frontend Stack**: Is the implementation using React, Vite, and Tailwind CSS correctly? (Pass: The plan uses the established frontend stack.)
- [x] **III. Python-Powered Backend**: Is all calculation logic contained within the Python backend? (Pass: All new calculations will reside in the backend.)
- [x] **IV. Clear API Boundary**: Is there a well-defined API contract between the frontend and backend? (Pass: A RESTful API will be defined in Phase 1.)
- [x] **V. Testability**: Are there corresponding unit/integration tests for the new frontend and backend code? (Pass: Testing is a required part of the implementation.)

## Project Structure

### Documentation (this feature)

```text
specs/002-complete-astro-chart/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── openapi.json
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── api/
│   │   └── main.py        # Add new chart endpoint here
│   ├── core/
│   │   └── calculations.py # Add new calculation logic here
│   └── models/
│       └── chart.py       # Update chart models
└── tests/
    ├── integration/
    │   └── test_api.py
    └── unit/
        └── test_calculations.py

frontend/
├── public/
│   └── locales/           # Add translation files here
│       └── zh_Hant/
│           └── translation.json
├── src/
│   ├── components/
│   │   └── NatalChart.jsx # Enhance this component
│   ├── services/
│   │   └── api.js         # Add new API call
│   └── i18n.js            # i18next configuration
└── tests/
    └── component/
        └── NatalChart.spec.js
```

**Structure Decision**: The project follows a standard monorepo structure. New logic will be integrated into the existing `frontend` and `backend` applications.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |