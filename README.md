# nlp-geocoding-api

Simple FastAPI project that handles requests to google's Geocoding API.

## Start service

- place `url` and your `API_KEY` in `.env` file
- run `docker compose up`

## Usage

Send `post` requests at `http://localhost:8000/encode` with a `locations` argument. Example:

```
curl --location --request POST 'http://localhost:8000/encode' \
--header 'Content-Type: application/json' \
--data-raw '{
    "locations": ["new york city"]
}'
```

response:

```
{
    "results": [
        {
            "formatted_address": "New York, NY, USA",
            "geometry": {
                "bounds": {
                    "northeast": {
                        "lat": 40.917705,
                        "lng": -73.700169
                    },
                    "southwest": {
                        "lat": 40.476578,
                        "lng": -74.258843
                    }
                },
                "location": {
                    "lat": 40.7127753,
                    "lng": -74.0059728
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                    "northeast": {
                        "lat": 40.917705,
                        "lng": -73.700169
                    },
                    "southwest": {
                        "lat": 40.476578,
                        "lng": -74.258843
                    }
                }
            }
        }
    ]
}
```

