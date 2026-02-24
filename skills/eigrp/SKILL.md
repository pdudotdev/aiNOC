---
name: EIGRP Troubleshooting
description: "EIGRP neighbor issues, topology/DUAL, stub configuration, redistribution metrics, MD5 auth — symptom-first methodology"
---

# EIGRP Troubleshooting Skill

## Scope
EIGRP neighbor issues, topology/DUAL, stub configuration, redistribution metrics, MD5 auth.
Covers EIGRP AS10 (R3C, R4C, R5C) and EIGRP AS20 (R8C, R9C).

## Start Here: Neighbor State

When an EIGRP neighbor is missing or unhealthy:

```
get_eigrp(device, "neighbors")
```

| Symptom | Root Cause |
|---------|-----------|
| Q count ≠ 0 | Stuck retransmission queue → congestion, MTU mismatch, or unidirectional link |
| Hold timer expires | Hellos not received → interface issue, auth mismatch, or K-value mismatch |
| No neighbor at all | Interface not in `network` statement, passive interface, auth failure, or AS mismatch |

### Neighbor Checklist
Run `get_eigrp(device, "config")` to verify:

1. **`network` statement covers the interface subnet?**
2. **K-values match on both ends?** (default: K1+K3 only — bandwidth and delay)
3. **Auth: key-chain name, key-id, and key-string match?**
4. **AS number identical on both sides?**
5. **Interface passive?** (`passive-interface` suppresses hellos)

---

## Symptom: Missing Routes (Topology Table)

When an expected route is missing from the topology table:

```
get_eigrp(device, "topology")
```

- **Passive (P)** = Stable. Successor (and possibly feasible successor) installed.
- **Active (A)** = DUAL reconverging. If stuck in Active (SIA): a neighbor is not responding to QUERY — check upstream neighbor connectivity and stub config.

### Feasibility Condition
Reported Distance (RD) < Feasible Distance (FD). If no route meets FC, no feasible successor → route goes Active on next failure.

---

## Symptom: Stub Configuration Issues

Stub routers limit what they advertise and do NOT respond to QUERYs — important for SIA prevention:

- `stub connected`: advertises only connected routes
- `stub summary`: advertises only summary routes
- `stub connected summary` (both): connected + summaries only
- Wrong stub variant = routes missing upstream

Check actual config with `get_eigrp(device, "config")`. Note: `eigrp stub` with no keywords defaults to `connected summary`.

---

## Symptom: Redistribution Routes Missing

When redistributed routes are missing from the EIGRP topology table:

```
get_eigrp(device, "topology")   → look for D EX (external) entries
get_eigrp(device, "config")     → check redistribute statement and metric
```

### Common Failures

1. **No seed metric** → EIGRP silently drops routes with infinite metric.
   - Fix: add `metric <bw> <delay> <reliability> <load> <mtu>` to the redistribute statement.

2. **Missing `subnets`** (OSPF side) → `redistribute eigrp X` without `subnets` drops all classless subnets.
   - Fix: add `subnets` keyword.

---

## Symptom: Summarization Issues

When an expected summary is missing and individual routes appear instead:

```
get_eigrp(device, "interfaces")    → check if summary-address is configured per interface
get_eigrp(device, "topology")      → individual routes present means summary not configured
```

Fix: `ip summary-address eigrp <AS> <network> <mask>` on the outbound interface.

---

## Verification Checklist (Post-Fix)

- [ ] `get_eigrp(device, "neighbors")` shows all expected neighbors with Q=0
- [ ] `get_eigrp(device, "topology")` shows all routes as Passive (P)
- [ ] `get_routing(device)` shows expected prefixes with correct EIGRP metrics
- [ ] No routes in Active (A) state — stuck Active = SIA risk
