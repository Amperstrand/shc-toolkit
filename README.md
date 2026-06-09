# SHC Toolkit

Python client and CLI for [Sovereign Hybrid Compute](https://blesta.sovereignhybridcompute.com) (SHC) User API.

## Install

```bash
pip install -e .
```

## Quick Start

```bash
# Set API key (get one at /account/api-keys)
export SHC_API_KEY="shc_live_..."

# List plans
shc catalog

# Order a VM (dry run first)
shc order --hostname my-vm --package-id 23 --pricing-id 55 \
  -o 108=50 -o 126=debian12-cloud -o 167=none --dry-run

# Order + pay + wait
shc order --hostname my-vm --package-id 23 --pricing-id 55 \
  -o 108=50 -o 126=debian12-cloud -o 167=none \
  --ssh-key ~/.ssh/id_ed25519.pub --pay

# List VMs
shc list

# VM details
shc info <service_id>

# Snapshot
shc snapshot-create <service_id> --name "pre-deploy"

# Cancel
shc cancel <service_id>
```

## Python Library

```python
from shc_toolkit import SHCClient

c = SHCClient()

# Order + pay + wait
result = c.submit_order(
    hostname="test-vm",
    package_id=23,
    pricing_id=55,
    ssh_key=open("~/.ssh/id_ed25519.pub").read().strip(),
    config_options={"108": "50", "126": "debian12-cloud", "167": "none"},
)
c.pay_invoice(result["invoice"]["invoice_id"], "my-unique-key")
vm = c.wait_for_provisioning(result["service_ids"][0])
print(f"VM ready: {vm['ips'][0]['ip']}")
```

## Config Option IDs

Option IDs are found via `GET /ordering/catalog`. For NVMe Starter (package_id 23):

| Option | ID | Example values |
|--------|-----|---------------|
| RAM | 106 | `4096` (base), `8192`, `16384` |
| CPU | 107 | `1` (base), `2`, `4` |
| Disk | 108 | `8` (base), `32`, `50`, `100` |
| IPv4 | 109 | `1` (base), `2`, `4` |
| Template | 126 | `debian12-cloud`, `debian13-cloud`, `ubuntu2404-cloud` |
| GUI | 167 | `none`, `gnome`, `kde` |

Values are the `value` field from the catalog, not `value_id`.

## Known Limitations

- **No nested KVM**: SHC does not expose VMX/SVM to guests. QEMU runs in TCG (software emulation) only.
- **Daily billing minimum**: You pay for a full day even if you use the VM for minutes.
- **Single location**: Katy, Texas only.

## NoDNS + Let's Encrypt DNS-01 Pipeline

The toolkit includes a NoDNS integration for provisioning DNS records via Nostr events, and a certbot auth hook for obtaining Let's Encrypt certificates via DNS-01 challenges — all without a traditional domain registrar.

### Architecture

```
VM (23.182.128.216)
  ├── nostr-sdk (Python) → publishes kind 11111 events to Nostr relays
  ├── nodns-bot (VPS 46.224.104.12) → processes events → DDNS updates to Knot DNS
  ├── certbot → DNS-01 challenge via nodns TXT records
  └── Caddy → serves HTTPS with Let's Encrypt cert

Nostr Relay ← events ← VM
    ↓
nodns-bot → Knot DNS (ns1.nodns.shop)
    ↓
Public DNS: npub1xxx.nodns.shop A 23.182.128.216
            _acme-challenge.npub1xxx.nodns.shop TXT <token>
```

### Prerequisites on VM

```bash
apt install -y certbot caddy python3-venv
python3 -m venv /home/debian/shc-toolkit
source /home/debian/shc-toolkit/bin/activate
pip install nostr-sdk
```

### One-time setup

```bash
# Generate nodns keypair (run once, save to /tmp/nodns-keypair.json)
python3 -c "
from nodns_vm import NoDNSKeyPair
kp = NoDNSKeyPair.generate()
import json
json.dump({'nsec': kp.nsec, 'npub': kp.npub, 'fqdn': kp.fqdn}, open('/tmp/nodns-keypair.json', 'w'), indent=2)
print(kp.fqdn)
"
```

### Publish DNS records

```python
from nodns_vm import NoDNSKeyPair, publish_dns_records, verify_dns
import json

kp = NoDNSKeyPair.from_nsec(json.load(open("/tmp/nodns-keypair.json"))["nsec"])

publish_dns_records(kp, [
    {"type": "A", "name": "@", "value": "23.182.128.216", "ttl": 300},
])
```

### Certbot DNS-01 with nodns auth hook

The auth hook (`/tmp/certbot-auth-hook.py`) is called by certbot for each domain:

```bash
sudo certbot certonly --manual --preferred-challenges dns \
  --manual-auth-hook /tmp/certbot-auth-hook.py \
  --manual-cleanup-hook /bin/true \
  -d <npub-fqdn>.nodns.shop \
  --agree-tos --email you@example.com --non-interactive
```

The auth hook publishes `_acme-challenge.<fqdn>` TXT via nostr-sdk, waits 15s for propagation, then certbot verifies.

### Caddy with manual cert

```caddyfile
<npub-fqdn>.nodns.shop {
    tls /etc/letsencrypt/live/<npub-fqdn>.nodns.shop/fullchain.pem \
        /etc/letsencrypt/live/<npub-fqdn>.nodns.shop/privkey.pem
    respond "Hello from NoDNS + HTTPS!" 200
}
```

Caddy runs as `caddy` user — cert files need `chown -R caddy:caddy /etc/letsencrypt/{archive,live}/`.

### Verified end-to-end

```bash
$ curl https://npub1mv7l45exqsu5nr5tnefkr33ruhzjj4r8prg6qtcedv4lyf3rzguqptuwm4.nodns.shop
Hello from NoDNS + Let's Encrypt DNS-01!
```

Certificate issued by Let's Encrypt via DNS-01 through nodns. No port 80, no traditional DNS provider, no domain registrar.
