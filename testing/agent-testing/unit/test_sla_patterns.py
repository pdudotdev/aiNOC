"""
UT-001 — SLA Pattern Detection

Tests the SLA_DOWN_RE regex from oncall_watcher.py against all expected
log message formats (match) and non-SLA messages (no match).
"""

import sys
from pathlib import Path

import pytest

# Import the regex directly from oncall_watcher without running main()
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from oncall_watcher import SLA_DOWN_RE


# ── Messages that MUST match ──────────────────────────────────────────────────

SHOULD_MATCH = [
    # Cisco IOS standard
    "%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down",
    # Cisco IOS with BOM prefix
    "BOM%TRACK-6-STATE: 2 ip sla 2 reachability Up -> Down",
    # Cisco IOS — different track/sla numbers
    "%TRACK-3-STATE: 10 ip sla 10 reachability Up -> Down",
    # Cisco alternate phrasing
    "ip sla 1 changed state reachable to down",
    "ip sla 3 transition up to down",
    # MikroTik Netwatch
    "netwatch,info event down [ type: simple, host: 10.10.10.10 ]",
    "netwatch event down host=192.168.1.1",
    # Case-insensitive variants
    "%TRACK-6-STATE: 1 ip sla 1 reachability Up -> DOWN",
    "NETWATCH,INFO Event Down [ type: simple, host: 10.0.0.1 ]",
]

# ── Messages that must NOT match ─────────────────────────────────────────────

SHOULD_NOT_MATCH = [
    # SLA going Up (not Down)
    "%TRACK-6-STATE: 1 ip sla 1 reachability Down -> Up",
    "ip sla 1 changed state down to reachable",
    # Unrelated syslog messages
    "%SYS-5-CONFIG_I: Configured from console",
    "%LINEPROTO-5-UPDOWN: Line protocol on Interface Ethernet0/1, changed state to up",
    "BGP neighbor 10.0.0.1 state changed to Established",
    # Empty and whitespace
    "",
    "   ",
]


@pytest.mark.parametrize("msg", SHOULD_MATCH)
def test_matches_sla_down(msg):
    assert SLA_DOWN_RE.search(msg), f"Expected match for: {msg!r}"


@pytest.mark.parametrize("msg", SHOULD_NOT_MATCH)
def test_no_match_non_sla(msg):
    assert not SLA_DOWN_RE.search(msg), f"Expected no match for: {msg!r}"
