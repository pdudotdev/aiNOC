---
name: BGP Troubleshooting
description: "BGP session state, missing routes, prefix policy, default-originate, next-hop-self, route reflector — decision trees and checklists"
---

# BGP Troubleshooting Skill

## Scope
BGP session state, missing routes, prefix policy, default-originate, next-hop-self, route reflector.
Covers: AS1010 (R2C, R3C), AS2020 (R18M, R19M), AS4040 (R12C=RR, R13C, R14C, R15C), AS5050 (R16C, R17C).

## Start Here: Session State

When a BGP neighbor is not Established:

```
get_bgp(device, "summary")
```

| State | Root Cause | Fix |
|-------|-----------|-----|
| Established + count | Healthy | — |
| Idle | TCP failing or admin shutdown | Check reachability, check `neighbor X shutdown` |
| Active | TCP SYN sent, no reply | Check ACL on TCP 179, check update-source, ebgp-multihop for non-direct eBGP |
| Connect | TCP in progress | Reachability issue |
| OpenSent | OPEN sent, waiting reply | Usually transient, else hold-timer mismatch |
| Idle (Admin) | `neighbor X shutdown` configured | Remove shutdown |

### Session Checklist

- **eBGP-specific**: neighbor must be directly connected (or `ebgp-multihop N` for non-direct).
- **Check update-source**: iBGP uses Loopback by default in this topology.
- **Verify reachability**: ping the neighbor IP from the device's configured source address.

---

## Symptom: Missing Routes

When a route should be in the BGP table but isn't:

```
get_bgp(device, "table")
get_bgp(device, "config")
```

### Route Presence Checklist

1. **Route in BGP table?** (`>` = best, `*` = valid, ` ` = not valid)
2. **Next-hop reachable?** (iBGP: next-hop-self needed if next-hop is external IP unknown to iBGP peer)
3. **Outbound prefix-list / route-map blocking advertisement?**
4. **`network` statement matching exact route in RIB?** (must be exact — not aggregate unless configured)
5. **`redistribute` configured?** Check metric-type and route-map filters
6. **Route in RIB but not in BGP?** → next-hop unreachable, route not valid

---

## Symptom: Default Route Missing

When ISP should be sending default but it's missing:

```
get_bgp(device, "table")    → look for 0.0.0.0/0 with a valid best path (>)
get_bgp(device, "summary")  → confirm session to ISP peer is Established
```

### Diagnosis

- **Default missing**: ISP may have `default-originate` only conditionally (e.g., `default-originate route-map`) — check ISP config
- **ISP policy**: ISPs in this topology filter customer-advertised defaults inbound (they send but don't accept)
- **Peer IPs**: Get ISP peer IPs from `INTENT.json` → each edge router has different ISP-facing IPs

---

## Symptom: iBGP Routes Not Propagating (Route Reflector)

When iBGP routes are missing on a peer:

```
get_bgp(device, "summary")    → verify iBGP session to RR is Established
get_bgp(rr_device, "config")  → verify peer has route-reflector-client configured
get_bgp(device, "table")      → check if route exists but isn't best path
```

### RR Checklist

- **iBGP routes not propagating** → confirm RR has `neighbor X route-reflector-client` for all clients
- **Next-hop still set to originator's IP (not RR)** → client needs `next-hop-self` or IGP must reach originator
- **Check RR cluster-id** if multiple RRs exist — mismatched cluster-id causes route drops

---

## Symptom: Wrong Best Path Selected

When a route exists but the wrong next-hop is being used:

```
get_bgp(device, "table")      → see all paths for a prefix
get_bgp(device, "config")     → check for weight, local-pref, or AS-path manipulation
```

### Best Path Selection (11-attribute order)

1. Highest Weight (Cisco-local, not advertised)
2. Highest Local Preference (iBGP, default 100)
3. Locally originated (network/redistribute/aggregate)
4. Shortest AS-path
5. Lowest Origin (IGP < EGP < Incomplete)
6. Lowest MED (same AS neighbor only)
7. eBGP over iBGP
8. Lowest IGP metric to next-hop
9. Oldest eBGP route
10. Lowest BGP Router ID
11. Lowest neighbor IP

---

## Verification Checklist (Post-Fix)

- [ ] `get_bgp(device, "summary")` shows all neighbors as Established
- [ ] `get_bgp(device, "table")` shows expected prefixes with `>` (best path)
- [ ] Default route `0.0.0.0/0` present from all ISP peers on each customer edge router (R2C, R3C, R18M, R19M)
- [ ] `get_routing(device)` shows BGP default route in RIB
