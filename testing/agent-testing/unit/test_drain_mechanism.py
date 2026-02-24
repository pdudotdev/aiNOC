"""
UT-003 — Tail Follow Drain Mechanism

Verifies tail_follow(filepath, drain):
1. Normal lines are yielded as written.
2. Setting drain[0] = True causes subsequent buffered lines to be skipped.
3. After the drain seek, drain[0] is reset to False.
4. New lines written after drain are yielded again.
"""

import sys
import tempfile
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from oncall_watcher import tail_follow


def _collect(gen, count: int, timeout: float = 5.0) -> list:
    """Collect up to `count` items from a generator with a timeout."""
    results = []
    deadline = time.time() + timeout

    class _Stop(Exception):
        pass

    def _run():
        for item in gen:
            results.append(item)
            if len(results) >= count:
                raise _Stop()

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join(timeout=timeout)
    return results


def test_normal_lines_yielded(tmp_path):
    log = tmp_path / "net.json"
    log.write_text("")
    drain = [False]

    gen = tail_follow(str(log), drain)

    collected = []
    done = threading.Event()

    def reader():
        for line in gen:
            collected.append(line)
            if len(collected) >= 3:
                done.set()
                return

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    time.sleep(0.3)
    with open(log, "a") as f:
        f.write('{"ts":"1","msg":"line1"}\n')
        f.write('{"ts":"2","msg":"line2"}\n')
        f.write('{"ts":"3","msg":"line3"}\n')

    done.wait(timeout=4)
    assert len(collected) == 3
    assert '{"ts":"1","msg":"line1"}' in collected


def test_drain_skips_buffered_lines(tmp_path):
    """After drain[0]=True is set, buffered lines written before the seek are skipped."""
    log = tmp_path / "net.json"
    log.write_text("")
    drain = [False]

    collected = []
    post_drain = []
    phase_lock = threading.Lock()
    drained = threading.Event()
    done = threading.Event()

    def reader():
        for line in tail_follow(str(log), drain):
            with phase_lock:
                if drain[0] is False and drained.is_set():
                    post_drain.append(line)
                else:
                    collected.append(line)
            if len(post_drain) >= 1:
                done.set()
                return

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    # Write one line before drain
    time.sleep(0.3)
    with open(log, "a") as f:
        f.write('{"ts":"pre","msg":"before_drain"}\n')
    time.sleep(0.2)

    # Trigger drain while writing more lines
    drain[0] = True
    with open(log, "a") as f:
        f.write('{"ts":"skipped","msg":"should_be_skipped"}\n')
    time.sleep(0.3)
    drained.set()

    # Write a line after drain completes — this should be yielded
    time.sleep(0.5)
    with open(log, "a") as f:
        f.write('{"ts":"after","msg":"after_drain"}\n')

    done.wait(timeout=5)
    assert any("before_drain" in c for c in collected)
    assert not any("should_be_skipped" in c for c in post_drain)
    assert any("after_drain" in c for c in post_drain)


def test_drain_resets_to_false(tmp_path):
    """After tail_follow processes drain[0]=True, it resets drain[0] to False."""
    log = tmp_path / "net.json"
    log.write_text("")
    drain = [False]

    reset_seen = threading.Event()

    def reader():
        for _ in tail_follow(str(log), drain):
            if drain[0] is False and reset_seen.is_set() is False:
                # Check if it was True before and is now False (reset happened)
                pass

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    time.sleep(0.2)
    drain[0] = True
    # Give tail_follow time to process the drain flag
    deadline = time.time() + 3
    while time.time() < deadline:
        if drain[0] is False:
            reset_seen.set()
            break
        time.sleep(0.05)

    assert reset_seen.is_set(), "drain[0] was not reset to False after drain seek"
