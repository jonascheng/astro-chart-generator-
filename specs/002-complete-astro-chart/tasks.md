# Actionable Tasks for Complete Astrological Chart

**Branch**: `002-complete-astro-chart`
**Implementation Plan**: [plan.md](./plan.md)

This document breaks down the implementation of the "Complete Astrological Chart" feature into a series of actionable tasks, organized by development phase and user story.

## Phase 1: Setup & Configuration

This phase prepares the development environment by installing new dependencies and setting up the necessary configuration files.

- [x] T001 Install `pyswisseph` dependency in the `backend` directory.
- [x] T002 Install `d3`, `react-i18next`, and `i18next` dependencies in the `frontend` directory.
- [x] T003 Download Swiss Ephemeris data files and place them in `backend/src/core/ephe/`.
- [x] T004 Create and configure the `i18next` initialization file at `frontend/src/i18n.js`.
- [x] T005 Create the Traditional Chinese translation file at `frontend/public/locales/zh_Hant/translation.json`.

## Phase 2: User Story 1 - Generate and View a Complete Astrological Chart

**Goal**: A user can enter their birth data and see a complete astrological chart rendered in the browser, with all UI text in Traditional Chinese.
**Independent Test**: Enter birth data, generate the chart, and verify that the chart, positions table, and all labels are rendered correctly as per the spec.

- [x] T006 [US1] Update the Pydantic models in `backend/src/models/chart.py` to match the structure defined in `data-model.md`.
- [x] T007 [US1] Implement the core calculation logic in `backend/src/core/calculations.py` using `pyswisseph` to generate the complete `ChartData` object.
- [x] T008 [US1] Implement the `POST /chart` endpoint in `backend/src/api/main.py` which uses the calculation logic and returns the `ChartData` object.
- [x] T009 [US1] Create a new service function in `frontend/src/services/api.js` to send a POST request to the `/chart` endpoint.
- [x] T010 [US1] Enhance the `frontend/src/pages/ChartPage.jsx` to fetch chart data using the new API service and pass it as a prop to the chart component.
- [x] T011 [US1] Implement the D3.js rendering logic in `frontend/src/components/NatalChart.jsx` to draw the main structure of the chart (zodiac ring, house lines) based on the received `ChartData`.
- [x] T012 [US1] Extend the D3.js logic in `frontend/src/components/NatalChart.jsx` to render the planet glyphs at their correct positions.
- [x] T013 [US1] Extend the D3.js logic in `frontend/src/components/NatalChart.jsx` to draw the aspect lines between planets.
- [x] T014 [US1] Create a new component `frontend/src/components/PositionsTable.jsx` that takes the `planets` and `points` data and renders the positions table.
- [x] T015 [US1] Integrate the `PositionsTable.jsx` component into `frontend/src/pages/ChartPage.jsx`.
- [x] T016 [US1] Integrate `react-i18next` throughout the new and modified components to ensure all UI text is translated.

## Phase 3: User Story 2 - Print the Astrological Chart

**Goal**: A user can print their generated chart.
**Independent Test**: Click the "Print Chart" button and verify that the browser's print dialog opens with a print-friendly version of the chart.

- [x] T017 [US2] Add a "Print Chart" button to the `frontend/src/pages/ChartPage.jsx` component.
- [x] T018 [US2] Implement the `onClick` handler for the print button to trigger the browser's print functionality. Create print-specific CSS to ensure the chart is formatted correctly for printing.

## Phase 4: Polish & Cross-Cutting Concerns

- [ ] T019 Review the final rendered chart and positions table, making stylistic adjustments in the CSS to ensure it closely matches `example-astro.png`.
- [ ] T020 Implement error handling in the frontend to gracefully manage API errors or invalid data responses from the backend.

## Dependency Graph

- **User Story 1 (US1)** is the foundational story and has no dependencies on other stories.
- **User Story 2 (US2)** depends on the completion of User Story 1, as the chart must be generated before it can be printed.

```
[US1] -> [US2]
```

## Sequential Execution

- All tasks within User Story 1 will be executed in order from T006 through T016.
- User Story 2 can be started as soon as the main chart component from User Story 1 is rendering data (after T013).

## Implementation Strategy

The implementation will follow a phased approach, focusing on delivering User Story 1 as the Minimum Viable Product (MVP). This ensures the core functionality of generating and viewing a chart is delivered first. User Story 2 and the final polishing phase will build upon this foundation.
