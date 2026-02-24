"""
UT-002 — Platform Map Commands

Verifies that PLATFORM_MAP returns the correct commands for each
cli_style (ios, eos, routeros) and all relevant query types.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "platforms"))
from platform_map import PLATFORM_MAP


# ── IOS ───────────────────────────────────────────────────────────────────────

class TestIOS:
    def test_ospf_neighbors(self):
        assert PLATFORM_MAP["ios"]["ospf"]["neighbors"] == "show ip ospf neighbor"

    def test_ospf_database(self):
        assert PLATFORM_MAP["ios"]["ospf"]["database"] == "show ip ospf database"

    def test_ospf_interfaces(self):
        assert PLATFORM_MAP["ios"]["ospf"]["interfaces"] == "show ip ospf interface"

    def test_ospf_config(self):
        assert "ospf" in PLATFORM_MAP["ios"]["ospf"]["config"]

    def test_ospf_borders(self):
        assert PLATFORM_MAP["ios"]["ospf"]["borders"] == "show ip ospf border-routers"

    def test_ospf_details(self):
        assert PLATFORM_MAP["ios"]["ospf"]["details"] == "show ip ospf"

    def test_eigrp_neighbors(self):
        assert PLATFORM_MAP["ios"]["eigrp"]["neighbors"] == "show ip eigrp neighbors"

    def test_eigrp_topology(self):
        assert PLATFORM_MAP["ios"]["eigrp"]["topology"] == "show ip eigrp topology"

    def test_eigrp_interfaces(self):
        assert "eigrp" in PLATFORM_MAP["ios"]["eigrp"]["interfaces"]

    def test_eigrp_config(self):
        assert "eigrp" in PLATFORM_MAP["ios"]["eigrp"]["config"]

    def test_bgp_summary(self):
        assert PLATFORM_MAP["ios"]["bgp"]["summary"] == "show ip bgp summary"

    def test_routing_table(self):
        assert PLATFORM_MAP["ios"]["routing_table"]["ip_route"] == "show ip route"

    def test_redistribution(self):
        assert "redistribute" in PLATFORM_MAP["ios"]["routing_policies"]["redistribution"]

    def test_interfaces(self):
        assert PLATFORM_MAP["ios"]["interfaces"]["interface_status"] == "show ip interface brief"

    def test_ping(self):
        assert PLATFORM_MAP["ios"]["tools"]["ping"] == "ping"

    def test_traceroute(self):
        assert PLATFORM_MAP["ios"]["tools"]["traceroute"] == "traceroute"


# ── EOS ───────────────────────────────────────────────────────────────────────

class TestEOS:
    def test_ospf_neighbors(self):
        assert PLATFORM_MAP["eos"]["ospf"]["neighbors"] == "show ip ospf neighbor"

    def test_ospf_interfaces(self):
        assert PLATFORM_MAP["eos"]["ospf"]["interfaces"] == "show ip ospf interface"

    def test_ospf_config(self):
        assert "ospf" in PLATFORM_MAP["eos"]["ospf"]["config"]

    def test_bgp_summary(self):
        assert PLATFORM_MAP["eos"]["bgp"]["summary"] == "show ip bgp summary"

    def test_routing_table(self):
        assert PLATFORM_MAP["eos"]["routing_table"]["ip_route"] == "show ip route"

    def test_interfaces(self):
        assert PLATFORM_MAP["eos"]["interfaces"]["interface_status"] == "show ip interface brief"

    def test_ping(self):
        assert PLATFORM_MAP["eos"]["tools"]["ping"] == "ping"


# ── RouterOS ──────────────────────────────────────────────────────────────────

class TestRouterOS:
    def test_ospf_neighbors(self):
        entry = PLATFORM_MAP["routeros"]["ospf"]["neighbors"]
        assert entry["method"] == "GET"
        assert "/ospf/neighbor" in entry["path"]

    def test_ospf_database(self):
        entry = PLATFORM_MAP["routeros"]["ospf"]["database"]
        assert entry["method"] == "GET"
        assert "/ospf/" in entry["path"]

    def test_ospf_interfaces(self):
        entry = PLATFORM_MAP["routeros"]["ospf"]["interfaces"]
        assert entry["method"] == "GET"

    def test_bgp_summary(self):
        entry = PLATFORM_MAP["routeros"]["bgp"]["summary"]
        assert entry["method"] == "GET"

    def test_routing_table(self):
        entry = PLATFORM_MAP["routeros"]["routing_table"]["ip_route"]
        assert entry["method"] == "GET"
        assert "/route" in entry["path"]

    def test_ping(self):
        entry = PLATFORM_MAP["routeros"]["tools"]["ping"]
        assert entry["method"] == "POST"
        assert "/ping" in entry["path"]

    def test_traceroute(self):
        entry = PLATFORM_MAP["routeros"]["tools"]["traceroute"]
        assert entry["method"] == "POST"
        assert "/traceroute" in entry["path"]
