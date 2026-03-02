# BGP Troubleshooting Skill

> **This is a template file.** Copy it to `SKILL.md` and replace the placeholder content
> with your network-specific BGP troubleshooting decision tree.
> The real `SKILL.md` is gitignored — this example shows the expected structure.

---

## PREREQUISITE

Before reading this skill, verify:
1. `get_interfaces(device)` — all relevant interfaces are Up/Up
2. `get_bgp(device, "summary")` — expected BGP sessions are in Established state

If any interface is down → root cause found, stop here.
If sessions are down (Idle/Active) → go directly to the **Session Checklist** below.
Only proceed to deeper sections if basics are healthy.

---

## Symptom: BGP Session Down (Idle / Active)

### Session Checklist

Check in this order. Stop when you find a mismatch.

1. **Interface / reachability** — `ping(device, neighbor_ip)`
   - Can the device reach the BGP neighbor IP?

2. **Neighbor configuration** — `get_bgp(device, "config")`
   - Is the correct neighbor IP and AS number configured?

3. **Timers** — `get_bgp(device, "config")`
   - Are keepalive/hold-time timers compatible between peers?
   - Default: keepalive 60s / hold-time 180s

4. **Authentication** — `get_bgp(device, "config")`
   - Is MD5 authentication configured consistently?

5. **Update-source** — `get_bgp(device, "config")`
   - Is the correct source interface configured for the session?

*Add additional checks specific to your environment.*

---

## Symptom: Routes Not Received / Prefixes Missing

*Add your BGP table investigation steps here.*

### Checklist

1. `get_bgp(device, "table")` — check for expected prefixes and path attributes
2. Check inbound route-maps and prefix-lists: `get_routing_policies(device, "route_maps")`
3. Verify next-hop reachability for received prefixes

---

## Symptom: Routes Not Advertised to Peer

*Add your outbound policy investigation steps here.*

### Checklist

1. Check outbound route-maps and prefix-lists
2. Verify network statements or redistribution into BGP
3. Check next-hop-self configuration for iBGP

---

## Fix Guidance

- Fix mismatches at the device that deviates from standard config.
- Always ask user approval before applying `push_config`.
- Verify the fix with `get_bgp(device, "summary")` confirming Established state.
