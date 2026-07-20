# AGENTS.md — SHC Toolkit Maintenance Guide

> **Read this before making any changes to shc-toolkit, terraform-provider-shc, or shc-pulumi.**

## Architecture

Three repos form the SHC IaC ecosystem:

```
shc-toolkit (Python, v2.4.24.0)
├── shc_toolkit/client.py        — SHCClient (REST, httpx, retry, cache, cost tracking, batch helper)
├── shc_toolkit/mcp_client.py    — SHCMCPClient (MCP Streamable HTTP, 157/157 TOOL_MAP coverage)
├── shc_toolkit/transport.py     — SHCTransport Protocol (ABC both transports implement)
├── shc_toolkit/generated/       — Auto-generated client from OpenAPI (932 files, 729 attrs models)
├── shc_toolkit/openapi.json     — Cached OpenAPI spec (single source of truth)
├── tests/                       — 310+ unit tests + 4 integration tests
├── ansible/                     — Ansible roles + dynamic inventory
├── scripts/                     — Codegen, audit, reaper, subnet-probe utilities
├── docs/                        — 10 guides (webhooks, agent-sessions, cloud-init, firecracker, ...)
└── .github/workflows/           — 9 CI workflows

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
4. Add MCP tools to `TOOL_MAP` in `shc_toolkit/mcp_client.py` + add SHCMCPClient methods. **Check `x-shc-mcp-exposure`** — 20 ops are `hidden` (identity-class, not API-key callable, not MCP-exposed). Do NOT add these to TOOL_MAP.
5. Add method signatures to `shc_toolkit/transport.py` (the Protocol ABC).
6. Add Go methods to `terraform-provider-shc/provider/client.go`.
7. Update `tests/test_unit.py` — bump `test_core_tool_count` to match new TOOL_MAP size.
8. Run: `python3 -m pytest tests/test_unit.py tests/test_github_runner.py tests/test_ansible.py tests/test_network_fixture.py`
9. Run: `ruff check shc_toolkit/ && ruff format --check shc_toolkit/` (AGENTS.md mandates both).
10. Run: `mypy shc_toolkit/ --ignore-missing-imports --no-strict-optional`
11. Run: `python3 scripts/audit_cross_repo.py`
12. Close the drift issue.
13. **Add a CHANGELOG entry** (see below).
14. **Sweep all docs for stale numbers** — test count, TOOL_MAP size, coverage %. A comprehensive grep prevents the "fix in one place, break in another" pattern that Oracle caught in round 2 of v2.4.24.0 verification.

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

## CI workflows (9 total)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `shc-tests.yml` | push, PR, schedule (6h) | Unit + smoke + integration + drift detection |
| `api-drift.yml` | schedule (daily 08:00) | OpenAPI + llms.txt drift → auto-creates issue |
| `cross-repo-parity.yml` | push, PR, schedule (weekly) | Size map + resolve_addons contract parity |
| `typecheck.yml` | push, PR | mypy + ruff lint + ruff format check (3 parallel jobs) |
| `coverage.yml` | push, PR | pytest --cov coverage reporting (baseline, no thresholds yet) |
| `security.yml` | push, PR (main) | bandit + safety + pip-audit security scanning |
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

- **shc-toolkit**: `<SHC_API_VERSION>.<toolkit_patch>` (e.g., `2.4.24.0`). Tagged as `v2.4.24.0`.
- **terraform-provider-shc**: Independent semver (`v0.1.0`). Does NOT mirror API version.
- **shc-pulumi**: Deprecated. No new versions planned.

## SHC account credentials

The SHC API key is stored in `SHC_API_KEY` environment variable. It is separate from the portal password. We do NOT store the portal password anywhere in the codebase. The API key has full-scope access (ordering, cancellation, billing).

## Known limitations

- **NoDNS**: Python-only feature. Not available in the TF provider or TF bridge. Use `shc nodns --ip <ip>` CLI separately.
- **Generated client**: May lag behind the spec if openapi-python-client hits spec bugs. SHCClient always covers the latest endpoints via hand-written methods. Generated client uses **attrs** classes, not Pydantic (openapi-python-client v0.29 default).
- **SHC "ready" fires before cloud-init finishes**: Wait ~120s after `provisioning_state: ready` before assuming full VM configuration.
- **API key lifecycle**: Keys expire after 90 days (max 730). A 401 on a working key means it expired — mint a new one at `/account/api-keys`.
- **Nested KVM**: Available ONLY on **Dev VPS plans** (pkg 80–84, Cherryvale, KS). Empirically verified 2026-07-20: NVMe Starter (pkg 23, Katy-TX) probed via SSH — `vmx/svm` count=0, `/dev/kvm` absent. SSD VPS in same datacenter (Cherryvale-KS) also lacks it. The limitation is plan-type-specific, not region-specific. Verify with `shc kvm-check <service_id>`.
- **debian13-cloud template deadlock**: As of 2026-07-20, the `debian13-cloud` template's cloud-init deadlocks — sshd never starts, all key-injection methods fail. Workaround: use `debian12-cloud` or `ubuntu2404-cloud`. This is an SHC platform bug, not a toolkit bug (see issue #24).
- **Identity-class operations**: `revokeApiKey`, `beginTwoFactorEnrollment`, `enableTwoFactor`, `disableTwoFactor`, `changePassword`, `linkNostrIdentity`, `unlinkNostrIdentity`, `updateNip05` are Basic+OTP-only — NOT callable with API keys and NOT exposed by the MCP server. Do NOT add these to TOOL_MAP (the MCP drift CI will flag them). The `x-shc-mcp-exposure: hidden` annotation (20 ops) in the spec marks these.

## Testing Protocol (MANDATORY)

When ANY change is made to shc-toolkit, the following MUST be run:

### 1. Unit Tests
```bash
python3 -m pytest tests/test_unit.py tests/test_github_runner.py tests/test_ansible.py tests/test_network_fixture.py -v --timeout=60
```
All tests must pass. Currently 310 tests (unit) + 4 integration tests.

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

## Lessons Learned (2026-07-20 Session)

### 1. SHC provisioning_state NEVER becomes "ready"
SHC VMs report `provisioning_state: "provisioning"` FOREVER — even the production europa-vpn-vps (running 17+ days) shows this. Never wait for `provisioning_state == "ready"`. Instead, check `service_status == "active"` AND `ips` array is non-empty.

**Affected**: shc-pulumi `_wait_for_ready()`, any code polling SHC VM state.
**Fix**: `if svc == "active" and ips: return vm`

### 2. GitHub Actions timeout kills cleanup code
When a workflow is cancelled (timeout), `terraform destroy` and other cleanup steps never run. Always use `if: always()` for cleanup steps.

**Affected**: terraform-provider-shc acceptance tests, shc-pulumi integration tests.
**Fix**: `if: always()` step that calls `reap_orphans()`.

### 3. Test VMs leak credits when CI is cancelled
Orphaned VMs (tf-acc-*, tollgate-*, ci-*) accumulate when CI runs are interrupted. The hourly reaper workflow destroys VMs older than 2 hours with test hostname prefixes.

**Pattern**: `client.reap_orphans(max_age_hours=2.0, dry_run=False)`

### 4. reqwest timeout breaks wiremock tests
Setting `.timeout()` on reqwest::Client causes wiremock mock server requests to immediately fail with TimedOut. Keep `BlossomClient::new()` timeout-free for tests; use `BlossomClient::with_timeout()` for production.

**Affected**: blossomfs HTTP timeout feature.
**Fix**: Two constructors — `new()` (no timeout, for tests) and `with_timeout()` (for FUSE operations).

### 5. FIPS config format changes between branches
The BleConfig struct has `#[serde(deny_unknown_fields)]`. Old configs with fields like `send_rate_bps`, `conn_param_*`, `srtt_reconnect_threshold_ms` cause parse failures when the struct is simplified. Always update `/etc/fips/fips.yaml` when switching branches.

**Affected**: fips production daemon restart after branch switch.
**Fix**: Strip unknown fields from config, or remove `deny_unknown_fields`.

### 6. ESP8266 has WiFi but NO Bluetooth
The ESP8266 (L106 core) has 802.11 WiFi hardware but does NOT have BLE/BT. Only ESP32 (LX6 core) and later have BLE. A full microfips Rust port is impossible on ESP8266 (no Rust WiFi driver, no Embassy support, 50KB RAM). The ESP8266 works as a WiFi UDP relay.

**Tested**: Full FIPS protocol stack through ESP8266 WiFi relay — 84 packets, 0% loss.

### 7. Delegation headers need all symbols exported
When a module delegates to tollgate_lab via try/except, ALL referenced symbols must be in the try block. Missing constants (like `HARDWARE_LOCK`) cause silent fallback to local code, which may have different paths.

**Pattern**: Test with `function_from_lib is function_from_tollgate_lab` → must be `True`.

### 8. `__future__` imports must be the first line
Python requires `from __future__ import annotations` to be the very first statement. Delegation headers placed before it cause SyntaxError.

**Fix**: Put `from __future__` at the very top, before docstrings and delegation headers.

### 9. openapi-python-client generates attrs, NOT Pydantic
The generated client (`shc_toolkit/generated/`) uses **attrs** classes, not Pydantic v2 BaseModel. Verified via `attrs.has(GetOrderResponse200Data) == True`, `issubclass(pydantic.BaseModel) == False`. Previous docs erroneously claimed "Pydantic models" since v2.4.3.1 — corrected in v2.4.24.0.

**Affected**: CHANGELOG, README, ROADMAP — all corrected in v2.4.24.0.
**Fix**: When documenting generated client models, say "attrs models" not "Pydantic models".

### 10. Batch API requires bare JSON array + Idempotency-Key
`POST /batch` expects the request body as a **bare JSON array** (`[{...}, {...}]`), NOT wrapped in `{"items": [...]}`. It also requires the `Idempotency-Key` header (replaying the same key returns the cached response). The `_post` helper wraps data in `json=data or {}` which breaks the bare array format — use `_request("POST", "/batch", json=requests, headers={"Idempotency-Key": ...})` directly.

**Affected**: `SHCClient.batch()` helper.
**Fix**: Use `_request` with explicit `json=requests` (bare list) + generated Idempotency-Key header.

### 11. MCP confirm=False probe mode now works on both transports
`SHCMCPClient.call_tool` now honors the `confirm` parameter: when `confirm=False`, it raises `SHCConfirmationRequiredError` instead of auto-retrying. This matches REST's behavior. All 17 SHCMCPClient wrapper methods pass `confirm=confirm` through. The Protocol docstring documents this parity.

**Affected**: Any transport-agnostic code using `confirm=False` for probe mode.
**Fix**: No action needed — the divergence that existed before v2.4.24.0 is resolved.

### 12. TOOL_MAP coverage gaps — SHCMCPClient methods can exist without TOOL_MAP entries
SHCMCPClient methods that call `call_tool("toolName", ...)` directly work correctly even WITHOUT a TOOL_MAP entry — they just aren't counted in `test_core_tool_count` and don't appear in the MCP coverage report. When auditing coverage, check BOTH: (a) does the SHCMCPClient method exist? (b) is there a TOOL_MAP entry for it?

**Affected**: `test_core_tool_count`, MCP drift CI coverage report.
**Fix**: When adding new MCP wrappers, always add BOTH the method AND the TOOL_MAP entry.

### 13. debian13-cloud template cloud-init deadlock
The `debian13-cloud` template's cloud-init deadlocks — sshd never starts. All key-injection methods fail (`ssh_key` in order → key baked but sshd never starts; `apply_ssh_key_live` → 409 guest agent not running; `get_vm_credentials` → returns creds but SSH unreachable). This is an SHC platform bug, not a toolkit bug.

**Affected**: ALL new VMs ordered with debian13-cloud template since ~2026-07-19.
**Fix**: Use `debian12-cloud` or `ubuntu2404-cloud` until SHC fixes the template. See issue #24.

### 14. Cloud-init API uses /virtual-machines/{id} path convention
Cloud-init endpoints use `/virtual-machines/{virtualMachineId}/cloud-init/...` — NOT the standard `/vm/{serviceId}/...` convention used everywhere else in the API. The value is the same `service_id`, only the URL path shape differs.

**Affected**: `validate_vm_cloud_init`, `update_vm_cloud_init`, `delete_vm_cloud_init`.
**Fix**: Don't "normalize" these paths to match convention — they are correct as-is per the spec.

### 15. Identity-class operations are Basic+OTP-only
Per SHC v2.4.13: `revokeApiKey`, `beginTwoFactorEnrollment`, `enableTwoFactor`, `disableTwoFactor`, `changePassword`, `linkNostrIdentity`, `unlinkNostrIdentity`, `updateNip05` are Basic-auth-plus-OTP identity operations. They are NOT callable with API keys and NOT exposed by the MCP server. The `x-shc-mcp-exposure: hidden` annotation marks these.

**Affected**: TOOL_MAP, MCP drift CI.
**Fix**: Do NOT add identity-class ops to TOOL_MAP. If added by mistake, the MCP drift CI will flag them within one run (issue #23 pattern).

### 16. Ralph loop interference — parallel commits can create confusion
A background ralph-loop agent may commit in parallel during a long session, sometimes sweeping up uncommitted changes from the main agent's working tree. Always check `git log --oneline -5` before committing to verify no unexpected commits appeared. The ralph loop's commits have descriptive messages but may not match the main agent's intent.

**Affected**: Any long-running session with the ralph loop active.
**Fix**: Check git log before committing. If the ralph loop committed your changes under a different message, either accept it or post a correction commit.

### 17. Subnet outage monitoring pattern
When a subnet-level outage occurs (e.g., 66.92.204.0/24), use `scripts/subnet-probe.py` to monitor and auto-reply to the support ticket when the VM recovers. The probe polls TCP port 22 every 60 seconds and posts a recovery notice with outage duration.

**Affected**: VM reachability during network outages.
**Fix**: `nohup python3 scripts/subnet-probe.py --service-id <id> --ticket-id <id> &`

### 18. Nested KVM empirically verified on non-Dev plans
NVMe Starter (pkg 23, Katy-TX) probed via SSH on 2026-07-20: `grep -c 'vmx|svm' /proc/cpuinfo` = 0, `/dev/kvm` absent. Confirms the documented limitation: only Dev VPS plans (pkg 80-84) expose VMX/SVM to guests. SSD VPS in the same datacenter (Cherryvale-KS) also lacks it — the limitation is plan-type-specific, not region-specific.

**Affected**: Firecracker PoC, QEMU/KVM-in-VM, any nested virtualization use case.
**Fix**: Always order Dev VPS plans (pkg 80-84) for nested KVM workloads. Verify with `shc kvm-check <service_id>`.
