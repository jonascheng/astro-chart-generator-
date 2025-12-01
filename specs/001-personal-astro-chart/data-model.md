# Data Model

This document defines the data structures for the Personal Astro Chart Generator, based on the entities identified in the feature specification.

## 1. BirthInput

Represents the user's provided data for generating a natal chart. This will be the payload sent from the frontend to the backend API.

-   **Entity**: `BirthInput`
-   **Description**: The data provided by the user to generate a natal chart.
-   **Fields**:
    -   `date`: `string` (format: `YYYY-MM-DD`) - **Required**. The user's birth date.
    -   `time`: `string` (format: `HH:MM`) - **Required**. The user's birth time.
    -   `country`: `string` - **Required**. The user's birth country.
    -   `city`: `string` - **Required**. The user's birth city.
-   **Validation Rules**:
    -   All fields are mandatory.
    -   `date` must be a valid calendar date.
    -   `time` must be a valid time.

## 2. NatalChart

Represents the calculated astrological chart data that the backend will compute and send back to the frontend.

-   **Entity**: `NatalChart`
-   **Description**: The calculated astrological chart, including planet positions, house cusps, and major aspects.
-   **Fields**:
    -   `planets`: `List[PlanetPosition]` - A list of calculated planetary positions.
    -   `houses`: `List[HouseCusp]` - A list of calculated house cusps.
    -   `aspects`: `List[MajorAspect]` - A list of major aspects between planets.

### Supporting Data Structures

#### PlanetPosition
- **Fields**:
    - `name`: `string` (e.g., "Sun", "Moon")
    - `sign`: `string` (e.g., "Aries", "Taurus")
    - `degrees`: `float` (e.g., 15.75)

#### HouseCusp
- **Fields**:
    - `house_number`: `integer` (1-12)
    - `sign`: `string`
    - `degrees`: `float`

#### MajorAspect
- **Fields**:
    - `aspect_type`: `string` (e.g., "Conjunction", "Sextile", "Square", "Trine", "Opposition")
    - `planet1`: `string`
    - `planet2`: `string`
    - `orb`: `float` (The degree of deviation from a perfect aspect)
