import time


CACHE_TTL = 60

_dashboard_cache = {}


def get_cached_dashboard(cache_key):
    cached = _dashboard_cache.get(cache_key)

    if cached is None:
        return None

    timestamp, data = cached

    if time.time() - timestamp > CACHE_TTL:
        del _dashboard_cache[cache_key]
        return None

    return data


def set_cached_dashboard(cache_key, data):
    _dashboard_cache[cache_key] = (
        time.time(),
        data,
    )


def clear_dashboard_cache():
    _dashboard_cache.clear()