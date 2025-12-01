"""Unit tests for astrological calculation logic."""

from src.core.calculations import (
    calculate_natal_chart,
    get_planet_positions,
    get_house_cusps,
    get_aspects,
)
from src.models import NatalChart, PlanetPosition, HouseCusp, MajorAspect


class TestCalculateNatalChart:
    """Tests for natal chart calculation."""

    def test_calculate_natal_chart_returns_natal_chart(self):
        """Test that calculate_natal_chart returns a NatalChart object."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        country = "USA"
        city = "New York"

        chart = calculate_natal_chart(birth_date, birth_time, country, city)

        assert isinstance(chart, NatalChart)
        assert isinstance(chart.planets, list)
        assert isinstance(chart.houses, list)
        assert isinstance(chart.aspects, list)

    def test_calculate_natal_chart_has_required_planets(self):
        """Test that chart includes essential planets."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        country = "USA"
        city = "New York"

        chart = calculate_natal_chart(birth_date, birth_time, country, city)

        planet_names = [p.name for p in chart.planets]

        # Check for essential planets
        assert "Sun" in planet_names
        assert "Moon" in planet_names
        assert "Mercury" in planet_names
        assert "Venus" in planet_names
        assert "Mars" in planet_names

    def test_calculate_natal_chart_has_all_houses(self):
        """Test that chart includes all 12 houses."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        country = "USA"
        city = "New York"

        chart = calculate_natal_chart(birth_date, birth_time, country, city)

        house_numbers = [h.house_number for h in chart.houses]

        assert len(house_numbers) == 12
        for i in range(1, 13):
            assert i in house_numbers

    def test_planet_positions_have_valid_degrees(self):
        """Test that planet positions have valid degrees."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        country = "USA"
        city = "New York"

        chart = calculate_natal_chart(birth_date, birth_time, country, city)

        for planet in chart.planets:
            assert 0 <= planet.degrees <= 360
            assert isinstance(planet.degrees, float)

    def test_house_cusps_have_valid_degrees(self):
        """Test that house cusps have valid degrees."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        country = "USA"
        city = "New York"

        chart = calculate_natal_chart(birth_date, birth_time, country, city)

        for house in chart.houses:
            assert 1 <= house.house_number <= 12
            assert 0 <= house.degrees <= 360
            assert isinstance(house.degrees, float)

    def test_aspects_have_valid_orbs(self):
        """Test that aspects have valid orbs."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        country = "USA"
        city = "New York"

        chart = calculate_natal_chart(birth_date, birth_time, country, city)

        valid_aspects = {
            "Conjunction",
            "Sextile",
            "Square",
            "Trine",
            "Opposition",
        }

        for aspect in chart.aspects:
            assert aspect.aspect_type in valid_aspects
            assert 0 <= aspect.orb <= 360
            assert isinstance(aspect.orb, float)


class TestGetPlanetPositions:
    """Tests for planet position calculation."""

    def test_get_planet_positions_returns_list(self):
        """Test that get_planet_positions returns a list."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        latitude = 40.7128
        longitude = -74.0060

        positions = get_planet_positions(
            birth_date, birth_time, latitude, longitude
        )

        assert isinstance(positions, list)
        assert len(positions) > 0

    def test_planet_positions_have_required_fields(self):
        """Test that planet positions have all required fields."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        latitude = 40.7128
        longitude = -74.0060

        positions = get_planet_positions(
            birth_date, birth_time, latitude, longitude
        )

        for position in positions:
            assert isinstance(position, PlanetPosition)
            assert position.name
            assert position.sign
            assert isinstance(position.degrees, float)


class TestGetHouseCusps:
    """Tests for house cusp calculation."""

    def test_get_house_cusps_returns_twelve_houses(self):
        """Test that get_house_cusps returns 12 houses."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        latitude = 40.7128
        longitude = -74.0060

        cusps = get_house_cusps(birth_date, birth_time, latitude, longitude)

        assert isinstance(cusps, list)
        assert len(cusps) == 12

    def test_house_cusps_have_required_fields(self):
        """Test that house cusps have all required fields."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        latitude = 40.7128
        longitude = -74.0060

        cusps = get_house_cusps(birth_date, birth_time, latitude, longitude)

        for i, cusp in enumerate(cusps, 1):
            assert isinstance(cusp, HouseCusp)
            assert cusp.house_number == i
            assert cusp.sign
            assert isinstance(cusp.degrees, float)


class TestGetAspects:
    """Tests for aspect calculation."""

    def test_get_aspects_returns_list(self):
        """Test that get_aspects returns a list."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        latitude = 40.7128
        longitude = -74.0060

        positions = get_planet_positions(
            birth_date, birth_time, latitude, longitude
        )
        aspects = get_aspects(positions)

        assert isinstance(aspects, list)

    def test_aspects_have_required_fields(self):
        """Test that aspects have all required fields."""
        birth_date = "1990-06-15"
        birth_time = "14:30"
        latitude = 40.7128
        longitude = -74.0060

        positions = get_planet_positions(
            birth_date, birth_time, latitude, longitude
        )
        aspects = get_aspects(positions)

        valid_aspects = {
            "Conjunction",
            "Sextile",
            "Square",
            "Trine",
            "Opposition",
        }

        for aspect in aspects:
            assert isinstance(aspect, MajorAspect)
            assert aspect.aspect_type in valid_aspects
            assert aspect.planet1
            assert aspect.planet2
            assert isinstance(aspect.orb, float)
