# aiNOC Manual Testing Strategy

End-to-end test scenarios for validating Standalone and On-Call agent functionality.
Run these after significant codebase changes to confirm correct agent behavior.

---

## Prerequisites

- Lab is up (`sudo clab deploy -t lab.yml`)
- All devices reachable (verify with `./run_tests.sh integration`)
- MCP server running or accessible
- `oncall_watcher.py` not already running (for On-Call tests)

---

## Standalone Mode Tests

These tests validate the agent's diagnostic and remediation workflow when a user
submits a network problem description directly at the Claude Code prompt.

Launch with:
```bash
cd /home/mcp/mcp-project
claude
```

---

### ST-001 — OSPF Timer Mismatch (R1A)

**Protocol**: OSPF | **Device**: R1A (Arista EOS) | **Symptom**: Adjacency down

#### Setup (break)

Connect to R1A via eAPI or SSH and apply:
```
interface Ethernet3
  ip ospf dead-interval 7
interface Ethernet4
  ip ospf dead-interval 7
```

#### Verify break

From R1A:
```
show ip ospf neighbor
```
Expected: R2C and R3C are **absent** from Area 0 neighbors (Ethernet3/Ethernet4).

#### Agent prompt
```
OSPF adjacencies are down on R1A. R1A shows no OSPF neighbors in Area 0
(expected: R2C on Ethernet4 and R3C on Ethernet3). Please investigate.
```

#### Expected agent behavior

1. Reads `skills/ospf/SKILL.md`
2. Calls `get_ospf(R1A, "neighbors")` → no Area 0 neighbors
3. Calls `get_ospf(R1A, "interfaces")` → dead-interval 7 on Ethernet3/Ethernet4
4. Identifies timer mismatch (EOS default dead-interval = 40s)
5. Proposes removing the dead-interval override on R1A Ethernet3 and Ethernet4
6. Asks user approval before applying
7. Applies fix, verifies R2C and R3C return to FULL state

#### Verify fix

```
show ip ospf neighbor
```
Expected: R2C and R3C present, state FULL.

#### Teardown (if agent did not fix)

```
interface Ethernet3
  no ip ospf dead-interval
interface Ethernet4
  no ip ospf dead-interval
```

---

### ST-002 — EIGRP Passive Interface (R8C)

**Protocol**: EIGRP | **Device**: R8C (Cisco IOS) | **Symptom**: Neighbor down

#### Setup (break)

SSH to R8C and apply:
```
router eigrp 20
  passive-interface Ethernet0/3
```

#### Verify break

From R8C:
```
show ip eigrp neighbors
```
Expected: R9C is **absent**.

From R9C:
```
show ip eigrp neighbors
```
Expected: R8C is **absent**.

#### Agent prompt
```
R9C has lost EIGRP connectivity. R9C cannot reach any OSPF-learned destinations
(e.g. 172.16.0.0/24). EIGRP neighbor to R8C is down. Please investigate.
```

#### Expected agent behavior

1. Reads `skills/eigrp/SKILL.md`
2. Calls `get_eigrp(R8C, "neighbors")` → no neighbors
3. Calls `get_eigrp(R8C, "interfaces")` → Ethernet0/3 is passive
4. Proposes removing passive-interface Ethernet0/3 on R8C
5. Asks approval, applies, verifies R9C neighbor returns FULL

#### Verify fix

```
show ip eigrp neighbors
```
On R8C: R9C present. On R9C: R8C present.

#### Teardown (if agent did not fix)

```
router eigrp 20
  no passive-interface Ethernet0/3
```

---

### ST-003 — Redistribution Break (R3C)

**Protocol**: Redistribution | **Device**: R3C (Cisco IOS) | **Symptom**: Routes missing

#### Setup (break)

SSH to R3C and remove OSPF→EIGRP redistribution:
```
router eigrp 10
  no redistribute ospf 1 metric 1000 1 255 1 1500
```

#### Verify break

From R4C:
```
show ip route
```
Expected: No `D EX` routes for `172.16.0.0/24` (OSPF Area 2 subnet) or other OSPF-originated prefixes.

#### Agent prompt
```
R4C is missing routes to the 172.16.0.0/24 subnet (Area 2 stub network).
Routes that should be redistributed from OSPF into EIGRP AS10 are absent on R4C.
Please investigate the redistribution configuration on R3C.
```

#### Expected agent behavior

1. Reads `skills/redistribution/SKILL.md`
2. Calls `get_routing(R4C, "172.16.0.0/24")` → route missing
3. Calls `get_routing_policies(R3C, "redistribution")` → redistribute statement absent
4. Proposes restoring: `redistribute ospf 1 metric 1000 1 255 1 1500` under `router eigrp 10`
5. Asks approval, applies, verifies route returns on R4C

#### Verify fix

From R4C:
```
show ip route 172.16.0.0
```
Expected: `D EX 172.16.0.0/24` present.

#### Teardown (if agent did not fix)

```
router eigrp 10
  redistribute ospf 1 metric 1000 1 255 1 1500
```

---

### ST-004 — OSPF Area Mismatch (R10C)

**Protocol**: OSPF | **Device**: R10C (Cisco IOS) | **Symptom**: Adjacency down, routes missing

#### Setup (break)

SSH to R10C and move its R1A-facing interface to a wrong area:
```
router ospf 1
  no network 172.16.0.4 0.0.0.3 area 2
  network 172.16.0.4 0.0.0.3 area 3
```

#### Verify break

From R1A:
```
show ip ospf neighbor
```
Expected: R10C missing from Area 2 neighbors.

From R10C:
```
show ip ospf neighbor
```
Expected: No neighbors.

#### Agent prompt
```
R10C has lost its OSPF adjacency to R1A. R10C is isolated and has no routes
to the rest of the network. Please investigate.
```

#### Expected agent behavior

1. Reads `skills/ospf/SKILL.md`
2. Calls `get_ospf(R10C, "neighbors")` → no neighbors
3. Calls `get_ospf(R10C, "config")` → area 3 mismatch
4. Cross-references with `intent/INTENT.json` (R10C expected in area 2)
5. Proposes correcting `network 172.16.0.4 0.0.0.3 area 2` on R10C
6. Asks approval, applies, verifies adjacency restored

#### Verify fix

```
show ip ospf neighbor
```
On R1A: R10C present, state FULL.

#### Teardown (if agent did not fix)

```
router ospf 1
  no network 172.16.0.4 0.0.0.3 area 3
  network 172.16.0.4 0.0.0.3 area 2
```

---

### ST-005 — Interface Shutdown (R9C Upstream)

**Protocol**: EIGRP | **Device**: R8C (Cisco IOS) | **Symptom**: Full connectivity loss from R9C

#### Setup (break)

SSH to R8C:
```
interface Ethernet0/3
  shutdown
```

#### Verify break

From R9C:
```
show ip eigrp neighbors
show ip route
```
Expected: No EIGRP neighbors, no routes (stub isolated).

#### Agent prompt
```
R9C has completely lost connectivity. No EIGRP neighbors visible and no routes
to any remote destination. Please investigate.
```

#### Expected agent behavior

1. Reads `skills/eigrp/SKILL.md`
2. Calls `get_eigrp(R9C, "neighbors")` → empty
3. Calls `get_interfaces(R8C)` → Ethernet0/3 down
4. Identifies admin-shutdown on R8C Ethernet0/3
5. Proposes `no shutdown` on R8C Ethernet0/3
6. Asks approval, applies, verifies R9C neighbor and routes return

#### Verify fix

From R9C: `show ip eigrp neighbors` → R8C present.

#### Teardown (if agent did not fix)

```
interface Ethernet0/3
  no shutdown
```

---

### ST-006 — EIGRP Stub/Summary Misconfiguration (R9C)

**Protocol**: EIGRP | **Device**: R9C (Cisco IOS) | **Symptom**: Individual loopback /24 routes advertised instead of /22 summary

#### Setup (break)

SSH to R9C and change stub from `connected summary` to `connected`:
```
router eigrp 20
  eigrp stub connected
```

#### Verify break

From R1A:
```
show ip route | include 9.9
```
Expected: Three separate `O E1 9.9.x.0/24` entries visible instead of a single `O E1 9.9.0.0/22`.

#### Agent prompt

```
Why are all routers in the network showing individual routes to R9C's loopbacks.
Check this and give me all potential fixes to choose from.
```

#### Expected agent behavior

1. Reads `skills/eigrp/SKILL.md`
2. Calls `get_routing(R1A, "9.9.0.0")` → confirms individual /24 routes
3. Calls `get_eigrp(R9C, "config")` → finds `eigrp stub connected` (no `summary` keyword)
4. Calls `get_eigrp(R9C, "interfaces")` → identifies summary-address on Et0/1
5. Identifies conflict: stub `connected` without `summary` overrides and advertises individual connected routes
6. Presents 3 fix options (change stub to include `summary`, modify interface summary, summarize at R8C)
7. User selects Option 2 (`eigrp stub connected summary`)
8. Applies fix, verifies /22 summary now present and individual /24s suppressed on R1A

#### Verify fix

```
show ip route | include 9.9
```
Expected: Single `O E1 9.9.0.0/22` present.

#### Teardown (if agent did not fix)

```
router eigrp 20
  eigrp stub connected summary
```

---

### ST-007 — EIGRP Redistribution Missing Metric (R3C)

**Protocol**: Redistribution | **Device**: R3C (Cisco IOS) | **Symptom**: R4C/R5C cannot reach OSPF domain

#### Setup (break)

SSH to R3C and replace the full redistribute command with bare `redistribute ospf 1` (no metric):
```
router eigrp 10
  no redistribute ospf 1 metric 10000 100 255 1 1500
  redistribute ospf 1
```

#### Verify break

From R4C:
```
show ip route | include D EX
```
Expected: No external EIGRP routes (D EX) visible. No routes to OSPF domain.

#### Agent prompt

```
R4C and R5C cannot reach anything beyond R3C. Verify and give me a few solutions.
```

#### Expected agent behavior

1. Reads `skills/redistribution/SKILL.md`
2. Calls `get_routing(R4C)` → confirms no D EX routes
3. Calls `get_routing_policies(R3C, "redistribution")` → finds `redistribute ospf 1` with no metric
4. Calls `get_eigrp(R3C, "config")` → identifies "Total Redist Count: 0"
5. Identifies root cause: missing metric causes EIGRP to treat redistributed routes as unreachable (infinity metric)
6. Presents multiple solutions (add metric inline, use default-metric, use route-map for selective redistribution)
7. Applies recommended solution: `redistribute ospf 1 metric 10000 100 255 1 1500`
8. Verifies D EX routes return on R4C

#### Verify fix

```
show ip route | include D EX
```
Expected: Multiple `D EX` routes present (e.g., `172.16.0.0/24`, `10.x.x.x`/30 subnets, loopback addresses).

#### Teardown (if agent did not fix)

```
router eigrp 10
  no redistribute ospf 1
  redistribute ospf 1 metric 10000 100 255 1 1500
```

---

### ST-008 — Policy-Based Routing Investigation (R8C)

**Protocol**: Routing Policy | **Device**: R8C (Cisco IOS) | **Symptom**: Traffic from R9C to 2.2.2.66 follows asymmetric path

#### Setup (break)

SSH to R8C and apply PBR configuration:
```
ip access-list extended 100
 10 permit ip host 192.168.20.2 host 2.2.2.66
route-map ACCESS-R2-LO permit 10
 match ip address 100
 set ip next-hop 10.1.1.6
interface Ethernet0/3
 ip policy route-map ACCESS-R2-LO
```

#### Verify break

From R8C, trace from R9C toward R2A loopback:
```
traceroute 2.2.2.66 source 192.168.20.2
```
Expected: Path goes through `10.1.1.6` (R7A), not R6A.

#### Agent prompt

```
Why does R8C forward packets from R9C destined for 2.2.2.66 to R7A?
```

#### Expected agent behavior

1. Reads routing policy skills
2. Calls `get_routing(R8C, "2.2.2.66")` → shows normal ECMP paths (R6A 10.1.1.2 and R7A 10.1.1.6 equal cost)
3. Calls `get_routing_policies(R8C, "route_maps")` → finds `ACCESS-R2-LO` with `set ip next-hop 10.1.1.6`
4. Calls `get_routing_policies(R8C, "access_lists")` → finds ACL 100 matching host 192.168.20.2 → host 2.2.2.66
5. Identifies PBR on Et0/3 overriding normal routing decisions
6. Correctly diagnoses root cause with explanation of ACL match and next-hop override
7. Proposes removal of PBR config
8. User responds "No" → agent gracefully accepts without applying changes
9. Documents case (diagnostic scenario, no fix applied)

#### Verify (diagnostic only)

Agent correctly identified:
- PBR as root cause
- The specific ACL and route-map involved
- The forced next-hop (10.1.1.6 = R7A)
- Clear explanation of why traffic is asymmetric

Agent gracefully accepted "No" and documented the case without forcing changes.

#### Teardown (if agent did not fix, restore clean state)

```
interface Ethernet0/3
  no ip policy route-map ACCESS-R2-LO
no route-map ACCESS-R2-LO
no ip access-list extended 100
```

---

## On-Call Mode Tests

These tests validate the full watcher → agent pipeline. The watcher monitors
`/var/log/network.json`, detects SLA Down events, and spawns a Claude agent session.

### Setup for all On-Call tests

In a separate terminal, start the watcher:
```bash
cd /home/mcp/mcp-project
python3 oncall_watcher.py
```

Monitor the watcher log in another terminal:
```bash
tail -f /home/mcp/mcp-project/oncall_watcher.log
```

Inject an SLA event using:
```bash
echo '{"ts":"<ISO_TIMESTAMP>","device":"<DEVICE_IP>","msg":"<SLA_MSG>"}' >> /var/log/network.json
```

Replace `<ISO_TIMESTAMP>` with current UTC time in ISO 8601 format, e.g.:
```bash
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
```

---

### OC-001 — OSPF Passive Interface → R4C SLA Failure

**SLA Path**: `R4C_TO_R10C` | **Break device**: R3C | **SLA source**: R4C (172.20.20.204)

#### Setup (break)

SSH to R3C:
```
router ospf 1
  passive-interface Ethernet0/3
```

#### Verify break

From R3C:
```
show ip ospf neighbor
```
Expected: R1A (via Ethernet0/3) **absent**.

From R4C:
```
show ip route 10.10.10.10
```
Expected: Route to R10C loopback `10.10.10.10` **absent**.

#### Inject SLA event

```bash
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"ts\":\"${TS}\",\"device\":\"172.20.20.204\",\"msg\":\"BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down\"}" >> /var/log/network.json
```

#### Expected watcher behavior

Within 2 seconds: watcher logs `Agent invoked for event on R4C`.
Claude Code session opens automatically.

#### Expected agent behavior

1. Reads `skills/oncall/SKILL.md`
2. Looks up `R4C_TO_R10C` in `sla_paths/paths.json` → scope: R4C, R3C, R1A, R10C
3. Traceroutes from R4C to `10.10.10.10` → stops at R3C
4. Reads `skills/ospf/SKILL.md`
5. Calls `get_ospf(R3C, "neighbors")` → R1A missing
6. Calls `get_ospf(R3C, "config")` → passive-interface on Ethernet0/3
7. Proposes removing passive-interface on R3C Ethernet0/3
8. Asks user approval (displayed in the agent session)
9. Applies fix, verifies R4C route to 10.10.10.10 returns
10. Documents case, asks user to type `/exit`

#### Verify fix

From R3C:
```
show ip ospf neighbor
```
Expected: R1A FULL.

From R4C:
```
show ip route 10.10.10.10
```
Expected: Route present via OSPF/EIGRP redistribution path.

#### Documentation check

- New case in `cases/cases.md` with R3C, R4C context
- `Verification: PASSED`
- `Case Status: FIXED`

#### Teardown (if agent did not fix)

```
router ospf 1
  no passive-interface Ethernet0/3
```

---

### OC-002 — EIGRP Interface Shutdown → R9C SLA Failure

**SLA Path**: `R9C_TO_R5C` or `R9C_TO_R11C` | **Break device**: R8C | **SLA source**: R9C (172.20.20.209)

#### Setup (break)

SSH to R8C:
```
interface Ethernet0/3
  shutdown
```

#### Verify break

From R9C:
```
show ip eigrp neighbors
```
Expected: R8C **absent** (R9C is fully isolated).

#### Inject SLA event

```bash
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"ts\":\"${TS}\",\"device\":\"172.20.20.209\",\"msg\":\"BOM%TRACK-6-STATE: 2 ip sla 2 reachability Up -> Down\"}" >> /var/log/network.json
```

#### Expected agent behavior

1. Reads `skills/oncall/SKILL.md`
2. Looks up `R9C_TO_R5C` in paths.json → scope includes R9C, R8C
3. Traceroutes from R9C → fails at first hop
4. Reads `skills/eigrp/SKILL.md`
5. Calls `get_eigrp(R9C, "neighbors")` → empty
6. Calls `get_interfaces(R8C)` → Ethernet0/3 admin down
7. Proposes `no shutdown` on R8C Ethernet0/3
8. Asks approval, applies, verifies R9C neighbor restored

#### Verify fix

From R8C:
```
show interfaces Ethernet0/3
```
Expected: Line protocol up.

From R9C:
```
show ip eigrp neighbors
```
Expected: R8C present.

#### Teardown (if agent did not fix)

```
interface Ethernet0/3
  no shutdown
```

---

### OC-003 — Deferred Event Handling (Storm Prevention)

**Purpose**: Validate that concurrent SLA events during an active session are deferred
and surfaced in a follow-up review session.

#### Setup

1. Start the watcher.
2. Break R3C OSPF (same as OC-001) and inject the R4C SLA Down event.
3. **While the agent session is active** (within 30s of injection), inject a second SLA event
   for a different device — e.g., R9C:

```bash
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"ts\":\"${TS}\",\"device\":\"172.20.20.209\",\"msg\":\"BOM%TRACK-6-STATE: 2 ip sla 2 reachability Up -> Down\"}" >> /var/log/network.json
```

#### Expected watcher behavior

- Second event logged as: `SKIPPED (deferred - occurred during active session) - R9C (...)`
- After first agent session closes (user types `/exit`), a **second agent session** opens automatically
  with the deferred review prompt listing the R9C failure.

#### Verify

Check `oncall_watcher.log`:
```
SKIPPED (deferred - occurred during active session) - R9C ...
Saved 1 deferred failure(s) to pending_events.json
Deferred review session invoked for 1 failure(s).
```

Second Claude session opens and presents the deferred failure list.

---

### OC-004 — Stale Lock Cleanup

**Purpose**: Validate that a crashed agent session does not permanently block new events.

#### Steps

1. Manually create a lock file with a nonexistent PID:
```bash
echo "999999" > /home/mcp/mcp-project/oncall.lock
```

2. Restart the watcher:
```bash
python3 oncall_watcher.py
```

#### Expected behavior

Watcher startup log shows:
```
[Watcher] ... Watcher started. Monitoring ...
```
No error about locked state. The stale lock was removed automatically.

3. Inject an SLA event — watcher should invoke the agent normally.

---

## Watcher Behavior Validation

These checks can be done without breaking lab config.

### WB-001 — Non-SLA Events Are Ignored

Inject a syslog message that is NOT an SLA Down event:
```bash
echo '{"ts":"2026-01-01T00:00:00Z","device":"172.20.20.201","msg":"%SYS-5-CONFIG_I: Configured from console"}' >> /var/log/network.json
```
Expected: Watcher does **not** invoke agent. Log shows no new `Agent invoked` entry.

### WB-002 — SLA Up Events Are Ignored

```bash
echo '{"ts":"2026-01-01T00:00:00Z","device":"172.20.20.204","msg":"%TRACK-6-STATE: 1 ip sla 1 reachability Down -> Up"}' >> /var/log/network.json
```
Expected: No agent invocation. (Only `Down` transitions trigger.)

### WB-003 — MikroTik Netwatch Event Detected

```bash
echo '{"ts":"2026-01-01T00:00:00Z","device":"172.20.20.218","msg":"netwatch,info event down [ type: simple, host: 10.0.0.1 ]"}' >> /var/log/network.json
```
Expected: Watcher **does** invoke agent (MikroTik format matched).

---

## Case Documentation Checks

After any Standalone or On-Call test run:

1. **New case added**:
```bash
grep "📄 CASE NO." /home/mcp/mcp-project/cases/cases.md | tail -5
```

2. **Case contains required fields**:
   - `Device:` (affected device name)
   - `Reported Issue:`
   - `Verification: PASSED`
   - `Case Status: FIXED`

3. **Lessons curated** (optional, check if lessons.md was updated):
```bash
cat /home/mcp/mcp-project/cases/lessons.md
```

---

## Maintenance Window Policy

The agent must refuse config pushes outside the maintenance window defined in
`policy/MAINTENANCE.json` (UTC Mon–Fri 06:00–18:00).

### MW-001 — Change Blocked Outside Window

To test this, temporarily edit the maintenance window to exclude the current time
(or run this test after 18:00 UTC on a weekday / any time on weekend).

Apply a break, submit a Standalone prompt, and confirm:
- Agent diagnoses the issue correctly
- Agent proposes the fix
- When user approves, `push_config` returns an error about maintenance window
- Agent reports the block to the user without retrying

**Do not modify `MAINTENANCE.json` permanently** — restore after testing.

---

## Regression Checklist

Run this checklist after any significant change to `MCPServer.py`, `oncall_watcher.py`,
`platforms/platform_map.py`, or any skill file:

| # | Check | Method |
|---|-------|--------|
| 1 | Unit tests pass | `./run_tests.sh unit` |
| 2 | Integration tests pass | `./run_tests.sh integration` |
| 3 | OSPF adjacency diagnosis works | ST-001 |
| 4 | EIGRP passive-interface diagnosis works | ST-002 |
| 5 | Redistribution diagnosis works | ST-003 |
| 6 | On-Call watcher detects SLA Down | WB-001 / WB-002 |
| 7 | On-Call agent invoked and diagnoses correctly | OC-001 or OC-002 |
| 8 | Case documented in cases.md | Post-test check |
| 9 | Deferred events handled | OC-003 (if relevant) |
| 10 | Stale lock cleaned up at startup | OC-004 |
| 11 | EIGRP stub/summary diagnosis works | ST-006 |
| 12 | EIGRP redistribution metric diagnosis works | ST-007 |
