from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.geocoding import GeocodingController

app = FastAPI()
geocoding_controller = GeocodingController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GeocodeRequest(BaseModel):
    locations: list[list[str]]


@app.post("/encode")
async def encode(request_data: GeocodeRequest):
    response = await geocoding_controller.get_coordinates(request_data.locations)

    return {"results": response}
