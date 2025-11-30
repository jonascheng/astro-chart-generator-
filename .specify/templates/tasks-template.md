---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are a constitutional requirement.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- All backend code lives in `backend/` (e.g., `backend/src/api/`, `backend/tests/`).
- All frontend code lives in `frontend/` (e.g., `frontend/src/components/`, `frontend/tests/`).

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create `backend` and `frontend` directory structures per implementation plan.
- [ ] T002 Initialize Python project in `backend/` with FastAPI/Flask dependencies.
- [ ] T003 Initialize React project in `frontend/` with Vite.
- [ ] T004 [P] Configure linting and formatting tools for both Python and TypeScript/React.

---

## Phase 2: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Backend unit test for [calculation] in `backend/tests/unit/test_core.py`.
- [ ] T011 [P] [US1] API contract test for [endpoint] in `backend/tests/integration/test_api.py`.
- [ ] T012 [P] [US1] Frontend component test for [ChartComponent] in `frontend/tests/component/ChartComponent.test.tsx`.

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create data model for [ChartData] in `backend/src/models/chart.py`.
- [ ] T014 [US1] Implement [Astrological Calculation] in `backend/src/core/calculator.py`.
- [ ] T015 [US1] Create API endpoint for chart generation in `backend/src/api/main.py`.
- [ ] T016 [P] [US1] Create API service for fetching chart data in `frontend/src/services/api.ts`.
- [ ] T017 [P] [US1] Create [ChartInputForm] React component in `frontend/src/components/ChartInputForm.tsx`.
- [ ] T018 [US1] Implement the main chart view page in `frontend/src/pages/ChartView.tsx`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Documentation updates for API and frontend components.
- [ ] TXXX Code cleanup and refactoring.
- [ ] TXXX Security hardening for the API.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: User Story 1
3. **STOP and VALIDATE**: Test User Story 1 independently.
4. Deploy/demo if ready.
