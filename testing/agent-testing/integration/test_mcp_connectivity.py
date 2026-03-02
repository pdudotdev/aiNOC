"""
IT-001 — MCP Tool Connectivity

Verifies that the MCP server tools can reach real devices and return
meaningful data. No configuration changes are made.
"""

import asyncio
import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Skip all tests in this module if NO_LAB is set (e.g. in CI without a running lab)
pytestmark = pytest.mark.skipif(
    os.environ.get("NO_LAB", "0") == "1",
    reason="Lab not running — set NO_LAB=0 to enable integration tests",
)

from tools.operational import get_interfaces, ping
from tools.protocol    import get_ospf
from input_models.models import InterfacesQuery, OspfQuery, PingInput


# ── helpers ───────────────────────────────────────────────────────────────────

def run(coro):
    return asyncio.run(coro)


# ── tests ─────────────────────────────────────────────────────────────────────

def test_get_interfaces_r10c():
    """IT-001a: R10C interfaces should be non-empty and include Ethernet0/1."""
    result = run(get_interfaces(InterfacesQuery(device="R10C")))
    assert result, "Expected non-empty result from get_interfaces(R10C)"
    text = str(result)
    assert "Ethernet0" in text or "eth" in text.lower(), (
        f"Expected interface data in result, got: {text[:200]}"
    )


def test_get_ospf_neighbors_r1a():
    """IT-001b: R1A should have valid OSPF neighbor data."""
    result = run(get_ospf(OspfQuery(device="R1A", query="neighbors")))
    assert result, "Expected non-empty OSPF neighbor result from R1A"
    text = str(result)
    # Should contain either neighbor entries or a valid (empty) table header
    assert "error" not in text.lower() or "neighbor" in text.lower(), (
        f"Unexpected error in OSPF neighbors: {text[:200]}"
    )


def test_ping_r10c_to_loopback():
    """IT-001c: Ping from R10C to its own loopback (172.16.0.5) should succeed."""
    result = run(ping(PingInput(device="R10C", destination="172.16.0.5")))
    assert result, "Expected non-empty ping result"
    text = str(result)
    assert "success" in text.lower() or "!" in text or "bytes" in text.lower(), (
        f"Ping appears to have failed: {text[:200]}"
    )
