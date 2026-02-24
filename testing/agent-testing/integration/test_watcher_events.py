"""
IT-002 — Watcher Event Parsing

Tests the watcher's event detection logic without spawning an actual agent.
Verifies:
- Non-SLA events are ignored
- SLA Down events are detected (lock file created)
- Stale lock cleanup works correctly
"""

import json
import os
import sys
import tempfile
import threading
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from oncall_watcher import (
    is_sla_down_event,
    is_lock_stale,
    cleanup_lock,
    LOCK_FILE,
)


# ── IT-002a: Event classification ─────────────────────────────────────────────

SLA_DOWN_MESSAGES = [
    "%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down",
    "BOM%TRACK-6-STATE: 2 ip sla 2 reachability Up -> Down",
    "netwatch,info event down [ type: simple, host: 10.0.0.1 ]",
]

NON_SLA_MESSAGES = [
    "%TRACK-6-STATE: 1 ip sla 1 reachability Down -> Up",
    "%SYS-5-CONFIG_I: Configured from console by admin",
    "BGP neighbor 10.0.0.1 state Established",
    "",
]


@pytest.mark.parametrize("msg", SLA_DOWN_MESSAGES)
def test_sla_down_detected(msg):
    assert is_sla_down_event(msg), f"Should detect SLA Down: {msg!r}"


@pytest.mark.parametrize("msg", NON_SLA_MESSAGES)
def test_non_sla_ignored(msg):
    assert not is_sla_down_event(msg), f"Should NOT detect SLA Down: {msg!r}"


# ── IT-002b: Stale lock detection ─────────────────────────────────────────────

def test_stale_lock_nonexistent_pid(tmp_path, monkeypatch):
    """A lock file pointing to a nonexistent PID is detected as stale."""
    lock = tmp_path / "test.lock"
    lock.write_text("999999")  # very unlikely to exist
    monkeypatch.setattr("oncall_watcher.LOCK_FILE", lock)
    assert is_lock_stale()


def test_stale_lock_current_pid(tmp_path, monkeypatch):
    """A lock file pointing to the current process is NOT stale."""
    lock = tmp_path / "test.lock"
    lock.write_text(str(os.getpid()))
    monkeypatch.setattr("oncall_watcher.LOCK_FILE", lock)
    assert not is_lock_stale()


def test_cleanup_lock_removes_file(tmp_path, monkeypatch):
    """cleanup_lock() removes the lock file if it exists."""
    lock = tmp_path / "test.lock"
    lock.write_text("12345")
    monkeypatch.setattr("oncall_watcher.LOCK_FILE", lock)
    cleanup_lock()
    assert not lock.exists()


def test_cleanup_lock_no_error_when_absent(tmp_path, monkeypatch):
    """cleanup_lock() does not raise if lock file doesn't exist."""
    lock = tmp_path / "nonexistent.lock"
    monkeypatch.setattr("oncall_watcher.LOCK_FILE", lock)
    cleanup_lock()   # Should not raise
