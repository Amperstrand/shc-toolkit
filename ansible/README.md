# SHC Ansible Integration

Full Ansible playbook for provisioning an SHC VPS, generating a NoDNS domain,
obtaining a Let's Encrypt certificate via DNS-01, and configuring Caddy as an
HTTPS reverse proxy.

## Quick Start

```bash
# 1. Set your SHC API key
export SHC_API_KEY="shc_live_..."

# 2. Install shc-toolkit (editable, from the repo root)
cd /path/to/shc-toolkit
pip install -e .

# 3. Run the playbook
cd ansible/
ansible-playbook -i localhost, playbook.yml

# 4. When done, tear down
ansible-playbook -i localhost, teardown.yml -e target_host=localhost \
  -e shc_service_id=<ID from step 3 output>
```

## What the playbook does

```
playbook.yml
  │
  ├── Role: shc_vm
  │     ├── Orders a VM via the SHC API
  │     ├── Waits for provisioning_state == "ready"
  │     ├── Injects your SSH public key via apply_ssh_key_live
  │     └── Adds the VM to the Ansible inventory dynamically
  │
  ├── Role: nodns
  │     ├── Generates a Nostr keypair (nsec/npub)
  │     ├── Installs nostr-sdk in a venv
  │     └── Registers <npub>.nodns.shop (auto-propagates via Nostr)
  │
  ├── Role: certbot
  │     ├── Installs certbot
  │     ├── Deploys the NoDNS auth hook script
  │     └── Requests a Let's Encrypt cert via DNS-01
  │
  └── Role: caddy
        ├── Installs Caddy
        ├── Configures reverse proxy with TLS
        └── Sets up daily renewal cron
```

## Configuration

All defaults are in `group_vars/all.yml`. Override before running:

```bash
# Use a larger VM
ansible-playbook playbook.yml -e shc_vm_size=nvme-2c-8gb

# Custom SSH key
ansible-playbook playbook.yml -e shc_vm_ssh_key_source=~/.ssh/my_key.pub

# Let's Encrypt staging (for testing)
ansible-playbook playbook.yml -e certbot_staging=true

# Different upstream app
ansible-playbook playbook.yml -e caddy_upstream=127.0.0.1:3000
```

## Dynamic Inventory

The `shc_inventory.py` script provides a dynamic inventory of all your SHC VMs:

```bash
# List all VMs
ansible all -i ansible/shc_inventory.py --list-hosts

# Ping all ready VMs
ansible shc_ready -i ansible/shc_inventory.py -m ping

# Run a command on all NVMe VMs
ansible shc_nvme -i ansible/shc_inventory.py -a "uptime"
```

Groups provided:
- `shc` — all SHC VMs
- `shc_ready` — VMs with provisioning_state == "ready"
- `shc_dev` / `shc_nvme` / `shc_ssd` / `shc_hdd` — by tier

## File Structure

```
ansible/
├── playbook.yml              # Main provisioning pipeline
├── teardown.yml              # Cancel VM + cleanup
├── shc_inventory.py          # Dynamic inventory script
├── group_vars/
│   └── all.yml               # Default configuration
└── roles/
    ├── shc_vm/
    │   └── tasks/main.yml    # Order + wait + SSH key injection
    ├── nodns/
    │   └── tasks/main.yml    # Keypair generation + DNS publishing
    ├── certbot/
    │   ├── tasks/main.yml    # Certificate request
    │   └── templates/
    │       ├── nodns-auth-hook.sh.j2
    │       └── nodns-cleanup-hook.sh.j2
    └── caddy/
        ├── tasks/main.yml    # Caddy installation + config
        ├── handlers/main.yml # Restart handler
        └── templates/
            └── Caddyfile.j2  # HTTPS reverse proxy config
```

## Requirements

- `shc-toolkit` installed (`pip install -e .` from repo root)
- `SHC_API_KEY` environment variable set
- Ansible 2.10+
- SSH key at `~/.ssh/id_ed25519.pub` (or override with `shc_vm_ssh_key_source`)

## Extending

Add your own roles after the pipeline:

```yaml
# playbook.yml — add at the end
  roles:
    - nodns
    - certbot
    - caddy
    - my_app        # Your app deployment role
    - monitoring    # Prometheus node exporter, etc.
```

The VM is in the `shc_ready` group with all SSH connection vars configured.
