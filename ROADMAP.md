# SHC Tooling Roadmap

Goal: Make SHC the easiest bitcoin-native VPS to manage with infrastructure-as-code.
Target: parity with DigitalOcean/Hetzner/Vultr tooling quality.

## Current State (2026-07-02)

| Repo | Tests | CI | Key Features |
|------|-------|----|-------------|
| shc-toolkit | 87 unit | Push + daily (REST+MCP) + OpenAPI drift + MCP drift | Spec-encoding sizes, config options, cost audit, MCP transport (117 tools), v2.4.0, catalog generator |
| shc-pulumi | 95 unit | Push + size-map drift | Spec-encoding sizes, config options, snapshots, backups, firewall, rDNS, NoDNS |
| terraform-provider-shc | 68 unit | Push + size-map drift + integration | Spec-encoding sizes, config options, cost audit, snapshots, backups, firewall, rDNS |

### API version: v2.4.0 (108 paths)

## Completed Work

### Spec-encoding size names (all 3 repos)
- 20 entries across 4 lines (nvme/ssd/hdd/dev)
- Format: `{line}-{cpu}c-{ram}gb` (e.g., `nvme-2c-8gb`)
- Legacy tier names (starter/standard/...) removed
- Generated from live catalog via `scripts/generate_sizes.py --format go|pulumi|python`

### Config options (all 3 repos)
- `disk_gb`, `ram_mb`, `cpu`, `template` params on VM resources
- Translated to SHC per-package option IDs via catalog lookup
- Python: `client.resolve_addons()`, Go: `client.ResolveAddons()`

### Cost audit (shc-toolkit + TF provider)
- Balance-diff tracking (never logs absolute balance)
- Proration matching SHC backend: `truncate(hours * round(daily/24, 4), 2)`
- Per-VM ledger disambiguation for concurrent activity
- Hooks into order/cancel lifecycle
- Pulumi inherits via shc-toolkit dependency

### MCP transport fixes
- All 117 server tool names verified via drift detection CI
- 12 tool name corrections (e.g., `createVirtualMachineFirewallRule` → `addVirtualMachineFirewallRule`)
- 4 missing methods added (get_vm_credentials, get_vm_network, get_vm_activity, get_vm_payments)
- Body wrapper pattern for destructive operations
- `structuredContent.result` unwrap for v2.4.0

### v2.4.0 adoption
- `error_code` + `retry_after_seconds` on SHCError
- Removed plaintext prefix strip workaround
- Consolidated summary+detail fetch (summary now includes runtime)
- Cancel response includes `cancel_credit.amount`
- Console session TTL support
- listApiKeys added to MCP TOOL_MAP

### CI infrastructure
- OpenAPI spec drift detection (shc-toolkit)
- MCP tool drift detection (shc-toolkit)
- Size-map drift detection (all 3 repos)
- Orphan VM cleanup (all 3 repos)
- Cross-repo parity audit script (`scripts/audit_cross_repo.py`)
- Catalog generator with multi-format output

### Other
- Affiliate disclosure updated to 5% recurring (grandfathered rate)
- Dev VPS snapshot/backup claim corrected (verified working)
- Billing claim corrected (hourly proration, not daily minimum)
- Cross-links between all 3 repos
- Dimi8146 (SHC provider) invited as admin collaborator

## Open Issues

| # | Title | Priority |
|---|-------|----------|
| [#2](https://github.com/Amperstrand/shc-toolkit/issues/2) | Wrap remaining 60 MCP server tools | Low (niche features) |
| [#4](https://github.com/Amperstrand/shc-toolkit/issues/4) | API v2.4.0 cleanup (remaining minor items) | Low |

## Feature Matrix

| Feature | shc-toolkit | TF | Pulumi |
|---------|:---:|:---:|:---:|
| VM lifecycle | create/read/update/delete | create/read/update/delete | create/read/update/delete |
| Size abstraction | resolve_size + SIZE_MAP | resolveSize + sizeMap | resolve_size + SIZE_MAP |
| Config options | resolve_addons + order_vm | ResolveAddons | resolve_addons |
| Cost audit | CostTracker | CostTracker | indirect (via toolkit) |
| Snapshots | create/list/restore/delete | create/delete | create/delete |
| Backups | create/list/restore/delete | create/delete | create/delete |
| Firewall | list/create/delete/edit | create/delete | create/delete |
| rDNS | get/set/clear | create/delete | create/delete |
| NoDNS | publish_dns_records | nodns=true | nodns=True |
| Credit pre-check | check_credit | CheckCredit | estimate_daily_cost |
| Catalog generator | --format go\|pulumi\|python | regenerate_sizes.sh | regenerate_sizes.sh |
| Drift detection CI | OpenAPI + MCP + size-map | size-map | size-map |
| MCP transport | 57/117 tools wrapped | N/A | N/A |

## Future Work (not started)

- Publish to PyPI and Terraform Registry
- Add release workflow (tag-triggered)
- CHANGELOG.md per repo
- Scheduled cross-repo audit CI job
- Balance monitoring alert (warn when balance < $1)
