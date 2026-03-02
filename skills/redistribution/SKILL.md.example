# Redistribution Troubleshooting Skill

> **This is a template file.** Copy it to `SKILL.md` and replace the placeholder content
> with your network-specific redistribution troubleshooting decision tree.
> The real `SKILL.md` is gitignored — this example shows the expected structure.

---

## PREREQUISITE

Before reading this skill, verify:
1. `get_interfaces(device)` — all relevant interfaces are Up/Up
2. `get_ospf(device, "neighbors")` — OSPF adjacencies are healthy (if applicable)
3. `get_eigrp(device, "neighbors")` — EIGRP adjacencies are healthy (if applicable)

If any interface is down or any adjacency is missing → fix that first.
Redistribution issues cannot be the root cause if basic protocol prerequisites are missing.

---

## Symptom: Redistributed Routes Missing

### Investigation Flow

1. **Identify the redistribution point** — check `intent/INTENT.json` for ASBR/redistributor roles

2. **Check the redistribution config** — `get_routing_policies(device, "redistribution")`
   - Is redistribution configured in the correct direction?
   - Is the correct route-map or metric applied?

3. **Check the route-map** — `get_routing_policies(device, "route_maps")`
   - Does the route-map permit the expected prefixes?
   - Are match conditions (prefix-list, tag, metric) correctly defined?

4. **Check the prefix-list** — `get_routing_policies(device, "prefix_lists")`
   - Does the prefix-list include the expected subnets?

5. **Verify routes exist in the source protocol** — `get_routing(device, prefix)`
   - Are the routes present in the source routing table before redistribution?

*Add environment-specific redistribution points and checks here.*

---

## Symptom: Routing Loops from Bidirectional Redistribution

*Add your loop prevention investigation steps here.*

### Checklist

1. Check route tagging on redistributed routes
2. Verify deny rules in route-maps block re-redistributed routes
3. Check administrative distance settings

---

## Fix Guidance

- Fix the redistribution point that has incorrect or missing config.
- Always ask user approval before applying `push_config`.
- Verify: `get_routing(downstream_device, affected_prefix)` confirms route is now present.
