"""Integration tests for the chart API endpoint."""


class TestChartEndpoint:
    """Tests for the /chart API endpoint."""

    def test_chart_endpoint_post_success(self, client):
        """Test POST /chart endpoint with valid input returns 200."""
        payload = {
            "date": "1990-06-15",
            "time": "14:30",
            "country": "USA",
            "city": "New York",
        }

        response = client.post("/chart", json=payload)

        assert response.status_code == 200

    def test_chart_endpoint_returns_natal_chart(self, client):
        """Test POST /chart endpoint returns a valid NatalChart."""
        payload = {
            "date": "1990-06-15",
            "time": "14:30",
            "country": "USA",
            "city": "New York",
        }

        response = client.post("/chart", json=payload)

        assert response.status_code == 200
        data = response.json()

        # Verify the response structure matches NatalChart
        assert "planets" in data
        assert "houses" in data
        assert "aspects" in data

        # Verify planets is a list
        assert isinstance(data["planets"], list)
        assert len(data["planets"]) > 0

        # Verify houses is a list
        assert isinstance(data["houses"], list)
        assert len(data["houses"]) > 0

        # Verify aspects is a list
        assert isinstance(data["aspects"], list)

    def test_chart_endpoint_planet_fields(self, client):
        """Test that each planet has required fields."""
        payload = {
            "date": "1990-06-15",
            "time": "14:30",
            "country": "USA",
            "city": "New York",
        }

        response = client.post("/chart", json=payload)

        assert response.status_code == 200
        data = response.json()

        for planet in data["planets"]:
            assert "name" in planet
            assert "sign" in planet
            assert "degrees" in planet
            assert 0 <= planet["degrees"] <= 360

    def test_chart_endpoint_house_fields(self, client):
        """Test that each house has required fields."""
        payload = {
            "date": "1990-06-15",
            "time": "14:30",
            "country": "USA",
            "city": "New York",
        }

        response = client.post("/chart", json=payload)

        assert response.status_code == 200
        data = response.json()

        for house in data["houses"]:
            assert "house_number" in house
            assert "sign" in house
            assert "degrees" in house
            assert 1 <= house["house_number"] <= 12
            assert 0 <= house["degrees"] <= 360

    def test_chart_endpoint_aspect_fields(self, client):
        """Test that each aspect has required fields."""
        payload = {
            "date": "1990-06-15",
            "time": "14:30",
            "country": "USA",
            "city": "New York",
        }

        response = client.post("/chart", json=payload)

        assert response.status_code == 200
        data = response.json()

        valid_aspects = {
            "Conjunction",
            "Sextile",
            "Square",
            "Trine",
            "Opposition",
        }

        for aspect in data["aspects"]:
            assert "aspect_type" in aspect
            assert "planet1" in aspect
            assert "planet2" in aspect
            assert "orb" in aspect
            assert aspect["aspect_type"] in valid_aspects

    def test_chart_endpoint_invalid_date_format(self, client):
        """Test POST /chart with invalid date format returns 422."""
        payload = {
            "date": "06/15/1990",  # Invalid format
            "time": "14:30",
            "country": "USA",
            "city": "New York",
        }

        response = client.post("/chart", json=payload)

        assert response.status_code == 422

    def test_chart_endpoint_invalid_time_format(self, client):
        """Test POST /chart with invalid time format returns 422."""
        payload = {
            "date": "1990-06-15",
            "time": "2:30 PM",  # Invalid format
            "country": "USA",
            "city": "New York",
        }

        response = client.post("/chart", json=payload)

        assert response.status_code == 422

    def test_chart_endpoint_missing_required_field(self, client):
        """Test POST /chart with missing field returns 422."""
        payload = {
            "date": "1990-06-15",
            "time": "14:30",
            "country": "USA",
            # Missing "city"
        }

        response = client.post("/chart", json=payload)

        assert response.status_code == 422

    def test_chart_endpoint_known_date_structure(self, client):
        """Test with known date and verify chart structure."""
        payload = {
            "date": "2000-01-01",
            "time": "12:00",
            "country": "USA",
            "city": "New York",
        }

        response = client.post("/chart", json=payload)

        assert response.status_code == 200
        data = response.json()

        # Verify structure
        assert len(data["planets"]) >= 7  # At least Sun through Saturn
        assert len(data["houses"]) == 12
        assert "planets" in data
        assert "houses" in data
        assert "aspects" in data
