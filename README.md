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
