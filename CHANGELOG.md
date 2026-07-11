# Changelog

All notable changes to shc-toolkit are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.3.1] — 2026-07-11

First release aligned with the SHC API version. Format: `<SHC_API_VERSION>.<toolkit_patch>`.
This release supports SHC API v2.4.3 (129 paths, 156 schemas).

### Added
- Auto-generated Python client from OpenAPI spec (`shc_toolkit.generated`) — 149 endpoint methods, 543 Pydantic models, 100% API coverage. Install with `pip install shc-toolkit[generated]`.
- `scripts/generate_client.sh` — regenerates the auto-generated client from the OpenAPI spec.
- 85 new MCP TOOL_MAP entries (23 → 108) — MCP coverage from 33% to 99% (141/142 server tools).
- 33 new SHCMCPClient wrapper methods for the new TOOL_MAP entries.
- 11 new SHCClient REST methods for v2.4.3 endpoints (VM term/addons, Orders).
- 11 new transport.py ABC method signatures.
- CI auto-creates deduplicated GitHub issues on API drift detection.
- Cross-repo parity CI workflow (`.github/workflows/cross-repo-parity.yml`).
- `resolve_addons` cross-repo contract parity check in `scripts/audit_cross_repo.py`.
- Network-blocking autouse fixture in `tests/conftest.py` — prevents unit tests from leaking real HTTP calls.
- `tests/test_network_fixture.py` — 4 regression tests for the network-blocking fixture.
- `tests/test_ansible.py` — 13 tests for the ansible/ subtree (inventory logic, YAML sanity, bug regressions).
- Molecule caddy scenario with `policy-rc.d` + self-signed cert `prepare.yml`.
- Weekly live E2E workflow (`.github/workflows/ansible-e2e.yml`) — runs full playbook against real SHC Dev VPS.
- 408 Request Timeout is now retried (2026 API resilience reference).
- Auto-generated `Idempotency-Key` header on all POST/PATCH/PUT/DELETE requests.
- `term` attribute on the Terraform VM resource (v2.4.3 VM term management).
- `caddy_manage_service` toggle on the caddy ansible role (for non-systemd environments).
- Pulumi Terraform Bridge migration guide (`MIGRATION-TO-BRIDGE.md` in shc-pulumi).

### Fixed
- `resolve_addons` now raises `ValueError("package_id X not found in catalog")` on unknown packages — was silently returning `{}` (Go provider already had this; Python was drifted).
- 3 flaky tests in `test_unit.py` that leaked real HTTP calls to the SHC API (`_safe_credit` cache invalidation + `get_vm_payments` unmocked path).
- `caddy_manage_service` toggle now correctly gates the `Restart caddy` handler (was only gating the explicit systemd task — handler leaked).
- TOOL_MAP duplicate key: `get_account_balance` was mapped to `getBillingBalance` (original) but overwritten to `getAccountBalance` (addition). Fixed by adding `get_billing_balance` as a separate entry.
- 4 ansible bugs: stale `inventory/shc-hosts.ini` refs, hardcoded `nsec1` prefix strip, missing OS group docs, `caddy_cert_path`/`caddy_domain`/`caddy_key_path` defaults (were defined but audit missed them).
- CI: `permissions: issues: write` was missing `contents: read`, causing `actions/checkout` to fail.
- CI: duplicate `workflow_dispatch:` key under `permissions:` block (YAML parse failure).
- CI: Python `IndentationError` in MCP drift detection script (11-space indent vs 10-space).
- API version corrected from v2.5.0 → v2.4.3 (SHC bot had prematurely labelled the spec).

### Changed
- OpenAPI spec refreshed to v2.4.3 (129 paths, 156 schemas).
- 5 ansible-lint findings fixed (3 `no-changed-when`, 1 `var-naming`, 1 `yaml[line-length]`). 6 `jinja[invalid]` false positives remain baselined.
- `shc_inventory.py` refactored: extracted pure `build_inventory(vms)` function for testability.
- `terraform-provider-shc` gained 10 new Go methods (VM term/addons + Orders).
- `ROADMAP.md` updated: API v2.4.3, 142 MCP tools, 99% coverage, 169 unit tests.
- 3 dependabot PRs merged (actions/checkout v4→v7, setup-python v5→v6, github-script v7→v9).

### Removed
- All NIP-90 DVM code paths from `physical-router-test-automation/docs/app.js` (217 lines, issue #8).
- `terraform-provider-shc/provider/sizes.go.bak` (untracked stale file).

## [0.5.0] — 2026-07-02

Initial public release with:
- SHCClient (REST), SHCMCPClient (MCP Streamable HTTP), dual transport
- VM lifecycle, ordering, snapshots, backups, firewall, rDNS, NoDNS
- CostTracker (balance-diff auditing), Cost audit
- GitHub Actions ephemeral runners
- ContextVM bootstrap
- Ansible integration (playbook + 4 roles + dynamic inventory)
- Cashu tollgate
