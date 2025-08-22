import httpx
import asyncio

from src.config import load_url_and_api_key


class GeocodingController:
    def __init__(self) -> None:
        self._url, self._api_key = load_url_and_api_key()

    async def get_coordinates(self, locations: list[list[str]]):
        async with httpx.AsyncClient() as client:
            return await asyncio.gather(
                *[self.geocode_location(client, location) for location in locations]
            )

    async def geocode_location(self, client: httpx.AsyncClient, location: list[str]):
        if not location:
            return {}

        requests = [self.geocoding_request(client, name) for name in location]
        responses = await asyncio.gather(*requests, return_exceptions=True)

        return [self.build_result(response) for response in responses]

    def geocoding_request(self, client: httpx.AsyncClient, location_name: str):
        params = {"key": self._api_key, "address": location_name}
        return client.get(self._url, params=params)

    def build_result(self, response: httpx.Response | Exception):
        if isinstance(response, Exception):
            return {}

        data = response.json().get("results", [])
        if not data:
            return {}

        data = data[0]
        return {
            "formatted_address": data.get("formatted_address"),
            "geometry": data.get("geometry"),
        }
