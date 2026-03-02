# Routing & Path Selection Skill

> **This is a template file.** Copy it to `SKILL.md` and replace the placeholder content
> with your network-specific path selection and routing policy decision tree.
> The real `SKILL.md` is gitignored — this example shows the expected structure.

---

## PREREQUISITE

Before investigating path selection or routing policy, verify:
1. `get_interfaces(device)` — all relevant interfaces are Up/Up
2. `get_<protocol>(device, "neighbors")` — protocol adjacencies are healthy

If any interface is down or any neighbor is missing → fix that first.
Path selection issues cannot be the root cause if basic adjacency prerequisites are missing.

---

## Symptom: Traffic Following Unexpected Path

### Investigation Flow

1. **Run traceroute** to identify the actual path taken
   - `traceroute(source_device, destination_ip)`

2. **Check the routing table** on the forwarding device
   - `get_routing(device, destination_prefix)`
   - What is the installed next-hop? What protocol installed it?

3. **Check for Policy-Based Routing (PBR)**
   - `get_routing_policies(device, "policy_based_routing")`
   - Is a route-map applied to the ingress interface?

4. **Check route-maps**
   - `get_routing_policies(device, "route_maps")`
   - Does any route-map force a specific next-hop?

5. **Check access-lists** used by the route-map
   - `get_routing_policies(device, "access_lists")`

*Add environment-specific path selection checks here.*

---

## Symptom: Route Filtered / Missing

### Investigation Flow

1. `get_routing(device, prefix)` — confirm route is absent
2. `get_routing_policies(device, "prefix_lists")` — check inbound/outbound filters
3. `get_routing_policies(device, "route_maps")` — check distribute-list or route-map
4. Check administrative distance if multiple protocols compete for the same prefix

---

## Symptom: NAT/PAT Not Working

> Use `nat_pat` query only on NAT_EDGE devices after ruling out routing issues.

1. `get_routing_policies(device, "nat_pat")` — check translation rules
2. `run_show(device, "show ip nat statistics")` — check hit counters

---

## Fix Guidance

- Fix the device that has incorrect or missing policy config.
- Always ask user approval before applying `push_config`.
- Verify with traceroute that traffic now follows the expected path.
