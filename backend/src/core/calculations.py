"""Core astrological calculation logic using pyswisseph."""

from typing import List, Tuple
import swisseph as swe

from src.models import (
    NatalChart,
    PlanetPosition,
    HouseCusp,
    MajorAspect,
)

# Zodiac signs
ZODIAC_SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

# Planet identifiers for pyswisseph
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

# Major aspects with their degrees and orbs
MAJOR_ASPECTS = {
    0: ("Conjunction", 8),
    60: ("Sextile", 6),
    90: ("Square", 8),
    120: ("Trine", 8),
    180: ("Opposition", 8),
}

# Geolocation data for major cities (lat, lon)
CITY_COORDS = {
    ("new york", "usa"): (40.7128, -74.0060),
    ("los angeles", "usa"): (34.0522, -118.2437),
    ("london", "uk"): (51.5074, -0.1278),
    ("paris", "france"): (48.8566, 2.3522),
    ("sydney", "australia"): (-33.8688, 151.2093),
    ("tokyo", "japan"): (35.6762, 139.6503),
    ("berlin", "germany"): (52.5200, 13.4050),
    ("madrid", "spain"): (40.4168, -3.7038),
}


def _get_city_coordinates(city: str, country: str) -> Tuple[float, float]:
    """
    Get latitude and longitude for a city.

    For now, uses a hardcoded lookup. In production, would use
    geolocation API.
    """
    key = (city.lower(), country.lower())
    if key in CITY_COORDS:
        return CITY_COORDS[key]

    # Default fallback (Greenwich Observatory)
    return (51.4769, 0.0000)


def _degrees_to_zodiac_sign(degrees: float) -> str:
    """Convert degrees (0-360) to zodiac sign."""
    sign_index = int(degrees // 30)
    return ZODIAC_SIGNS[sign_index % 12]


def _calculate_jd(date_str: str, time_str: str) -> float:
    """
    Calculate Julian Day number from date and time.

    Args:
        date_str: Date in YYYY-MM-DD format
        time_str: Time in HH:MM format

    Returns:
        Julian Day number
    """
    year, month, day = map(int, date_str.split("-"))
    hour, minute = map(int, time_str.split(":"))

    # Convert to decimal hour
    time_decimal = hour + minute / 60.0

    # Calculate Julian Day
    jd = swe.julday(year, month, day, time_decimal)
    return jd


def get_planet_positions(
    date_str: str, time_str: str, latitude: float, longitude: float
) -> List[PlanetPosition]:
    """
    Calculate planet positions for a given date, time, and location.

    Args:
        date_str: Date in YYYY-MM-DD format
        time_str: Time in HH:MM format
        latitude: Latitude of location
        longitude: Longitude of location

    Returns:
        List of PlanetPosition objects
    """
    jd = _calculate_jd(date_str, time_str)

    positions = []

    for planet_name, planet_id in PLANETS.items():
        # Calculate planet position
        lon, lat, distance, speed_lon, speed_lat, speed_dist = (
            swe.calc_ut(jd, planet_id)
        )

        # Normalize longitude to 0-360 range
        lon = lon % 360

        # Get zodiac sign
        sign = _degrees_to_zodiac_sign(lon)

        # Get degrees within sign
        sign_degrees = lon % 30

        positions.append(
            PlanetPosition(name=planet_name, sign=sign, degrees=sign_degrees)
        )

    return positions


def get_house_cusps(
    date_str: str, time_str: str, latitude: float, longitude: float
) -> List[HouseCusp]:
    """
    Calculate house cusps for a given date, time, and location.

    Args:
        date_str: Date in YYYY-MM-DD format
        time_str: Time in HH:MM format
        latitude: Latitude of location
        longitude: Longitude of location

    Returns:
        List of HouseCusp objects (12 houses)
    """
    jd = _calculate_jd(date_str, time_str)

    # Set geographic location for house calculation
    swe.set_topo(longitude, latitude, 0)

    # Calculate houses (Placidus houses)
    houses, ascmc = swe.houses_ut(jd, latitude, longitude, b"P")

    cusps = []

    for house_num in range(1, 13):
        lon = houses[house_num - 1]
        lon = lon % 360

        sign = _degrees_to_zodiac_sign(lon)
        sign_degrees = lon % 30

        cusps.append(
            HouseCusp(
                house_number=house_num,
                sign=sign,
                degrees=sign_degrees,
            )
        )

    return cusps


def get_aspects(positions: List[PlanetPosition]) -> List[MajorAspect]:
    """
    Calculate major aspects between planets.

    Args:
        positions: List of PlanetPosition objects

    Returns:
        List of MajorAspect objects
    """
    aspects = []

    # Create a dict for easier lookup
    planet_dict = {p.name: p for p in positions}

    # Check all planet pairs
    planet_names = list(planet_dict.keys())
    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            planet1_name = planet_names[i]
            planet2_name = planet_names[j]

            planet1 = planet_dict[planet1_name]
            planet2 = planet_dict[planet2_name]

            # Calculate degrees difference
            diff = abs(planet1.degrees - planet2.degrees)

            # Check for major aspects
            for aspect_degrees, (aspect_type, orb) in MAJOR_ASPECTS.items():
                # Check if difference matches aspect (considering orb)
                angle_diff = min(diff, 360 - diff)

                if abs(angle_diff - aspect_degrees) <= orb:
                    aspects.append(
                        MajorAspect(
                            aspect_type=aspect_type,
                            planet1=planet1_name,
                            planet2=planet2_name,
                            orb=abs(angle_diff - aspect_degrees),
                        )
                    )
                    break

    return aspects


def calculate_natal_chart(
    date_str: str,
    time_str: str,
    country: str,
    city: str,
) -> NatalChart:
    """
    Calculate a complete natal chart for a given birth information.

    Args:
        date_str: Birth date in YYYY-MM-DD format
        time_str: Birth time in HH:MM format
        country: Birth country
        city: Birth city

    Returns:
        NatalChart object with planets, houses, and aspects
    """
    # Get coordinates for the city
    latitude, longitude = _get_city_coordinates(city, country)

    # Calculate positions
    planets = get_planet_positions(date_str, time_str, latitude, longitude)
    houses = get_house_cusps(date_str, time_str, latitude, longitude)
    aspects = get_aspects(planets)

    return NatalChart(planets=planets, houses=houses, aspects=aspects)
