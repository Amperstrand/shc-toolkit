# SHC Tooling Roadmap

Goal: Make SHC the easiest bitcoin-native VPS to manage with infrastructure-as-code.
Target: parity with DigitalOcean/Hetzner/Vultr tooling quality.

## Current State (2026-06-29)

| Repo | Tests | CI | Resources | Data Sources |
|------|-------|----|-----------|-------------|
| shc-toolkit | 37 unit + integration | Push + daily drift | CLI (55+ commands), gcloud shim (15 commands) | — |
| shc-pulumi | 22 unit | Push (pending secret) | VM, Snapshot | — |
| terraform-provider-shc | 11 unit | Push (pending secret) | VM, Snapshot, Backup | VM, Catalog |

## Session Plan

Each session is independently executable. Dependencies noted where they exist.

### Session 1: CI Proof *(no dependencies, do first)*

Prove the integration CI actually works end-to-end in GitHub Actions.

- [ ] Add `SHC_API_KEY` secret to `Amperstrand/shc-toolkit`
- [ ] Add `SHC_API_KEY` secret to `Amperstrand/shc-pulumi`
- [ ] Add `SHC_API_KEY` secret to `Amperstrand/terraform-provider-shc`
- [ ] Push empty commit to each repo to trigger CI
- [ ] Fix any CI failures (path issues, dependency install, Python version)
- [ ] Verify green checkmarks on all repos
- [ ] Verify VMs created and cleaned up (check `shc list` after CI runs)

### Session 2: Firewall Resource *(no dependencies)*

Add firewall rule management to both IaC providers and expand gcloud.

**API endpoints:**
- `GET /vm/{id}/firewall` — list rules + policy
- `POST /vm/{id}/firewall/rules` — create rule
- `PATCH /vm/{id}/firewall/rules/{pos}` — edit rule
- `DELETE /vm/{id}/firewall/rules/{pos}` — delete rule
- `PATCH /vm/{id}/firewall/policy` — set default policy

**Terraform:**
- New file: `provider/firewall_resource.go`
- Resource: `shc_firewall_rule` (service_id, action, protocol, port, source, direction)
- Register in `provider.go`
- Add test: `provider/firewall_resource_test.go`
- Add doc: `docs/resources/firewall_rule.md`

**Pulumi:**
- New file: `src/shc_pulumi/firewall.py`
- Resource: `SHCFirewallRuleResource`
- Add test: `tests/test_firewall.py`
- Update `__init__.py` exports

**gcloud (shc-toolkit):**
- Expand `compute firewall-rules` to support `update`, `list --format=json` with full rule details
- Add `compute firewall-rules describe <name>`

**GitHub issues:** [#1 terraform](https://github.com/Amperstrand/terraform-provider-shc/issues/1), [#1 pulumi](https://github.com/Amperstrand/shc-pulumi/issues/1)

### Session 3: VM Power Management *(no dependencies)*

Add start/stop/restart/shutdown/reset/reinstall to both providers.

**API endpoints:**
- `PATCH /vm/{id}/start`
- `PATCH /vm/{id}/stop` (hard stop)
- `PATCH /vm/{id}/shutdown` (graceful)
- `PATCH /vm/{id}/restart` (graceful reboot)
- `PATCH /vm/{id}/reset` (hard reset)
- `PATCH /vm/{id}/reinstall` (OS reinstall)

**Terraform:**
- Option A: Add `power_state` argument to `shc_vm` (computed, default "running")
- Option B: Separate `shc_vm_power` resource
- Recommended: Option A (simpler for users)

**Pulumi:**
- Add `power_state` input to `SHCVMResource`
- Implement `update()` method to handle power state changes without replacement

**gcloud:**
- Add `compute instances reboot/restart` (maps to restart_vm)
- Add `compute instances suspend/resume` (maps to stop_vm/start_vm)

**GitHub issues:** [#3 terraform](https://github.com/Amperstrand/terraform-provider-shc/issues/3), [#2 pulumi](https://github.com/Amperstrand/shc-pulumi/issues/2)

### Session 4: rDNS Resource *(no dependencies)*

Add reverse DNS management.

**API endpoints:**
- `GET /vm/{id}/rdns` — list rDNS-eligible IPs
- `POST /vm/{id}/rdns` — set PTR (async, returns job_id)
- `DELETE /vm/{id}/rdns` — clear PTR (confirmation required)

**Constraint:** FCrDNS required — hostname must A/AAAA-resolve back to the IP.

**Terraform:**
- New file: `provider/rdns_resource.go`
- Resource: `shc_rdns` (service_id, ip, hostname)
- Import support: `service_id:ip`
- Register in `provider.go`

**Pulumi:**
- New file: `src/shc_pulumi/rdns.py`
- Resource: `SHCrDNSResource`

**gcloud:**
- Not applicable (gcloud doesn't have rDNS commands)

**GitHub issues:** [#2 terraform](https://github.com/Amperstrand/terraform-provider-shc/issues/2)

### Session 5: gcloud Full Parity *(depends on sessions 2-4)*

Expand `shc-compute` from ~15 to ~40+ commands.

**Missing commands to add:**

| gcloud command | SHC API | Priority |
|---------------|---------|----------|
| `compute instances restart` | `PATCH /vm/{id}/restart` | High |
| `compute instances suspend` | `PATCH /vm/{id}/stop` | High |
| `compute instances resume` | `PATCH /vm/{id}/start` | High |
| `compute instances reset` | `PATCH /vm/{id}/reset` | Medium |
| `compute instances reinstall` | `PATCH /vm/{id}/reinstall` | Medium |
| `compute instances set-machine-type` | `PATCH /vm/{id}/upgrade` | High |
| `compute machine-types list` | `GET /ordering/catalog` | High |
| `compute zones list` | Static (Katy TX, Cherryvale KS) | Medium |
| `compute regions list` | Static | Low |
| `compute project-info describe` | `GET /account` | Medium |
| `compute project-info list` | `GET /account` | Low |
| `compute operations list` | `GET /vm/{id}/jobs` | Medium |
| `compute operations describe` | `GET /vm/{id}/jobs/{jobId}` | Medium |
| `compute images describe` | `GET /vm/templates` | Low |
| `compute disks list` | `GET /vm/{id}/detail` (disk info) | Low |
| `compute addresses list` | `GET /vm/{id}/network` | Low |
| `compute networks list` | `GET /vm/{id}/network` | Low |
| `compute firewall-rules update` | `PATCH /vm/{id}/firewall/rules/{pos}` | Medium |
| `compute firewall-rules describe` | `GET /vm/{id}/firewall` | Medium |
| `compute snapshots describe` | `GET /vm/{id}/snapshots` (filtered) | Low |
| `compute snapshots label` | Not supported (no labels API) | N/A |

**Testing:** Each new command needs a test in `tests/test_unit.py` (mocked) and
verification via `shc-compute compute <command> --help`.

### Session 6: Data Sources / Discovery *(depends on session 5)*

Add data sources so users don't hardcode IDs.

**Terraform:**
- `data "shc_templates"` — list available OS templates
- `data "shc_machine_types"` — list available plans with specs/pricing
- `data "shc_zones"` — list available zones/regions

**Pulumi:**
- `get_templates()` helper
- `get_machine_types()` helper
- Expand `get_plan()` to return full spec (CPU, RAM, disk, pricing)

**gcloud:**
- `compute machine-types list --format=json` (already planned in session 5)
- `compute images list --format=json` (expand existing)

**GitHub issues:** [#4 terraform](https://github.com/Amperstrand/terraform-provider-shc/issues/4), [#3 pulumi](https://github.com/Amperstrand/shc-pulumi/issues/3)

### Session 7: Snapshot/Backup Restore + Scheduling *(no dependencies)*

**API endpoints:**
- `POST /vm/{id}/snapshots/restore` — restore from snapshot (confirmation required)
- `POST /vm/{id}/backups/restore` — restore from backup (confirmation required)
- `GET /vm/{id}/data-preferences` — view backup schedule
- `PATCH /vm/{id}/data-preferences` — set backup schedule

**Terraform:**
- Add `restore` support to snapshot/backup resources or new `shc_snapshot_restore` resource
- Add `backup_schedule` argument to `shc_vm`

**Pulumi:**
- Add restore method to snapshot/backup providers
- Add backup schedule support to VM provider

### Session 8: Migration Docs + Real-World Examples *(depends on sessions 2-6)*

**Documents to create:**

- `docs/migrating-from-digitalocean.md` — map DO droplet configs to SHC plans, Terraform translation
- `docs/migrating-from-hetzner.md` — map Hetzner Cloud to SHC, Terraform translation
- `docs/migrating-from-gcloud.md` — map gcloud commands to shc-compute commands

**Example stacks:**

- `examples/web-server/` — Caddy + HTTPS on SHC VM (uses shc-toolkit provisioning)
- `examples/ci-runner/` — self-hosted runner on SHC VM (uses Terraform)
- `examples/bitcoin-node/` — Bitcoin Core + Lightning (uses Pulumi)
- `examples/cdn-origin/` — origin server with firewall rules (uses Terraform)
- `examples/multi-vm/` — multiple VMs with shared firewall (uses Pulumi)

### Session 9: Provider Maturity *(ongoing)*

- Add `Validate()` functions for package_id, pricing_id, port ranges, IP format
- Add custom plan modifiers (e.g., prevent disk-reducing upgrades)
- Add `UseStateForUnknown` for computed fields
- Add state migration/versioning
- Add `description` fields to all schema attributes
- Add `conflicts_with` validators
- Handle VM lock during backup job (retry cancel with backoff)

### Session 10: Publishing *(after sessions 2-6)*

- Publish `shc-toolkit` to PyPI (`pip install shc-toolkit`)
- Publish `shc-pulumi` to PyPI (`pip install shc-pulumi`)
- Publish `terraform-provider-shc` to Terraform Registry (`registry.terraform.io`)
- Add release workflow (tag-triggered, auto-publish)
- Add `CHANGELOG.md` to each repo

## Quick Reference: API Feature Matrix

| Feature | Dev VPS (80-84) | NVMe/SSD/HDD (23+) | Terraform | Pulumi | gcloud |
|---------|:---:|:---:|:---:|:---:|:---:|
| VM lifecycle | Works | Works | create/delete | create/delete | create/delete/start/stop/reset |
| Snapshots | Works | Works | create/delete | create/delete | create/list/delete |
| Backups | Works | Works | create/delete | — | — |
| Firewall | Works | Works | — | — | list/create/delete |
| rDNS | Works | Works | — | — | — |
| ISO | Works | Works | — | — | — |
| Console | Works | Works | — | — | — |
| Jobs | Works | Works | — | — | — |
| Metrics | Works | Works | — | — | — |
| Upgrades | Works | Works | — | — | set-machine-type |
| Catalog/Templates | Works | Works | data source | get_plan() | images list |
| Power ops | Works | Works | — | — | start/stop/reset |
| Reinstall | Works | Works | — | — | — |

## Session Dependencies

```
Session 1 (CI Proof) ─── no dependencies
Session 2 (Firewall) ─── no dependencies
Session 3 (Power Mgmt) ─ no dependencies
Session 4 (rDNS) ──────── no dependencies
Session 5 (gcloud) ────── depends on 2, 3, 4 (uses their API wrappers)
Session 6 (Data Sources) ─ depends on 5
Session 7 (Restore) ───── no dependencies
Session 8 (Docs/Examples) ─ depends on 2, 3, 4, 5, 6
Session 9 (Maturity) ──── ongoing, any time
Session 10 (Publishing) ── depends on 2, 3, 4, 5, 6
```

Sessions 1-4 and 7 can be done in any order. Sessions 5-6 and 8-10 have dependencies.
