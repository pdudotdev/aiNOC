---
name: On-Call SLA Troubleshooting
description: "SLA path failure workflow — read sla_paths.json, traceroute-first localization, ECMP handling, protocol triage"
---

# On-Call SLA Troubleshooting Skill

## Scope
On-Call mode investigation guide — reading sla_paths.json, traceroute-first localization, ECMP handling, protocol triage order.

---

## Step 0: Read the sla_paths.json Entry for the Failed Path

Use the **Read** tool to read the file `sla_paths/paths.json` (this is a local file — do NOT use `readMcpResource`).

Locate the path entry matching the source device from the log event. Extract these key fields:

- **`source_device`**: the device that generated the SLA failure event
- **`destination_ip`**: IP being pinged by the SLA
- **`scope_devices`**: ALL devices you may need to investigate
- **`ecmp`**: if true, TWO paths exist — both must be checked
- **`ecmp_node`**: the device where the path splits
- **`ecmp_next_hops`**: the two next-hop devices after the split

---

## Step 1: Traceroute from Source Device (Always First)

If `source_ip` is available in the paths.json entry, always pass it:

```
traceroute(device=<source_device>, destination=<destination_ip>, source=<source_ip>)
```

Using `source_ip` forces the traceroute onto the monitored path. If the source interface is down, the traceroute fails immediately at R10C — correctly localizing the issue without alternate-path confusion.

Read the output:

- **Path stops at hop N (or fails at source)**: issue is on or before that hop → proceed to Step 3
- **Timeout at first hop**: issue is on the source device itself (interface down, EIGRP/OSPF neighbor lost, no default route) → proceed to Step 3
- **Full path to destination**: do NOT conclude "transient" yet — go to Step 1a

### Step 1a: Source-Device Sanity Check (when traceroute succeeds)

Even if the traceroute completes, the SLA was triggered for a reason. Verify the source device's local state with exactly two queries:

```
get_interfaces(device=<source_device>)
get_ospf(device=<source_device>, query="neighbors")   ← run on source_device, NOT the next-hop
```

> **Critical**: Always query routing protocol neighbors on the **source_device** first. Querying the next-hop device may show healthy adjacencies even when the source-side interface is down.

**Branch A — Appears Recovered** (source interface Up/Up AND all expected neighbors present):

Present this summary table and ask the user before doing anything else:

```
| Check | Result | Status |
|-------|--------|--------|
| Traceroute to <destination_ip> | Full path, all hops respond | ✓ |
| Source interface (<source_interface>) | Up/Up | ✓ |
| Routing protocol neighbors on <source_device> | All expected neighbors present | ✓ |

The SLA path appears to have recovered. Likely cause: transient condition
(brief routing instability, probe timing) now resolved.

What would you like to do?
  A) Document as resolved (transient/recovered) and close the case
  B) Run deeper diagnostics (interface error counters, neighbor state history)
  C) Return to the deferred SLA list / exit without investigating further
```

- If user picks **A**: document the case (mark as FIXED - transient/recovered), curate lessons.md, then proceed to session closure.
- If user picks **B**: proceed to Step 3 (read the relevant protocol skill and investigate deeper).
- If user picks **C**: proceed to session closure without documentation (the event was transient and self-resolved).
- **Do NOT proceed to Step 3 without the user explicitly requesting it** — unnecessary investigation wastes time and cost.

**Branch B — Issue still present** (source interface down OR expected neighbor missing):

This is the root cause. Proceed directly to Step 3.

---

## Step 2: ECMP Handling

If `ecmp=true`, the traceroute shows ONE of the two paths. The other path may also be broken.

After fixing one path, verify the ECMP node still has both paths:

```
get_routing(ecmp_node, prefix=<destination or next_hop>)   → expect 2 equal-cost entries
```

---

## Step 3: Protocol Triage — Which Skill to Read Next

Map the breaking hop to its protocol:

| Breaking Hop Device | Protocol to Investigate | Skill to Read |
|--------------------|------------------------|---------------|
| R9C (source) | EIGRP AS20 (to R8C) | `skills/eigrp/SKILL.md` |
| R8C | EIGRP AS20 neighbor + OSPF Area1 + bidirectional redistribution | `skills/eigrp/SKILL.md`, `skills/ospf/SKILL.md`, and if redistributed routes are missing: `skills/redistribution/SKILL.md` |
| R6A, R7A | OSPF Area1 NSSA | `skills/ospf/SKILL.md` |
| R4C, R5C (source) | EIGRP AS10 (to R3C) | `skills/eigrp/SKILL.md` |
| R3C | OSPF Area0 / EIGRP AS10 / Redistribution / BGP | Traceroute direction matters: inbound from R4C/R5C side → `skills/eigrp/SKILL.md`; outbound toward R1A/R2C → `skills/ospf/SKILL.md`; toward ISP → `skills/bgp/SKILL.md`; redistributed routes missing → `skills/redistribution/SKILL.md` |
| R2C | OSPF Area0 (to R1A/R3C) / OSPF ABR Area1 NSSA (to R6A/R7A) / BGP | If OSPF neighbors down → `skills/ospf/SKILL.md`; if BGP to ISP down → `skills/bgp/SKILL.md`. Note: R2C has no EIGRP. |
| R1A | OSPF ABR (Areas 0↔2) | `skills/ospf/SKILL.md` |
| R10C, R11C (as source or breaking hop) | OSPF Area2 stub (adjacency to R1A, default route from ABR) | `skills/ospf/SKILL.md` |
| R12C (ISP A edge / RR) | BGP | `skills/bgp/SKILL.md` |
| R13C, R14C, R15C (ISP A transit/core) | Outside our admin domain — not in scope_devices for any SLA path. If traceroute transits through them and stops, verify eBGP session to R12C and escalate to ISP A. | `skills/bgp/SKILL.md` (eBGP to R12C only) |
| R16C, R17C (ISP B edge) | BGP | `skills/bgp/SKILL.md` |
| R18M, R19M (source) | OSPF Area0 (London) / BGP | `skills/ospf/SKILL.md` or `skills/bgp/SKILL.md` |

---

## Time Efficiency Rules

- **Localize first, don't investigate all**: traceroute narrows to 1-2 devices max before running protocol tools
- **ECMP: check both paths** before concluding the issue is fixed
- **Don't re-check devices that are not on the scope_devices list**: out-of-scope devices won't affect this SLA path

---

## Presenting Findings

Always present your analysis summary in a Markdown table before proposing a fix:

| Finding | Detail | Status |
|---------|--------|--------|
| Traceroute result | Stopped at hop N — device X | ✗ |
| Interface / neighbor state | e.g. Ethernet3 admin down | ✗ |
| Root cause | Brief description | ✗ |

Use ✓ for healthy items and ✗ for the identified issues. This lets the user scan the summary instantly before approving any configuration change.
