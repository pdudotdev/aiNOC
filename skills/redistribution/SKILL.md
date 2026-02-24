---
name: Redistribution Troubleshooting
description: "Cross-protocol redistribution (OSPF↔EIGRP) — seed metrics, subnets keyword, loop risk, route-map filtering"
---

# Redistribution Troubleshooting Skill

## Scope
Cross-protocol redistribution troubleshooting at the two redistribution points: R3C (EIGRP AS10 ↔ OSPF bidirectional, route-map filtered) and R8C (EIGRP AS20 ↔ OSPF Area 1 bidirectional).

## Redistribution Points in This Network

| Device | Direction | Notes |
|--------|-----------|-------|
| R3C | EIGRP AS10 ↔ OSPF (bidirectional) | Both ways: EIGRP→OSPF and OSPF→EIGRP (filtered via route-map). R4C/R5C use static default routes pointing to R3C as return path. Loop risk — mitigated by route-map on the OSPF→EIGRP redistribute statement. |
| R8C | EIGRP AS20 ↔ OSPF Area1 (bidirectional) | OSPF routes redistributed into EIGRP AS20 for R9C reachability. Loop risk — mitigated by a route-map on the redistribute statement. |

---

## Symptom: Missing Redistributed Routes

When routes should appear after redistribution but don't:

```
get_routing_policies(device, "redistribution")   → active redistribution statements
get_ospf(device, "database")                      → check for Type 5/7 LSAs on ASBR
get_eigrp(device, "topology")                     → check for redistributed routes (D EX entries)
```

### Common Failures

1. **No seed metric (EIGRP)** → EIGRP silently drops routes with infinite metric
   - Fix: add `metric <bw> <delay> <reliability> <load> <mtu>` to the redistribute statement

2. **Missing `subnets` keyword (OSPF)** → `redistribute eigrp X` without `subnets` drops all classless subnets
   - Fix: add `subnets` keyword

3. **Route-map filtering** → redistribution may use a route-map that filters routes
   - Check with `get_routing_policies(device, "route_maps")`

4. **Metric-type E2 vs E1** → E2 (default) = fixed external cost from ASBR; E1 = cumulative (internal + external)
   - Check which is configured: `get_ospf(device, "config")`

---

## Symptom: Routing Loop Risk (Bidirectional Redistribution)

When a device redistributes in both directions (OSPF↔EIGRP), routes learned from one protocol can be re-injected back, creating a loop.

```
get_routing_policies(device, "redistribution")   → check for route-map on the redistribute statement
get_routing_policies(device, "route_maps")       → verify the route-map logic filters appropriately
```

### Loop Prevention Analysis

- **AD protection**: OSPF internal/IA (AD 110) beats EIGRP external (AD 170), so re-injected EIGRP external routes won't displace OSPF routes. But always verify with `get_routing(device)` that best paths are correct.
- **Route-map filtering**: the most reliable prevention — route-map on the redistribute statement ensures only intended routes are advertised in each direction.

---

## Verification Checklist (Post-Fix)

- [ ] `get_ospf(asbr_device, "database")` shows Type 5 or Type 7 LSAs for redistributed routes
- [ ] `get_eigrp(receiving_device, "topology")` shows redistributed routes as D EX (external)
- [ ] `get_routing(device)` shows redistributed prefixes with expected next-hops
- [ ] No routing loops: verify EIGRP external routes are not displacing OSPF routes on the redistributing device
