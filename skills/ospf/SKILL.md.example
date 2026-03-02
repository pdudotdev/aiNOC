# OSPF Troubleshooting Skill

> **This is a template file.** Copy it to `SKILL.md` and replace the placeholder content
> with your network-specific OSPF troubleshooting decision tree.
> The real `SKILL.md` is gitignored — this example shows the expected structure.

---

## PREREQUISITE

Before reading this skill, verify:
1. `get_interfaces(device)` — all relevant interfaces are Up/Up
2. `get_ospf(device, "neighbors")` — expected neighbors are present and FULL

If any interface is down → root cause found, stop here.
If neighbors are missing → go directly to the **Adjacency Checklist** below.
Only proceed to deeper sections if basics are healthy.

---

## Symptom: No OSPF Neighbors / Adjacency Down

### Adjacency Checklist

Check in this order. Stop when you find a mismatch.

1. **Interface state** — `get_interfaces(device)`
   - Is the interface admin-up and line-protocol up?

2. **Hello/Dead interval** — `get_ospf(device, "interfaces")`
   - Do both sides have matching hello and dead intervals?
   - Default: hello 10s / dead 40s (IOS, EOS); hello 10s / dead 40s (RouterOS)

3. **Area number** — `get_ospf(device, "config")`
   - Are both sides configured in the same OSPF area?

4. **Network type** — `get_ospf(device, "interfaces")`
   - Do both sides agree on the network type (point-to-point, broadcast, etc.)?

5. **Authentication** — `get_ospf(device, "config")`
   - Is authentication configured consistently on both sides?

6. **Passive interface** — `get_ospf(device, "config")`
   - Is the interface accidentally set to passive?

*Add additional checks specific to your environment.*

---

## Symptom: Missing Routes / Incomplete LSDB

*Add your LSDB investigation steps here.*

### Checklist

1. `get_ospf(device, "database")` — check for missing LSAs
2. Check ABR configuration for area filtering
3. Check route summarization and filtering at ABRs

---

## Symptom: External Routes Missing (Type 5 / Type 7)

*Add your redistribution and NSSA investigation steps here.*

### Checklist

1. Verify ASBR redistribution configuration
2. Check NSSA area type configuration on all ABRs
3. Verify route-map and metric settings for redistributed routes

---

## Fix Guidance

- **Fix mismatches at the source**: identify which device deviates from the standard config and fix that device.
- **Never change a correctly-configured peer** to match a misconfigured outlier.
- Always ask user approval before applying `push_config`.
- Verify the fix with the same tool that identified the problem.
