import httpx
import asyncio

from app.config import load_url_and_api_key


class GeocodingController:
    def __init__(self) -> None:
        self._url, self._api_key = load_url_and_api_key()

    async def get_coordinates(self, locations: list[str]):
        async with httpx.AsyncClient() as client:
            return await asyncio.gather(
                *[self.geocoding_request(client, location) for location in locations]
            )

    async def geocoding_request(self, client: httpx.AsyncClient, location: str):
        if not location:
            return {}

        params = {"key": self._api_key, "address": location}
        response = await client.get(self._url, params=params)
        response.raise_for_status()
        results = response.json()["results"]

        if not results:
            return {}

        result = results[0]
        return {
            "formatted_address": result["formatted_address"],
            "geometry": result["geometry"],
        }
