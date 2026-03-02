"""Shared aiohttp connection pools for device transports.

Lazily initialized on first use; closed via close_sessions() on server shutdown.
Sessions are re-created when the running event loop changes (e.g. in tests where
each asyncio.run() spins up a new loop).
"""
import asyncio
import aiohttp
from settings import USERNAME, PASSWORD

# Timeout applied to all device-facing HTTP connections.
DEVICE_TIMEOUT = aiohttp.ClientTimeout(total=30, connect=10)

_EAPI_SESSION: aiohttp.ClientSession | None = None
_EAPI_LOOP:    asyncio.AbstractEventLoop | None = None
_REST_SESSION:  aiohttp.ClientSession | None = None
_REST_LOOP:     asyncio.AbstractEventLoop | None = None


async def get_eapi_session() -> aiohttp.ClientSession:
    """Return (or lazily create) the shared eAPI connection pool."""
    global _EAPI_SESSION, _EAPI_LOOP
    loop = asyncio.get_running_loop()
    if _EAPI_SESSION is None or _EAPI_SESSION.closed or _EAPI_LOOP is not loop:
        if _EAPI_SESSION is not None and not _EAPI_SESSION.closed:
            await _EAPI_SESSION.close()
        _EAPI_SESSION = aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(USERNAME, PASSWORD),
            timeout=DEVICE_TIMEOUT,
        )
        _EAPI_LOOP = loop
    return _EAPI_SESSION


async def get_rest_session() -> aiohttp.ClientSession:
    """Return (or lazily create) the shared RouterOS REST connection pool."""
    global _REST_SESSION, _REST_LOOP
    loop = asyncio.get_running_loop()
    if _REST_SESSION is None or _REST_SESSION.closed or _REST_LOOP is not loop:
        if _REST_SESSION is not None and not _REST_SESSION.closed:
            await _REST_SESSION.close()
        _REST_SESSION = aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(USERNAME, PASSWORD),
            timeout=DEVICE_TIMEOUT,
        )
        _REST_LOOP = loop
    return _REST_SESSION


async def close_sessions() -> None:
    """Close all open sessions. Called from the MCP server lifespan on shutdown."""
    for session in (_EAPI_SESSION, _REST_SESSION):
        if session is not None and not session.closed:
            await session.close()
