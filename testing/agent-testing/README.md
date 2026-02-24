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

### Integration Tests (read-only, real devices)
| ID | File | Description |
|----|------|-------------|
| IT-001 | integration/test_mcp_connectivity.py | MCP tool reachability |
| IT-002 | integration/test_watcher_events.py | Watcher event parsing without agent spawn |
| IT-003 | integration/test_mcp_tools.py | Full MCP tool coverage (all vendors, cache behavior) |

## End-to-End Testing

E2E tests (Standalone and On-Call scenarios) are performed manually.
See `testing/manual_testing.md` for the full manual test strategy.
