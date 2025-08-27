import json
from unittest.mock import patch

import httpx
import pytest

from src.geocoding import GeocodingController

with open("fixtures/london_response.json", "r") as response, open(
    "fixtures/london_expected.json", "r"
) as expected:
    london_fixture = json.load(response)
    london_expected = json.load(expected)


@pytest.mark.asyncio
@patch("src.geocoding.redis_client.get")
@patch("src.geocoding.redis_client.set")
@patch(
    "src.geocoding.load_url_and_api_key",
    return_value=("http://mock-url", "mock-api-key"),
)
@patch("httpx.AsyncClient.get")
async def test_get_coordinates_google_api_hit(
    mock_http_get, mock_load_url_and_api_key, mock_redis_set, mock_redis_get
):
    mock_response = httpx.Response(
        status_code=200,
        content=json.dumps(london_fixture),
        request=httpx.Request("GET", "http://mock-url"),
    )
    mock_http_get.return_value = mock_response
    mock_redis_get.return_value = None

    controller = GeocodingController()
    result = await controller.get_coordinates([["london"]])

    mock_http_get.assert_called_once_with(
        "http://mock-url", params={"key": "mock-api-key", "address": "london"}
    )
    mock_redis_get.assert_called()
    mock_redis_set.assert_called()
    assert result == london_expected


@pytest.mark.asyncio
@patch("src.geocoding.redis_client.get")
@patch("src.geocoding.redis_client.set")
@patch(
    "src.geocoding.load_url_and_api_key",
    return_value=("http://mock-url", "mock-api-key"),
)
@patch("httpx.AsyncClient.get")
async def test_get_coordinates_cache_hit(
    mock_http_get, mock_load_url_and_api_key, mock_redis_set, mock_redis_get
):
    mock_redis_get.return_value = json.dumps(london_fixture)

    controller = GeocodingController()
    result = await controller.get_coordinates([["london"]])

    mock_http_get.assert_not_called()
    mock_redis_get.assert_called()
    mock_redis_set.assert_not_called()

    london_expected[0][0]["source"] = "Redis cache"
    assert result == london_expected


@pytest.mark.asyncio
@patch("src.geocoding.redis_client.get")
@patch("src.geocoding.redis_client.set")
@patch(
    "src.geocoding.load_url_and_api_key",
    return_value=("http://mock-url", "mock-api-key"),
)
@patch("httpx.AsyncClient.get")
async def test_get_coordinates_empty_results(
    mock_http_get, mock_load_url_and_api_key, mock_redis_set, mock_redis_get
):
    mock_response = httpx.Response(
        status_code=200,
        content=json.dumps({"results": []}),
        request=httpx.Request("GET", "http://mock-url"),
    )
    mock_http_get.return_value = mock_response
    mock_redis_get.return_value = None

    controller = GeocodingController()
    result = await controller.get_coordinates([["The Void"]])

    mock_redis_get.assert_called()
    mock_redis_set.assert_not_called()

    expected = [[{}]]
    assert result == expected
