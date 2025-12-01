# Tasks: Personal Astro Chart Generator

**Input**: Design documents from `/specs/001-personal-astro-chart/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The user has requested a Test-Driven Development (TDD) approach. Test tasks are included and should be written first.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [Story] Description`


- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- All backend code lives in `backend/` (e.g., `backend/src/api/`, `backend/tests/`).
- All frontend code lives in `frontend/` (e.g., `frontend/src/components/`, `frontend/tests/`).

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create `backend` and `frontend` directory structures per implementation plan.
- [X] T002 Initialize Python project in `backend/` with FastAPI dependencies and create `.python-version` file.
- [X] T003 Initialize React project in `frontend/` with Vite and Tailwind CSS.
- [X] T004 Create `docker-compose.yml`, `backend/Dockerfile`, and `frontend/Dockerfile` per the research decisions.
- [X] T005 Configure linting and formatting tools for both Python (Ruff) and TypeScript/React (ESLint, Prettier).

---

## Phase 2: Foundational (Backend Models)

**Purpose**: Define the core data structures in the backend.

- [X] T006 Implement Pydantic models for `BirthInput` and `NatalChart` in `backend/src/models/chart.py` based on `data-model.md`.

---

## Phase 3: User Story 1 - Generate a Natal Chart (Priority: P1) 🎯 MVP

**Goal**: As a user, I want to enter my birth date, time, and location to see a visual representation of my personal natal chart.

**Independent Test**: Enter valid birth information, click "Generate Chart", and verify that a chart image is displayed, initially with mock data, then with real data.

### Backend: API Layer (Mock)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T007 [US1] Write an integration test for the `/chart` endpoint expecting a successful response in `backend/tests/integration/test_api.py`.
- [ ] T008 [US1] Implement a mock API for the `/chart` endpoint that returns a static, valid `NatalChart` response in `backend/src/api/main.py`.
- [ ] T009 [US1] Refine the integration test to check for specific fields in the mock response in `backend/tests/integration/test_api.py`.

### Frontend: UI and API Integration

- [ ] T010 [US1] Create the basic UI layout for the chart generation page with input fields and a button in `frontend/src/pages/ChartPage.jsx`.
- [ ] T011 [US1] Implement a service to call the backend's `/chart` endpoint in `frontend/src/services/api.js`.
- [ ] T012 [US1] Connect the UI to the API service and display the raw JSON data from the mock backend in `frontend/src/pages/ChartPage.jsx`.

**Checkpoint**: At this point, the frontend form should be able to make a request to the backend and display the mock JSON response.

### Backend: Core Logic (Real Implementation)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [US1] Write unit tests for the core astrological calculation logic in `backend/tests/unit/test_calculations.py`.
- [ ] T014 [US1] Implement the real astrological calculation logic using `pyswisseph` in `backend/src/core/calculations.py`. This will replace the mock response.
- [ ] T015 [US1] Integrate the real calculation logic into the `/chart` endpoint in `backend/src/api/main.py`.
- [ ] T016 [US1] Update the integration test in `backend/tests/integration/test_api.py` to use a known date/time/location and assert that the calculated positions are correct within a tolerance.

### Frontend: Visualization

- [ ] T017 [US1] Implement the chart visualization component to render the data from the API in `frontend/src/components/NatalChart.jsx`.
- [ ] T018 [US1] Integrate the chart visualization component into the main page in `frontend/src/pages/ChartPage.jsx`, replacing the raw JSON display.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T019 Add client-side validation for the input form in `frontend/src/pages/ChartPage.jsx`.
- [ ] T020 Add error handling to the frontend to display messages from the API (e.g., for invalid locations) in `frontend/src/pages/ChartPage.jsx`.
- [ ] T021 Implement structured logging in the backend in `backend/src/api/main.py`.
- [ ] T022 Review and improve the accessibility of the frontend, aiming for a Lighthouse score of 90+.

---

## Dependencies & Parallel Execution

### Story Dependencies
- **User Story 1** is the foundational story and has no dependencies on other stories.



## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete **Phase 1: Setup**.
2.  Complete **Phase 2: Foundational**.
3.  Implement **Phase 3: User Story 1** incrementally, following the TDD approach and checkpoints.
4.  **STOP and VALIDATE**: After `T018`, User Story 1 is complete and should be thoroughly tested.
5.  Optionally, begin **Phase 4: Polish** tasks.
