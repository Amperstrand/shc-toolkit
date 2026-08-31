# AGENTS.md — SHC Toolkit Maintenance Guide

> **Read this before making any changes to shc-toolkit, terraform-provider-shc, or shc-pulumi.**

## Architecture

Three repos form the SHC IaC ecosystem:

```
shc-toolkit (Python, v2.4.24.0)
├── shc_toolkit/client.py        — SHCClient (REST, httpx, retry, cost tracking, batch helper)
├── shc_toolkit/catalog_model.py — Static catalog model (replaces 10.3MB /ordering/catalog fetch)
├── shc_toolkit/mcp_client.py    — SHCMCPClient (MCP Streamable HTTP, 157/157 TOOL_MAP coverage)
├── shc_toolkit/transport.py     — SHCTransport Protocol (ABC both transports implement)
├── shc_toolkit/generated/       — Auto-generated client from OpenAPI (932 files, 729 attrs models)
├── shc_toolkit/openapi.json     — Cached OpenAPI spec (single source of truth)
├── tests/                       — network-isolated unit tests + gated integration tests
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
12. Run: `SHC_API_KEY=... python3 scripts/validate_catalog_model.py` (verify catalog model still matches live API after any pricing changes).
13. Close the drift issue.
14. **Add a CHANGELOG entry** (see below).
15. **Sweep all docs for stale numbers** — test count, TOOL_MAP size, coverage %. A comprehensive grep prevents the "fix in one place, break in another" pattern that Oracle caught in round 2 of v2.4.24.0 verification.

## Regenerating the auto-generated client

```bash
# Fix known spec quirks first (empty array schemas, duplicate enum keys)
bash scripts/generate_client.sh
```

**Known issues with openapi-python-client v0.29.0:**
- Empty array schemas (`items: []`) in restore-hints and batch endpoints — the script fixes these.
- Duplicate enum keys (e.g., `CLOUD_INIT_POLICY_VIOLATION`) — this is a spec bug on SHC's side. If regeneration fails with "Duplicate key", the generated client stays at the previous spec version. This is fine — the generated client is a bonus (type-safe models), not a dependency. SHCClient works without it.

## CHANGELOG discipline (MANDATORY for all agents)

**Every change that adds a feature, fixes a bug, or alters behavior MUST add a CHANGELOG entry in the SAME commit.** Not as an afterthought, not in a follow-up — in the commit that introduces the change.

### When to add an entry

| Change type | Category | Example |
|-------------|----------|---------|
| New feature, endpoint, file, flag | `Added` | `catalog_model.py` — static catalog model |
| Modified behavior, refactored, config change | `Changed` | `get_catalog()` now returns model data instead of fetching |
| Bug fix, correctness fix | `Fixed` | `submit_order` resolves order_form_id from preview |
| Deleted code, removed feature | `Removed` | Removed disk cache infrastructure |

### Format

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Each repo has its own `CHANGELOG.md`.

Entries go under `## [Unreleased]` → promoted to a version tag on release.

```markdown
### Changed
- **Brief description of what changed.** One paragraph explaining the before/after
  and why. Mention the file or module name.
```

### Checklist before committing

1. Does the CHANGELOG have an entry for THIS change?
2. Is it under `[Unreleased]`?
3. Is the category correct (`Added` / `Changed` / `Fixed` / `Removed`)?
4. Does the entry explain what changed and why (not just what)?
5. If you bumped `pyproject.toml` version, is there a `## [version]` header?

## Documentation audit

**Before committing, check these are not stale:**

1. `pyproject.toml` version matches the spec version (`<API_VERSION>.<patch>`)
2. `ROADMAP.md` — API version, path count, test count, MCP coverage %, TOOL_MAP size
3. `README.md` — testing status section, MCP tool count

## Cross-repo audits

Mechanical parity: `python3 scripts/audit_cross_repo.py` (size maps, billing claims, Dev VPS claims, resolve_addons contract — must be all-pass; it runs in cross-repo-parity CI).

Semantic parity: `docs/cross-repo-audit-prompts.md` contains four AI-agent prompts (behavioral parity, lessons-ported, DRY boundaries, live drift smoke test). Run Prompt 1+2 after every SHC API update, Prompt 3 after refactors, Prompt 4 before tagging.
4. `CHANGELOG.md` — has an entry for the current change
5. `test_core_tool_count` in `tests/test_unit.py` — matches `len(TOOL_MAP)`
6. Cross-repo audit passes: `python3 scripts/audit_cross_repo.py`

## CI workflows (10 total)

**Trigger policy**: nothing runs on push/PR — the API changes rarely and per-commit CI is noise. Everything is `workflow_dispatch` (run on demand) + tag push (`v*`, pre-release verification) + a staggered monthly schedule. No high-frequency jobs remain: the reaper was eased from hourly to daily (2026-08-27) — primary cleanup is the on-VM self-destruct timers plus the lab machine's local cron. To run any suite: `gh workflow run <name>` or ask the agent.

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `shc-tests.yml` | dispatch, tag, monthly (1st) | Unit + smoke + integration + drift detection |
| `api-drift.yml` | dispatch, monthly (1st 08:00) | OpenAPI + llms.txt drift + catalog model validation + live order smoke → auto-creates issue |
| `cross-repo-parity.yml` | dispatch, tag, monthly (2nd) | Size map + resolve_addons contract parity |
| `typecheck.yml` | dispatch, tag | mypy + ruff lint + ruff format check (3 parallel jobs) |
| `coverage.yml` | dispatch, tag | pytest --cov coverage reporting (baseline, no thresholds yet) |
| `security.yml` | dispatch, tag | bandit + safety + pip-audit security scanning |
| `ansible.yml` | dispatch, tag | ansible-lint + molecule caddy scenario |
| `ansible-e2e.yml` | dispatch, monthly (7th) | Full playbook against real SHC Dev VPS |
| `reap-orphan-vms.yml` | daily (05:23) + dispatch | Destroy orphaned test VMs >2h old (3-min timeout, pip-cached, concurrency-guarded) |
| `publish.yml` | tag push (`v*.*.*`) | PyPI publishing (Trusted Publishing) |

## Auto-issue-creation

Both drift jobs in `shc-tests.yml` and the catalog model validation in `api-drift.yml` auto-create deduplicated GitHub issues when drift is detected. The issues include the diff details and action items. Close them after resolving the drift.

## Testing rules

- **Network-blocking fixture** (`tests/conftest.py`): unit tests cannot make real HTTP calls. Mock or use `@pytest.mark.allow_network`.
- **Integration tests** (`tests/test_shc_api.py`): require `SHC_API_KEY` secret, create + destroy real VMs. Run on tag push and monthly schedule.
- **Operate-lane integration test** (`tests/test_nostr_operate_lane.py`): gated on `SHC_OPERATE_LIVE` (a context name owning a VM); read-only — exchanges a grant, reads the VM, asserts 403s. Skips everywhere else.
- **MCP drift detection**: compares `TOOL_MAP` values against live MCP server tool names. Zero broken tools required.

## The network-blocking fixture

`tests/conftest.py` patches BOTH `requests.Session.request` AND `httpx.Client.request` to raise. SHCClient uses httpx; SHCMCPClient uses requests. If a unit test forgets to mock something, the fixture catches it immediately (instead of silently leaking to the live API).

Bypass with `@pytest.mark.allow_network` or `SHC_TEST_LIVE=1` env var.

## Version scheme

- **shc-toolkit**: `<SHC_API_VERSION>.<toolkit_patch>` (e.g., `2.4.24.0`). Tagged as `v2.4.24.0`.
- **terraform-provider-shc**: Independent semver (`v0.1.0`). Does NOT mirror API version.
- **shc-pulumi**: Deprecated. No new versions planned.

## SHC account credentials

Everything lives in `~/.config/shc/credentials.sh` (0600, outside all repos, sourced from `~/.zshrc`): portal/Basic password, auth username, and the key inventory. Live-earned auth facts (2026-08-27):

- **HTTP Basic username is the BARE Blesta username** (`o6XPQHfhFRpoYo7ev`), NOT the account email — full-email Basic 401s identically to a wrong password. The spec's `basicAuth` description warns: "For many accounts the username is the email address, but that is not guaranteed for every account type." This trap caused a full-morning "password was rotated" misdiagnosis (and the 2026-07-16 lockout scare).
- Account/notice email: `npub1ugz9wzvg5lc6thnvzghmxvn9swrtl7nx36lsvl3794sq0r67agls8l6ztt@nomail.name` — a mailbox on OUR OWN nomail.name infrastructure. Password loss is a non-event: trigger `/client/login/reset/`, pull the email from the nomail R2 quarantine (`cd ~/src/nomail/apps/email-worker && npx wrangler r2 object get nomail-emails/quarantine/<id>.eml --remote`), open the confirmreset link — which sets the new password AND auto-creates a logged-in portal session (the normal form-login is broken SHC-side for this account: rejects both the email and the username).
- API key (`SHC_API_KEY` in both repo secrets + `~/.zshenv`): `ci-main` (id 404, full scope, expires 2027-02-23). Suicide key (`SHC_SUICIDE_KEY`, both repos): `ci-self-destruct` (30d, expires 2026-09-26 — re-mint monthly). `full5-domcapture` (id 218, the old CI key) expires 2026-10-01, superseded.
- **Nostr auth cannot replace API keys**: user-api securitySchemes are `basicAuth` (+`X-User-Api-OTP` when 2FA) and API key only; the nostr plugin lane is deliberately vm-scoped cannot-spend (lesson 23). nsec buys portal-login/identity/zk-backup conveniences, not CI auth.

## Operator-skills corpus (llms-full.txt)

`https://blesta.sovereignhybridcompute.com/agent-skills/llms-full.txt` is SHC's
agent-facing contract corpus (header carries `x-shc-release` version, op_count,
fingerprints). Audited 2026-08-26 against v2.4.15 of the corpus (API spec at
2.4.24, 177 ops — no drift). Key contracts it defines that BOTH repos must keep:

- **Confirmation gate**: spend/destructive ops 409 `confirmation_required`
  carrying a single-use `confirmation_id`; re-send the IDENTICAL request with
  header `X-User-Api-Confirm`. `?confirm=true` and body `confirm:true` are NOT
  accepted. Probe mode = `confirm=False` → raise, never auto-resend.
- **Routine ops are NOT gated** (portal parity): power on/off/restart/shutdown/
  reset, mount/unmount ISO, add/edit firewall rule, set rDNS, create
  backup/snapshot, ADD ssh key. Gated: reinstall, restore/delete backup or
  snapshot, cancel, delete firewall rule/ssh key/contact.
- **Nostr operate-lane** (agent side): customer signs `kind:30078` grant
  (`d=shc:agent:<pubkey>`, `scope=operate`, `area=vm:<id>`, `aud`, `nbf`/`exp`);
  agent signs NIP-98 `kind:27235` (`u`/`method`/fresh nonce), `Authorization:
  Nostr <base64>`, POST `/plugin/nostr_auth/main/operate_token` body
  `{"grant": <event>}` → short-TTL (~900s) vm-scoped cannot-spend Bearer
  (403s other services + all spend). Implemented as the module-level
  `exchange_nostr_operate_grant()` (no account key needed — the lane's whole
  point) + `validate_operate_grant()` local pre-check; guide in
  `docs/nostr-operate-lane.md` (v2.4.24.3+).
- **shc-pay BIP21**: credit responses may carry `payment_link` (prefer),
  `bolt11`, `onchain_address` → stitch `bitcoin:<addr>?lightning=<bolt11>` /
  `bitcoin:<addr>` / `lightning:<bolt11>`; none → checkout_url fallback.
  Implemented in `jit_pay.payment_uri()`.
- **Spend is scope-gated**: an `operate` key cannot spend; only `full` keys or
  HTTP Basic.

The terraform provider was audited the same day: confirm-gate, header-only
confirm re-send, active+IP readiness — conformant, no changes required.

## Zero-GUI account onboarding (2026-08-22/23, live-proven)

`shc register` (default: unattended) creates a complete account with ONE
Lightning payment and zero browser-GUI interaction. The generated Nostr
keypair IS the account identity: email `npub…@nomail.name` (free
cashu.email mailbox, readable via `shc mail` with the same key), nostr
link via NIP-98. Contexts (one per account) live at
`~/.config/shc/contexts/<name>.json` (0600): email, password,
client_id, api_key, **nsec** — the nsec is the portable identity and the
recovery/mail key. `shc topup --context <name>` re-funds an existing
account (recovery path); any `shc` command on a TTY with no key offers
the wizard (`SHC_NO_REGISTER`/`--no-register` opt-out; CI/non-TTY
unchanged). First top-up QR **opens in the browser by default**
(`--no-browser` for terminal QR + URL).

**Live-earned SHC API contracts** (all hit during the 2026-08-22/23
E2E; encode, don't re-earn):
- `POST /register` is anonymous; the minted key is capped at
  `operate` scope — mint a `full` key via `POST /account/api-keys` over
  HTTP Basic (fresh accounts have no 2FA, so no OTP header).
- nostr link = NIP-98 kind **27235** with `u`, `method`, `challenge`
  tags (the challenge response's `nip98.required_tags` self-documents).
- `POST /account/credit` amount is a 2-decimal **STRING** (JSON float
  422s); only ONE pending top-up per account (409 conflict until the
  prior invoice pays or lapses).
- order invoices generate **asynchronously** — `invoice_id` is absent
  from the order response; poll `GET /orders` then pay from credit via
  `POST /payment/<id>/checkout` (idempotency key: 16–128 chars,
  `[A-Za-z0-9_-]` — dots REJECTED).
- **end-of-term cancel BEFORE the invoice settles VOIDS it** and wedges
  the service in `pending` forever (no jobs, no invoice). Schedule
  `cancel --end-of-term` only AFTER `provisioning_state: ready`.
- SSH key: order-time `ssh_key` rides the cloud-init seed on every
  tier, but `apply-live` is confirmation-gated (409→confirm) and races
  sshd boot — verify landing via `GET /vm/<id>/ssh-keys` fingerprint,
  retry, and STRIP trailing newlines (SHC silently no-ops otherwise).

## Known limitations

- **NoDNS**: Python-only feature. Not available in the TF provider or TF bridge. Use `shc nodns --ip <ip>` CLI separately.
- **Generated client**: May lag behind the spec if openapi-python-client hits spec bugs. SHCClient always covers the latest endpoints via hand-written methods. Generated client uses **attrs** classes, not Pydantic (openapi-python-client v0.29 default).
- **SHC "ready" fires before cloud-init finishes**: Wait ~120s after `provisioning_state: ready` before assuming full VM configuration.
- **API key lifecycle**: Keys expire after 90 days (max 730). A 401 on a working key means it expired — mint a new one at `/account/api-keys`.
- **Nested KVM**: Available ONLY on **Dev VPS plans** (pkg 80–84, Cherryvale, KS). Empirically verified 2026-07-20: NVMe Starter (pkg 23, Katy-TX) probed via SSH — `vmx/svm` count=0, `/dev/kvm` absent. SSD VPS in same datacenter (Cherryvale-KS) also lacks it. The limitation is plan-type-specific, not region-specific. Verify with `shc kvm-check <service_id>`.
- **Dev zone (issue #28) — RESOLVED 2026-08-25**: Dev VPS (Cherryvale, KS) provisioning recovered; probe verifies pkg 80 in ~90–100s with both debian12 and debian13. If it regresses, `scripts/dev-zone-probe.py` detects it.
- **Identity-class operations**: `revokeApiKey`, `beginTwoFactorEnrollment`, `enableTwoFactor`, `disableTwoFactor`, `changePassword`, `linkNostrIdentity`, `unlinkNostrIdentity`, `updateNip05` are Basic+OTP-only — NOT callable with API keys and NOT exposed by the MCP server. Do NOT add these to TOOL_MAP (the MCP drift CI will flag them). The `x-shc-mcp-exposure: hidden` annotation (20 ops) in the spec marks these.

## Testing Protocol (MANDATORY)

When ANY change is made to shc-toolkit, the following MUST be run:

### 1. Unit Tests
```bash
python3 -m pytest tests/test_unit.py tests/test_github_runner.py tests/test_ansible.py tests/test_network_fixture.py -v --timeout=60
```
All tests must pass. (Exact test counts are deliberately not pinned here — they drift within days; `python3 -m pytest tests/ --collect-only -q` prints the current number.)

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

The daily reaper workflow runs automatically (eased from hourly 2026-08-27; the lab machine's local cron is the fast path). But after manual testing:
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

### 13. debian13-cloud template works fine (earlier deadlock diagnosis was wrong)
`debian13-cloud` was previously thought to deadlock (cloud-init never starts sshd). The actual problem was the **Dev zone scheduler hang** (issue #28). Verified in BOTH directions 2026-08-25: debian13 provisions in Katy TX (NVMe/SSD/HDD) AND in the recovered Cherryvale Dev zone (102s, pkg 80). The default template is `debian13-cloud` everywhere.

**Affected**: Default template on `order_vm()`, `reinstall_with_cloud_init()`, `check_stock()`, CLI `--template` flags.
**Fix**: None needed — root cause was the zone scheduler (resolved 2026-08-25). `scripts/dev-zone-probe.py` guards against regression.

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

### 19. Scripted multi-file edits fail partially and silently
Two incidents in one session: a Python edit script aborted mid-list leaving `cross-repo-parity.yml` unconverted while four sibling files converted (AGENTS.md then documented the intended-but-false state); a trigger-block replacement dropped `workflow_dispatch:` from `integration.yml`, producing valid YAML that GitHub rejects with a 0s failure. Both shipped because the edits *looked* done.

**Affected**: any scripted bulk edit across workflow/config files.
**Fix**: after a scripted multi-file edit, grep for the intended end-state across ALL targets (not the ones the script reported), and exercise the result (e.g. `gh workflow run <name>`) — YAML-valid ≠ workflow-valid.

### 20. VMs bill by existence — stopped is NOT free

SHC charges the full daily price while a service **exists**, regardless of power state. `stop_vm`/`shutdown_vm` save nothing. Cleanup = `cancel_vm(id, immediate=True)`, which also refunds the unused part of the current day. Renewals draw down credit silently — the transaction ledger only records credits/topups (`list_transactions`), and `list_invoices` stays empty, so historical spend is not queryable via the API.

**Affected**: any agent ordering VMs through this toolkit (several projects on the shared lab machine use one account).
**Fix**: cancel every VM in the session that ordered it; never leave a VM `stopped` at task end (incident: `lightning-playground`, stopped 9 days, $3.12); give ephemeral VMs a reaper-reapable hostname prefix (see `reap_orphans()` KEEP/REAP lists); register long-lived VMs in `physical-router-test-automation/config/approved-resources.yaml` and audit with its `scripts/cost-status.py` (exit 1 on unapproved billables).

### 21. Silent `except` blocks hide broken request paths for weeks
`jit_pay.poll_shc_invoice()` shipped with `shc_client._get("/payment/{invoice_id}")` (f-prefix stripped by an old scripted lint pass — the same failure mode as lesson 19) and a broad `except Exception` that printed "Polling error" and kept looping. Result: every zero-balance `shc order --pay` reported a payment timeout even after the wallet paid, for weeks, because the polling loop "worked" (looped, printed, timed out) instead of crashing.

**Affected**: any long-lived loop with except-swallow retry (payment/invoice/readiness polling).
**Fix**: unit-test the exact request path such helpers hit (assert the path string), not just the loop outcome; treat a polling helper that never asserts its request shape as untested. Found by the 2026-08-26 llms-full.txt corpus audit.

### 22. Plugin routes return FLAT error bodies — and live negative testing is how you find out
`POST /plugin/nostr_auth/main/operate_token` (and possibly other `/plugin/...` routes) errors as `{"error": "<string>"}` (e.g. `{"error": "Grant is not bound to this agent key"}`), NOT the nested `{"error": {code, message, ...}}` shape of `/user-api/v2`. `_error_from_body` assumed the nested shape and raised `AttributeError` on the real 403 — unit tests with hand-rolled mocks (which copied the nested shape) could never catch this. Found in minutes by feeding the LIVE server deliberately bad grants: expired (locally rejected pre-HTTP), wrong-agent ("Grant is not bound to this agent key"), forged sig ("Invalid grant signature").

**Affected**: any client code that hits plugin routes or assumes one error-envelope shape.
**Fix**: `_error_from_body` handles both shapes (flat 401/403 strings map to `SHCAuthError`); treat a short live negative pass (expired / wrong-party / forged / replayed) as part of shipping any new API surface — the server's real error envelopes are a contract you haven't learned until you've been rejected by it.

### 23. Cancel is MONEY: only full-scope can destroy; Bearer cannot mint keys; never plant the account key on a VM
Live-probed 2026-08-27: **operate-scope API keys and nostr operate leases both 403 `cancel_vm`** (confirm-gate or not) — cancel refunds/prorates, so it sits in the spend class ("operate = ops but no money/billing"). Separately: **Bearer API keys cannot mint other keys** (`POST /account/api-keys` is forbidden for them; HTTP Basic only). Consequences for self-cleaning VMs (the "suicide token" pattern):

- The token planted on a VM so it can cancel itself MUST be full-scope. Bounded exposure = pre-minted short-expiry key (`SHC_SUICIDE_KEY` secret, CI-friendly) or per-run mint over Basic (`SHC_ACCOUNT_EMAIL`/`SHC_ACCOUNT_PASSWORD`, `expires_in_days=1` minimum) — it self-revokes, since `revokeApiKey` is Basic+OTP-only and a controller key can't revoke it.
- `shc_toolkit/selfdestruct.py` (`arm_self_destruct`) plants key file (0400) + systemd `OnBootSec` timer + stdlib-python cancel script (409→`X-User-Api-Confirm` dance) via one base64 SSH command; `shc github-runner provision --self-destruct-minutes N` wires it. NEVER arm on boxes running untrusted code (tollgate) — the key is account-wide spend for its lifetime.
- **physical-router-test-automation shipped the anti-pattern for months**: its bootstrap planted the FULL ACCOUNT `SHC_API_KEY` on every test VM (env export, sole consumer the inline kill-switch). Now arms the bounded module when a key source is configured; legacy inline switch remains as warned fallback until `SHC_SUICIDE_KEY` is set on the runner.
- `at`-job kill-switches die silently on reboot; systemd timers don't.
- Live-fire proof: VM ordered → armed 4-min timer → self-cancelled at T+216s, $0.01 total (1h minimum). Nostr leases remain exactly the wrong primitive here — poetic: the credential you'd want to leave on a box is the one that can't kill it.

### 24. API keys can READ password-reset emails — treat every key as account-takeover-capable
`GET /emails` (Bearer-callable) returns the full body of every transactional email, including portal **Password Reset** links (verified live 2026-08-27: portal reset request → email id 54189 with the `confirmreset/?sid=…` link appears in `/emails` within seconds).

**The full takeover chain, live-proven on our own account (legitimate self-recovery use):**
1. Working API key (any scope with Email History area — default keys have it) — nothing else needed. Not the password, not the mailbox.
2. Portal `/client/login/reset/` form: anonymous, only needs the account email (readable via `GET /account`).
3. `GET /emails` → newest "Password Reset" → the `confirmreset/?sid=…` link.
4. Open link (single-use, no old password asked) → set a NEW password → portal login succeeds.
5. Logged in: change the account email in the portal (`/client/main/edit/` — applies immediately, **no confirmation to the old address**), mint API keys from the portal API-keys page (`/client/apikeys/`), change 2FA. Attacker now controls password, email, and keys; the owner's mailbox never sees a thing.

**The logical flaw worth reporting to SHC:** identity ops are carefully Basic-gated — `POST /account/password` ("requires the current password"), `PATCH /account/contact` (the only email-changing endpoint, Basic-only), 2FA toggle. But the *effect* of all that gating is void: an API key alone yields both a password change (steps 2-4) and an email change (step 5). If an API key is not allowed to change the password (it isn't), it must not be able to read the emails that reset the password — `GET /emails` should exclude auth/security mail (password resets, 2FA enrollment, login notifications), or those messages should be redacted. Until then: **store every SHC API key with password-grade care**; a leaked key is a full account takeover, not a scoped credential.

- Legitimate self-recovery runbook (dead mailbox, working key): steps 2-5 above; we then pointed the account at a fresh nomail.name mailbox (cashu.email == nomail.name, same worker; `shc mail` reads it with the nsec).
- Portal also supports **Login with Nostr** — an account with a linked nsec can log in passwordless with one signature.
- Quirk (this account only): user-api HTTP Basic rejects email+password ("Authentication failed") even with a correct password the portal accepts — the spec says the Basic username "is the email for many accounts but not guaranteed"; this legacy account (#1522) evidently has a distinct hidden username. Identity ops for it go through the portal; the portal API-keys page can mint keys when Basic is unavailable (that's how the CI `SHC_SUICIDE_KEY` was minted).
- Recovered credentials live in `~/.config/shc/credentials.sh` (0600, outside all repos, sourced from `~/.zshrc`) — see lesson 26.

### 25. shutdown ≠ cancel: SHC bills by service existence — a stopped VM accrues its full price
Owner-caught 2026-08-27: the clboss-soak VM was shut down after a textbook drain contract and the session recorded as done; it sat **stopped-but-billable ~13h** until cancelled (snapshot first — snapshots survive the cancel). `stop`/`shutdown` are pauses; **only `cancel` ends billing.** Guards now standing (defense in depth):

- Point-of-error: `stop_vm`/`shutdown_vm` print "still bills while stopped" (client.py `_warn_billable_while_stopped`, pinned in tests/test_billing_semantics.py).
- Background: `reap_orphans` reaps stopped-and-stale VMs of ANY hostname past `--max-age-hours` (the incident VM matched no test prefix — that was the gap), fail-open on unprobeable VMs; exclude/keep lists always win (628958a).
- Controller-dead: the on-VM self-destruct timer (lesson 23) cancels even when nothing outside the VM is alive — strictly stronger than any workstation TTL, which dies with its launcher anyway (the setsid lesson from playground #44).
- Rule for every agent/playbook: teardown and TTL arms fire **cancel**, never shutdown. Track the class in issue #38 (open remainder: "STILL BILLING" marker in `shc list`, `shc info` cost block).

### 26. Basic-auth username ≠ account email; recovery runs through our own nomail quarantine
2026-08-27: the CI account password was declared "rotated" after a morning of 401s — wrong conclusion. The user-api Basic username is the bare Blesta login (`o6XPQHfhFRpoYo7ev`); testing with a full email (old OR new) 401s exactly like a wrong password, so wrong-username is indistinguishable from wrong-password until you try the variants. The spec's `basicAuth` description documents precisely this ("username is the email address… not guaranteed for every account type").

**Affected**: any Basic-auth path — `mint_suicide_key`, `SHC_ACCOUNT_EMAIL`/`SHC_ACCOUNT_PASSWORD` envs (must carry the USERNAME form), portal Playwright scripts.
**Fix**: before concluding "password changed", test username variants (bare local part, full email, old and new). The working username is recorded in `~/.config/shc/credentials.sh` (`SHC_USER`). Verified recovery loop when the password IS lost: portal `POST /client/login/reset/` → the email lands in OUR nomail.name R2 quarantine (unknown-recipient mail is retained readable: `npx wrangler r2 object get nomail-emails/quarantine/<id>.eml --remote` from `~/src/nomail/apps/email-worker`) → the confirmreset link sets a new password AND auto-creates a logged-in portal session — GUI access without the (currently SHC-broken) form login. The account's notice email was also re-pointed to `npub…@nomail.name`, anchoring all future reset mail to infrastructure we control. Bonus lesson: `GET /account` via Bearer is the cheapest account-identity check; `gh secret list` timestamps are the cheapest "who changed what when" forensic signal when a parallel actor is suspected.

### 27. "Zone fixed" ≠ zone usable — verify end-to-end reachability, not API state; and fork-PR green is not artifacts
Earned 2026-08-27/28 running the PRTA cloud lab against a freshly-repaired Dev zone (issue #28 closed 08-25 as fixed).

- **Billing-state lies.** Dev VMs ordered post-fix reach `active/ready` with IPs in the NEW subnet `64.188.7.0/24` (the old `66.92.204.0/24` range is gone), but are unroutable from every vantage — including **cross-zone from a Katy-TX VM inside SHC itself** (`Network is unreachable`), and `/vm/{id}/detail` 404s right after order (hypervisor-registration gap; matches the #24 comment). "Ready" was a billing state, not a running VM. Evidence matrix filed on #28 (2026-08-28).
- **Trier-of-last-resort is wrong.** NVMe/HDD (Katy, reachable ~150ms) have **no `/dev/kvm` and no vmx flags** — probed live. Only the Dev tier has nested KVM, and Dev is bound to Cherryvale via `module_group_id`; the catalog exposes no Dev option in a reachable zone. If a nested-KVM workload matters, ask SHC to expose the Dev tier in Katy before assuming "a reachable zone" exists.
- **Fork-PR green is an illusion.** `Build and Publish` on a fork PR resolves SUCCESS with every packaging job SKIPPED (secrets withheld from fork PRs) — zero artifacts, zero Blossom events. Cloud-lab deploys against such a PR time out in `ensure_artifact`. Mirror the PR head to a same-repo branch to get a real build (and note `publish-metadata` needs ALL package jobs — one failing leg skips the whole publish).
- **Agent footguns in one session**: `pkill -f "cloud-lab.py submit"` matched the agent's own `bash -c` cmdline and killed the session mid-heredoc (twice). Kill by explicit PID from `ps`, never `pkill -f` with a pattern your own command contains. Long-lived submits need `setsid nohup ... < /dev/null` AND a tmux/interactive parent — bare nohup from a tool runner dies with the process group.
- Working probe recipe (kept in PRTA `scripts/` history): order 1 Dev VM, poll `list_vms` (NOT `/vm/{id}/detail` — 404 until registered) for ip, then ICMP + TCP/22, plus a Katy control VM for cross-zone isolation. Cancel immediately on any negative result — Dev VMs bill from order acceptance.
