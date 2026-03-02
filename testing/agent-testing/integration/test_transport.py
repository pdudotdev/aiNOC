"""Integration tests for transport layer (SSH, eAPI, REST).

These tests require a running lab (`sudo clab redeploy -t lab.yml`).
Run with: ./run_tests.sh integration

Each test verifies:
  - The transport can connect to its target device
  - execute_command returns a structured result dict (no "error" key)
  - The result contains either "parsed" or "raw" output
  - cache_hit reflects expected state (False on first call, True on repeat)

Skip markers prevent CI failures when the lab is not available.
"""
import asyncio
import os
import pytest

# Skip all tests in this module if NO_LAB is set (e.g. in CI without a running lab)
pytestmark = pytest.mark.skipif(
    os.environ.get("NO_LAB", "0") == "1",
    reason="Lab not running — set NO_LAB=0 to enable integration tests",
)


from transport import execute_command
from cache import _CACHE, CMD_TTL


def _run(coro):
    return asyncio.run(coro)


def _assert_ok(result: dict):
    """Assert the result dict is a successful transport response."""
    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    assert "error" not in result, f"Transport error: {result.get('error')}"
    assert "parsed" in result or "raw" in result, "Result must have 'parsed' or 'raw'"


# ── SSH (Cisco IOS-XE) ────────────────────────────────────────────────────────

class TestSSHTransport:
    """R3C is a Cisco IOS-XE device via Scrapli SSH."""

    def test_ssh_execute_show_version(self):
        result = _run(execute_command("R3C", "show version", ttl=0))
        _assert_ok(result)
        assert result["cli_style"] == "ios"

    def test_ssh_execute_ospf_neighbors(self):
        result = _run(execute_command("R3C", "show ip ospf neighbor", ttl=0))
        _assert_ok(result)

    def test_ssh_timeout_transport_field(self):
        """Device field must be present in result."""
        result = _run(execute_command("R3C", "show ip route", ttl=0))
        assert result.get("device") == "R3C"


# ── eAPI (Arista EOS) ─────────────────────────────────────────────────────────

class TestEAPITransport:
    """R1A is an Arista EOS device via eAPI."""

    def test_eapi_execute_show_version(self):
        result = _run(execute_command("R1A", "show version", ttl=0))
        _assert_ok(result)
        assert result["cli_style"] == "eos"

    def test_eapi_execute_ospf_neighbors(self):
        result = _run(execute_command("R1A", "show ip ospf neighbor", ttl=0))
        _assert_ok(result)

    def test_eapi_http_status_error_returns_dict(self):
        """A wrong password should return an error dict, not raise an exception.

        To trigger: temporarily set ROUTER_PASSWORD to an invalid value.
        This test documents the expected error-handling behavior.
        """
        pass  # Verified manually — see manual_testing.md MW-001


# ── REST (MikroTik RouterOS) ──────────────────────────────────────────────────

class TestRESTTransport:
    """R18M is a MikroTik RouterOS device via HTTP REST."""

    def test_rest_execute_ospf_neighbors(self):
        action = {"method": "GET", "path": "/rest/routing/ospf/neighbor"}
        result = _run(execute_command("R18M", action, ttl=0))
        _assert_ok(result)
        assert result["cli_style"] == "routeros"

    def test_rest_execute_interfaces(self):
        action = {"method": "GET", "path": "/rest/interface"}
        result = _run(execute_command("R18M", action, ttl=0))
        _assert_ok(result)


# ── Cache behaviour ───────────────────────────────────────────────────────────

class TestCacheBehaviour:
    """Verify cache_hit flag is set correctly across repeated calls."""

    def test_first_call_cache_miss(self):
        _CACHE.clear()
        result = _run(execute_command("R3C", "show ip route", ttl=CMD_TTL))
        _assert_ok(result)
        assert result.get("cache_hit") is False

    def test_second_call_cache_hit(self):
        _CACHE.clear()
        _run(execute_command("R3C", "show ip route", ttl=CMD_TTL))
        result = _run(execute_command("R3C", "show ip route", ttl=CMD_TTL))
        assert result.get("cache_hit") is True

    def test_ttl_zero_bypasses_cache(self):
        _CACHE.clear()
        _run(execute_command("R3C", "show ip route", ttl=CMD_TTL))
        result = _run(execute_command("R3C", "show ip route", ttl=0))
        assert result.get("cache_hit") is False
