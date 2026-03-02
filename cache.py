"""Bounded LRU cache for command results.

Prevents redundant network queries within a TTL window.
Oldest entries are evicted when MAX_CACHE_SIZE is reached.
"""
import time
from collections import OrderedDict

CMD_TTL       = 5    # Default TTL in seconds
MAX_CACHE_SIZE = 256  # Cap memory: oldest entries evicted at capacity

_CACHE: OrderedDict = OrderedDict()


def cache_get(device: str, command: str, ttl: int):
    key = (device, command.strip().lower())
    if key in _CACHE:
        ts, result = _CACHE[key]
        if time.time() - ts < ttl:
            return result
        # Expired — delete immediately to keep cache lean
        del _CACHE[key]
    return None


def cache_set(device: str, command: str, result: dict):
    key = (device, command.strip().lower())
    # Evict the oldest entry when at capacity (only if this key is new)
    if len(_CACHE) >= MAX_CACHE_SIZE and key not in _CACHE:
        _CACHE.popitem(last=False)
    _CACHE[key] = (time.time(), result)
