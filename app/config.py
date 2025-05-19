import os


def load_envs() -> tuple[str, str]:
    url = os.getenv("GEOCODING_URL")
    api_key = os.getenv("GEOCODING_API_KEY")
    if not url or not api_key:
        raise ValueError("No url or api key specified.")

    return url, api_key
