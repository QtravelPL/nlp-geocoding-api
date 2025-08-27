import asyncio
import logging

import httpx

from src.cache import RedisClient, cache_response
from src.config import load_url_and_api_key

redis_client = RedisClient().connection


class GeocodingController:
    def __init__(self) -> None:
        self._url, self._api_key = load_url_and_api_key()
        self.logger = logging.getLogger("uvicorn.error")

    async def get_coordinates(self, locations: list[list[str]]):
        async with httpx.AsyncClient() as client:
            return await asyncio.gather(
                *[self.geocode_location(client, location) for location in locations]
            )

    async def geocode_location(self, client: httpx.AsyncClient, location: list[str]):
        if not location:
            return {}

        requests = [
            self.geocoding_request(client=client, location_name=name)
            for name in location
        ]
        responses = await asyncio.gather(*requests, return_exceptions=True)

        return [self.build_result(response) for response in responses]

    @cache_response(redis_client=redis_client)
    def geocoding_request(self, client: httpx.AsyncClient, location_name: str):
        params = {"key": self._api_key, "address": location_name}
        return client.get(self._url, params=params)

    def build_result(self, response: httpx.Response | dict):
        """Builds a hash with results from given response.

        Args:
            response (httpx.Response | Exception | dict): response might be one of 2 types
                - http.Response when data provided from google API
                - python dictionary when data provided from cache

        Returns:
            dict: a dictionary with brief address info and it's location
        """
        if isinstance(response, httpx.Response):
            response = response.json()
            source = "Geocoding API"
        else:
            source = "Redis cache"

        data = response.get("results", [])
        if not data:
            self.logger.error(response)
            return {}

        data = data[0]
        return {
            "formatted_address": data.get("formatted_address"),
            "geometry": data.get("geometry"),
            "source": source,
        }
