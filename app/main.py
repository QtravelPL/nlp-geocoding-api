from fastapi import FastAPI
from pydantic import BaseModel

from app.geocoding import GeocodingController

app = FastAPI()
geocoding_controller = GeocodingController()


class GeocodeRequest(BaseModel):
    location: str


@app.post("/encode/")
async def encode(request_data: GeocodeRequest):
    response = await geocoding_controller.get_coordinates(request_data.location)

    return {"results": response}
