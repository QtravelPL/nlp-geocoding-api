import json
import pytest
from unittest.mock import patch, MagicMock

from src.geocoding import GeocodingController

with open("fixtures/london_response.json", "r") as response, open(
    "fixtures/london_expected.json", "r"
) as expected:
    london_fixture = json.load(response)
    london_expected = json.load(expected)


@pytest.mark.asyncio
@patch(
    "src.geocoding.load_url_and_api_key",
    return_value=("http://mock-url", "mock-api-key"),
)
@patch("httpx.AsyncClient.get")
async def test_get_coordinates_success(mock_http_get, mock_load_url_and_api_key):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = london_fixture
    mock_http_get.return_value = mock_response

    controller = GeocodingController()
    result = await controller.get_coordinates([["london"]])

    assert result == london_expected
    mock_http_get.assert_called_once_with(
        "http://mock-url", params={"key": "mock-api-key", "address": "london"}
    )


@pytest.mark.asyncio
@patch(
    "src.geocoding.load_url_and_api_key",
    return_value=("http://mock-url", "mock-api-key"),
)
@patch("httpx.AsyncClient.get")
async def test_get_coordinates_empty_results(mock_http_get, mock_load_url_and_api_key):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"results": []}
    mock_http_get.return_value = mock_response

    controller = GeocodingController()

    result = await controller.get_coordinates([["The Void"]])

    expected = [[{}]]
    assert result == expected
