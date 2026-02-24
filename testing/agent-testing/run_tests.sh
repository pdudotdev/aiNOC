#!/usr/bin/env bash
# aiNOC Agent Test Suite Runner
# Usage: ./run_tests.sh [unit|integration|all]
#
# unit        — no device connectivity, fast (~seconds)
# integration — read-only device queries (~1 min)
# all         — unit + integration

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-all}"

echo "========================================"
echo " aiNOC Agent Test Suite"
echo " Mode: ${MODE}"
echo " Dir:  ${SCRIPT_DIR}"
echo "========================================"

# Ensure we're running from the agent-testing directory
cd "${SCRIPT_DIR}"

# Check dependencies
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "ERROR: pytest not found. Run: pip install -r /home/mcp/mcp-project/requirements.txt"
    exit 1
fi

PASS=0
FAIL=0
ERRORS=()

run_pytest() {
    local label="$1"
    local path="$2"

    echo ""
    echo "── ${label} ────────────────────────────────"
    if python3 -m pytest "${path}" -v 2>&1; then
        PASS=$((PASS + 1))
        echo "  [PASS] ${label}"
    else
        FAIL=$((FAIL + 1))
        ERRORS+=("${label}")
        echo "  [FAIL] ${label}"
    fi
}

case "${MODE}" in
    unit)
        run_pytest "UT-001 SLA Patterns"     "unit/test_sla_patterns.py"
        run_pytest "UT-002 Platform Map"     "unit/test_platform_map.py"
        run_pytest "UT-003 Drain Mechanism"  "unit/test_drain_mechanism.py"
        ;;

    integration)
        run_pytest "IT-001 MCP Connectivity"  "integration/test_mcp_connectivity.py"
        run_pytest "IT-002 Watcher Events"    "integration/test_watcher_events.py"
        run_pytest "IT-003 MCP Tools"         "integration/test_mcp_tools.py"
        ;;

    all)
        run_pytest "UT-001 SLA Patterns"      "unit/test_sla_patterns.py"
        run_pytest "UT-002 Platform Map"      "unit/test_platform_map.py"
        run_pytest "UT-003 Drain Mechanism"   "unit/test_drain_mechanism.py"
        run_pytest "IT-001 MCP Connectivity"  "integration/test_mcp_connectivity.py"
        run_pytest "IT-002 Watcher Events"    "integration/test_watcher_events.py"
        run_pytest "IT-003 MCP Tools"         "integration/test_mcp_tools.py"
        ;;

    *)
        echo "Usage: $0 [unit|integration|all]"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo " Results: ${PASS} passed, ${FAIL} failed"
if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo " Failed:"
    for e in "${ERRORS[@]}"; do
        echo "   - ${e}"
    done
fi
echo "========================================"

if [[ ${FAIL} -gt 0 ]]; then
    exit 1
fi
