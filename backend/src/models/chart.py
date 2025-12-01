"""Data models for the astro chart generator."""

from datetime import date, time
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class Planet(BaseModel):
    """Represents a planet or celestial body position."""

    name: str = Field(..., description="Planet name (e.g., 'Sun', 'Moon')")
    longitude: float = Field(
        ..., ge=0, le=360, description="Celestial longitude in degrees"
    )
    sign: str = Field(..., description="Zodiac sign (e.g., 'Aries')")
    degree: int = Field(..., ge=0, le=29, description="Degree within sign")
    minute: int = Field(..., ge=0, le=59, description="Minute within degree")
    house: int = Field(
        ..., ge=1, le=12, description="House number (1-12)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sun",
                "longitude": 274.34,
                "sign": "Capricorn",
                "degree": 4,
                "minute": 20,
                "house": 3,
            }
        }


class Point(BaseModel):
    """Represents a key astrological point (AC, MC, etc.)."""

    name: str = Field(
        ...,
        description="Point name (e.g., 'Ascendant', 'MC')",
    )
    longitude: float = Field(
        ..., ge=0, le=360, description="Celestial longitude in degrees"
    )
    sign: str = Field(..., description="Zodiac sign")
    degree: int = Field(..., ge=0, le=29, description="Degree within sign")
    minute: int = Field(..., ge=0, le=59, description="Minute within degree")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ascendant",
                "longitude": 153.25,
                "sign": "Virgo",
                "degree": 3,
                "minute": 15,
            }
        }


class House(BaseModel):
    """Represents a house cusp."""

    number: int = Field(..., ge=1, le=12, description="House number (1-12)")
    longitude: float = Field(
        ..., ge=0, le=360, description="Celestial longitude of house cusp"
    )
    sign: str = Field(..., description="Zodiac sign")

    class Config:
        json_schema_extra = {
            "example": {
                "number": 1,
                "longitude": 153.25,
                "sign": "Virgo",
            }
        }


class Aspect(BaseModel):
    """Represents an aspect between two planets."""

    planet1: str = Field(..., description="First planet/point name")
    planet2: str = Field(..., description="Second planet/point name")
    type: str = Field(
        ...,
        description=(
            "Aspect type (Conjunction, Sextile, Square, Trine, Opposition)"
        ),
    )
    orb: float = Field(
        ...,
        ge=0,
        le=360,
        description="Orb of the aspect in degrees",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "planet1": "Sun",
                "planet2": "Mars",
                "type": "Square",
                "orb": 1.2,
            }
        }


class ChartData(BaseModel):
    """Represents complete astrological chart data."""

    planets: List[Planet] = Field(
        ..., description="List of 10 planets (Sun through Pluto)"
    )
    points: List[Point] = Field(
        ..., description="List of 4 astrological points (ASC, DSC, MC, IC)"
    )
    houses: List[House] = Field(..., description="List of 12 house cusps")
    aspects: List[Aspect] = Field(..., description="List of aspects")

    class Config:
        json_schema_extra = {
            "example": {
                "planets": [
                    {
                        "name": "Sun",
                        "longitude": 274.34,
                        "sign": "Capricorn",
                        "degree": 4,
                        "minute": 20,
                        "house": 3,
                    }
                ],
                "points": [
                    {
                        "name": "Ascendant",
                        "longitude": 153.25,
                        "sign": "Virgo",
                        "degree": 3,
                        "minute": 15,
                    }
                ],
                "houses": [
                    {
                        "number": 1,
                        "longitude": 153.25,
                        "sign": "Virgo",
                    }
                ],
                "aspects": [
                    {
                        "planet1": "Sun",
                        "planet2": "Mars",
                        "type": "Square",
                        "orb": 1.2,
                    }
                ],
            }
        }


# Legacy alias for backward compatibility
NatalChart = ChartData


class BirthInput(BaseModel):
    """Represents user input for natal chart generation."""

    date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Birth date in YYYY-MM-DD format",
    )
    time: str = Field(
        ...,
        pattern=r"^\d{2}:\d{2}:\d{2}$",
        description="Birth time in HH:MM:SS format",
    )
    country: str = Field(..., min_length=1, description="Birth country")
    city: str = Field(..., min_length=1, description="Birth city")
    timezone: Optional[str] = Field(
        None, description="IANA timezone (e.g., 'America/New_York')"
    )

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
            if len(parts) != 3:
                raise ValueError()
            hour, minute, second = int(parts[0]), int(parts[1]), int(parts[2])
            time(hour=hour, minute=minute, second=second)
        except (ValueError, TypeError):
            raise ValueError("Time must be a valid time in HH:MM:SS format")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "date": "1990-06-15",
                "time": "14:30:00",
                "country": "USA",
                "city": "New York",
                "timezone": "America/New_York",
            }
        }
