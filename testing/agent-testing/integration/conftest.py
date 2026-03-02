"""Session-level cleanup for integration tests."""
import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from transport.pool import close_sessions


@pytest.fixture(autouse=True, scope="session")
def cleanup_transport_sessions():
    """Close aiohttp session pools after all integration tests complete.

    Prevents ClientSession.__del__ noise during process teardown caused by
    orphaned sessions interacting with pyats logging during GC.
    """
    yield
    asyncio.run(close_sessions())
