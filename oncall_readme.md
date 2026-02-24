# On-Call Watcher — Usage Guide

## Overview

The `oncall_watcher.py` script monitors `/var/log/network.json` (written by Vector) for IP SLA path-down events and automatically invokes Claude Code to troubleshoot the network issue. It implements:

- **Multi-vendor event detection**: Cisco (TRACK-6-STATE), Arista, MikroTik (netwatch)
- **Storm prevention**: Only one Claude session runs at a time; extra events are logged and skipped
- **Cost efficiency**: Claude sessions auto-exit when the user types `/exit`
- **Log rotation handling**: Automatically detects and reopens rotated log files

---

## Quick Start

### 1. Start the Watcher (One-Time Setup per Session)

```bash
cd /home/mcp/mcp-project
source mcp/bin/activate
python oncall_watcher.py
```

**Expected output:**
```
[aiNOC On-Call Watcher] Monitoring /var/log/network.json for IP SLA Down events.
[Watcher] Watcher started. Monitoring /var/log/network.json for IP SLA Down events.
```

Leave this terminal tab open. The watcher will idle, monitoring for events.

### 2. When an IP SLA Event Occurs

When a device's IP SLA path goes down, Vector logs the event to `/var/log/network.json`, and the watcher detects it:

```
[Watcher] Agent invoked — R9C (172.20.20.209): BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down
# Claude Code session opens here in the same terminal...
```

Claude automatically opens with the SLA event context and begins On-Call Mode troubleshooting:

```
On-Call Mode triggered: IP SLA path failure detected.

Log event:
  Timestamp : 2026-02-23T14:30:00Z
  Source    : R9C (172.20.20.209)
  Event     : BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down

Please follow the On-Call Mode troubleshooting workflow as defined in your instructions.
```

### 3. During the Claude Session

Claude will:
1. Follow the On-Call Mode workflow (steps 2–8 from CLAUDE.md)
2. Access `sla_paths/paths.json` to understand the failed path
3. Run diagnostic commands on affected devices
4. Identify the root cause
5. Ask for your approval before making config changes
6. Apply and verify the fix
7. Document the case in `cases/cases.md`

### 4. Ending the Session

After Claude presents the summary, you'll see:

```
---
Summary: IP SLA path R9C_TO_R5C (5.5.1.1) was down due to EIGRP neighbor flap.
Fixed by: Adjusted EIGRP hold-timer on R8C.
Verified: Path reachability restored.

Type /exit to close this On-Call session and resume watcher monitoring,
or keep the session open if you want to continue investigating.
```

**To resume watcher monitoring:**
```
/exit
```

The watcher will then log the session end and resume idle monitoring:

```
[Watcher] Agent session ended. Resuming monitoring.
```

---

## Storm Prevention (Multi-Event Handling)

If multiple IP SLA events occur within a short time:

- **First event**: Watcher detects it, creates `oncall.lock`, invokes Claude
- **Second event (while Claude is busy)**: Logged as skipped (no concurrent sessions)
  ```
  [Watcher] SKIPPED (agent busy) - R5C (172.20.20.205): BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down
  ```
- **After Claude exits**: Lock file is removed, watcher resumes monitoring

**Review skipped events**: Check `oncall_watcher.log` for any events that arrived while the agent was busy.

---

## Log Files & Monitoring

### `oncall_watcher.log`

Timestamped log of all watcher activity:

```
[2026-02-23 14:30:00 UTC] Watcher started. Monitoring /var/log/network.json for IP SLA Down events.
[2026-02-23 14:30:15 UTC] Agent invoked for event on R9C: BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down
[2026-02-23 14:35:00 UTC] SKIPPED (agent busy) - R5C: BOM%TRACK-6-STATE: 1 ip sla 2 reachability Up -> Down
[2026-02-23 14:40:10 UTC] Agent session ended. Resuming monitoring.
```

### `oncall.lock`

Created when Claude session starts, deleted when it exits. If this file persists after Claude exits, it's stale and will be auto-cleaned on the next event detection.

---

## Event Patterns Detected

The watcher recognizes IP SLA Down events from:

### Cisco IOS/IOS-XE (Primary)
```
BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down
%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down
```

### Arista EOS
```
Similar TRACK format (if configured)
```

### MikroTik RouterOS (via Netwatch)
```
netwatch,info event down [ type: simple, host: 220.50.50.5 ]
```

**Important**: Events with "Down -> Up" (recovery) are ignored; only "Up -> Down" (failures) trigger the watcher.

---

## Troubleshooting the Watcher

### Q: Watcher doesn't detect new events
- **Check**: Is Vector running and writing to `/var/log/network.json`?
  ```bash
  ps aux | grep vector
  tail -f /var/log/network.json
  ```
- **Check**: Are SLA events actually being generated on source devices?
  ```bash
  docker exec R9C show track | include "ip sla"
  ```

### Q: Watcher detects event but Claude doesn't open
- **Check**: Is the Claude binary at `/home/mcp/.local/bin/claude`?
  ```bash
  which claude
  ```
- **Check**: Is the MCP server running (`MCPServer.py`)?
  ```bash
  ps aux | grep MCPServer
  ```

### Q: Multiple Claude sessions open at once (storm occurred)
- **Cause**: Stale lock file from a crashed Claude session
- **Fix**: Delete `oncall.lock` manually:
  ```bash
  rm -f /home/mcp/mcp-project/oncall.lock
  ```

### Q: Watcher exits or crashes
- **Check**: Review terminal output and `oncall_watcher.log` for error details
- **Restart**: Simply run `python oncall_watcher.py` again

---

## Advanced: Manual Testing

### Test regex pattern matching:

```bash
python3 << 'EOF'
import re
SLA_DOWN_RE = re.compile(
    r'(?:'
    r'%?TRACK-\d+-STATE:.*ip\s+sla.*reachability\s+\S+\s+->\s+Down'
    r'|'
    r'ip\s+sla\s+\d+.*(?:changed.*state|transition).*(?:up|reachable).*(?:to|->)\s*down'
    r'|'
    r'netwatch.*event\s+down'
    r')',
    re.IGNORECASE
)
test_msg = "BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down"
print("Match:", bool(SLA_DOWN_RE.search(test_msg)))
EOF
```

### Inject a test event into the log:

```bash
# Add a test JSON line to the log (it will be detected if watcher is running)
python3 -c "
import json
event = {
    'ts': '2026-02-23T14:30:00Z',
    'device': '172.20.20.209',
    'severity': 'notice',
    'msg': 'BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down'
}
with open('/var/log/network.json', 'a') as f:
    f.write(json.dumps(event) + '\n')
"
```

---

## File Rotation Handling

The watcher automatically detects when `/var/log/network.json` is rotated by Vector:

1. Tracks the file's inode (unique ID)
2. If inode changes → file was rotated
3. Automatically reopens the new file from the beginning
4. Resumes monitoring without losing events

No manual intervention needed.

---

## Graceful Shutdown

To stop the watcher:

```bash
# Press Ctrl+C in the terminal where it's running
^C
```

The watcher will:
1. Clean up the lock file (if any)
2. Log "Watcher stopped (signal received)"
3. Exit gracefully

---

## Architecture Summary

```
Network Device SLA Fails
        ↓
  System logs via syslog (UDP :514)
        ↓
  Vector parses and normalizes → /var/log/network.json
        ↓
  oncall_watcher.py tail-follows the file
        ↓
  Regex matches "IP SLA Down" pattern
        ↓
  Check oncall.lock (storm prevention)
        ↓
  Resolve device IP to name (R9C, R5C, etc.)
        ↓
  invoke claude "Context prompt with SLA details"
        ↓
  Claude troubleshoots interactively (user supervises)
        ↓
  User types /exit when done
        ↓
  Lock file deleted, watcher resumes monitoring
```

---

## Integration with CLAUDE.md

When Claude is invoked, it receives CLAUDE.md as its system prompt, which defines:

- **On-Call Mode workflow**: Steps to follow (check paths.json, traceroute, etc.)
- **Session closure**: Present summary + prompt user to `/exit`
- **Case documentation**: Auto-append to `cases/cases.md` with findings

---

## Summary

- **Start**: `python oncall_watcher.py`
- **Monitor**: Leave it running in a terminal
- **Event**: Claude auto-invokes on SLA failures
- **Finish**: User types `/exit` to resume monitoring
- **Logs**: Check `oncall_watcher.log` for history

Enjoy automated On-Call troubleshooting! 🚀
