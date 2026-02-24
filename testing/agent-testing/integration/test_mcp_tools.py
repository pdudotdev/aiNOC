"""
IT-003 — Full MCP Tool Coverage

Ports testing/tool_tests.py to pytest. Verifies connectivity and tool correctness
for all three platform types (IOS, EOS, RouterOS) and validates cache behavior.

Requires live device access.
"""

import asyncio
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from MCPServer import (
    execute_command,
    get_ospf,
    get_eigrp,
    get_bgp,
    get_interfaces,
    get_routing,
    get_routing_policies,
    ping,
    traceroute,
    run_show,
    OspfQuery,
    EigrpQuery,
    BgpQuery,
    InterfacesQuery,
    RoutingQuery,
    RoutingPolicyQuery,
    PingInput,
    TracerouteInput,
    ShowCommand,
)


# ── device constants (mirror tool_tests.py) ───────────────────────────────────

IOS1 = "R3C"
IOS2 = "R5C"
IOS3 = "R8C"

EOS1 = "R1A"
EOS2 = "R6A"
EOS3 = "R7A"

ROS1 = "R18M"
ROS2 = "R19M"
ROS3 = "R20M"


# ── helpers ───────────────────────────────────────────────────────────────────

def run(coro):
    return asyncio.run(coro)


# ── IT-003a: platform connectivity ────────────────────────────────────────────

def test_connectivity_ios():
    """IT-003a-1: SSH to Cisco IOS (R3C) — show version."""
    result = run(execute_command(IOS1, "show version"))
    assert result, "Expected non-empty result from execute_command(R3C)"
    text = str(result)
    assert "version" in text.lower(), f"Expected version info, got: {text[:200]}"


def test_connectivity_eos():
    """IT-003a-2: eAPI to Arista EOS (R1A) — show version."""
    result = run(execute_command(EOS1, "show version"))
    assert result, "Expected non-empty result from execute_command(R1A)"
    text = str(result)
    assert "version" in text.lower(), f"Expected version info, got: {text[:200]}"


def test_connectivity_ros():
    """IT-003a-3: REST to MikroTik RouterOS (R18M) — GET /rest/ip/route."""
    action = {"method": "GET", "path": "/rest/ip/route"}
    result = run(execute_command(ROS1, action))
    assert result, "Expected non-empty result from execute_command(R18M)"


# ── IT-003b: protocol tools ────────────────────────────────────────────────────

def test_ospf_eos():
    """IT-003b-1: get_ospf neighbors on EOS (R1A)."""
    result = run(get_ospf(OspfQuery(device=EOS1, query="neighbors")))
    assert result, "Expected non-empty OSPF result from R1A"
    text = str(result)
    assert "error" not in text.lower() or "neighbor" in text.lower(), (
        f"Unexpected error in OSPF result: {text[:200]}"
    )


def test_eigrp_ios():
    """IT-003b-2: get_eigrp neighbors on IOS (R3C)."""
    result = run(get_eigrp(EigrpQuery(device=IOS1, query="neighbors")))
    assert result, "Expected non-empty EIGRP result from R3C"
    text = str(result)
    assert "error" not in text.lower() or "neighbor" in text.lower(), (
        f"Unexpected error in EIGRP result: {text[:200]}"
    )


def test_bgp_ros():
    """IT-003b-3: get_bgp summary on RouterOS (R18M)."""
    result = run(get_bgp(BgpQuery(device=ROS1, query="summary")))
    assert result, "Expected non-empty BGP result from R18M"


def test_interfaces_ros():
    """IT-003b-4: get_interfaces on RouterOS (R19M)."""
    result = run(get_interfaces(InterfacesQuery(device=ROS2, query="interface_status")))
    assert result, "Expected non-empty interfaces result from R19M"


def test_routing_ios():
    """IT-003b-5: get_routing prefix lookup on IOS (R5C)."""
    result = run(get_routing(RoutingQuery(device=IOS2, prefix="10.0.0.9")))
    assert result, "Expected non-empty routing result from R5C"


def test_ping_eos():
    """IT-003b-6: ping from EOS (R6A) to 10.1.1.5."""
    result = run(ping(PingInput(device=EOS2, destination="10.1.1.5")))
    assert result, "Expected non-empty ping result from R6A"
    text = str(result)
    assert "success" in text.lower() or "!" in text or "bytes" in text.lower(), (
        f"Ping appears to have failed: {text[:200]}"
    )


def test_routing_policies_ios():
    """IT-003b-7: get_routing_policies route_maps on IOS (R8C)."""
    result = run(get_routing_policies(RoutingPolicyQuery(device=IOS3, query="route_maps")))
    assert result, "Expected non-empty routing policies result from R8C"


def test_traceroute_ros():
    """IT-003b-8: traceroute from RouterOS (R20M)."""
    result = run(traceroute(TracerouteInput(device=ROS3, destination="172.16.77.2")))
    assert result, "Expected non-empty traceroute result from R20M"


def test_run_show_eos():
    """IT-003b-9: run_show fallback on EOS (R7A)."""
    result = run(run_show(ShowCommand(device=EOS3, command="show ip arp")))
    assert result, "Expected non-empty run_show result from R7A"


def test_redistribution_ros():
    """IT-003b-10: get_routing_policies redistribution on RouterOS (R18M)."""
    result = run(get_routing_policies(RoutingPolicyQuery(device=ROS1, query="redistribution")))
    assert result, "Expected non-empty redistribution result from R18M"


# ── IT-003c: cache behavior ────────────────────────────────────────────────────

def test_cache_behavior():
    """IT-003c: execute_command caching — miss, hit, miss after TTL (6s sleep)."""
    import time

    device = IOS1
    command = "show clock"

    r1 = run(execute_command(device, command))
    assert r1.get("cache_hit") is False, f"First call should be a cache miss, got: {r1.get('cache_hit')}"

    r2 = run(execute_command(device, command))
    assert r2.get("cache_hit") is True, f"Second call (within TTL) should be a cache hit, got: {r2.get('cache_hit')}"

    time.sleep(6)  # CMD_TTL = 5s

    r3 = run(execute_command(device, command))
    assert r3.get("cache_hit") is False, f"Third call (after TTL) should be a cache miss, got: {r3.get('cache_hit')}"
