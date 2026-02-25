📄 CASE NO. - 00001-R10C-SLA
Date: 2026-02-24 06:53 UTC
Device(s): R10C

🔹 Reported Issue:
  - IP SLA path 1 on R10C (R10C_TO_R16C) transitioned from Up to Down
  - SLA monitoring: R10C (172.16.0.6) to R16C (200.50.50.6)

🔹 All Commands Used To Isolate Issue:
  - traceroute (R10C to 200.50.50.6, source 172.16.0.6) → FAILED: "Invalid source address"
  - get_interfaces (R10C)
  - get_ospf neighbors (R10C)

🔹 Commands That Actually Identified the Issue:
  - get_interfaces (R10C) → revealed Ethernet0/1 is administratively down

🔹 Proposed Fixes (Per Device):
  - Enable interface Ethernet0/1 on R10C (no shutdown)

🔹 Commands Used Upon User Approval:
  interface Ethernet0/1
   no shutdown

🔹 Post-Fix State:
  - Ethernet0/1 (172.16.0.6): UP/UP
  - Traceroute: successful to 200.50.50.6 via R1A → ECMP (R2C/R3C) → R16C
  - SLA path restored

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Read sla_paths.json → identified R10C_TO_R16C path
  - [x] Step 1: traceroute from R10C to 200.50.50.6 → failed at source
  - [x] Step 1a: sanity check on source device → found Ethernet0/1 administratively down
  - [x] Identify root cause → interface shutdown on SLA source path
  - [x] Apply fix → enable interface
  - [x] Verify fix → traceroute succeeds, interface up

🔸 Lessons Learned:
  - SLA path failures due to administratively shutdown interfaces on the source device are immediately identifiable via get_interfaces query on the source device. The source_interface field in paths.json is critical for validation.
  - Traceroute with source IP should be the first troubleshooting step; if it fails at the source, always immediately check source device interface status before drilling into protocol-level issues.
  - The on-call skill Step 1a (source device sanity check) is essential even when traceroute reveals the issue at the source — it confirms the exact interface status.

---

📄 CASE NO. - 00002-R4C-SLA
Date: 2026-02-24 08:15 UTC
Device(s): R1A, R3C, R4C

🔹 Reported Issue:
  - IP SLA path 1 on R4C (R4C_TO_R10C) transitioned from Up to Down
  - SLA monitoring: R4C (192.168.10.2) to R10C (10.10.10.10)

🔹 All Commands Used To Isolate Issue:
  - traceroute (R4C to 10.10.10.10, source 192.168.10.2) → FAILED: timeouts at hop 2, hop 3 returns ISP address with !H
  - get_interfaces (R4C) → all interfaces up/up, source interface Ethernet0/1 healthy
  - get_eigrp neighbors (R4C) → R3C and R5C neighbors up
  - get_interfaces (R3C) → all interfaces up/up
  - get_eigrp neighbors (R3C) → R4C neighbor up
  - get_ospf neighbors (R3C) → R1A neighbor (2.2.2.2) FULL/- on Ethernet1/0
  - get_interfaces (R1A) → Ethernet1-4 all connected/up
  - get_ospf neighbors (R1A) → only Area 2 neighbors (R10C, R11C)
  - run_show ospf interface brief (R1A) → **Ethernet3, Ethernet4 in Area 1, 0 neighbors each**
  - get_routing (R3C, prefix 10.10.10.10) → "Subnet not in table"
  - get_ospf database (R3C) → Type 3 LSAs for 10.10.10.10 and 11.11.11.11 PRESENT in Area 0 LSDB
  - get_routing (R1A) → 10.10.10.10/32 route present via OSPF to R10C

🔹 Commands That Actually Identified the Issue:
  - run_show ospf interface brief (R1A) → revealed Ethernet3 and Ethernet4 incorrectly in Area 1 instead of Area 0
  - get_ospf neighbors (R1A) → confirmed NO adjacencies in Area 0 (0 neighbors on Ethernet3/4)

🔹 Proposed Fixes (Per Device):
  - Reconfigure R1A interfaces Ethernet3 and Ethernet4 from Area 1 to Area 0

🔹 Commands Used Upon User Approval:
  interface Ethernet3
   ip ospf area 0.0.0.0
  interface Ethernet4
   ip ospf area 0.0.0.0

🔹 Post-Fix State:
  - R1A Ethernet3: Area 0.0.0.0, 1 neighbor (R3C FULL)
  - R1A Ethernet4: Area 0.0.0.0, 0 neighbors (no peer on other end)
  - R1A OSPF neighbors: now includes R3C (3.3.3.3) in Area 0
  - R3C routing table: 10.10.10.10/32 now present (inter-area via 10.0.0.5)
  - Traceroute R4C → R10C: succeeds via R3C → R1A → R10C
  - Ping R4C → R10C: 5/5 packets successful, 1-2ms RTT

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Read sla_paths.json → identified R4C_TO_R10C path with scope [R4C, R3C, R1A, R10C]
  - [x] Step 1: traceroute from R4C → fails at hop 2, indicating issue in path to R1A/R10C
  - [x] Step 1a: sanity check on R4C (source device) → all interfaces and EIGRP neighbors healthy
  - [x] Step 3: protocol triage → path goes EIGRP (R4C→R3C) → OSPF Area 0 (R3C→R1A) → OSPF Area 2 (R1A→R10C)
  - [x] Check R3C OSPF state → has neighbor R1A, but NO route to 10.10.10.10
  - [x] Check R1A OSPF state → only Area 2 neighbors, no Area 0 neighbors despite interfaces being up
  - [x] Check R1A OSPF interface config → **Ethernet3/4 in Area 1, not Area 0** (root cause)
  - [x] Apply fix → move Ethernet3/4 to Area 0
  - [x] Verify → R1A-R3C adjacency forms, R3C gets route to 10.10.10.10, traceroute succeeds

🔸 Lessons Learned:
  - **ABR misconfiguration is a common root cause**: R1A is an ABR but its interfaces were in wrong areas, breaking inter-area route propagation. Always verify ABR interface-to-area mappings when inter-area routes are missing.
  - **LSDB vs RIB mismatch indicates SPF calculation issue or config problem**: R3C had Type 3 LSAs in its LSDB but routes didn't appear in RIB. This pointed to OSPF config error (missing adjacency in Area 0) rather than LSA flooding issue.
  - **OSPF neighbor adjacencies must form before route propagation**: The fact that R1A had zero neighbors on Ethernet3/4 immediately ruled out both SPF calculation and LSDB flooding as root causes, narrowing focus to config.
  - **On-Call workflow is highly effective**: Traceroute localization → source sanity check → protocol-specific investigation identified root cause efficiently without random debugging.


---

📄 CASE NO. - 00003-R11C-SLA
Date: 2026-02-24 09:04 UTC
Device(s): R11C, R1A, R2C, R3C

🔹 Reported Issue:
  - IP SLA path 1 on R11C (R11C_TO_R12C) transitioned from Up to Down
  - SLA monitoring: R11C (172.16.0.10) to R12C (200.40.40.2, ISP A)

🔹 All Commands Used To Isolate Issue:
  - get_interfaces (R11C) → Ethernet0/1 (172.16.0.10) UP/UP
  - get_ospf neighbors (R11C) → R1A (1.1.1.1) FULL/- on Ethernet0/1
  - get_routing (R11C, prefix 200.40.40.2) → "Network not in table"
  - get_routing (R11C) → **NO default route (0.0.0.0/0)**
  - get_ospf neighbors (R1A) → only Area 2 neighbors (R10C, R11C), **NO Area 0 neighbors**
  - run_show ospf interface brief (R1A) → **Ethernet3, Ethernet4 in Area 0.0.0.1 (wrong!), 0 neighbors each**
  - get_ospf neighbors (R2C) → no neighbor to R1A on Ethernet0/3
  - run_show ospf interface brief (R2C) → Ethernet0/3 to R1A in Area 0.0.0.0, 0 neighbors

🔹 Commands That Actually Identified the Issue:
  - run_show ospf interface brief (R1A) → revealed Ethernet3 and Ethernet4 in Area 0.0.0.1 instead of Area 0.0.0.0
  - get_ospf neighbors (R1A) → confirmed NO adjacencies in Area 0 backbone

🔹 Proposed Fixes (Per Device):
  - Reconfigure R1A interfaces Ethernet3 and Ethernet4 from Area 0.0.0.1 to Area 0.0.0.0

🔹 Commands Used Upon User Approval:
  router ospf 1
   no network 10.0.0.4 0.0.0.3 area 0.0.0.1
   no network 10.0.0.0 0.0.0.3 area 0.0.0.1
   network 10.0.0.4 0.0.0.3 area 0.0.0.0
   network 10.0.0.0 0.0.0.3 area 0.0.0.0

🔹 Post-Fix State:
  - R1A Ethernet3: Area 0.0.0.0, 1 neighbor (R3C 3.3.3.3 FULL)
  - R1A Ethernet4: Area 0.0.0.0, 1 neighbor (R2C 2.2.2.2 FULL)
  - R11C routing table: default route present (0.0.0.0/0 via 172.16.0.9, OSPF inter-area)
  - Traceroute R11C → R12C: succeeds via R1A → ECMP (R2C/R3C) → R12C
  - Ping R11C → R12C: 5/5 packets successful, 1ms RTT

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Read sla_paths.json → identified R11C_TO_R12C path with ECMP via R1A to R2C/R3C
  - [x] Step 1: traceroute from R11C → failed (no route to destination)
  - [x] Step 1a: sanity check on R11C (source device) → interfaces/neighbors healthy, but NO default route
  - [x] Identify missing routes → traced to missing Area 0 routes propagated to Area 2
  - [x] Check R1A OSPF state → Area 0 interfaces configured in wrong area (0.0.0.1 instead of 0.0.0.0)
  - [x] Verify R1A adjacencies → confirmed zero neighbors in Area 0 backbone
  - [x] Apply fix → move Ethernet3/4 to Area 0.0.0.0
  - [x] Verify → R1A-R2C/R3C adjacencies form, R11C receives default route, traceroute succeeds

🔸 Lessons Learned:
  - **ABR area misconfiguration cascades through network**: R1A's incorrect area assignment broke inter-area route propagation to all Area 2 stub devices (R10C, R11C). This is a high-impact misconfiguration affecting multiple SLA paths.
  - **Missing default route in stub area is a red flag**: When a stub area leaf device (R11C) has no default route despite healthy OSPF neighbor to ABR, immediately suspect ABR configuration issue or broken inter-area adjacency.
  - **Zero neighbors on an interface with healthy physical link indicates area/authentication mismatch**: R1A's Area 0 interfaces were up/up but had 0 neighbors due to area mismatch, not interface issues. This pattern is distinct from physical layer failures.
  - **Recurring misconfiguration**: This is the same ABR area bug as R4C-SLA-002 (same date), suggesting configuration may need permanent correction or validation to prevent future recurrence.

---

📄 CASE NO. - 00004-R10C-SLA
Date: 2026-02-24 09:47 UTC
Device(s): R10C, R1A, R2C, R3C

🔹 Reported Issue:
  - IP SLA path 1 on R10C (R10C_TO_R16C) transitioned from Up to Down
  - SLA monitoring: R10C (172.16.0.6) to R16C (200.50.50.6, ISP B)
  - **Note**: Different failure than earlier R10C-SLA-001; same source/destination, different root cause

🔹 All Commands Used To Isolate Issue:
  - traceroute (R10C to 200.50.50.6, source 172.16.0.6) → FAILED: "!N" (no route) at hop 1 (R1A)
  - get_interfaces (R10C) → Ethernet0/1 UP/UP, has default route 0.0.0.0/0
  - get_ospf neighbors (R10C) → R1A (1.1.1.1) FULL/- on Ethernet0/1 in Area 2
  - get_routing (R1A) → **NO default route (0.0.0.0/0), NO Area 0 routes**
  - get_ospf neighbors (R1A) → only Area 2 neighbors (R10C, R11C), **NO Area 0 neighbors despite Area 0 interfaces up**
  - ping (R1A to R2C 10.0.0.2) → SUCCESS (layer 3 connectivity OK)
  - ping (R1A to R3C 10.0.0.6) → SUCCESS (layer 3 connectivity OK)
  - run_show ospf interface (R1A Ethernet3) → **hello-interval 33, dead-interval 40**
  - run_show ospf interface (R2C Ethernet0/3) → **hello-interval 10, dead-interval 40**
  - run_show ospf neighbor (R2C Ethernet0/3) → 0 neighbors

🔹 Commands That Actually Identified the Issue:
  - run_show ospf interface (R1A Ethernet3/4) → revealed hello-interval 33 vs expected 10
  - run_show ospf interface (R2C Ethernet0/3) → revealed hello-interval 10, confirming mismatch
  - ping (R1A to R2C/R3C) → confirmed layer 3 OK, but OSPF not forming (not physical layer)

🔹 Proposed Fixes (Per Device):
  - Configure R1A interfaces Ethernet3 and Ethernet4 to use standard OSPF timers: hello-interval 10, dead-interval 40

🔹 Commands Used Upon User Approval:
  interface Ethernet3
   ip ospf hello-interval 10
   ip ospf dead-interval 40
  interface Ethernet4
   ip ospf hello-interval 10
   ip ospf dead-interval 40

🔹 Post-Fix State:
  - R1A Ethernet3: hello-interval 10, dead-interval 40, 1 neighbor (R3C 3.3.3.3 FULL, Area 0)
  - R1A Ethernet4: hello-interval 10, dead-interval 40, 1 neighbor (R2C 2.2.2.2 FULL, Area 0)
  - R1A routing table: default route present (0.0.0.0/0 via OSPF E1, ECMP to R2C/R3C)
  - Traceroute R10C → R16C: succeeds via R1A → R2C → R16C (ISP B)
  - Ping R10C → R16C: 5/5 packets successful, 1-2ms RTT

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Step 0: Read sla_paths.json → identified R10C_TO_R16C path with ECMP at R1A (next-hops: R2C, R3C)
  - [x] Step 1: traceroute from R10C → failed at first hop with "!N" (no route) at R1A
  - [x] Step 1a: sanity check on R10C (source device) → interfaces/neighbors healthy, has default route
  - [x] Identify routing issue on R1A → R1A has NO default route, NO Area 0 routes
  - [x] Check R1A OSPF adjacencies → Area 0 interfaces up/up but zero neighbors (not physical layer)
  - [x] Layer 3 connectivity check → ping to R2C/R3C succeeds, confirming physical links work
  - [x] OSPF interface detailed inspection → discovered hello-interval mismatch (R1A 33 vs Cisco 10)
  - [x] Verify on neighbor devices → R2C/R3C confirm hello-interval 10 and zero neighbors to R1A
  - [x] Root cause identification → **OSPF timer mismatch prevents adjacency formation**
  - [x] Apply fix → align timers to standard (hello 10, dead 40)
  - [x] Verify → R1A-R2C/R3C adjacencies form, R1A learns default route, traceroute succeeds
  - [x] ECMP verification → both paths (R1A→R2C and R1A→R3C) operational

🔸 Lessons Learned:
  - **OSPF timer mismatch is a silent killer**: Interfaces can be up/up with healthy layer 3 connectivity, yet OSPF adjacencies never form if timers don't match. This is invisible in basic diagnostics and requires explicit OSPF interface inspection (hello/dead intervals).
  - **Arista EOS vs Cisco IOS timer defaults differ**: R1A (Arista EOS) defaulted to hello-interval 33, while Cisco devices use 10. Interoperability requires explicit timer alignment on the non-default device.
  - **Zero neighbors despite healthy interface is OSPF-specific**: Unlike area mismatches or physical failures, timer mismatch manifests as OSPF interface up but neighbor count zero. Layer 3 connectivity confirms physical link; OSPF neighbor absence points to adjacency formation issue (area, auth, timers, options E-bit).
  - **On-Call workflow effectiveness**: The structured approach (traceroute → source sanity → layer 3 check → OSPF interface inspection) efficiently narrowed from broad "no route" issue to specific timer mismatch, avoiding hours of random protocol debugging.
  - **Stub area depends critically on ABR health**: Area 2 stub leaves (R10C, R11C) cannot function if the ABR (R1A) lacks Area 0 adjacencies. A single misconfigured router (R1A) cascades failures across multiple SLA paths and leaf devices. ABR is a critical point of failure.

---

📄 CASE NO. - 00005-R4C-SLA
Date: 2026-02-24 10:51 UTC
Device(s): R4C, R3C, R1A, R10C

🔹 Reported Issue:
  - IP SLA path 1 on R4C (R4C_TO_R10C) transitioned from Up to Down
  - SLA monitoring: R4C (192.168.10.2) to R10C (10.10.10.10)

🔹 All Commands Used To Isolate Issue:
  - traceroute (R4C to 10.10.10.10, source 192.168.10.2) → FAILED: path diverged to ISP A (200.40.40.6) with !H
  - get_interfaces (R4C) → all interfaces up/up, source interface Ethernet0/1 healthy
  - get_eigrp neighbors (R4C) → R3C and R5C neighbors present, HEALTHY
  - get_routing (R4C, prefix 10.10.10.10) → "Subnet not in table" (MISSING ROUTE)
  - get_routing (R3C, prefix 10.10.10.10) → "Subnet not in table" (MISSING ROUTE)
  - get_ospf database (R3C) → Type 3 LSA for 10.10.10.10 present, age 1590s (STALE)
  - get_ospf database (R1A) → Summary LSA for 10.10.10.10 present, age 1611s (STALE)
  - get_ospf neighbors (R1A) → only Area 2 neighbors (R10C, R11C), **NO Area 0 neighbors**
  - get_ospf neighbors (R3C) → only R2C on Ethernet1/0, **NO neighbor on Ethernet0/3 (to R1A)**
  - ping (R3C to R1A 10.0.0.5) → SUCCESS (layer 3 OK)
  - run_show ospf interface (R3C Ethernet0/3) → Area 0, MD5 auth enabled, Neighbor Count 0
  - run_show ospf interface (R1A Ethernet3) → Area 0, MD5 auth enabled, hello-interval 333, dead-interval 40 (MISMATCH!)
  - ping (R1A to R2C/R3C) → SUCCESS (layer 3 OK)
  - run_show ospf database router 1.1.1.1 (on R3C) → R1A marked "**not-reachable in topology**"

🔹 Commands That Actually Identified the Issue:
  - run_show ospf interface (R1A Ethernet3) → revealed hello-interval 333 vs expected 10
  - run_show ospf database router (on R3C) → revealed R1A marked as unreachable (adjacency not forming)
  - ping (R1A to R2C/R3C) → confirmed layer 3 OK, so OSPF timer mismatch confirmed

🔹 Proposed Fixes (Per Device):
  - Configure R1A interfaces Ethernet3 and Ethernet4 to use standard OSPF timers: hello-interval 10, dead-interval 40

🔹 Commands Used Upon User Approval:
  interface Ethernet3
   ip ospf hello-interval 10
   ip ospf dead-interval 40
  interface Ethernet4
   ip ospf hello-interval 10
   ip ospf dead-interval 40

🔹 Post-Fix State:
  - R1A Ethernet3: hello-interval 10, dead-interval 40, 1 neighbor (R3C 3.3.3.3 FULL, Area 0)
  - R1A Ethernet4: hello-interval 10, dead-interval 40, 1 neighbor (R2C 2.2.2.2 FULL, Area 0)
  - R3C routing table: 10.10.10.10/32 present (inter-area via 10.0.0.5, metric 10101)
  - R4C routing table: 10.10.10.10/32 present (EIGRP redistributed from OSPF, metric 281856)
  - Traceroute R4C → R10C: succeeds via R3C (192.168.10.1) → R1A (10.0.0.5) → R10C (172.16.0.6)
  - Ping R4C → R10C: 5/5 packets successful, 1ms avg RTT

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Step 0: Read sla_paths.json → identified R4C_TO_R10C path with single egress R3C
  - [x] Step 1: traceroute from R4C → diverged to ISP A (200.40.40.6), routing issue not layer 3
  - [x] Step 1a: sanity check on R4C (source device) → interfaces/EIGRP neighbors healthy
  - [x] Check R3C for route to 10.10.10.10 → missing from RIB despite LSA in LSDB
  - [x] Check R1A OSPF adjacencies in Area 0 → confirmed zero neighbors on Area 0 interfaces
  - [x] Check R1A-R3C link connectivity → ping succeeds, so physical link OK
  - [x] OSPF interface inspection on R1A → discovered hello-interval 333 (vs expected 10)
  - [x] Verify on R3C → confirmed hello-interval 10, confirming mismatch
  - [x] Root cause: **OSPF hello timer mismatch prevents adjacency formation, breaking ABR-to-backbone link**
  - [x] Apply fix → align R1A timers to hello 10, dead 40
  - [x] Verify → R1A-R3C adjacency FULL, routes propagate, end-to-end traceroute succeeds

🔸 Lessons Learned:
  - **OSPF timer mismatch with extreme values is harder to spot**: The hello-interval 333 seconds is far more extreme than the 33 seconds seen in previous case (R10C-SLA-004). This value (5.5 minutes) makes adjacency formation impossible since dead-interval is 40 seconds. Extreme timer mismatches warrant explicit verification on ALL ABR interfaces.
  - **Stale LSA age in LSDB is a diagnostic red flag**: When LSAs are 1600+ seconds old (nearly 27 minutes) and not refreshing, it indicates the originating router (R1A) is not properly refreshing its advertisements. This points to either crashed/restarted ABR or broken adjacencies preventing LSA updates.
  - **ABR isolation cascades route propagation failure**: R1A without Area 0 neighbors means NO inter-area routes propagate from Area 2 to Area 0 to EIGRP domain. The failure manifests at R4C as missing route to 10.10.10.10 despite R10C being healthy.
  - **Multi-protocol chain is vulnerable to single ABR**: The path R4C (EIGRP AS10) → R3C (OSPF/EIGRP redistributor) → R1A (OSPF ABR) → R10C (OSPF Area 2) is entirely dependent on R1A's Area 0 adjacencies. One misconfigured router breaks the entire chain.
  - **On-Call skill effectiveness: Traceroute localization catches off-path routes**: The traceroute diverging to ISP A (200.40.40.6) immediately signaled a wrong default route/routing decision. This unusual path was the first diagnostic clue that something was wrong with the OSPF area 0 connectivity.

---

📄 CASE NO. - 00006-R11C-SLA
Date: 2026-02-24 11:09 UTC
Device(s): R11C, R1A, R2C, R3C

🔹 Reported Issue:
  - IP SLA path 1 on R11C (R11C_TO_R12C) transitioned from Up to Down
  - SLA monitoring: R11C (172.16.0.10) to R12C (200.40.40.2, ISP A)
  - Syslog event: BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down

🔹 All Commands Used To Isolate Issue:
  - traceroute (R11C to 200.40.40.2, source 172.16.0.10) → FAILED: "!N" at hop 1 (R1A 172.16.0.9)
  - get_interfaces (R11C) → Ethernet0/1 (172.16.0.10) UP/UP
  - get_ospf neighbors (R11C) → R1A (1.1.1.1) FULL/- on Ethernet0/1, Area 2
  - get_interfaces (R1A) → Ethernet3, Ethernet4 connected/up, Area 0
  - get_ospf interfaces (R1A) → Ethernet3/4: neighborCount 0, hello 10, dead 11 (Area 0)
  - get_ospf neighbors (R2C) → R3C on Ethernet1/0 (Area 0), **0 neighbors on Ethernet0/3 to R1A**
  - get_ospf interfaces (R2C) → Ethernet0/3 (Area 0): hello 10, dead 40, neighborCount 0
  - get_ospf neighbors (R3C) → R2C on Ethernet1/0 (Area 0), **0 neighbors on Ethernet0/3 to R1A**
  - get_ospf interfaces (R3C) → Ethernet0/3 (Area 0): hello 10, dead 40, neighborCount 0
  - get_routing (R1A) → NO routes to ISP prefixes (200.40.40.0/24, 200.50.50.0/24), only stub Area 2 routes

🔹 Commands That Actually Identified the Issue:
  - get_ospf interfaces (R1A) → revealed **dead-interval 11 seconds** on Area 0 interfaces
  - Comparison with R2C/R3C → revealed **dead-interval 40 seconds** on same area
  - Root cause: **OSPF dead-interval timer mismatch prevents neighbor formation**

🔹 Proposed Fixes (Per Device):
  - Configure R1A interfaces Ethernet3 and Ethernet4 dead-interval to 40 seconds to match R2C/R3C

🔹 Commands Used Upon User Approval:
  interface Ethernet3
   ip ospf dead-interval 40
  interface Ethernet4
   ip ospf dead-interval 40

🔹 Post-Fix State:
  - R1A Ethernet3: dead-interval 40, **1 neighbor (R3C 3.3.3.3 FULL, Area 0)** ✓
  - R1A Ethernet4: dead-interval 40, **1 neighbor (R2C 2.2.2.2 FULL, Area 0)** ✓
  - R1A routing table: default route present (0.0.0.0/0 ospfExternalType1, ECMP to R2C/R3C)
  - Traceroute R11C → R12C: succeeds via R1A (hop 1) → ECMP (R2C/R3C at hop 2) → R12C (hop 3)
  - Ping R11C → R12C: 5/5 packets successful, 1-2ms RTT

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Step 0: Read sla_paths.json → identified R11C_TO_R12C path with ECMP at R1A (next-hops: R2C, R3C)
  - [x] Step 1: traceroute from R11C → failed at first hop with "!N" (unreachable) at R1A
  - [x] Step 1a: sanity check on R11C (source device) → interfaces/neighbors healthy (FULL adjacency to R1A)
  - [x] Identify routing issue on R1A → R1A has NO routes to ISP prefixes (no default route)
  - [x] Check R1A OSPF adjacencies → Area 0 interfaces up/up but **zero neighbors**
  - [x] OSPF interface detailed inspection → discovered **dead-interval 11s on R1A vs 40s on R2C/R3C**
  - [x] Verify timer mismatch on neighbor devices → R2C/R3C confirm dead-interval 40 and zero neighbors to R1A
  - [x] Root cause identification → **OSPF dead-interval timer mismatch (R1A: 11s vs R2C/R3C: 40s) prevents adjacency formation**
  - [x] Apply fix → align R1A dead-interval to 40 seconds
  - [x] Verify → R1A-R2C/R3C adjacencies form immediately, R1A learns default route via OSPF, traceroute succeeds
  - [x] ECMP verification → both paths (R1A→R2C and R1A→R3C) operational

🔸 Lessons Learned:
  - **OSPF dead-interval mismatch is DIFFERENT from hello-interval mismatch**: Dead-interval controls how long to wait before declaring neighbor down. R1A (Arista EOS) had dead-interval 11s (non-standard, possibly from a previous hello-interval override). This is rarer than hello mismatch but equally deadly to adjacency formation. Always verify BOTH hello and dead intervals on both ends.
  - **EOS timer defaults differ significantly from Cisco IOS**: R1A (Arista EOS) continued to show anomalous timer values (hello 10 was OK, but dead 11 is bizarre). This suggests EOS may have a bug or unusual default behavior for dead-interval calculation. Explicit timer configuration is safer than relying on defaults in heterogeneous networks.
  - **OSPF adjacency formation requires perfect parameter alignment**: Even with area ID correct, authentication enabled, interfaces up/up, and layer 3 connectivity confirmed, a single mismatched timer prevents adjacency. The OSPF Adjacency Checklist (hello/dead timers first) is critical.
  - **R1A as single point of failure repeats across multiple SLA paths**: This is the 4th incident this shift involving R1A's Area 0 adjacencies (R4C-SLA-002, R11C-SLA-003, R10C-SLA-004, R4C-SLA-005, and now R11C-SLA-006). ABR health is critical to network stability. Consider dedicated monitoring/alerting for ABR adjacency state.
  - **On-Call traceroute-first approach caught immediate root cause**: Traceroute failure at first hop → interfaces up on source → routing table inspection → OSPF adjacency check → timer inspection. Structured workflow avoided hours of random debugging and identified the exact parameter mismatch quickly.

---

📄 CASE NO. - 00007-R11C-SLA
Date: 2026-02-24 11:24 UTC
Device(s): R11C, R1A, R2C, R3C

🔹 Reported Issue:
  - IP SLA path on R11C (R11C_TO_R12C) transitioned from Up to Down
  - Syslog event: BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down
  - SLA monitoring: R11C (source 172.16.0.10) to R12C (200.40.40.2, ISP A)

🔹 All Commands Used To Isolate Issue:
  - traceroute (R11C to 200.40.40.2, source 172.16.0.10) → FAILED: "!N" (no route) at hop 1 (R1A 172.16.0.9)
  - get_interfaces (R11C) → Ethernet0/1 (172.16.0.10) UP/UP
  - get_ospf neighbors (R11C) → R1A (1.1.1.1) FULL/- on Ethernet0/1, Area 0.0.0.2
  - get_ospf neighbors (R1A) → R11C and R10C FULL (Area 2), **R2C and R3C in INIT state** (Area 0)
  - run_show ospf interface (R1A) → Ethernet3/4: **deadInterval 7 seconds** (Area 0.0.0.0)
  - run_show ospf interface (R2C Ethernet0/3) → dead 40 seconds, hello 10, **neighborCount 0**
  - run_show ospf interface (R3C Ethernet0/3) → dead 40 seconds, hello 10, **neighborCount 0**

🔹 Commands That Actually Identified the Issue:
  - get_ospf neighbors (R1A) → revealed R2C/R3C in INIT state instead of FULL
  - run_show ospf interface (R1A) → **deadInterval 7 seconds on Area 0 interfaces**
  - Comparison with R2C/R3C → **deadInterval 40 seconds** on Area 0 interfaces
  - Root cause: **OSPF dead-interval timer mismatch (R1A: 7s vs R2C/R3C: 40s) prevents adjacency formation**

🔹 Proposed Fixes (Per Device):
  - Configure R1A interfaces Ethernet3 and Ethernet4 to use dead-interval 40 seconds (Cisco standard)

🔹 Commands Used Upon User Approval:
  interface Ethernet3
   ip ospf dead-interval 40
  interface Ethernet4
   ip ospf dead-interval 40

🔹 Post-Fix State:
  - R1A Ethernet3: deadInterval 40, **1 neighbor (R3C 3.3.3.3 FULL, Area 0.0.0.0)** ✓
  - R1A Ethernet4: deadInterval 40, **1 neighbor (R2C 2.2.2.2 FULL, Area 0.0.0.0)** ✓
  - R1A routing table: 200.40.40.0/24 now reachable via OSPF default route (ECMP to R2C/R3C)
  - Traceroute R11C → R12C: succeeds with full path (R11C → R1A → R3C → R12C)
  - Ping R11C → R12C: 5/5 packets successful, 1-2ms RTT

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Step 0: Read sla_paths.json → identified R11C_TO_R12C path with ECMP at R1A
  - [x] Step 1: traceroute from R11C → failed at hop 1 with "!N" (no route) at R1A
  - [x] Step 1a: sanity check on R11C (source device) → Ethernet0/1 UP/UP, OSPF FULL to R1A
  - [x] Identified routing issue on R1A → R1A has no route to ISP prefixes
  - [x] Check R1A OSPF adjacencies in Area 0 → R2C/R3C in INIT state, not progressing to FULL
  - [x] OSPF interface inspection on R1A → discovered **deadInterval 7s (Area 0 interfaces)**
  - [x] Verify on R2C/R3C → confirmed deadInterval 40s, confirming mismatch
  - [x] Root cause identification → **OSPF dead-interval timer mismatch**
  - [x] Apply fix → align R1A dead-interval to 40 seconds
  - [x] Verify → R1A-R2C and R1A-R3C adjacencies immediately form (FULL), routing restored

🔸 Lessons Learned:
  - **Dead-interval 7s is a non-standard Arista EOS default**: This is the 6th case in one shift involving R1A OSPF timer mismatches. R1A keeps reverting to non-standard timers (7s, 11s, 33s, 333s). **URGENT: Baseline R1A OSPF timer configuration to Cisco standard (hello 10, dead 40) and enforce via configuration management.**
  - **INIT state adjacencies that don't progress to FULL indicate parameter mismatch**: This is distinct from DOWN/FULL states. INIT means routers exchange hellos but fail to progress—classic sign of hello/dead timer or option misalignment.
  - **Multi-vendor OSPF requires explicit timer homogenization**: Cisco IOS defaults (hello 10, dead 40) differ from Arista EOS non-standard defaults. Never rely on vendor defaults in heterogeneous networks.
  - **Recurring R1A failures indicate systemic device or management issue**: Six SLA path failures in one shift, all rooted in R1A's OSPF timers. Consider: device restart, IOS upgrade, config template enforcement, or dedicated continuous monitoring of R1A OSPF adjacency state.
  - **ABR is critical single point of failure**: R1A serves all Area 2 stub leaves and core-to-ISP paths. Implement continuous OSPF neighbor adjacency monitoring on all ABR interfaces with alerts for INIT state lasting >10 seconds.

---

📄 CASE NO. - 00008-R10C-SLA
Date: 2026-02-24 12:20 UTC
Device(s): R10C, R1A, R2C, R3C, R16C

🔹 Reported Issue:
  - IP SLA path 1 on R10C (R10C_TO_R16C) transitioned from Up to Down
  - Syslog event: BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down
  - SLA monitoring: R10C (source 172.16.0.6) to R16C (200.50.50.6, ISP B)
  - **Note**: Different root cause than previous R10C SLA failures; similar to R4C-SLA-002/R11C-SLA-003 ABR area misconfiguration

🔹 All Commands Used To Isolate Issue:
  - ping (R10C to 200.50.50.6, source 172.16.0.6) → 0/5 packets successful (COMPLETE FAILURE)
  - get_interfaces (R10C) → Ethernet0/1 (172.16.0.6) UP/UP
  - get_ospf neighbors (R10C) → R1A (1.1.1.1) FULL/- on Ethernet0/1, Area 2
  - get_routing (R10C) → **NO default route (0.0.0.0/0), NO route to 200.50.50.6**
  - get_routing (R1A) → **empty routing table, NO Area 0 routes, NO default route**
  - get_ospf neighbors (R1A) → only Area 2 neighbors (R10C, R11C), **NO Area 0 neighbors**
  - run_show ospf interface (R1A) → Ethernet3/4: **Area 0.0.0.3** (wrong!), neighborCount 0 each
  - run_show ospf interface (R2C Ethernet0/3) → **Area 0.0.0.0** (correct), neighborCount 0
  - Confirmed: **R1A interfaces in Area 0.0.0.3 vs R2C/R3C in Area 0.0.0.0**

🔹 Commands That Actually Identified the Issue:
  - run_show ospf interface (R1A) → revealed **Ethernet3 and Ethernet4 in Area 0.0.0.3 instead of Area 0.0.0.0**
  - Verified against INTENT.json → confirmed interfaces should be in Area 0.0.0.0
  - get_ospf neighbors (R1A) → confirmed NO adjacencies in Area 0 backbone

🔹 Proposed Fixes (Per Device):
  - Reconfigure R1A interfaces Ethernet3 and Ethernet4 from Area 0.0.0.3 to Area 0.0.0.0

🔹 Commands Used Upon User Approval:
  interface Ethernet3
   no ip ospf area 0.0.0.3
   ip ospf area 0.0.0.0
  interface Ethernet4
   no ip ospf area 0.0.0.3
   ip ospf area 0.0.0.0

🔹 Post-Fix State:
  - R1A Ethernet3: **Area 0.0.0.0, 1 neighbor (R3C 3.3.3.3 loading→FULL, Area 0)** ✓
  - R1A Ethernet4: **Area 0.0.0.0, 1 neighbor (R2C 2.2.2.2 FULL, Area 0)** ✓
  - R1A routing table: **default route present (0.0.0.0/0 ospfExternalType1, ECMP via Ethernet3/4)**
  - R10C routing table: **default route present (0.0.0.0/0 OSPF inter-area via R1A)**
  - Ping R10C → R16C: **5/5 packets successful, 1-2ms RTT**

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Step 0: Read sla_paths.json → identified R10C_TO_R16C path with ECMP at R1A (next-hops: R2C, R3C)
  - [x] Step 1: ping from R10C to 200.50.50.6 → 0% success (complete reachability failure)
  - [x] Step 1a: sanity check on R10C (source device) → Ethernet0/1 UP/UP, OSPF FULL to R1A
  - [x] Identified routing issue on R10C → **NO default route, NO route to destination**
  - [x] Check R1A routing state → R1A has **empty routing table, NO Area 0 routes**
  - [x] Check R1A OSPF adjacencies → **NO Area 0 neighbors despite interfaces up/up**
  - [x] OSPF interface inspection on R1A → discovered **Ethernet3/4 in Area 0.0.0.3 (wrong area)**
  - [x] Verify against INTENT.json → confirmed interfaces should be in Area 0.0.0.0
  - [x] Root cause identification → **Area assignment mismatch (R1A in 0.0.0.3 vs R2C/R3C in 0.0.0.0)**
  - [x] Apply fix → move R1A Ethernet3/4 from Area 0.0.0.3 to Area 0.0.0.0
  - [x] Verify → R1A-R2C and R1A-R3C adjacencies form (FULL), R1A learns default route, R10C receives default, ping succeeds

🔸 Lessons Learned:
  - **R1A OSPF area configuration is repeatedly misconfigured**: This is the 8th SLA path failure this shift involving R1A. Previous cases: 4× timer mismatches (hello/dead intervals), and now 2× area mismatches (Area 0.0.0.1 and 0.0.0.3 instead of 0.0.0.0). **URGENT: Enforce R1A OSPF configuration via config management to prevent recurring misconfiguration.**
  - **Area misconfiguration vs timer mismatch have similar symptoms but different diagnostic approach**: Both prevent OSPF adjacency formation and break inter-area routing. However: area mismatches show 0 neighbors on interfaces that are physically up/up; timer mismatches may show neighbors in INIT/EXSTART state (depending on timing of diagnosis). **Always check area ID before timer investigation.**
  - **Empty routing table on ABR is a critical red flag**: When R1A (ABR) has no routes to ISP prefixes and no default route, the Area 0 adjacencies have failed. Combined with healthy Area 2 adjacencies, this pattern immediately points to Area 0 connectivity issue, not physical layer.
  - **INTENT.json validation is essential for configuration verification**: The correct area assignment (Area 0.0.0.0 for Ethernet3/4) was explicitly documented in INTENT.json. Cross-referencing actual config against INTENT caught the area mismatch immediately.
  - **ABR is the critical convergence point for multi-area networks**: R10C depends on R1A (ABR) to receive routes from Area 0. When R1A's Area 0 adjacencies fail (whether due to area ID, timers, or authentication), all stub area leaves (R10C, R11C) lose connectivity to ISP routes. A single ABR misconfiguration cascades across multiple SLA paths.
  - **OSPF adjacency formation is multi-factor**: Successful adjacency requires: (1) area ID match, (2) authentication credentials match, (3) hello/dead timer match, (4) interface up/up, (5) layer 3 connectivity. R1A failures have cycled through area ID (case 2, 3, 8), timers (cases 4, 5, 6, 7). **Implement checklist-based troubleshooting for OSPF adjacency: area → auth → timers → interface → layer 3.**

---

📄 CASE NO. - 00009-R11C-SLA
Date: 2026-02-24 12:39 UTC
Device(s): R11C, R1A, R2C, R3C

🔹 Reported Issue:
  - IP SLA path on R11C (R11C_TO_R12C) transitioned from Up to Down
  - Syslog event: BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down
  - SLA monitoring: R11C (source 172.16.0.10) to R12C (200.40.40.2, ISP A)

🔹 All Commands Used To Isolate Issue:
  - traceroute (R11C to 200.40.40.2, source 172.16.0.10) → FAILED: "!N" (no route) at hop 1 (R1A 172.16.0.9)
  - get_interfaces (R11C) → Ethernet0/1 (172.16.0.10) UP/UP
  - get_ospf neighbors (R11C) → R1A (1.1.1.1) FULL/- on Ethernet0/1, Area 0.0.0.2
  - get_interfaces (R1A) → All interfaces connected/up (Eth1/2/3/4)
  - get_ospf neighbors (R1A) → R11C and R10C FULL (Area 2), **NO Area 0 neighbors**
  - get_ospf interfaces (R1A) → Ethernet3/4 (Area 0): neighborCount 0, **passive: true** ← ROOT CAUSE FOUND
  - get_routing (R1A) → Empty routing table (only connected routes)

🔹 Commands That Actually Identified the Issue:
  - get_ospf interfaces (R1A) → revealed **passive-interface enabled (passive: true) on Ethernet3 and Ethernet4**
  - Comparison with neighbor devices → R2C/R3C waiting for hellos from R1A (passive disables hello transmission)
  - Root cause: **OSPF passive-interface prevents neighbor adjacency formation on Area 0 links**

🔹 Proposed Fixes (Per Device):
  - Remove passive-interface configuration from R1A Ethernet3 and Ethernet4

🔹 Commands Used Upon User Approval:
  router ospf 1
  no passive-interface Ethernet3
  no passive-interface Ethernet4

🔹 Post-Fix State:
  - R1A Ethernet3: passive: false, **1 neighbor (R3C 3.3.3.3 FULL, Area 0)** ✓
  - R1A Ethernet4: passive: false, **1 neighbor (R2C 2.2.2.2 transitioning to FULL, Area 0)** ✓
  - R1A routing table: default route present (0.0.0.0/0 ospfExternalType1, ECMP to R3C/R2C via 10.0.0.6 and 10.0.0.2)
  - R1A routing table: ISP routes now present (via default route fallback)
  - Traceroute R11C → R12C: succeeds via R1A (hop 1) → ECMP R2C/R3C (hop 2) → R12C (hop 3)
  - Ping R11C → R12C: 5/5 packets successful, 1-2ms RTT ✓

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Step 0: Read sla_paths.json → identified R11C_TO_R12C path with ECMP at R1A (next-hops: R2C, R3C)
  - [x] Step 1: traceroute from R11C → failed at first hop with "!N" (no route) at R1A 172.16.0.9
  - [x] Step 1a: sanity check on R11C (source device) → Ethernet0/1 UP/UP, OSPF FULL to R1A
  - [x] Identify routing issue on R1A → R1A has EMPTY routing table, NO routes to ISP prefixes
  - [x] Check R1A OSPF adjacencies → Area 0 interfaces up/up but ZERO neighbors (not physical layer)
  - [x] OSPF interface detailed inspection → discovered **passive: true on Ethernet3/4 (Area 0)**
  - [x] Layer 3 connectivity check → not needed (physical interfaces up, layer 3 reachable per OSPF from Area 2)
  - [x] Root cause identification → **passive-interface disables OSPF hellos, preventing adjacency formation on Area 0**
  - [x] Apply fix → remove passive-interface from R1A Ethernet3 and Ethernet4
  - [x] Verify → R1A-R2C/R3C adjacencies form (R3C FULL immediately, R2C in transition), R1A learns default route, traceroute succeeds, ping 100%
  - [x] ECMP verification → both paths (R1A→R2C and R1A→R3C) operational via ECMP

🔸 Lessons Learned:
  - **Passive-interface is a silent adjacency killer**: Unlike timers or area ID mismatches that produce immediate/quick symptoms, passive-interface disables hello transmission entirely. The interface appears UP/UP, OSPF process runs, but no hellos are sent → neighbor never forms. This is **invisible in basic interface status checks** and requires explicit OSPF interface inspection to detect.
  - **OSPF interface passive status must be verified during adjacency troubleshooting**: The OSPF Adjacency Checklist should include: (1) passive-interface status, (2) area ID, (3) authentication, (4) timers, (5) interface physical state. Passive-interface is the FIRST check because it's the most fundamental blocker.
  - **R1A continues to be a misconfiguration hotspot**: This is the 9th SLA path failure involving R1A in a single shift (cases 2, 3, 4, 5, 6, 7, 8, 9). Configuration issues have spanned: Area ID mismatches, OSPF timer mismatches, and now passive-interface misconfiguration. **CRITICAL: Implement automated compliance checking or lock R1A configuration to prevent further manual misconfiguration incidents.**
  - **Multi-protocol chain resilience depends on ABR stability**: R1A is the single point of failure for: (1) inter-area routing (Area 0 ↔ Area 2), (2) external route propagation (ISP routes to Area 2 stub leaves), (3) EIGRP redistribution chain (EIGRP AS10 → OSPF → ISP). Any R1A misconfiguration cascades to multiple SLA paths and business-critical routing.
  - **Passive-interface use case is narrow**: Passive-interface is intended for loopback interfaces and management subnets to prevent unnecessary OSPF flooding. On transit/ABR links (R1A Eth3/4), passive-interface must NEVER be enabled. Configuration validation should reject passive-interface on ABR backbone links.

---

📄 CASE NO. - 00010-R11C-SLA
Date: 2026-02-24 12:56 UTC
Device(s): R11C, R1A, R2C, R3C

🔹 Reported Issue:
  - IP SLA path on R11C (R11C_TO_R12C) transitioned from Up to Down
  - Syslog event: BOM%TRACK-6-STATE: 1 ip sla 1 reachability Up -> Down
  - SLA monitoring: R11C (source 172.16.0.10) to R12C (200.40.40.2, ISP A)

🔹 All Commands Used To Isolate Issue:
  - traceroute (R11C to 200.40.40.2, source 172.16.0.10) → FAILED: "!N" (Administratively prohibited) at hop 1 (R1A 172.16.0.9)
  - get_interfaces (R11C) → Ethernet0/1 (172.16.0.10) UP/UP, Loopback1 (11.11.11.11) UP/UP
  - get_ospf neighbors (R11C) → R1A (1.1.1.1) FULL/- on Ethernet0/1, Area 0.0.0.2
  - get_routing (R11C, prefix 200.40.40.2) → No route in routing table
  - get_interfaces (R1A) → Ethernet3 (10.0.0.5) connected/up, Ethernet4 (10.0.0.1) connected/up
  - get_ospf neighbors (R1A) → R11C and R10C FULL (Area 2), **NO Area 0 neighbors on Ethernet3/4**
  - get_routing (R1A) → Empty routing table (no route to 200.40.40.0/30 or default route)
  - get_ospf neighbors (R2C) → R3C on Ethernet1/0 (FULL), **NO neighbor on Ethernet0/3 to R1A**
  - get_ospf neighbors (R3C) → R2C on Ethernet1/0 (FULL), **NO neighbor on Ethernet0/3 to R1A**
  - run_show ospf interface (R1A Ethernet3) → **helloInterval 9, deadInterval 19** (Area 0)
  - run_show ospf interface (R2C Ethernet0/3) → helloInterval 10, deadInterval 40 (Area 0)
  - run_show ospf interface (R3C Ethernet0/3) → helloInterval 10, deadInterval 40 (Area 0)

🔹 Commands That Actually Identified the Issue:
  - run_show ospf interface (R1A) → revealed **hello-interval 9 seconds, dead-interval 19 seconds** on Area 0 interfaces
  - Comparison with R2C/R3C → revealed **hello-interval 10 seconds, dead-interval 40 seconds** (Cisco standard)
  - Root cause: **OSPF hello/dead timer mismatch prevents neighbor formation**

🔹 Proposed Fixes (Per Device):
  - Configure R1A interfaces Ethernet3 and Ethernet4 to use standard Cisco timers: hello-interval 10, dead-interval 40

🔹 Commands Used Upon User Approval:
  interface Ethernet3
   ip ospf hello-interval 10
   ip ospf dead-interval 40
  interface Ethernet4
   ip ospf hello-interval 10
   ip ospf dead-interval 40

🔹 Post-Fix State:
  - R1A Ethernet3: hello-interval 10, dead-interval 40, **1 neighbor (R3C 3.3.3.3 FULL, Area 0)** ✓
  - R1A Ethernet4: hello-interval 10, dead-interval 40, **1 neighbor (R2C 2.2.2.2 FULL, Area 0)** ✓
  - R1A routing table: default route present (0.0.0.0/0 ospfExternalType1, ECMP to R3C/R2C)
  - R1A routing table: ISP A routes present (via default route)
  - Traceroute R11C → R12C: succeeds via R1A (hop 1) → ECMP R2C/R3C (hop 2) → R12C (hop 3)
  - Ping R11C → R12C: 5/5 packets successful, 1-2ms RTT ✓

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Step 0: Read sla_paths.json → identified R11C_TO_R12C path with ECMP at R1A (next-hops: R2C, R3C)
  - [x] Step 1: traceroute from R11C → failed at first hop with "!N" (unreachable) at R1A 172.16.0.9
  - [x] Step 1a: sanity check on R11C (source device) → Ethernet0/1 UP/UP, OSPF FULL to R1A, Loopback1 UP/UP
  - [x] Identify routing issue on R1A → R1A has NO routes to ISP prefixes (200.40.40.0/30)
  - [x] Check R1A OSPF adjacencies → Area 0 interfaces up/up but **zero neighbors on Ethernet3/4**
  - [x] Verify on neighbor devices → R2C/R3C confirm zero neighbors to R1A on Ethernet0/3
  - [x] OSPF interface detailed inspection → discovered **hello-interval 9s, dead-interval 19s on R1A vs 10s, 40s on R2C/R3C**
  - [x] Root cause identification → **OSPF hello/dead timer mismatch prevents adjacency formation on Area 0 backbone**
  - [x] Apply fix → align R1A timers to standard Cisco defaults (hello 10, dead 40)
  - [x] Verify → R1A-R2C/R3C adjacencies form immediately (FULL), R1A learns default route, traceroute succeeds
  - [x] ECMP verification → both paths (R1A→R2C and R1A→R3C) operational

🔸 Lessons Learned:
  - **OSPF hello/dead timer mismatch is more common on Arista EOS**: R1A (Arista EOS) continues to revert to non-standard timers. Previous cases showed 33s (R4C-SLA-005), 11s (R11C-SLA-006), 7s (R11C-SLA-007), and now 9/19s (current). This is the **10th SLA path failure involving R1A in one shift**. **CRITICAL: Baseline and enforce R1A OSPF configuration with hello-interval 10 and dead-interval 40 via config lock or management system. Arista EOS may have a bug or configuration management issue.**
  - **Multiple timer mismatches in rapid succession indicate systemic device issue**: Rather than random misconfiguration, R1A consistently presents different non-standard timer values, suggesting: (1) device restart with corrupted config, (2) config template inconsistency, (3) Arista EOS software bug, or (4) configuration management automation error. Root cause is likely systemic, not individual manual typos.
  - **R1A is THE critical single point of failure**: This is the 10th SLA path failure this shift attributed to R1A misconfiguration. R1A serves 4 critical functions: (1) Area 0 ↔ Area 2 ABR, (2) Stub area default route injection, (3) Inter-domain routing to ISP, (4) EIGRP redistribution point. **Implement 24/7 continuous monitoring of R1A's OSPF adjacency state with immediate escalation alerts.**
  - **On-Call OSPF Adjacency Checklist refined**: Based on 10 cases, the checklist order is: (1) passive-interface status, (2) area ID, (3) authentication keys match, (4) **hello/dead timer match**, (5) interface physical state, (6) layer 3 connectivity. Timer checks require explicit OSPF interface inspection (not just neighbor state).
  - **Timer inspection is NOT obvious from high-level tools**: `get_ospf neighbors` shows "FULL" state but doesn't reveal missing neighbors. Only `run_show ospf interface` detail inspection reveals the mismatch. Always drill into OSPF interface parameters when zero neighbors exist on up/up interfaces with protocol running.

---

📄 CASE NO. - 00011-R4C-SLA
Date: 2026-02-24 13:07 UTC
Device(s): R4C, R3C, R1A, R10C

🔹 Reported Issue:
  - IP SLA path 1 on R4C (R4C_TO_R10C) transitioned from Up to Down
  - SLA monitoring: R4C (192.168.10.2) to R10C (10.10.10.10)
  - Impact: R10C (OSPF Area 2 stub) loopback unreachable from EIGRP domain (R4C)

🔹 All Commands Used To Isolate Issue:
  - traceroute (R4C to 10.10.10.10, source 192.168.10.2) → FAILED: routed to ISP addresses (200.40.40.6) with !H (Host Unreachable)
  - get_interfaces (R4C) → all interfaces UP/UP
  - get_eigrp neighbors (R4C) → all neighbors healthy (R3C, R5C FULL)
  - get_routing (R4C, prefix 10.10.10.10) → "Subnet not in table"
  - get_routing (R3C, prefix 10.10.10.10) → "Subnet not in table"
  - get_routing (R1A, prefix 10.10.10.10) → has route via OSPF from R10C
  - get_ospf neighbors (R1A) → only Area 0 neighbors visible (R3C, R2C), missing Area 2 neighbors
  - get_ospf interfaces (R1A) → Ethernet1 and Ethernet2 (Area 2) show dead_interval=123 (non-standard), neighbor_count=0
  - get_ospf neighbors (R10C) → only R11C neighbor present, missing R1A on Ethernet0/1

🔹 Commands That Actually Identified the Issue:
  - get_ospf interfaces (R1A) → revealed dead interval mismatch (123 vs 40)
  - get_ospf interfaces (R10C) → confirmed standard dead interval of 40 on R10C's side, confirming timer mismatch root cause

🔹 Proposed Fixes (Per Device):
  - Remove custom dead interval timers on R1A's Ethernet1 and Ethernet2, allowing OSPF to use default 40 seconds (vs current 123)

🔹 Commands Used Upon User Approval:
  interface Ethernet1
   no ip ospf dead-interval
  interface Ethernet2
   no ip ospf dead-interval

🔹 Post-Fix State:
  - R1A Ethernet1 dead_interval: 40 (restored), neighbor_count: 1 (R10C FULL)
  - R1A Ethernet2 dead_interval: 40 (restored), neighbor_count: 1 (R11C FULL)
  - R1A now has route 10.10.10.10/32 via OSPF from R10C
  - R3C redistributes route from OSPF to EIGRP via route-map OSPF-TO-EIGRP
  - R4C ping to 10.10.10.10: 100% success (5/5), RTT 1-2ms
  - Traceroute: R4C → R3C → R1A → R10C (correct path)
  - SLA path restored

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Read sla_paths.json → identified R4C_TO_R10C path
  - [x] Step 1: traceroute from R4C to 10.10.10.10 → diverted to ISP, path broken
  - [x] Step 1a: sanity check on source device (R4C) → interfaces and neighbors healthy
  - [x] Verify routing on source device → R4C missing route to 10.10.10.10
  - [x] Trace upstream: R3C also missing route, R1A missing route, R10C has loopback
  - [x] Identify OSPF area structure: R1A should be ABR connecting Area 0 and Area 2
  - [x] Check R1A OSPF interfaces → found dead interval mismatch on Area 2 interfaces (123 vs 40)
  - [x] Root cause: OSPF adjacency formation blocked by dead interval mismatch between R1A and R10C/R11C
  - [x] Apply fix: reset dead intervals to standard 40s
  - [x] Verify adjacencies formed: R1A now has R10C and R11C as neighbors (FULL)
  - [x] Verify route propagation: R4C can now reach 10.10.10.10 via correct path

🔸 Lessons Learned:
  - OSPF timer mismatches (especially dead interval) are subtle blockers to adjacency formation. They result in zero neighbors on otherwise healthy interfaces. Always compare timer values between neighbors before investigating other adjacency parameters (auth, area type, network type).
  - SLA path failures in multi-protocol environments (EIGRP + OSPF + redistribution) require tracing the entire route propagation chain: verify source routing first, then check each redistribution point (ABR/ASBR) for route presence and redistribution configuration.
  - The on-call workflow (traceroute-first, then sanity check, then protocol-specific troubleshooting) was efficient here. Traceroute quickly revealed the routing misdirection (ISP instead of internal), and protocol inspection at each hop pinpointed the ABR as the break point.

---

📄 CASE NO. - 00012-R4C-SLA
Date: 2026-02-24 13:31 UTC
Device(s): R4C, R1A
SLA Path: R4C_TO_R10C (R4C 192.168.10.2 → R10C 10.10.10.10)

🔹 Reported Issue:
  - IP SLA 1 on R4C transitioned from Up to Down
  - Reachability monitoring path: R4C (172.20.20.204) to R10C (10.10.10.10) failed
  - Event timestamp: 2026-02-24T13:31:23.767Z

🔹 All Commands Used To Isolate Issue:
  - traceroute (R4C to 10.10.10.10, source 192.168.10.2) → path diverted to ISP (200.40.40.6), !H at hop 3
  - get_interfaces (R4C, R3C, R1A, R10C)
  - get_eigrp (R4C neighbors)
  - get_ospf (R3C, R1A, R10C neighbors / database / interfaces)
  - get_routing (R4C, R3C, R1A for 10.10.10.10)
  - ping (R4C → 10.0.0.5 [R1A], R4C → 10.10.10.10)

🔹 Commands That Actually Identified the Issue:
  - get_ospf (R1A interfaces) → revealed Ethernet1 (Area 2) configured as passive-interface
  - get_ospf (R1A neighbors) → showed ONLY Area 0 neighbors (R3C, R2C), missing R10C/R11C

🔹 Proposed Fixes (Per Device):
  - R1A: Remove passive-interface configuration on Ethernet1 (Area 2 interface to R10C)
  - Command: no passive-interface Ethernet1 under router ospf 1

🔹 Commands Used Upon User Approval:
  router ospf 1
   no passive-interface Ethernet1

🔹 Post-Fix State:
  - R1A Ethernet1: Passive disabled, OSPF adjacency to R10C (10.10.10.10) now FULL
  - R1A routing table: Now has route 10.10.10.10/32 via OSPF (metric 101, next-hop 172.16.0.6)
  - R3C routing table: Now has route 10.10.10.10/32 via OSPF (metric 10101, redistributed to EIGRP)
  - R4C → 10.10.10.10: Ping 100% success (5/5), RTT 1-2ms
  - Traceroute: R4C → R3C (192.168.10.1) → R1A (10.0.0.5) → R10C (172.16.0.6) ✓

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Read sla_paths.json → identified R4C_TO_R10C path (scope: R4C, R3C, R1A, R10C)
  - [x] Step 1: traceroute from R4C with source 192.168.10.2 to 10.10.10.10
  - [x] Analysis: Traceroute shows path to ISP (200.40.40.6) instead of internal R1A path
  - [x] Step 1a: Source device sanity check on R4C → interfaces Up/Up, EIGRP neighbors present
  - [x] Trace path forward: R3C missing route → R1A missing route → suspect ABR (R1A)
  - [x] Check R1A OSPF interfaces: Found Ethernet1 (Area 2) is passive-interface
  - [x] Verify root cause: Passive interface prevents OSPF hellos → no neighbor adjacency
  - [x] Apply fix: Remove passive-interface on R1A Ethernet1
  - [x] Verify adjacency: R1A-R10C now FULL, routes appear in RIB
  - [x] Verify SLA path: Traceroute and ping both succeed with correct path

🔸 Lessons Learned:
  - A passive OSPF interface completely blocks adjacency formation even when all other parameters (timers, auth, area, network type) are correctly configured. The interface appears Up/Up with proper IP addressing, making it deceptively healthy.
  - When an ABR (R1A) shows neighbors in only ONE area (Area 0 only, missing Area 2 neighbors), immediately check if Area 2 interfaces are configured as passive. This is a classic overlooked configuration issue.
  - Traceroute-first triage works: A path diversion to ISP immediately signals that intermediate routers (R3C, R1A) lack internal routes, focusing investigation at the redistribution/OSPF propagation layer.
  - The on-call workflow efficiently isolated this issue: traceroute → source health check → path trace → ABR interface inspection. No deep protocol debugging was needed once the passive interface was found.

---

📄 CASE NO. - 00013-R4C-SLA
Date: 2026-02-24 14:26 UTC
Device(s): R4C, R3C, R1A, R10C
SLA Path: R4C_TO_R10C (R4C 192.168.10.2 → R10C 10.10.10.10)

🔹 Reported Issue:
  - IP SLA 1 on R4C transitioned from Up to Down
  - SLA monitoring path: R4C (192.168.10.2 on Ethernet0/1) to R10C (10.10.10.10)
  - Event timestamp: 2026-02-24T14:26:54.378Z
  - **Note**: Similar to case 00012 (13:31 UTC), same R4C_TO_R10C path but different/recurrent SLA event

🔹 All Commands Used To Isolate Issue:
  - traceroute (R4C to 10.10.10.10, source 192.168.10.2) → path diverted to 200.40.40.6 (ISP), !H at hop 3
  - get_interfaces (R4C) → Ethernet0/1 Up/Up, source interface healthy
  - get_eigrp neighbors (R4C) → R3C and R5C present, HEALTHY
  - get_routing (R3C, prefix 10.10.10.10) → "Subnet not in table"
  - get_ospf neighbors (R3C) → R1A on Ethernet0/3 FULL
  - get_ospf database (R3C) → Type 3 LSAs present
  - get_routing (R1A, prefix 10.10.10.10) → missing route
  - get_ospf neighbors (R1A) → ONLY Area 0 neighbors (R3C, R2C), NO Area 2 neighbors
  - get_interfaces (R1A) → Ethernet1/2 connected/up (physical links OK)
  - get_ospf interfaces (R1A) → **Ethernet1: Area 2, passive=TRUE; Ethernet2: Area 2, passive=TRUE**
  - get_ospf neighbors (R10C) → R11C only, NO neighbor to R1A on Ethernet0/1
  - Identified second passive interface: Ethernet2 (172.16.0.9/30 to R11C)

🔹 Commands That Actually Identified the Issue:
  - get_ospf interfaces (R1A) → revealed Ethernet1 AND Ethernet2 configured as passive-interface
  - get_ospf neighbors comparison → R1A only shows Area 0 neighbors, missing Area 2 neighbors

🔹 Root Cause Analysis:
  - **R1A's Area 2 interfaces (Ethernet1 and Ethernet2) configured as OSPF passive interfaces**
  - Passive interfaces do NOT send/receive OSPF hellos, preventing adjacency formation
  - Both interfaces are physically up but OSPF adjacencies cannot form
  - Result: R10C/R11C loopbacks NOT advertised to Area 0 → NOT redistributed to EIGRP → R4C has NO route to 10.10.10.10

🔹 Proposed Fixes (Per Device):
  - R1A: Remove passive-interface configuration on Ethernet1 and Ethernet2
  - Commands: no passive-interface Ethernet1 && no passive-interface Ethernet2 (under router ospf 1)

🔹 Commands Used Upon User Approval:
  router ospf 1
   no passive-interface Ethernet1
   no passive-interface Ethernet2

🔹 Post-Fix State:
  - R1A Ethernet1 (172.16.0.5/30): Passive=FALSE, OSPF adjacency to R10C (10.10.10.10) NOW FULL ✓
  - R1A Ethernet2 (172.16.0.9/30): Passive=FALSE, OSPF adjacency to R11C (11.11.11.11) NOW FULL ✓
  - R1A routing table: 10.10.10.10/32 via OSPF (metric 101, next-hop 172.16.0.6) ✓
  - R3C routing table: 10.10.10.10/32 via OSPF (metric 10101, redistributed to EIGRP) ✓
  - R4C routing table: 10.10.10.10/32 via EIGRP AS10 (metric 281856, next-hop 192.168.10.1) ✓
  - Traceroute R4C → R10C: Full path successful
    - Hop 1: 192.168.10.1 (R3C)
    - Hop 2: 10.0.0.5 (R1A)
    - Hop 3: 172.16.0.6 (R10C destination) ✓

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Step 0: Read sla_paths.json → identified R4C_TO_R10C path (scope: R4C, R3C, R1A, R10C, no ECMP)
  - [x] Step 1: traceroute from R4C (192.168.10.2 → 10.10.10.10) → path diverted to ISP 200.40.40.6 at hop 2, !H at hop 3
  - [x] Step 1a: Source device (R4C) sanity check → Ethernet0/1 Up/Up, EIGRP neighbors present and healthy
  - [x] Localize breaking hop: R3C missing route → R1A missing route → investigate R1A (ABR)
  - [x] Check R3C OSPF state → neighbors present but route not in RIB (LSA in LSDB but not propagated)
  - [x] Check R1A OSPF state → ONLY Area 0 neighbors present, missing Area 2 neighbors (R10C, R11C)
  - [x] Check R1A interfaces → Ethernet1/2 physically up/up but OSPF neighbors absent
  - [x] Query R1A OSPF interfaces → discovered both Ethernet1 and Ethernet2 configured as passive
  - [x] Identify root cause → passive-interface prevents OSPF hellos, no adjacency formation, routes not propagated
  - [x] Apply fix → remove passive-interface configuration from both Ethernet1 and Ethernet2
  - [x] Verify adjacency formation → R1A-R10C and R1A-R11C now FULL
  - [x] Verify route propagation → routes now present at R3C and R4C
  - [x] Verify SLA path → traceroute successful, 3-hop path as expected

🔸 Lessons Learned:
  - **Incomplete fix leads to recurrence**: Case 00012 (13:31 UTC) may have only fixed Ethernet1, leaving Ethernet2 passive. This case (14:26 UTC, 55 minutes later) suggests the fix was incomplete. **Always check ALL interfaces in the same area when discovering passive-interface issues on an ABR.**
  - **Passive interface is a "silent killer" for OSPF adjacencies**: Unlike physical down interfaces or authentication failures that produce clear error states, passive interfaces leave the link physically up with no visible reason for adjacency failure. The OSPF `interfaces` query is the ONLY way to detect this misconfiguration.
  - **ABR with partially-configured passive interfaces creates asymmetric routing**: R1A had Area 0 neighbors (Ethernet3/4 active) but no Area 2 neighbors (Ethernet1/2 passive). This resulted in routes flowing INTO R1A but not OUT to Area 2, creating the classic symptom of "internal routes missing at downstream routers."
  - **SLA path failures 55 minutes apart suggest configuration instability**: The recurrence of R4C_TO_R10C failure so soon after case 00012 indicates either (a) incomplete fix, (b) configuration drift, or (c) manual rollback. Recommend checking configuration management and automation for anomalies. Consider persistent monitoring of R1A's interface passive status.
  - **On-Call workflow identifies multi-layer issues efficiently**: Traceroute → source health → intermediate routing inspection → OSPF interface inspection → passive-interface detection. Structured approach caught both the root cause AND its broad impact across all Area 2 devices.

---

📄 CASE NO. - 00014-R8C-SLA
Date: 2026-02-24 18:19 UTC
Device(s): R8C

🔹 Reported Issue:
  - IP SLA path 1 on R9C (R9C_TO_R5C) transitioned from Up to Down
  - SLA monitoring: R9C (192.168.20.2) to R5C (5.5.1.1)

🔹 All Commands Used To Isolate Issue:
  - get_interfaces (R9C) → Ethernet0/1 (192.168.20.2) UP/UP
  - ping (R9C to 5.5.1.1, source 192.168.20.2) → 0/5 packets, FAILED
  - get_eigrp neighbors (R9C) → R8C (192.168.20.1) neighbor present, hold 11, uptime 01:03:26
  - get_routing (R9C, prefix 5.5.1.1) → "Network not in table"
  - get_routing (R9C, full) → only 8.8.8.8/32 from EIGRP, no 5.5.1.1
  - get_routing (R8C, prefix 5.5.1.1) → "Network not in table"
  - get_ospf neighbors (R8C) → NO neighbors present (empty)
  - get_interfaces (R8C) → **Ethernet0/1 administratively down, Ethernet0/2 administratively down**

🔹 Commands That Actually Identified the Issue:
  - get_interfaces (R8C) → revealed Ethernet0/1 and Ethernet0/2 administratively down
  - get_ospf neighbors (R8C) → confirmed no OSPF neighbors (direct result of shutdown interfaces)

🔹 Proposed Fixes (Per Device):
  - Enable Ethernet0/1 on R8C (no shutdown) — connects to R6A
  - Enable Ethernet0/2 on R8C (no shutdown) — connects to R7A

🔹 Commands Used Upon User Approval:
  interface Ethernet0/1
   no shutdown
  interface Ethernet0/2
   no shutdown

🔹 Post-Fix State:
  - R8C Ethernet0/1: UP/UP (10.1.1.1)
  - R8C Ethernet0/2: UP/UP (10.1.1.5)
  - R8C routing table: now has OSPF routes (0.0.0.0/0, 6.6.6.6/32, 7.7.7.7/32, 2.2.2.66/32, etc.)
  - R9C EIGRP routes: now receiving multiple EIGRP-EX routes from R8C (0.0.0.0/0, 6.6.6.6/32, 7.7.7.7/32, etc.)
  - R9C ping to 5.5.1.1: 5/5 packets successful, 100% success rate, RTT 1-2ms

🔹 Verification: PASSED
🔹 Case Status: FIXED

📋 CASE METADATA

🔸 Case Handling Plan:
  - [x] Step 0: Read sla_paths.json → identified R9C_TO_R5C path with ECMP at R8C (splits to R6A/R7A)
  - [x] Step 1: get_interfaces (R9C) → confirmed source interface Ethernet0/1 UP/UP
  - [x] Step 1: ping R9C → 5.5.1.1 → FAILED (0/5 packets)
  - [x] Step 1a: get_eigrp neighbors (R9C) → R8C neighbor healthy (hold 11)
  - [x] Step 1a: get_routing (R9C) → route to 5.5.1.1 MISSING, only 8.8.8.8/32 received
  - [x] Localize breaking hop → R8C (next hop for R9C EIGRP routes)
  - [x] get_ospf neighbors (R8C) → ZERO neighbors despite needing R6A/R7A connections
  - [x] get_interfaces (R8C) → **found Ethernet0/1 and Ethernet0/2 administratively down** (root cause)
  - [x] Apply fix → enable both interfaces
  - [x] Verify R8C routes → OSPF routes now present
  - [x] Verify R9C routes → EIGRP-EX routes now received
  - [x] Verify SLA path → ping 5/5 successful, 100% success rate

🔸 Lessons Learned:
  - **OSPF interface shutdown breaks redistribution chains**: R8C is a redistribution point (EIGRP ↔ OSPF). When its OSPF-facing interfaces are shutdown, all downstream EIGRP neighbors lose access to routes from the OSPF domain, breaking the entire chain. This is especially critical for ECMP split points where both interfaces feed the SLA path.
  - **Check interface status on IGP redistribution routers**: When routes disappear despite healthy protocol neighbors on the source device, immediately check the redistribution router's interfaces. Shutdown OSPF interfaces on a router that advertises into EIGRP will silently starve EIGRP speakers of external routes.
  - **ECMP node interface health is critical to SLA path reliability**: R8C splits to R6A/R7A (ECMP). Shutdown of even ONE interface (Ethernet0/1 OR Ethernet0/2) would break one ECMP branch. Both being shutdown completely broke the entire path. Always verify ALL ECMP next-hop interfaces are active when troubleshooting ECMP SLA paths.
  - **Empty OSPF neighbor list on a connected interface is suspicious**: R8C's OSPF neighbors query returned empty, yet interfaces to R6A/R7A were configured. This should have triggered immediate interface inspection. When a routing protocol reports zero neighbors but the interface is expected to have peers, always check: (1) shutdown status, (2) timer mismatch, (3) passive-interface, (4) area mismatch.
  - **Maintenance window escalation was accepted**: Emergency out-of-window approval was granted due to SLA path failure severity. Configuration was applied successfully outside the 06:00-18:00 UTC maintenance window after management escalation.

