## Regression Checklist (Manual Tests Performed by User)

Run this checklist after any significant change to `MCPServer.py`, `oncall_watcher.py`,
`platforms/platform_map.py`, `tools/`, `transport/`, or any skill file:

| # | Check | Method |
|---|-------|--------|
| 1 | All unit tests pass (217 tests) | `./run_tests.sh unit` |
| 2 | Integration tests pass (lab required) | `./run_tests.sh integration` |
| 3 | OSPF adjacency diagnosis works | ST-001 |
| 4 | EIGRP passive-interface diagnosis works | ST-002 |
| 5 | Redistribution diagnosis works | ST-003 |
| 6 | Policy-based routing diagnosis works | ST-004 |
| 7 | EIGRP stub configuration works | ST-005 |
| 8 | BGP timer mismatch diagnosis works | ST-006 |
| 9 | OSPF area type change diagnosis works | ST-007 |
| 10 | Multi-vendor OSPF timer mismatch (MikroTik) | ST-008 |
| 11 | On-Call agent invoked and diagnoses correctly | OC-001 |
| 12 | Concurrent SLA failures → deferred queue | OC-002 |
| 13 | On-Call watcher log interactions | WB-001 – WB-003 |
| 14 | Maintenance window blocks push_config | MW-001 |

**Unit test coverage by file (run `./run_tests.sh unit`):**

| Test File | What It Covers |
|-----------|----------------|
| `test_drain_mechanism.py` | tail_follow drain flag and line-yield logic |
| `test_platform_map.py` | PLATFORM_MAP command lookups for all vendors/queries |
| `test_sla_patterns.py` | SLA_DOWN_RE regex matching (all vendor formats) |
| `test_input_validation.py` | Literal enum rejection, ShowCommand read-only enforcement |
| `test_cache.py` | Bounded LRU eviction, TTL expiry, cache hit/miss |
| `test_command_validation.py` | FORBIDDEN CLI list, RouterOS JSON path/method validation, rollback advisory |
| `test_maintenance_window.py` | check_maintenance_window inside/outside window; push_config blocked outside |

**Integration test coverage (requires running lab):**

| Test File | What It Covers |
|-----------|----------------|
| `test_mcp_connectivity.py` | Basic device reachability via MCP tools |
| `test_mcp_tools.py` | All protocol/routing/operational tools against live devices |
| `test_transport.py` | SSH/eAPI/REST transport layer: structured output, cache hit/miss, timeout |

**NOTE:** All Standalone or On-Call cases are documented as Jira tickets (see Jira project SUP).

**MW-001 verification**: `push_config` now enforces the maintenance window — it returns an error dict when `check_maintenance_window` returns `allowed: false`. To test: temporarily narrow the window in `MAINTENANCE.json` to exclude current time, submit a Standalone prompt, approve the proposed fix, and confirm the agent reports a maintenance window block. Restore `MAINTENANCE.json` after testing.
