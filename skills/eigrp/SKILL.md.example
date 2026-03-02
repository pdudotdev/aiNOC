# EIGRP Troubleshooting Skill

> **This is a template file.** Copy it to `SKILL.md` and replace the placeholder content
> with your network-specific EIGRP troubleshooting decision tree.
> The real `SKILL.md` is gitignored — this example shows the expected structure.

---

## PREREQUISITE

Before reading this skill, verify:
1. `get_interfaces(device)` — all relevant interfaces are Up/Up
2. `get_eigrp(device, "neighbors")` — expected neighbors are present

If any interface is down → root cause found, stop here.
If neighbors are missing → go directly to the **Neighbor Checklist** below.
Only proceed to deeper sections if basics are healthy.

> Note: EIGRP is supported only on IOS devices in this environment.

---

## Symptom: No EIGRP Neighbors

### Neighbor Checklist

Check in this order. Stop when you find a mismatch.

1. **Interface state** — `get_interfaces(device)`
   - Is the interface admin-up and line-protocol up?

2. **AS number** — `get_eigrp(device, "config")`
   - Are both sides in the same EIGRP AS?

3. **Passive interface** — `get_eigrp(device, "config")`
   - Is the interface accidentally set to passive?

4. **Authentication** — `get_eigrp(device, "config")`
   - Is MD5 authentication configured consistently?

5. **Network statement** — `get_eigrp(device, "config")`
   - Does the network statement include the interface subnet?

*Add additional checks specific to your environment.*

---

## Symptom: Routes Missing from Topology Table

*Add your topology investigation steps here.*

### Checklist

1. `get_eigrp(device, "topology")` — check feasible successors
2. Verify stub configuration if device is an EIGRP stub
3. Check summary-address configuration

---

## Symptom: Wrong Path Selected (Metric Issue)

*Add your metric and path selection investigation steps here.*

### Checklist

1. Compare composite metrics (bandwidth, delay) on each path
2. Check variance configuration for unequal-cost load balancing
3. Verify K-values match on all routers

---

## Fix Guidance

- Fix mismatches at the device that deviates from standard config.
- Always ask user approval before applying `push_config`.
- Verify the fix with the same tool that identified the problem.
