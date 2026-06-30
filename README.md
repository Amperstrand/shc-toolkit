# SHC Toolkit

Python client, CLI, and provisioning toolkit for [Sovereign Hybrid Compute](https://blesta.sovereignhybridcompute.com/order/forms/a/lecture-mushroom-lunar) (SHC) — the quickest way to spin up a VM, give it a [NoDNS](https://nodns.shop/) domain via Nostr, and get HTTPS with Let's Encrypt DNS-01. No domain registrar needed.

> **Disclosure**: The SHC link above is an affiliate link. If you sign up through it, we may receive credit toward our SHC account at no extra cost to you. We use SHC as the CI backend for our open-source projects and genuinely recommend the service.

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
116 tools over Streamable HTTP. Every spend and destructive op is confirm-gated.

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

## Known Limitations

- **Nested KVM**: Available ONLY on **Dev VPS plans** (pkg 80–84, Cherryvale, KS). NVMe/SSD/HDD VPS plans do NOT expose VMX/SVM to guests — QEMU runs in TCG (software emulation) only. Verify after ordering with `grep -E 'vmx|svm' /proc/cpuinfo`.
- **Daily billing minimum**: You pay for a full day even if you use the VM for minutes.
- **Single location**: Katy, Texas only.
- **API key lifecycle**: API keys expire after 90 days (max 730). A 401 on a working key means it expired — mint a new one at `/account/api-keys`. Maximum 25 active keys per account.
- **Snapshots & backups not available on Dev VPS**: Dev VPS plans (pkg 80–84, Cherryvale, KS) do NOT have storage infrastructure for snapshots or backups. The API returns `upstream_failure: "Unable to load storage inventory"`. NVMe/SSD/HDD VPS plans (pkg 23+, Katy, TX) support snapshots, backups, and all other storage features. All other API features (firewall, rDNS, ISO, console, jobs, metrics, upgrades) work on both plan types.

## Cashu Tollgate — SSH for ecash

A pay-per-minute SSH server that accepts [Cashu](https://cashu.space) ecash tokens as payment. Users paste a token as their SSH username and get an interactive bash shell for as many minutes as the token is worth. Includes a static faucet page for minting free test tokens.

→ **[Full documentation](tollgate/README.md)**

⚠️ **Warning:** This creates ephemeral shell accounts on your server. Do not run on production infrastructure without understanding the security implications. Consult your IT department before running at work.

## License

MIT
