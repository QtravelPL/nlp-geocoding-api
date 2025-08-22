# nlp-geocoding-api

Simple FastAPI project that handles requests to google's Geocoding API.

## Start service

- place `url` and your `API_KEY` in `.env` file
- run `docker compose up`

## Usage

Send `post` requests at `http://localhost:8000/encode` with a `locations` argument.\
Each location is a list of names/alternate names. Note that api returns geocoded location for **every** name. Example:

```
curl --location --request POST 'http://localhost:8000/encode' \
--header 'Content-Type: application/json' \
--data-raw '{
    "locations": [["włoszech", "włochy"], ["londynu", "londyn"]]
}'
```

Response:

```
{
    "results": [
        [
            {
                "formatted_address": "Italy",
                "geometry": {
                    "bounds": {
                        "northeast": {
                            "lat": 47.092,
                            "lng": 18.7975999
                        },
                        "southwest": {
                            "lat": 35.4897,
                            "lng": 6.6267201
                        }
                    },
                    "location": {
                        "lat": 41.87194,
                        "lng": 12.56738
                    },
                    "location_type": "APPROXIMATE",
                    "viewport": {
                        "northeast": {
                            "lat": 47.092,
                            "lng": 18.7975999
                        },
                        "southwest": {
                            "lat": 35.4897,
                            "lng": 6.6267201
                        }
                    }
                }
            },
            {
                "formatted_address": "Italy",
                "geometry": {
                    "bounds": {
                        "northeast": {
                            "lat": 47.092,
                            "lng": 18.7975999
                        },
                        "southwest": {
                            "lat": 35.4897,
                            "lng": 6.6267201
                        }
                    },
                    "location": {
                        "lat": 41.87194,
                        "lng": 12.56738
                    },
                    "location_type": "APPROXIMATE",
                    "viewport": {
                        "northeast": {
                            "lat": 47.092,
                            "lng": 18.7975999
                        },
                        "southwest": {
                            "lat": 35.4897,
                            "lng": 6.6267201
                        }
                    }
                }
            }
        ],
        [
            {
                "formatted_address": "London, UK",
                "geometry": {
                    "bounds": {
                        "northeast": {
                            "lat": 51.6723432,
                            "lng": 0.148271
                        },
                        "southwest": {
                            "lat": 51.38494009999999,
                            "lng": -0.3514683
                        }
                    },
                    "location": {
                        "lat": 51.5072178,
                        "lng": -0.1275862
                    },
                    "location_type": "APPROXIMATE",
                    "viewport": {
                        "northeast": {
                            "lat": 51.8822255,
                            "lng": 0.148271
                        },
                        "southwest": {
                            "lat": 51.38494009999999,
                            "lng": -0.4149317
                        }
                    }
                }
            },
            {
                "formatted_address": "London, UK",
                "geometry": {
                    "bounds": {
                        "northeast": {
                            "lat": 51.6723432,
                            "lng": 0.148271
                        },
                        "southwest": {
                            "lat": 51.38494009999999,
                            "lng": -0.3514683
                        }
                    },
                    "location": {
                        "lat": 51.5072178,
                        "lng": -0.1275862
                    },
                    "location_type": "APPROXIMATE",
                    "viewport": {
                        "northeast": {
                            "lat": 51.8822255,
                            "lng": 0.148271
                        },
                        "southwest": {
                            "lat": 51.38494009999999,
                            "lng": -0.4149317
                        }
                    }
                }
            }
        ]
    ]
}
```

