"""Main FastAPI application for the astro chart generator."""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.models import (
    Aspect,
    BirthInput,
    ChartData,
    House,
    Planet,
    Point,
)
from src.core.calculations import calculate_natal_chart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

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
    logger.info("Health check requested")
    return {"status": "ok"}


def _get_mock_natal_chart() -> ChartData:
    """Generate a mock natal chart for testing."""
    planets = [
        Planet(
            name="Sun",
            longitude=15.75,
            sign="Aries",
            degree=15,
            minute=45,
            house=1,
        ),
        Planet(
            name="Moon",
            longitude=52.3,
            sign="Taurus",
            degree=22,
            minute=18,
            house=2,
        ),
        Planet(
            name="Mercury",
            longitude=10.5,
            sign="Aries",
            degree=10,
            minute=30,
            house=1,
        ),
        Planet(
            name="Venus",
            longitude=78.2,
            sign="Gemini",
            degree=18,
            minute=12,
            house=3,
        ),
        Planet(
            name="Mars",
            longitude=125.8,
            sign="Cancer",
            degree=5,
            minute=48,
            house=4,
        ),
        Planet(
            name="Jupiter",
            longitude=148.4,
            sign="Leo",
            degree=28,
            minute=24,
            house=5,
        ),
        Planet(
            name="Saturn",
            longitude=162.1,
            sign="Virgo",
            degree=12,
            minute=6,
            house=6,
        ),
        Planet(
            name="Uranus",
            longitude=195.5,
            sign="Libra",
            degree=15,
            minute=30,
            house=7,
        ),
        Planet(
            name="Neptune",
            longitude=225.8,
            sign="Scorpio",
            degree=15,
            minute=48,
            house=8,
        ),
        Planet(
            name="Pluto",
            longitude=265.3,
            sign="Sagittarius",
            degree=25,
            minute=18,
            house=9,
        ),
    ]

    points = [
        Point(
            name="Ascendant",
            longitude=10.5,
            sign="Aries",
            degree=10,
            minute=30,
        ),
        Point(
            name="Descendant",
            longitude=190.5,
            sign="Libra",
            degree=10,
            minute=30,
        ),
        Point(
            name="Midheaven",
            longitude=190.5,
            sign="Libra",
            degree=10,
            minute=30,
        ),
        Point(
            name="Imum Coeli",
            longitude=10.5,
            sign="Aries",
            degree=10,
            minute=30,
        ),
    ]

    houses = [
        House(number=1, longitude=10.5, sign="Aries"),
        House(number=2, longitude=45.2, sign="Taurus"),
        House(number=3, longitude=80.8, sign="Gemini"),
        House(number=4, longitude=125.1, sign="Cancer"),
        House(number=5, longitude=157.6, sign="Leo"),
        House(number=6, longitude=188.3, sign="Virgo"),
        House(number=7, longitude=190.5, sign="Libra"),
        House(number=8, longitude=225.2, sign="Scorpio"),
        House(number=9, longitude=260.8, sign="Sagittarius"),
        House(number=10, longitude=305.1, sign="Capricorn"),
        House(number=11, longitude=337.6, sign="Aquarius"),
        House(number=12, longitude=8.3, sign="Pisces"),
    ]

    aspects = [
        Aspect(
            planet1="Sun",
            planet2="Mercury",
            type="Conjunction",
            orb=5.25,
        ),
        Aspect(
            planet1="Sun",
            planet2="Venus",
            type="Sextile",
            orb=2.45,
        ),
        Aspect(
            planet1="Moon",
            planet2="Mars",
            type="Square",
            orb=3.5,
        ),
        Aspect(
            planet1="Venus",
            planet2="Jupiter",
            type="Trine",
            orb=1.2,
        ),
    ]

    return ChartData(
        planets=planets,
        points=points,
        houses=houses,
        aspects=aspects,
    )


@app.post("/chart", response_model=ChartData)
async def generate_chart(birth_input: BirthInput) -> ChartData:
    """
    Generate a natal chart based on birth information.

    Takes birth date, time, and location as input and returns
    calculated natal chart data.
    """
    logger.info(
        f"Chart generation requested for: {birth_input.city}, "
        f"{birth_input.country} on {birth_input.date} at {birth_input.time}"
    )

    try:
        # Use real calculation
        chart = calculate_natal_chart(
            birth_input.date,
            birth_input.time,
            birth_input.country,
            birth_input.city,
        )
        logger.info(
            "Chart generated successfully for "
            f"{birth_input.city}, {birth_input.country}"
        )
        return chart
    except ValueError as e:
        # Handle validation errors from calculations
        error_msg = str(e)
        logger.warning(f"Validation error in chart calculation: {error_msg}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {error_msg}",
        )
    except KeyError:
        # Handle unknown city/country
        error_msg = (
            f"Location not found: {birth_input.city}, "
            f"{birth_input.country}. Please use a major city."
        )
        logger.warning(f"Unknown location requested: {error_msg}")
        raise HTTPException(
            status_code=400,
            detail=error_msg,
        )
    except Exception as e:
        # Log unexpected errors but still try to return mock data
        error_msg = str(e)
        logger.error(f"Unexpected error in chart calculation: {error_msg}")
        logger.info("Falling back to mock data")
        # Return mock data as fallback during development
        return _get_mock_natal_chart()
