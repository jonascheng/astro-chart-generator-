"""Data models for the astro chart generator."""

from datetime import date, time
from typing import List

from pydantic import BaseModel, Field, field_validator


class PlanetPosition(BaseModel):
    """Represents a planet's position in the zodiac."""

    name: str = Field(..., description="Planet name (e.g., 'Sun', 'Moon')")
    sign: str = Field(
        ..., description="Zodiac sign (e.g., 'Aries', 'Taurus')"
    )
    degrees: float = Field(
        ..., ge=0, le=360, description="Position in degrees (0-360)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sun",
                "sign": "Aries",
                "degrees": 15.75,
            }
        }


class HouseCusp(BaseModel):
    """Represents the cusp of an astrological house."""

    house_number: int = Field(
        ..., ge=1, le=12, description="House number (1-12)"
    )
    sign: str = Field(..., description="Zodiac sign")
    degrees: float = Field(
        ..., ge=0, le=360, description="Position in degrees (0-360)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "house_number": 1,
                "sign": "Aries",
                "degrees": 10.5,
            }
        }


class MajorAspect(BaseModel):
    """Represents a major aspect between two planets."""

    aspect_type: str = Field(
        ...,
        description=(
            "Type of aspect (Conjunction, Sextile, Square, Trine, "
            "Opposition)"
        ),
    )
    planet1: str = Field(..., description="First planet name")
    planet2: str = Field(..., description="Second planet name")
    orb: float = Field(
        ...,
        ge=0,
        le=360,
        description="Orb (degree of deviation from perfect aspect)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "aspect_type": "Conjunction",
                "planet1": "Sun",
                "planet2": "Moon",
                "orb": 2.5,
            }
        }


class NatalChart(BaseModel):
    """Represents a calculated natal chart."""

    planets: List[PlanetPosition] = Field(
        ..., description="List of planetary positions"
    )
    houses: List[HouseCusp] = Field(
        ..., description="List of house cusps"
    )
    aspects: List[MajorAspect] = Field(
        ..., description="List of major aspects"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "planets": [
                    {"name": "Sun", "sign": "Aries", "degrees": 15.75},
                    {"name": "Moon", "sign": "Taurus", "degrees": 22.3},
                ],
                "houses": [
                    {
                        "house_number": 1,
                        "sign": "Aries",
                        "degrees": 10.5,
                    },
                    {
                        "house_number": 2,
                        "sign": "Taurus",
                        "degrees": 15.2,
                    },
                ],
                "aspects": [
                    {
                        "aspect_type": "Conjunction",
                        "planet1": "Sun",
                        "planet2": "Moon",
                        "orb": 2.5,
                    }
                ],
            }
        }


class BirthInput(BaseModel):
    """Represents user input for natal chart generation."""

    date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Birth date in YYYY-MM-DD format",
    )
    time: str = Field(
        ..., pattern=r"^\d{2}:\d{2}$", description="Birth time in HH:MM format"
    )
    country: str = Field(..., min_length=1, description="Birth country")
    city: str = Field(..., min_length=1, description="Birth city")

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        """Validate that date is a valid calendar date."""
        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError(
                "Date must be a valid calendar date in YYYY-MM-DD format"
            )
        return v

    @field_validator("time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        """Validate that time is a valid time."""
        try:
            parts = v.split(":")
            if len(parts) != 2:
                raise ValueError()
            hour, minute = int(parts[0]), int(parts[1])
            time(hour=hour, minute=minute)
        except (ValueError, TypeError):
            raise ValueError("Time must be a valid time in HH:MM format")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "date": "1990-06-15",
                "time": "14:30",
                "country": "USA",
                "city": "New York",
            }
        }
