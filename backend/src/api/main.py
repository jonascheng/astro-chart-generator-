"""Main FastAPI application for the astro chart generator."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.models import (
    BirthInput,
    NatalChart,
    PlanetPosition,
    HouseCusp,
    MajorAspect,
)

app = FastAPI(
    title="Astro Chart Generator API",
    description="API for generating personal natal charts",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


def _get_mock_natal_chart() -> NatalChart:
    """Generate a mock natal chart for testing."""
    planets = [
        PlanetPosition(name="Sun", sign="Aries", degrees=15.75),
        PlanetPosition(name="Moon", sign="Taurus", degrees=22.3),
        PlanetPosition(name="Mercury", sign="Aries", degrees=10.5),
        PlanetPosition(name="Venus", sign="Gemini", degrees=18.2),
        PlanetPosition(name="Mars", sign="Cancer", degrees=5.8),
        PlanetPosition(name="Jupiter", sign="Leo", degrees=28.4),
        PlanetPosition(name="Saturn", sign="Virgo", degrees=12.1),
    ]

    houses = [
        HouseCusp(house_number=1, sign="Aries", degrees=10.5),
        HouseCusp(house_number=2, sign="Taurus", degrees=15.2),
        HouseCusp(house_number=3, sign="Gemini", degrees=20.8),
        HouseCusp(house_number=4, sign="Cancer", degrees=25.1),
        HouseCusp(house_number=5, sign="Leo", degrees=27.6),
        HouseCusp(house_number=6, sign="Virgo", degrees=28.3),
        HouseCusp(house_number=7, sign="Libra", degrees=10.5),
        HouseCusp(house_number=8, sign="Scorpio", degrees=15.2),
        HouseCusp(house_number=9, sign="Sagittarius", degrees=20.8),
        HouseCusp(house_number=10, sign="Capricorn", degrees=25.1),
        HouseCusp(house_number=11, sign="Aquarius", degrees=27.6),
        HouseCusp(house_number=12, sign="Pisces", degrees=28.3),
    ]

    aspects = [
        MajorAspect(
            aspect_type="Conjunction",
            planet1="Sun",
            planet2="Mercury",
            orb=5.25,
        ),
        MajorAspect(
            aspect_type="Sextile",
            planet1="Sun",
            planet2="Venus",
            orb=2.45,
        ),
        MajorAspect(
            aspect_type="Square",
            planet1="Moon",
            planet2="Mars",
            orb=16.5,
        ),
        MajorAspect(
            aspect_type="Trine",
            planet1="Venus",
            planet2="Jupiter",
            orb=10.2,
        ),
    ]

    return NatalChart(planets=planets, houses=houses, aspects=aspects)


@app.post("/chart", response_model=NatalChart)
async def generate_chart(birth_input: BirthInput) -> NatalChart:
    """
    Generate a natal chart based on birth information.

    Takes birth date, time, and location as input and returns
    calculated natal chart data.
    """
    # Mock implementation - returns static chart data
    # TODO: Replace with real pyswisseph calculations
    return _get_mock_natal_chart()
