# Feature Specification: Personal Astro Chart Generator

**Feature Branch**: `001-personal-astro-chart`
**Created**: 2025-11-30
**Status**: Draft
**Input**: User description: "我們先設計一個簡單的個人星盤查詢功能，前端頁面可以接受出生日期時間，出生國家及城市，然後可以繪製出對應的星盤"

## Clarifications
### Session 2025-11-30
- Q: How should the system handle an ambiguous city name? → A: Present the user with a list of matching cities to choose from.
- Q: What level of detail should be displayed on the chart initially? → A: Include major aspects (e.g., Conjunction, Sextile, Square, Trine, Opposition) between planets.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate a Natal Chart (Priority: P1)

As a user interested in astrology, I want to enter my birth date, time, and location, so that I can see a visual representation of my personal natal chart.

**Why this priority**: This is the core and only feature of the application. Without it, the application has no value.

**Independent Test**: This can be fully tested by entering valid birth information, generating the chart, and verifying that a chart image is displayed. It delivers the primary value proposition of the application.

**Acceptance Scenarios**:

1.  **Given** a user is on the chart generation page,
    **When** they enter a valid date (e.g., "1990-05-15"), time (e.g., "14:30"), country (e.g., "USA"), and city (e.g., "New York"), and click "Generate Chart",
    **Then** the system displays a visual natal chart.

2.  **Given** a user is on the chart generation page,
    **When** they enter an invalid date (e.g., "1990-02-30"),
    **Then** the system displays a clear error message like "Invalid date provided."

3.  **Given** a user is on the chart generation page,
    **When** they leave the city field blank and click "Generate Chart",
    **Then** the system displays a clear error message like "City is a required field."

4.  **Given** a user has generated a chart,
    **When** they look at the chart,
    **Then** it correctly shows the positions of the sun, moon, and planets in their respective zodiac signs and houses.

### Edge Cases
- **Invalid Timezone**: What happens if the city and country combination does not resolve to a valid timezone? The system should default to a standard timezone (like UTC) and notify the user, or show an error.
- **Leap Years**: How does the system handle birth dates on February 29th? It must correctly validate and process these dates.
- **Ambiguous City Names**: If a city name returns multiple results, the system must present the user with a list of matching locations (e.g., "Springfield, Illinois, USA" vs. "Springfield, Massachusetts, USA") to select from.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST provide user interface fields for Date of Birth, Time of Birth, Country, and City.
-   **FR-002**: The system MUST validate that all required fields are filled before attempting to generate a chart.
-   **FR-003**: The system MUST validate the date and time inputs for correctness (e.g., no 61st minute, no 32nd day of a month).
-   **FR-004**: The system MUST use the provided location data to determine the correct geographic coordinates and timezone for calculation.
-   **FR-005**: The system MUST accurately calculate the positions of celestial bodies (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto) and house cusps (Placidus system).
-   **FR-006**: The system MUST render a visual, graphical representation of the natal chart showing the zodiac wheel, planets in signs, and house divisions.
-   **FR-007**: The system MUST also display major aspects (e.g., Conjunction, Sextile, Square, Trine, Opposition) between planets on the chart.

### Key Entities *(include if feature involves data)*

-   **BirthInput**: Represents the user's provided data.
    -   Attributes: date (YYYY-MM-DD), time (HH:MM), country (string), city (string).
-   **NatalChart**: Represents the calculated astrological chart.
    -   Attributes: A collection of planet positions (planet, sign, degree), a collection of house cusps (house number, sign, degree), and a list of major aspects (aspect type, orb, involved planets).

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 95% of users can successfully generate a chart on their first attempt without encountering a validation error (assuming valid data).
-   **SC-002**: The end-to-end chart generation, from clicking the "Generate Chart" button to the chart being displayed, must take less than 5 seconds.
-   **SC-003**: The calculated planetary positions must be accurate to within 1 degree of arc when compared to the official Swiss Ephemeris (e.g., Swiss Ephemeris) for 100 test cases spanning different dates and locations.
-   **SC-04**: The application's user interface must achieve a Lighthouse accessibility score of 90 or higher.