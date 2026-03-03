# Changelog

All notable changes to this project are documented in this file.

---

## [v4.0.0]

> Major **quality, reliability, and security** release.  
> No new protocols or vendors — hardened foundation for v5.0.

### 🔐 Security & Safety
- Enforced maintenance windows in `push_config` (blocked outside policy)
- Restricted `run_show` to read-only commands (no config bypass)
- RouterOS REST validation (forbidden paths blocked, POST rejected)
- Syslog prompt injection mitigation (sanitize + delimiter)
- Expanded forbidden command set (5 → 14 patterns)
- Configurable TLS/SSL per transport:
  - `VERIFY_TLS`
  - `ROUTEROS_USE_HTTPS`
  - `SSH_STRICT_HOST_KEY`

### 🏗 Architecture
- Decomposed monolithic `MCPServer.py` (798 lines) into:
  - `tools/`
  - `transport/`
  - `core/`
  - `input_models/`
- Implemented bounded LRU cache (256 entries, TTL-based eviction)
- Added connection pooling for eAPI and REST transports
- Enforced HTTP timeouts on all device and Jira connections
- Added structured JSON logging with configurable levels

### 🧠 Troubleshooting Methodology
- Introduced **6 Core Troubleshooting Principles** (mandatory, ordered) — see `CLAUDE.example.md`
- Rewrote Standalone Mode into 10 deterministic steps with decision gates
- Added protocol skill prerequisite gates (interfaces + neighbors verified before deep investigation)
- Implemented role-aware risk assessment using `INTENT.json` and SLA paths

### 🚨 On-Call & Operational
- SLA recovery (Up) event detection and logging
- Added daemon mode (`-d` flag) with tmux session support
- Added systemd service file (`oncall/oncall-watcher.service`) for production deployment
- Added pre-change snapshot support in `push_config`
- Generated rollback advisory for all config changes

### 🧪 Testing
- 230 unit tests across 9 test files (up from 3 in v3.0)
- 4 integration test files with `NO_LAB` skip guards
- 12 manual E2E scenarios:
  - 7 standalone
  - 1 on-call
  - 1 maintenance window
  - 3 watcher
- Enforced Pydantic `Literal` validation on all query parameters

---

## [v3.0.0]

> Focus: Multi-mode operations, improved diagnosis flow, optimized AI performance, reduced hallucinations and costs.

### 🧠 AI & Workflow Improvements
- Added `mcp_tool_map.json` for improved MCP tool selection
- Updated `INTENT.json` for cleaner network context
- Added `CLAUDE.md` with defined workflows and guidance
- Added troubleshooting skills for improved coherence
- Added `cases.md` and `lessons.md` (see `/cases.example`)
- aiNOC now documents cases and curates reusable lessons

### 🧪 Testing & Quality
- Well-defined test suites
- Regression test checklist

### 🌐 Enhancements
- Added MikroTik API reference
- Minor bug fixes

---

## [v2.0.0]

> Focus: Topology expansion, MCP toolset improvements, optimized AI performance, reduced hallucinations and costs, beyond SSH connectivity.

### 🧠 AI & Tooling Improvements
- Structured outputs:
  - Cisco: Genie
  - Arista: eAPI
  - MikroTik: REST API
- Strict command determinism:
  - `platform_map`
  - Query enums in input models
  - Platform-aware commands
- Tool caching to prevent duplicate commands and troubleshooting loops
- Protocol-specific MCP tools
- Targeted config sections (avoiding full `show run` dumps)
- Updated `INTENT.json` and `NETWORK.json`
- Legacy `run_show` tool now fallback-only
- Improved tool docstrings

### 🌐 Platform & Protocol Expansion
- Routers: 20
- MCP tools: 14
- New vendor: MikroTik
- New protocol: BGP
- Cisco: Genie parsing
- Arista: eAPI (replacing SSH)
- MikroTik: REST API queries
- Platform command map
- Improved topology diagram

### 🏗 Architecture & Code Quality
- Cleaner, modular codebase
- Enhanced `INTENT.json`
- Minor bug fixes

---

## [v1.0.0]

### 🚀 Initial Release
- Routers: 11
- Protocols: 2 (OSPF, EIGRP)
- Vendors: 2 (Arista, Cisco)
- MCP server tools: 6