import httpx

from app.config import load_envs


class GeocodingController:
    def __init__(self) -> None:
        self._url, self._api_key = load_envs()

    async def get_coordinates(self, location: str):
        params = {"key": self._api_key, "address": location}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self._url, params=params)
                response.raise_for_status()
                results = response.json()["results"]
            except KeyError as e:
                raise e

        return [
            {
                "formatted_address": result["formatted_address"],
                "geometry": result["geometry"],
            }
            for result in results
        ]
