import json
import pytest
from unittest.mock import patch, MagicMock

from app.geocoding import GeocodingController

with open("fixtures/london_response.json", "r") as response, open(
    "fixtures/london_expected.json", "r"
) as expected:
    london_fixture = json.load(response)
    london_expected = json.load(expected)


@pytest.mark.asyncio
@patch("app.geocoding.load_envs", return_value=("http://mock-url", "mock-api-key"))
@patch("httpx.AsyncClient.get")
async def test_get_coordinates_success(mock_http_get, mock_load_envs):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = london_fixture
    mock_http_get.return_value = mock_response

    controller = GeocodingController()
    result = await controller.get_coordinates("London")

    assert result == london_expected
    mock_http_get.assert_called_once_with(
        "http://mock-url", params={"key": "mock-api-key", "address": "London"}
    )


@pytest.mark.asyncio
@patch("app.geocoding.load_envs", return_value=("http://mock-url", "mock-api-key"))
@patch("httpx.AsyncClient.get")
async def test_get_coordinates_empty_results(mock_http_get, mock_load_envs):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}
    mock_http_get.return_value = mock_response

    controller = GeocodingController()

    with pytest.raises(KeyError) as exc_info:
        await controller.get_coordinates("The Void")

    assert str(exc_info.value) == "'results'"
