# SHC Tooling Roadmap

Goal: Make SHC the easiest bitcoin-native VPS to manage with infrastructure-as-code.
Target: parity with DigitalOcean/Hetzner/Vultr tooling quality.

## Current State (2026-07-11)

| Repo | Tests | CI | Key Features |
|------|-------|----|-------------|
| shc-toolkit | 207 unit + mypy | Push + daily (REST+MCP) + OpenAPI drift + MCP drift + cross-repo parity + typecheck + ansible + publish | Spec-encoding sizes, config options, cost audit, MCP transport (157 tools, 99% wrapped), v2.4.3, catalog generator, auto-generated client (718 files, 100% endpoints), idempotency keys, 408 retry |
| shc-pulumi | 95 unit | Push + CI | Spec-encoding sizes, config options, snapshots, backups, firewall, rDNS, NoDNS. TF Bridge migration guide published. |
| terraform-provider-shc | 57 unit | Push + CI + integration | Spec-encoding sizes, config options, cost audit, snapshots, backups, firewall, rDNS, VM term attribute |

### API version: v2.4.15 (148 paths)
### Toolkit version: 2.4.15.1 (API-aligned: `<SHC_API_VERSION>.<toolkit_patch>`)

## Completed Work

### v2.4.15.1 Release (2026-07-11)
- **MCP coverage**: 33% → 99% (141/142 tools, 124 TOOL_MAP entries)
- **Auto-generated Python client**: 718 files from OpenAPI spec (149 endpoints, 543 Pydantic models)
- **API resilience**: 408 retry, auto-idempotency keys on confirmed requests, ±20% jitter
- **Package maturity**: CHANGELOG.md, pyproject.toml v2.4.15.1, mypy CI (0 errors), PyPI publish workflow
- **CI improvements**: auto-issue-creation on drift, cross-repo parity CI, network-blocking test fixture
- **Ansible**: 4 bugs fixed, 13 tests, ansible-lint CI, molecule caddy scenario, weekly live E2E
- **Pulumi**: TF Bridge migration guide (replaces hand-written Python provider)
- **Terraform**: 10 new Go methods (VM term/addons + Orders), `term` attribute on VM resource
- **resolve_addons parity**: caught real drift (Python silently swallowed unknown package_id vs Go's explicit error)

### Ephemeral GitHub Actions runners (2026-07-04)
- `shc github-runner provision|destroy` CLI + `shc_toolkit.github_runner` module
- Live-validated: 135.8 s cold-start, $0.01/run prorated cost
- 31 unit tests

### Spec-encoding size names (all 3 repos)
- 20 entries across 4 lines (nvme/ssd/hdd/dev)
- Generated from live catalog via `scripts/generate_sizes.py`

### Config options (all 3 repos)
- `disk_gb`, `ram_mb`, `cpu`, `template` params translated to SHC option IDs

### Cost audit (shc-toolkit + TF provider)
- Balance-diff tracking (never logs absolute balance)
- Per-VM ledger disambiguation for concurrent activity

### CI infrastructure
- OpenAPI spec drift detection + auto-issue-creation (shc-toolkit)
- MCP tool drift detection (shc-toolkit)
- Size-map drift detection (all 3 repos)
- Cross-repo parity audit CI (shc-toolkit)
- mypy type checking CI (shc-toolkit)
- ansible-lint + molecule CI (shc-toolkit)
- Weekly live E2E (shc-toolkit)
- PyPI publish on tag (shc-toolkit)

## All Issues Closed

| # | Title | Closed |
|---|-------|---------|
| #1 | Ansible playbook for SHC + NoDNS + certbot HTTPS pipeline | 2026-07-05 |
| #2 | Wrap remaining 60 MCP server tools | 2026-07-11 (99% coverage) |
| #3 | Cost audit for Terraform Go provider | 2026-07-02 |
| #4 | API v2.4.0 cleanup | 2026-07-08 |
| #8 | Remove deprecated DVM code paths | 2026-07-09 |
| #9 | Molecule testing for ansible roles | 2026-07-11 |

## Feature Matrix

| Feature | shc-toolkit | TF | Pulumi |
|---------|:---:|:---:|:---:|
| VM lifecycle | create/read/update/delete | create/read/update/delete | create/read/update/delete |
| VM term management | ✅ (v2.4.3) | ✅ (term attribute) | ✅ (via TF bridge) |
| Size abstraction | resolve_size + SIZE_MAP | resolveSize + sizeMap | resolve_size + SIZE_MAP |
| Config options | resolve_addons + order_vm | ResolveAddons | resolve_addons |
| Cost audit | CostTracker | CostTracker | indirect (via toolkit) |
| Snapshots | create/list/restore/delete/verify/protect | create/delete | create/delete |
| Backups | create/list/restore/delete/verify/protect | create/delete | create/delete |
| Firewall | list/create/delete/edit/policy | create/delete | create/delete |
| rDNS | get/set/clear | create/delete | create/delete |
| NoDNS | publish_dns_records | nodns=true | nodns=True |
| Credit pre-check | check_credit | CheckCredit | estimate_daily_cost |
| Orders | list/get/cancel (v2.4.3) | list/get/cancel | N/A |
| Catalog generator | --format go\|pulumi\|python | regenerate_sizes.sh | regenerate_sizes.sh |
| Drift detection CI | OpenAPI + MCP + size-map + cross-repo | size-map | size-map |
| MCP transport | 156/157 tools wrapped (99%) | N/A | N/A |
| Auto-generated client | 718 files, 149 endpoints, 543 models | N/A | N/A |
| API resilience | 408 retry + jitter + idempotency | N/A | N/A |
| Type checking | mypy 0 errors | go vet | N/A |

## Future Work (not started)

- WorkOS refactor: SHCClient uses generated client (httpx) internally for raw API calls
- TF provider schema versioning: SchemaVersion + StateUpgrader on VM resource
- TF Registry docs: terraform-plugin-docs generation
- TF acceptance tests: TF_ACC=1 go test
- CLI config profiles: named configurations (like gcloud's `config configurations`)
- Circuit breaker pattern (deferred — overkill for VPS API with 3 max retries)
