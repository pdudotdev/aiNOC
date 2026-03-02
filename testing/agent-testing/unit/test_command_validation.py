"""Unit tests for validate_commands() — FORBIDDEN CLI list and RouterOS JSON validation."""
import json
import pytest
from tools.config import validate_commands, FORBIDDEN, FORBIDDEN_REST_PATHS, VALID_REST_PUSH_METHODS


# ── FORBIDDEN CLI commands ─────────────────────────────────────────────────────

FORBIDDEN_CLI_CASES = [
    "reload",
    "write erase",
    "erase startup-config",
    "format flash:",
    "delete flash:running-config",
    "boot system flash",
    "crypto key zeroize rsa",
    "no router ospf 1",
    "no router eigrp 10",
    "default interface Ethernet0/1",
    "clear ip ospf process",
    "clear ip bgp *",
    "clear ip eigrp neighbors",
    "clear ip route *",
    "debug all",
    # Case-insensitive matching
    "RELOAD",
    "Write Erase",
    "NO ROUTER BGP 65000",
]


@pytest.mark.parametrize("cmd", FORBIDDEN_CLI_CASES)
def test_forbidden_cli_command_blocked(cmd):
    """Verify that known-dangerous CLI commands are rejected by validate_commands().
    Parametrized across all FORBIDDEN patterns including case variants.
    """
    with pytest.raises(ValueError, match="Forbidden command"):
        validate_commands([cmd])


SAFE_CLI_CASES = [
    "ip ospf hello-interval 10",
    "ip ospf dead-interval 40",
    "neighbor 10.0.0.1 remote-as 65001",
    "network 192.168.1.0 0.0.0.255 area 0",
    "ip route 0.0.0.0 0.0.0.0 1.2.3.4",
    "router ospf 1",           # "no router" is forbidden; "router " is allowed
    "passive-interface default",
    "no passive-interface Ethernet0/1",
]


@pytest.mark.parametrize("cmd", SAFE_CLI_CASES)
def test_safe_cli_command_passes(cmd):
    """Legitimate configuration commands must pass validate_commands() without error.
    Confirms that the FORBIDDEN set does not over-block valid operational commands.
    """
    validate_commands([cmd])  # must not raise


# ── RouterOS JSON: forbidden paths ────────────────────────────────────────────

@pytest.mark.parametrize("path", sorted(FORBIDDEN_REST_PATHS))
def test_routeros_forbidden_path_blocked(path):
    """RouterOS REST actions targeting system-critical paths must be blocked.
    Paths like /rest/system/reboot or /rest/user could take the device offline.
    """
    action = json.dumps({"method": "PUT", "path": path, "body": {}})
    with pytest.raises(ValueError, match="Forbidden REST path"):
        validate_commands([action])


def test_routeros_safe_path_passes():
    """A PATCH to a non-forbidden RouterOS OSPF path must pass validate_commands().
    Confirms the forbidden-path set does not block valid OSPF configuration changes.
    """
    action = json.dumps({
        "method": "PATCH",
        "path": "/rest/routing/ospf/instance/abc123",
        "body": {"hello-interval": "10"},
    })
    validate_commands([action])  # must not raise


# ── RouterOS JSON: invalid HTTP methods ───────────────────────────────────────

@pytest.mark.parametrize("method", ["GET", "POST", "HEAD", "OPTIONS"])
def test_routeros_invalid_method_blocked(method):
    """RouterOS REST actions with read-only or unsupported HTTP methods must be blocked.
    GET belongs in run_show; POST is unsupported on RouterOS 7.x for configuration.
    """
    action = json.dumps({"method": method, "path": "/rest/routing/ospf/instance"})
    with pytest.raises(ValueError, match="Invalid REST method"):
        validate_commands([action])


@pytest.mark.parametrize("method", sorted(VALID_REST_PUSH_METHODS))
def test_routeros_valid_method_passes(method):
    """RouterOS REST actions with valid push methods (PUT/PATCH/DELETE) must pass.
    These are the only methods allowed for RouterOS configuration changes.
    """
    action = json.dumps({
        "method": method,
        "path": "/rest/routing/ospf/instance/abc123",
        "body": {},
    })
    validate_commands([action])  # must not raise


# ── Mixed batch: one forbidden stops the whole batch ──────────────────────────

def test_forbidden_in_batch_raises():
    """A single forbidden command in a batch must reject the entire batch.
    Prevents partially applied changes that could leave the device in an inconsistent state.
    """
    cmds = [
        "ip ospf hello-interval 10",
        "reload",                      # forbidden
        "ip ospf dead-interval 40",
    ]
    with pytest.raises(ValueError, match="Forbidden command"):
        validate_commands(cmds)


# ── Rollback advisory generation ──────────────────────────────────────────────

from tools.config import _generate_rollback_advisory


def test_rollback_inverts_no_prefix():
    """A 'no <cmd>' command must produce '<cmd>' as the rollback advisory.
    Inversion lets the operator quickly undo a negation if needed.
    """
    result = _generate_rollback_advisory(["no ip ospf hello-interval 10"])
    assert result == ["ip ospf hello-interval 10"]


def test_rollback_adds_no_prefix():
    """A positive configuration command must produce 'no <cmd>' as the rollback advisory.
    The rollback advisory gives operators a ready-made undo command.
    """
    result = _generate_rollback_advisory(["ip ospf dead-interval 40"])
    assert result == ["no ip ospf dead-interval 40"]


def test_rollback_routeros_advisory():
    """RouterOS REST commands must produce a manual-action advisory, not an inverted command.
    RouterOS PATCH/PUT rollback requires the original resource ID which may not be known.
    """
    action = json.dumps({"method": "PATCH", "path": "/rest/routing/ospf/instance/abc"})
    result = _generate_rollback_advisory([action])
    assert result[0].startswith("# RouterOS PATCH rollback requires manual action")


def test_rollback_batch():
    """A batch of commands must produce a matching batch of rollback advisories.
    Each command is independently inverted, preserving order.
    """
    cmds = ["ip ospf hello-interval 5", "no ip ospf dead-interval"]
    result = _generate_rollback_advisory(cmds)
    assert result[0] == "no ip ospf hello-interval 5"
    assert result[1] == "ip ospf dead-interval"
