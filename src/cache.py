import json
import os
from functools import wraps

import httpx
import redis


class RedisClient:
    def __init__(self):
        host = os.environ.get("REDIS_HOST", "redis")
        port = os.environ.get("REDIS_PORT", 6379)
        pool = redis.ConnectionPool(host=host, port=port)
        self.connection = redis.Redis(connection_pool=pool)
        self.connection.ping()


def cache_response(redis_client: redis.Redis, namespace: str = "geolocations"):
    """
    Caching decorator. Attempts to retrieve the data from redis, otherwise calls the function and caches the response.

    namespace: Namespace for cache keys in Redis.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            location = kwargs.get("location_name")
            if location:
                cache_key = f"{namespace}:{location}"
                cached_value = redis_client.get(cache_key)
                if cached_value:
                    return json.loads(cached_value)

            response: httpx.Response
            response = await func(*args, **kwargs)

            if response.json().get("results"):
                redis_client.set(cache_key, response.text)

            return response

        return wrapper

    return decorator
