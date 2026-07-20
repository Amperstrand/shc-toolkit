# AGENTS.md — SHC Toolkit Maintenance Guide

> **Read this before making any changes to shc-toolkit, terraform-provider-shc, or shc-pulumi.**

## Architecture

Three repos form the SHC IaC ecosystem:

```
shc-toolkit (Python, v2.4.15.1)
├── shc_toolkit/client.py        — SHCClient (REST, httpx, retry, cache, cost tracking)
├── shc_toolkit/mcp_client.py    — SHCMCPClient (MCP Streamable HTTP transport)
├── shc_toolkit/transport.py     — SHCTransport Protocol (ABC both transports implement)
├── shc_toolkit/generated/       — Auto-generated client from OpenAPI (openapi-python-client)
├── shc_toolkit/openapi.json     — Cached OpenAPI spec (single source of truth)
├── tests/                       — 207+ tests (unit, ansible, network fixture, integration)
├── ansible/                     — Ansible roles + dynamic inventory
├── scripts/                     — Codegen, audit, reaper utilities
└── .github/workflows/           — 7 CI workflows

terraform-provider-shc (Go, v0.1.0)
├── provider/client.go           — SHCClient (Go HTTP client)
├── provider/vm_resource.go      — VM resource with schema versioning
└── provider/*_test.go           — 57+ unit tests + 4 TF_ACC acceptance tests

shc-pulumi (Python, maintenance mode)
└── src/shc_pulumi/              — Dynamic provider (deprecated → use TF Bridge)
```

## When SHC ships an API update

1. **The drift detection CI will auto-create a GitHub issue** with the diff.
2. Refresh the spec: `curl -sS https://blesta.sovereignhybridcompute.com/user-api/openapi.json > shc_toolkit/openapi.json`
3. Wrap new endpoints in `shc_toolkit/client.py` (REST methods).
4. Add MCP tools to `TOOL_MAP` in `shc_toolkit/mcp_client.py` + add SHCMCPClient methods.
5. Add method signatures to `shc_toolkit/transport.py` (the Protocol ABC).
6. Add Go methods to `terraform-provider-shc/provider/client.go`.
7. Update `tests/test_unit.py` — bump `test_core_tool_count` to match new TOOL_MAP size.
8. Run: `python3 -m pytest tests/test_unit.py tests/test_github_runner.py tests/test_ansible.py tests/test_network_fixture.py`
9. Run: `mypy shc_toolkit/ --ignore-missing-imports --no-strict-optional`
10. Run: `python3 scripts/audit_cross_repo.py`
11. Close the drift issue.
12. **Add a CHANGELOG entry** (see below).

## Regenerating the auto-generated client

```bash
# Fix known spec quirks first (empty array schemas, duplicate enum keys)
bash scripts/generate_client.sh
```

**Known issues with openapi-python-client v0.29.0:**
- Empty array schemas (`items: []`) in restore-hints and batch endpoints — the script fixes these.
- Duplicate enum keys (e.g., `CLOUD_INIT_POLICY_VIOLATION`) — this is a spec bug on SHC's side. If regeneration fails with "Duplicate key", the generated client stays at the previous spec version. This is fine — the generated client is a bonus (type-safe models), not a dependency. SHCClient works without it.

## CHANGELOG discipline

**Every commit that adds a feature or fixes a bug MUST add a CHANGELOG entry.**

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Each repo has its own `CHANGELOG.md`.

Entry goes under `[Unreleased]` → promoted to a version tag on release.

Categories: `Added`, `Changed`, `Fixed`, `Removed`.

## Documentation audit

**Before committing, check these are not stale:**

1. `pyproject.toml` version matches the spec version (`<API_VERSION>.<patch>`)
2. `ROADMAP.md` — API version, path count, test count, MCP coverage %, TOOL_MAP size
3. `README.md` — testing status section, MCP tool count
4. `CHANGELOG.md` — has an entry for the current change
5. `test_core_tool_count` in `tests/test_unit.py` — matches `len(TOOL_MAP)`
6. Cross-repo audit passes: `python3 scripts/audit_cross_repo.py`

## CI workflows (7 total)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `shc-tests.yml` | push, PR, schedule (6h) | Unit + smoke + integration + drift detection |
| `api-drift.yml` | schedule (daily 08:00) | OpenAPI + llms.txt drift → auto-creates issue |
| `cross-repo-parity.yml` | push, PR, schedule (weekly) | Size map + resolve_addons contract parity |
| `typecheck.yml` | push, PR | mypy type checking |
| `ansible.yml` | push, PR | ansible-lint + molecule caddy scenario |
| `ansible-ease.yml` | schedule (weekly) | Full playbook against real SHC Dev VPS |
| `publish.yml` | tag push (`v*.*.*`) | PyPI publishing (Trusted Publishing) |

## Auto-issue-creation

Both drift jobs in `shc-tests.yml` auto-create deduplicated GitHub issues when drift is detected. The issues include the diff details and action items. Close them after resolving the drift.

## Testing rules

- **Network-blocking fixture** (`tests/conftest.py`): unit tests cannot make real HTTP calls. Mock or use `@pytest.mark.allow_network`.
- **Integration tests** (`tests/test_shc_api.py`): require `SHC_API_KEY` secret, create + destroy real VMs. Run on push and schedule.
- **MCP drift detection**: compares `TOOL_MAP` values against live MCP server tool names. Zero broken tools required.

## The network-blocking fixture

`tests/conftest.py` patches BOTH `requests.Session.request` AND `httpx.Client.request` to raise. SHCClient uses httpx; SHCMCPClient uses requests. If a unit test forgets to mock something, the fixture catches it immediately (instead of silently leaking to the live API).

Bypass with `@pytest.mark.allow_network` or `SHC_TEST_LIVE=1` env var.

## Version scheme

- **shc-toolkit**: `<SHC_API_VERSION>.<toolkit_patch>` (e.g., `2.4.15.1`). Tagged as `v2.4.15.1`.
- **terraform-provider-shc**: Independent semver (`v0.1.0`). Does NOT mirror API version.
- **shc-pulumi**: Deprecated. No new versions planned.

## SHC account credentials

The SHC API key is stored in `SHC_API_KEY` environment variable. It is separate from the portal password. We do NOT store the portal password anywhere in the codebase. The API key has full-scope access (ordering, cancellation, billing).

## Known limitations

- **NoDNS**: Python-only feature. Not available in the TF provider or TF bridge. Use `shc nodns --ip <ip>` CLI separately.
- **Generated client**: May lag behind the spec if openapi-python-client hits spec bugs. SHCClient always covers the latest endpoints via hand-written methods.
- **SHC "ready" fires before cloud-init finishes**: Wait ~120s after `provisioning_state: ready` before assuming full VM configuration.
- **API key lifecycle**: Keys expire after 90 days (max 730). A 401 on a working key means it expired — mint a new one at `/account/api-keys`.

## Testing Protocol (MANDATORY)

When ANY change is made to shc-toolkit, the following MUST be run:

### 1. Unit Tests
```bash
python3 -m pytest tests/ -v --timeout=60
```
All tests must pass. Currently 213 tests (207 existing + 6 reap_orphans).

### 2. Lint
```bash
ruff check shc_toolkit/
ruff format --check shc_toolkit/
```
Both must be clean (zero errors).

### 3. Live API Smoke Test (when SHC_API_KEY is available)
```bash
export SHC_API_KEY=<key>
python3 -c "
from shc_toolkit.client import SHCClient
c = SHCClient(api_key=os.environ['SHC_API_KEY'])
vms = c.list_vms()
print(f'API OK: {len(vms)} VMs')
orphans = c.reap_orphans(dry_run=True)
print(f'Reap dry-run: {len(orphans)} orphans')
"
```

### 4. Verify No VMs Are Leaking
```bash
shc reap --dry-run
```
Should report "No orphaned VMs found" in a clean state.

### Downstream Projects

Changes to shc-toolkit affect these projects — verify they still work:
- **shc-pulumi**: `pip install -e . && python3 -m pytest tests/` (95 tests)
- **terraform-provider-shc**: `make testacc` (needs SHC_API_KEY, creates real VMs)
- **physical-router-test-automation**: depends on shc-toolkit via cloud_lab
- **tollgate-lab**: depends on shc-toolkit via tollgate_lab.cloud.shc

### When to Reap Orphaned VMs

The hourly reaper workflow runs automatically. But after manual testing:
```bash
shc reap  # destroys test VMs older than 2 hours
shc reap --max-age-hours 0  # destroy ALL test VMs immediately
```
