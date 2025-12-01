# Feature Specification: Complete Astrological Chart and Traditional Chinese UI

**Feature Branch**: `002-complete-astro-chart`
**Created**: 2025-12-01
**Status**: Draft
**Input**: User description: "我想要讓輸出的星盤更完整，請參考 @example-astro.png ，使用介面請使用繁體中文"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate and View a Complete Astrological Chart (Priority: P1)

As a user, I want to generate a complete astrological chart based on my birth data, so that I can see a detailed representation of my astrological profile in Traditional Chinese.

**Why this priority**: This is the core feature request, providing the primary value to the user.

**Independent Test**: Can be fully tested by entering birth data, generating the chart, and verifying that the output matches the specified completeness and language.

**Acceptance Scenarios**:

1.  **Given** a user has entered their birth date, time, and location,
    **When** they request to generate a chart,
    **Then** the system displays a circular astrological chart.
2.  **Given** the chart is displayed,
    **When** the user inspects the chart,
    **Then** it includes the zodiac signs, 12 houses, and the positions of all planets (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto), Ascendant (ASC), Descendant (DSC), Midheaven (MC), and Imum Coeli (IC).
3.  **Given** the chart is displayed,
    **When** the user views the accompanying table,
    **Then** the table lists all celestial bodies with their corresponding zodiac sign, degree, and house number.
4.  **Given** the chart is displayed,
    **When** the user examines the interface,
    **Then** all labels, headings, and text are displayed in Traditional Chinese.
5.  **Given** the chart is displayed,
    **When** the user looks for aspect lines,
    **Then** lines representing major aspects (conjunction, opposition, trine, square) are drawn between planets.

### Edge Cases

-   What happens if the user provides an invalid birth date or time? The system should display a clear error message in Traditional Chinese.
-   How does the system handle locations where the timezone is ambiguous? [NEEDS CLARIFICATION: How should the system resolve ambiguous locations? Should it ask the user for more information, or use a default?]

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST generate a circular astrological chart image.
-   **FR-002**: The chart MUST display zodiac signs, 12 houses, and planet glyphs at their calculated positions.
-   **FR-003**: The chart MUST include positions for the Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, ASC, DSC, MC, and IC.
-   **FR-004**: The system MUST display a table detailing the zodiac sign, degree (to the minute), and house for each of the bodies listed in FR-003.
-   **FR-005**: The system MUST draw aspect lines for major aspects (e.g., 90°, 120°, 180°).
-   **FR-006**: All text in the user interface related to chart generation and display MUST be in Traditional Chinese.
-   **FR-007**: The system MUST provide feedback if the user inputs invalid birth data.

### Key Entities

-   **Natal Chart**: Represents the astrological chart for a specific person and birth time. Key attributes include:
    -   Birth Data (Date, Time, Location)
    -   Planet Positions (Zodiac Sign, Degree, House)
    -   House Cusps
    -   Aspects

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: The generated astrological chart contains all elements present in the reference image (`example-astro.png`), including planets, signs, houses, aspects, and the positions table.
-   **SC-002**: 100% of the UI text for the chart generation and display feature is in Traditional Chinese.
-   **SC-003**: The system correctly calculates and displays planet and house positions with 100% accuracy against a trusted third-party astrology calculation library.