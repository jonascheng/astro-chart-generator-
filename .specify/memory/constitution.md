<!--
Sync Impact Report:
- Version change: none → v1.0.0
- Modified principles: none (initial creation)
- Added sections: Core Principles, Governance
- Removed sections: none
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: none
-->
# Astro Chart Generator Constitution

## Core Principles

### I. Simplicity and Focus
The application must focus on its core function: generating a single, accurate astrological natal chart. Features outside this scope, such as synastry, progressions, or detailed interpretations, are explicitly excluded to maintain a clean and focused user experience.

### II. Modern Frontend Stack
The user interface will be a single-page application built with React (managed via Vite) and styled with Tailwind CSS. The UI must be responsive, ensuring a consistent and accessible experience across desktop and mobile browsers.

### III. Python-Powered Backend
All astrological calculations, data processing, and API services shall be implemented in Python. This ensures that the complex domain logic is centralized and managed within a robust, dedicated backend environment.

### IV. Clear API Boundary
A clear, well-documented RESTful or GraphQL API must exist between the frontend and backend. This separation of concerns is critical for independent development, testing, and deployment of the client and server. The contract must be defined and agreed upon before implementation.

### V. Testability
Both the frontend and backend must be independently testable. The frontend will use unit and component tests (e.g., with Vitest/Jest and React Testing Library). The Python backend must have comprehensive unit tests for its calculation engine and API endpoints.

## Governance

Compliance with this constitution is mandatory for all development activities. All feature specifications, implementation plans, and code contributions will be evaluated against these principles.

- **Amendment Process**: Changes to this constitution require a new version bump and a documented rationale.
- **Principle Adherence**: All work must align with the defined principles. Deviations require explicit, temporary exemption approved by the project lead.

**Version**: 1.0.0 | **Ratified**: 2025-11-30 | **Last Amended**: 2025-11-30