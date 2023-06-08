from functools import wraps
import inspect
from cachetools import TTLCache
import sys

CACHE = TTLCache(maxsize=100, ttl=300)  # Max 100 entries, each with a TTL of 300 seconds (5 minutes)

def cached_with_dependency(cache):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            signature = inspect.signature(func)
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            cache_key = f"{func.__name__}:{str(bound_args.arguments)}"
            cached_value = cache.get(cache_key)

            if cached_value is None:
                result = await func(*args, **kwargs)
                cache[cache_key] = result
            else:
                result = cached_value

            return result
        return wrapper
    return decorator