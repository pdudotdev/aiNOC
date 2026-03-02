# aiNOC Agent Test Suite

Structured test framework for validating aiNOC agent behavior after codebase changes.

## Prerequisites

```bash
cd /home/mcp/mcp-project
pip install -r requirements.txt
```

Credentials are loaded from `/home/mcp/mcp-project/.env`:
```
ROUTER_USERNAME=admin
ROUTER_PASSWORD=admin
```

## Running Tests

```bash
chmod +x run_tests.sh

# Run all tests
./run_tests.sh all

# Run only unit tests (no device connectivity required)
./run_tests.sh unit

# Run integration tests (real devices, read-only)
./run_tests.sh integration
```

## Test Categories

### Unit Tests (no devices)
| ID | File | Description |
|----|------|-------------|
| UT-001 | unit/test_sla_patterns.py | SLA_DOWN_RE regex against all log formats |
| UT-002 | unit/test_platform_map.py | PLATFORM_MAP command mapping per cli_style |
| UT-003 | unit/test_drain_mechanism.py | tail_follow drain/EOF-seek logic |
| UT-004 | unit/test_input_validation.py | Literal enum rejection, ShowCommand read-only enforcement |
| UT-005 | unit/test_cache.py | Bounded LRU eviction, TTL expiry, cache hit/miss |
| UT-006 | unit/test_command_validation.py | FORBIDDEN CLI list, RouterOS JSON path/method validation |
| UT-007 | unit/test_maintenance_window.py | check_maintenance_window inside/outside window |
| UT-008 | unit/test_risk_assessment.py | Risk level logic (low/medium/high) |
| UT-009 | unit/test_syslog_sanitize.py | Syslog message sanitization |

### Integration Tests (read-only, real devices)
| ID | File | Description |
|----|------|-------------|
| IT-001 | integration/test_mcp_connectivity.py | MCP tool reachability (requires lab, skip with NO_LAB=1) |
| IT-002 | integration/test_watcher_events.py | Watcher event parsing without agent spawn (no lab required) |
| IT-003 | integration/test_mcp_tools.py | Full MCP tool coverage — all vendors, cache, push_config CRUD (requires lab, skip with NO_LAB=1) |
| IT-004 | integration/test_transport.py | SSH/eAPI/REST transport layer: structured output, cache, timeouts (requires lab, skip with NO_LAB=1) |

## End-to-End Testing

E2E tests (Standalone and On-Call scenarios) are performed manually.
See `testing/manual_testing.md` for the full manual test strategy.
