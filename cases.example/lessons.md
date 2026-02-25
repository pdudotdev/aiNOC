# Top Lessons Learned

Curated from resolved cases. Agent updates this file after each case closure.
Read this file at session start — it replaces reading the full cases/cases.md.
For detailed case history, read cases/cases.md directly.

Maximum 10 entries. Each entry: one actionable lesson in 1-2 lines.

### Promotion Criteria
A lesson belongs here if it: (1) applies broadly to future cases, (2) corrects a methodology mistake, and (3) isn't already captured above.

---

1. **Source-first on SLA failure**: When an SLA path fails, always run `get_interfaces(source_device)` immediately. A shutdown `source_interface` (from paths.json) is immediately identifiable and is the root cause — do not escalate to protocol-level investigation until source device interfaces are confirmed Up/Up.

2. **Always pass `source_ip` in traceroute for SLA paths**: Without a source IP, traceroute may succeed via an alternate path and mask the actual monitored-path failure. Always use `traceroute(source_device, destination_ip, source=source_ip)` when `source_ip` is defined in paths.json.

3. **ABR misconfiguration breaks inter-area routes**: When inter-area routes are missing despite LSAs present in LSDB, verify ABR's interface-to-area mappings via `get_ospf(abr_device, "interfaces")`. Incorrect area assignments prevent adjacencies and route propagation — a common multi-area OSPF root cause.

4. **LSDB vs RIB mismatch → adjacency or config issue**: If LSAs present in database but routes missing from RIB, root cause is OSPF adjacency failure or config error, not LSA flooding. Check neighbor states before investigating SPF calculations.

5. **Default route missing in stub area = broken ABR backbone adjacency**: Stub area leaf devices rely on ABR to originate default route. If default route is absent despite healthy OSPF neighbor to ABR, the ABR has broken inter-area adjacencies (area misconfiguration or backbone connectivity issue). Verify ABR's Area 0 neighbors immediately — zero neighbors on Area 0 interfaces indicates area assignment error.

6. **OSPF timer mismatch is a silent killer in multi-vendor networks**: Mismatched hello/dead intervals between OSPF neighbors prevent adjacency formation despite physical connectivity and layer 3 reachability working correctly. With mixed vendors (Arista EOS vs Cisco IOS), explicit timer alignment is critical — Arista defaults to hello 33, Cisco to hello 10. Zero neighbors on a healthy up/up interface with layer 3 connectivity = suspect timer mismatch; inspect `get_ospf(device, "interfaces")` hello/dead intervals on both sides.

7. **ABR is a critical single point of failure for multi-area networks**: When an ABR lacks backbone adjacencies (Area 0), all downstream areas lose inter-area routes and external routes simultaneously. A single misconfigured or broken ABR cascades failures across multiple SLA paths and leaf devices. Monitor ABR state aggressively; ABR backbone adjacencies are prerequisites for all stub/NSSA area functionality.

8. **Stale LSA age in LSDB indicates broken originating router adjacencies**: When Type 3 or Router LSAs appear in the LSDB with age 1500+ seconds (25+ minutes) and remain stale (not incrementing toward max-age or refreshing), the originating router (especially ABR) likely has broken inter-area adjacencies preventing proper LSA refresh. This pattern indicates ABR connectivity failure rather than LSDB flooding issues. Compare LSA age across neighbors; identical ages across multiple neighbors suggests stale advertisement from source.

9. **OSPF passive-interface silently blocks adjacencies**: Passive-interface prevents hello/hello exchange but leaves the physical link and layer 3 connectivity appearing healthy. Result: interface up/up, layer 3 reachable, but neighbor count zero. Always inspect `get_ospf(device, "interfaces")` for `passive` flag when neighbors are absent despite correct parameters (timers, area, auth, network type). This is especially critical on ABRs where passive Area N interfaces prevent inter-area route propagation.

10. **Redistribution point interface shutdown silently breaks downstream protocol propagation**: When a router redistributes routes between two IGPs (e.g., OSPF → EIGRP), administratively shutdown interfaces on the source-protocol side prevent routes from being redistributed to the downstream protocol. On ECMP split points where redistribution happens, shutdown of both branches completely isolates downstream EIGRP speakers from OSPF-domain routes. Root cause: get_neighbors on upstream protocol returns expected peers, but destination-protocol neighbors receive no external routes. Always verify interface status on ALL redistribution-facing interfaces when downstream protocol neighbors report zero external routes.
