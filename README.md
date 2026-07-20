# SHC Toolkit

Python client, CLI, and provisioning toolkit for [Sovereign Hybrid Compute](https://blesta.sovereignhybridcompute.com/order/forms/a/lecture-mushroom-lunar) (SHC) — the quickest way to spin up a VM, give it a [NoDNS](https://nodns.shop/) domain via Nostr, and get HTTPS with Let's Encrypt DNS-01. No domain registrar needed.

> **Disclosure**: The SHC link above is an affiliate link. If you sign up through it, we receive a **5% recurring commission** (grandfathered rate) on your spending, at no extra cost to you. We use SHC as the CI backend for our open-source projects and genuinely recommend the service.

## Related Projects

- [terraform-provider-shc](https://github.com/Amperstrand/terraform-provider-shc) — Terraform provider for SHC
- [shc-pulumi](https://github.com/Amperstrand/shc-pulumi) — Pulumi provider for SHC

## What you get

- **`shc` CLI** — order, manage, and snapshot VMs from the command line
- **Python client** — `SHCClient` wraps the full SHC User API
- **NoDNS integration** — publish DNS records via Nostr events (kind 11111)
- **Certbot DNS-01** — get Let's Encrypt certs without opening port 80
- **Provisioning helpers** — one-call setup for Caddy + HTTPS on a fresh VM

## Install

```bash
pip install -e .
```

Requires Python 3.11+.

## Quick Start

```bash
export SHC_API_KEY="shc_live_..."

shc catalog
shc order --hostname my-vm --package-id 23 --pricing-id 55 \
  -o 108=50 -o 126=debian12-cloud -o 167=none \
  --ssh-key ~/.ssh/id_ed25519.pub --pay
shc list
shc info <service_id>
shc cancel <service_id>
```

## Python Library

```python
from shc_toolkit import SHCClient

c = SHCClient()
vms = c.list_vms()
c.start_vm(123)
c.create_snapshot(123, name="pre-deploy")
```

## NoDNS + Let's Encrypt DNS-01

NoDNS maps Nostr keypairs to `.nodns.shop` subdomains. You publish DNS records as kind 11111 Nostr events, and the [nodns-bot](https://github.com/nicobao/nodns) pushes them to Knot DNS. No domain registration, no DNS provider account.

### Architecture

```
Your machine
  └── nostr-sdk → publishes kind 11111 events to Nostr relays
                    ↓
              nodns-bot → Knot DNS (ns1.nodns.shop)
                    ↓
              Public DNS: <npub>.nodns.shop A <your-vm-ip>
```

### Publish DNS from Python

```python
from shc_toolkit.nodns import NoDNSKeyPair, publish_dns_records

kp = NoDNSKeyPair.generate()
print(f"Domain: {kp.fqdn}")
print(f"Save this nsec to update records later: {kp.nsec}")

publish_dns_records(kp, [
    {"type": "A", "name": "@", "value": "<your-vm-ip>", "ttl": 300},
])
```

### Publish DNS from CLI

```bash
shc nodns --ip <your-vm-ip>
```

### Full pipeline: VM → DNS → HTTPS

The provisioning module automates the complete flow on a fresh Debian VM:

```python
from shc_toolkit.client import SHCClient
from shc_toolkit.nodns import NoDNSKeyPair, publish_dns_records
from shc_toolkit.provision import install_caddy, get_cert_dns01

# 1. Order a VM (or use an existing one)
c = SHCClient()
vm = c.get_vm_summary(123)
ip = vm["ips"][0]["ip"]

# 2. Publish A record via NoDNS
kp = NoDNSKeyPair.generate()
publish_dns_records(kp, [{"type": "A", "name": "@", "value": ip, "ttl": 300}])

# 3. Install Caddy + get Let's Encrypt cert via DNS-01
install_caddy(ip)
get_cert_dns01(ip, kp.fqdn, keypair_path="/tmp/nodns-keypair.json")
```

For the certbot auth hook to work, save the keypair and deploy `nodns_vm.py` to the VM first. See `shc_toolkit/provision.py` for details.

### Verified end-to-end

```bash
$ curl https://npub1mv7l45exqsu5nr5tnefkr33ruhzjj4r8prg6qtcedv4lyf3rzguqptuwm4.nodns.shop
Hello from NoDNS + Let's Encrypt DNS-01!
```

Certificate issued by Let's Encrypt via DNS-01 through nodns. No port 80, no traditional DNS provider, no domain registrar.

## SHC API Reference

The SHC User API has full documentation available at:

- **Interactive docs**: https://blesta.sovereignhybridcompute.com/user-api/docs/
- **OpenAPI 3.1 spec**: https://blesta.sovereignhybridcompute.com/user-api/openapi.json
- **LLM-friendly docs**: https://blesta.sovereignhybridcompute.com/user-api/llms.txt

This toolkit covers the most common endpoints (VM lifecycle, ordering, snapshots, billing). For operations not yet wrapped (reinstall, backups, etc.), use `SHCClient._request()` directly or open a PR.

## MCP Transport

The toolkit supports dual transport: REST v2 (default) or MCP Streamable HTTP.
Both transports are **fully functional** for all operations including reads,
writes, spend/destructive actions with confirmation flow, and upgrades.

The flagship SHC MCP server at `https://mcp.sovereignhybridcompute.com/` exposes
142 tools over Streamable HTTP. The toolkit wraps **141/142 (99%)** — the only
unwrapped tool is `buyVirtualMachine` (a deprecated alias for
`createVirtualMachineOrder`). Every spend and destructive op is confirm-gated
with automatic `Idempotency-Key` generation and `X-User-Api-Confirm` handling.

CI tests randomly select REST or MCP per run, ensuring both transports receive
equal coverage over time without doubling test cost.

### Using MCP transport

```python
from shc_toolkit import create_client

# Auto (defaults to REST — change with SHC_TRANSPORT=mcp)
c = create_client(transport="auto")

# Force MCP
c = create_client(transport="mcp")

# Force REST (default)
c = create_client(transport="rest")
```

Or via environment variable:

```bash
export SHC_TRANSPORT=mcp   # or 'rest' or 'auto'
```

Install the MCP optional dependency:

```bash
pip install shc-toolkit[mcp]
```

Both transports implement the same `SHCTransport` interface — your code works
unchanged regardless of which backend is selected.

## Config Option IDs

Option IDs differ by VPS line. Always read them from `shc catalog` or `GET /ordering/catalog`.

For NVMe Starter (package_id 23):

| Option | ID | Example values |
|--------|-----|---------------|
| RAM | 106 | `4096` (base), `8192`, `16384` |
| CPU | 107 | `1` (base), `2`, `4` |
| Disk | 108 | `8` (base), `32`, `50`, `100` |
| IPv4 | 109 | `1` (base), `2`, `4` |
| Template (NVMe/HDD/SSD) | 126 | `debian13-cloud`, `debian12-cloud`, `ubuntu2404-cloud`, `ubuntu2204-cloud`, `fedora43-cloud`, `arch-cloud`, `nixos-cloud`, `almalinux9-cloud`, `alpine323-cloud`, `devuan5-cloud`, `openbsd79-cloud` |
| Template (Dev VPS) | 174 | Same as above |
| GUI | 167 | `none`, `gnome`, `kde`, `xfce`, `cinnamon`, `mate` |

Values are the `value` field from the catalog, not `value_id`.

### Windows BYOL

Windows is available bring-your-own-license on all VPS lines: Windows Server 2022/2025 (Core or Desktop) and Windows 11 Pro. Windows Server requires >=32GB disk; Windows 11 requires >=64GB disk. Apply your own license after first boot.

### GUI requirements

GUI requires >=16GB disk AND >=4GB RAM.

## Ephemeral GitHub Actions runners

Disposable per-job CI runners on cheap SHC VPSs. The toolkit orders a VPS,
bootstraps the GitHub Actions runner over SSH with `--ephemeral`, registers
it with a unique per-run label, and the workflow destroys the VM in an
`if: always()` teardown job when the benchmark finishes.

**Live-measured cold-start**: 135.8 s end-to-end on `dev-4c-16gb`
(`$0.90/day`, **~$0.01 per run** prorated). Workload execution matches
`ubuntu-latest` per-shard. Full perf comparison and the Firecracker
cold-start reduction target live in
[`docs/github-ephemeral-runners.md`](docs/github-ephemeral-runners.md).

**Firecracker PoC validated**: nested KVM works on SHC Dev VPS, μVMs boot
in **~2 s** vs the 100 s VPS scheduling floor — **50× faster per job,
150× throughput at parallelism 4**. Pool-mode architecture and live
benchmark numbers in
[`docs/firecracker-pool-mode.md`](docs/firecracker-pool-mode.md).

```bash
export SHC_API_KEY="shc_live_..."
export SHC_GITHUB_ADMIN_TOKEN="ghp_..."   # PAT with repo admin / runners:write

shc github-runner provision \
  --repo Amperstrand/tollgate-module-basic-go \
  --labels shc-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}
shc github-runner destroy --service-id "$SERVICE_ID"
```

Intended audience: OSS maintainers with expensive / slow / custom CI who
want pay-per-minute runners on machines they control.

## Known Limitations

- **Nested KVM**: Available ONLY on **Dev VPS plans** (pkg 80–84, Cherryvale, KS). NVMe/SSD/HDD VPS plans do NOT expose VMX/SVM to guests — QEMU runs in TCG (software emulation) only. Verify after ordering with `grep -E 'vmx|svm' /proc/cpuinfo`.
- **Hourly proration**: You're charged the full daily rate at order time, but get refunded for unused hours when you cancel (minimum 1 hour charge). A 2-hour session on a $0.49/day plan costs ~$0.04.
- **Single location**: Katy, Texas only.
- **API key lifecycle**: API keys expire after 90 days (max 730). A 401 on a working key means it expired — mint a new one at `/account/api-keys`. Maximum 25 active keys per account.
- **Snapshot/backup limit**: All VPS plans (including Dev VPS) support 1 snapshot and 1 backup concurrently (`snapshot_limit: 1`, `backup_limit: 1` per package). Verified working on Dev VPS via front-door E2E (2026-07-01).

## Cashu Tollgate — SSH for ecash

A pay-per-minute SSH server that accepts [Cashu](https://cashu.space) ecash tokens as payment. Users paste a token as their SSH username and get an interactive bash shell for as many minutes as the token is worth. Includes a static faucet page for minting free test tokens.

→ **[Full documentation](tollgate/README.md)**

⚠️ **Warning:** This creates ephemeral shell accounts on your server. Do not run on production infrastructure without understanding the security implications. Consult your IT department before running at work.

## License

MIT

## Auto-Generated Client

The toolkit includes an auto-generated Python client (`shc_toolkit.generated`)
with **100% API endpoint coverage** (148 endpoint modules, 727 attrs models)
generated from the OpenAPI spec via `openapi-python-client`.

```bash
pip install shc-toolkit[generated]  # installs httpx + attrs
```

```python
from shc_toolkit.generated import Client
from shc_toolkit.generated.api.ordering import get_ordering_catalog

client = Client(base_url="https://blesta.sovereignhybridcompute.com/user-api/v2",
                headers={"Authorization": "Bearer shc_live_..."})
catalog = get_ordering_catalog.sync(client=client)
```

The generated client provides type-safe raw API calls. For convenience features
(retry with jitter, cost tracking, confirmation flow, cache, MCP transport), use
`SHCClient` instead — it wraps the generated layer and adds production niceties.
The hand-written `SHCClient` returns raw `dict` / `list[dict]`; users who want
typed responses should reach for `shc_toolkit.generated` directly.

Regenerate from the latest spec: `bash scripts/generate_client.sh`

## Pulumi Support

The recommended way to use SHC from Pulumi is via the **Terraform Bridge** —
no separate Python provider needed:

```bash
# Build the TF provider
go build -o terraform-provider-shc .

# Generate a Pulumi SDK from the TF provider
pulumi package add terraform-provider ./terraform-provider-shc --language python
```

The generated Pulumi SDK includes all resources (Vm, Snapshot, Backup,
FirewallRule, Rdns) + the `term` attribute (v2.4.3 VM term management).

→ **[Migration guide from shc-pulumi](https://github.com/Amperstrand/shc-pulumi/blob/main/MIGRATION-TO-BRIDGE.md)**

## Changelog

→ **[CHANGELOG.md](CHANGELOG.md)** — full version history in Keep a Changelog format.

## Testing Status

### v2.4.24.0 Release
- **219 unit tests** (network-isolated, zero flakes across 5 consecutive runs)
- **mypy type checking**: 0 errors (17 source files; generated/ excluded)
- **Cross-repo parity**: 5/5 checks pass (size map, feature matrix, resolve_addons contract, billing claims, Dev VPS claims)
- **API**: v2.4.24 (148 paths, 197 schemas, 177 operations); live MCP server exposes 157 tools; curated x-shc-core subset is 35; `TOOL_MAP` wraps 124 entries
- **API resilience**: 408 retry, exponential backoff with ±20% jitter, auto-generated Idempotency-Key on all confirmed requests
- **Generated typed client**: 932 files, 148 endpoint modules, 727 attrs models
- **CI**: 7 workflows (unit, smoke, integration, OpenAPI drift, MCP drift, cross-repo parity, typecheck, ansible, publish) + auto-issue-creation on drift
- **Ansible**: 13 unit tests + ansible-lint CI + molecule caddy scenario + weekly live E2E

### MCP Transport (Verified 2026-06-30)
- READS: All working (getAccount, getBillingBalance, listVirtualMachines, getOrderingCatalog)
- WRITES: All working (createVirtualMachineOrder with confirmation flow, cancelVirtualMachine)
- CI: Randomly selects REST or MCP per run for equal coverage

### NoDNS (Working — Fixed 2026-06-30)
- Code is complete and correct (keypair generation, event publishing, DNS verification)
- **VERIFIED**: Published A record resolves correctly within 10 seconds
- `shc nodns --ip <ip> --zone nodns.shop` publishes, `shc order --nodns` auto-publishes after VM creation

### ContextVM (Verified 2026-07-01)
- Bootstrap code complete and tested on NVMe VPS (Debian 13, Katy TX)
- VM becomes discoverable MCP server on Nostr via `wss://relay.contextvm.org`
