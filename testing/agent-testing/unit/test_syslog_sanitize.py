"""Unit tests for sanitize_syslog_msg() — prompt injection defense.

UT-009 — Syslog Sanitization

sanitize_syslog_msg() strips non-printable characters and truncates messages
to prevent crafted syslog entries from injecting instructions into the agent prompt.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from oncall.watcher import sanitize_syslog_msg


# ── Normal message handling ───────────────────────────────────────────────────

def test_normal_message_preserved():
    """A normal syslog message with only printable ASCII must pass through unchanged.
    Confirms the function does not mangle valid operational log data.
    """
    msg = "%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down"
    assert sanitize_syslog_msg(msg) == msg


def test_empty_message_returns_empty():
    """An empty string input must return an empty string without error."""
    assert sanitize_syslog_msg("") == ""


def test_message_with_spaces_preserved():
    """Spaces (printable) must be preserved; only non-printable chars are stripped."""
    msg = "hello world from device"
    assert sanitize_syslog_msg(msg) == msg


# ── Non-printable character stripping ────────────────────────────────────────

def test_null_bytes_stripped():
    """Null bytes (\\x00) are non-printable and must be removed.
    An attacker could embed null bytes to confuse downstream parsers.
    """
    msg = "hello\x00world"
    assert sanitize_syslog_msg(msg) == "helloworld"


def test_control_characters_stripped():
    """C0 control characters (\\x01-\\x1f) must be stripped.
    These could be used to inject ANSI escape sequences or terminal control codes.
    """
    msg = "hello\x01\x1f\x07world"
    assert sanitize_syslog_msg(msg) == "helloworld"


def test_tab_stripped():
    """Tab (\\t) is non-printable per str.isprintable() and must be stripped."""
    msg = "hello\tworld"
    assert sanitize_syslog_msg(msg) == "helloworld"


def test_newline_stripped():
    """Newlines (\\n) are non-printable and must be stripped.
    A newline in a syslog message could break the prompt's line structure.
    """
    msg = "line1\nline2"
    assert sanitize_syslog_msg(msg) == "line1line2"


def test_only_non_printable_returns_empty():
    """A message consisting entirely of non-printable chars must return an empty string."""
    assert sanitize_syslog_msg("\x00\x01\x02\x03") == ""


def test_mixed_printable_and_non_printable():
    """Only the printable portion of a mixed message is retained."""
    msg = "SLA\x00\x01 Down\n event"
    assert sanitize_syslog_msg(msg) == "SLA Down event"


# ── Length truncation ─────────────────────────────────────────────────────────

def test_message_within_limit_not_truncated():
    """A message shorter than max_length (500) must not be truncated."""
    msg = "A" * 100
    assert sanitize_syslog_msg(msg) == msg


def test_message_at_limit_not_truncated():
    """A message exactly at max_length must not be truncated."""
    msg = "A" * 500
    assert sanitize_syslog_msg(msg) == msg


def test_message_over_limit_truncated():
    """A message longer than 500 chars must be truncated to exactly 500 chars.
    Long messages can inflate the agent prompt and hide injected content after the cutoff.
    """
    msg = "A" * 600
    result = sanitize_syslog_msg(msg)
    assert len(result) == 500
    assert result == "A" * 500


def test_custom_max_length_respected():
    """The max_length parameter must override the default 500-char limit."""
    msg = "hello world"
    assert sanitize_syslog_msg(msg, max_length=5) == "hello"


def test_truncation_after_stripping():
    """Truncation is applied after non-printable stripping, not before.
    Ensures the 500-char limit applies to the clean output, not the raw input.
    """
    # 400 non-printable + 200 'A' → after stripping: 200 'A' → no truncation
    msg = "\x00" * 400 + "A" * 200
    result = sanitize_syslog_msg(msg)
    assert result == "A" * 200
    assert len(result) == 200
