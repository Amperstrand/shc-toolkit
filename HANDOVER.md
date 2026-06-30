# HANDOVER: SHC Dev VPS Migration for TollGate Cloud Lab

**Written**: 2026-06-22
**Author**: Sisyphus session (macbook, physical-router-test-automation)
**Audience**: Next LLM/agent picking up the SHC migration work
**Status**: Blocked — VM 605 is bricked. Need to diagnose, recover, and retry.

---

## Executive Summary

We're evaluating migrating the TollGate cloud lab from GCP to SHC (Sovereign Hybrid Compute) Dev VPS for cheaper nested-KVM CI runs ($0.01/run vs $0.05/run on GCP). We ordered a Dev VPS Standard (VM 605) but it's currently **bricked** — boots to a login prompt but has no network connectivity. This document covers everything we tried, what went wrong, and what to do next.

---

## What We're Trying to Achieve

Replace GCP as the cloud lab backend for `physical-router-test-automation`. The cloud lab runs nested KVM (OpenWrt + Debian QEMU VMs) to test the TollGate WiFi payment system. Currently runs on GCP `n1-standard-2` at ~$0.05/run. SHC Dev VPS Standard (2C/8GB, nested KVM) is $0.49/day with hourly refunds → ~$0.01/run. 5x cheaper.

### SHC Product Lines (3 lines, 20 packages total)

| Line | Location | Nested KVM | Use For |
|------|----------|------------|---------|
| NVMe VPS (pkg 23-35) | Katy, Texas | **No** | Regular workloads |
| SSD VPS (pkg 56-60) | Cherryvale, Kansas | **No** | Regular workloads |
| **Dev VPS (pkg 80-84)** | Cherryvale, Kansas | **Yes** | **TollGate cloud lab** |
| HDD VPS (pkg 36-40) | Katy, Texas | **No** | Budget workloads |

Dev VPS plans (the ones we want):

| Package | Specs | $/day | Snapshots |
|---------|-------|-------|-----------|
| 80 Starter | 1C/4GB/8GB | $0.26 | 1 |
| **81 Standard** | **2C/8GB/16GB** | **$0.49** | **1** |
| 82 Professional | 4C/16GB/32GB | $0.96 | 1 |
| 83 Business | 8C/32GB/64GB | $1.91 | 1 |
| 84 Enterprise | 16C/64GB/128GB | $3.79 | 1 |

**Important**: The README.md in this repo says "No nested KVM" under Known Limitations. **That is OUTDATED.** The Dev VPS line explicitly supports nested KVM. The README was written before Dev VPS plans were discovered.

### Pricing/Billing Model

- SHC charges per day (daily renewal)
- **Hourly refund**: When you cancel a VM, you get refunded for unused hours (rounded down). So a 30-minute run on a $0.49/day VM costs $0.49 - (23/24 * $0.49) = ~$0.02 refund → net cost ~$0.47... actually the exact refund mechanism needs verification. The SHC website says "hourly refunds" but the API doesn't expose the exact formula.
- **Daily billing**: You pay for a full day even if you use the VM for minutes. The refund comes when you cancel.
- This makes SHC attractive for CI: spin up, run tests (~30min), cancel, get refund for unused hours.

---

## VM 605 Timeline — What Happened

### Provisioning
- **2026-06-22 01:55 UTC**: VM 605 ordered as Dev VPS Standard (pkg 81)
- IP assigned: `66.92.204.236`, gateway `66.92.204.1`
- Template: `debian13-cloud`
- SSH key registered in API: our RSA public key
- **`bootstrap_completed_at`: null** — cloud-init NEVER completed

### Console Investigation (previous session, ~11:00-11:30 UTC)
The previous session captured 7 console screenshots showing:

1. `console-embedded.png`: VM at login prompt — `Debian GNU/Linux 13 tollgate-ci-01 tty1`
2. `console-after-username.png`: Tried logging in as `debian` user — password prompt appeared
3. `console-state-3.png`: Tried username `disagree-ranch-cart-escape-nephew-secret` (appears to be a generated passphrase being used as username — likely confused with the password)
4. `console-state-4.png`: Same login attempt, password field blank
5. `console-after-login.png`: Same — still at password prompt
6. `console-after-root.png`: Tried `root` login — password prompt
7. `console-after-root-password.png`: Same state, password being entered

**Key finding**: The VM boots to a Debian 13 login prompt on tty1. The OS kernel loads successfully. But nobody successfully logged in — they didn't know the password. The console screenshots show multiple failed login attempts.

### Reinstall
- **2026-06-22 08:18:51 UTC**: Reinstall job (293) triggered
- **2026-06-22 13:19:52 UTC**: Reinstall completed (took **5 hours** — abnormally long)
- Job message: `"Reinstall complete! Your server is starting up. New password is in Service Info."`
- Job error: `null` (no error reported)

### Post-Reinstall (our session, ~08:40 UTC)
- `runtime.state: "running"` — hypervisor sees VM as running
- `runtime.cpu_percent: 0-2%` — idle
- `runtime.mem_percent: 2-3%` — minimal usage
- `provisioning_state: "provisioning"` — stuck, never transitions to "completed"
- `bootstrap_completed_at: null` — cloud-init still never ran/completed
- `activity: []` — **empty activity log** (no events recorded at all)
- **ping**: 100% packet loss
- **SSH (port 22)**: connection timeout
- **Firewall**: ACCEPT/ACCEPT, no rules — nothing blocking at hypervisor level

### What We Tried
1. **SSH direct**: `ssh debian@66.92.204.236` → timeout
2. **Ping**: `ping 66.92.204.236` → 100% packet loss
3. **Port check**: `nc -z -w 5 66.92.204.236 22` → timeout
4. **VM restart**: `c.restart_vm(605)` → confirmed, VM came back as "running" but still unreachable
5. **Console session**: `c.create_console_session(605)` → returns a VNC URL with **30-second TTL** — too short to use from CLI

---

## Root Cause Analysis

### Most Likely: cloud-init Failed to Configure Networking

The VM boots (kernel loads, init starts, tty1 login prompt appears on console), but has no network connectivity. The most probable chain:

1. VM was provisioned/reinstalled with `debian13-cloud` template
2. cloud-init was supposed to: configure network interfaces, create the `debian` user, inject SSH keys, set hostname
3. **cloud-init failed or never executed** (`bootstrap_completed_at: null`, empty activity log)
4. Without cloud-init, the guest OS has no network configuration (interfaces may be down, no DHCP client running, wrong interface names)
5. The kernel boots fine (it doesn't need cloud-init), but userspace networking is unconfigured
6. The VM is "running" at the hypervisor level but unreachable from outside

### Why cloud-init Might Have Failed

**Hypothesis A: NoCloud datasource misconfigured for Dev VPS**
The Dev VPS line uses nested KVM (Proxmox-based). The NoCloud datasource (which provides cloud-init seed data via a CD-ROM or disk) might not be properly attached for Dev VPS instances. Regular NVMe/SSD VPS plans might work fine because they use a different Proxmox configuration.

**Hypothesis B: Network interface name mismatch**
Debian 13 with systemd may name interfaces differently (e.g., `ens18`, `enp6s18`) than what cloud-init's network configuration expects. If cloud-init tries to configure `eth0` but the actual interface is `ens18`, networking silently fails.

**Hypothesis C: The 5-hour reinstall broke something**
A reinstall that takes 5 hours is abnormal (should be 5-15 minutes). The reinstall may have partially failed — the disk image was written but post-install configuration (cloud-init, network) was not completed properly. The job reports "completed" because the disk imaging step finished, but the bootstrap step was skipped or failed silently.

**Hypothesis D: Password-based auth only, no SSH key injection**
The reinstall message says "New password is in Service Info." This suggests the reinstall may have reset to password-based authentication without injecting the SSH key. Even if networking worked, SSH key auth might not be configured. The password would be visible in the SHC web panel under Service Info (not accessible via API).

### Evidence Summary

| Evidence | Points To |
|----------|-----------|
| Console shows login prompt | OS boots fine, kernel OK |
| `bootstrap_completed_at: null` | cloud-init never finished |
| Empty activity log | No bootstrap events at all |
| 5-hour reinstall time | Reinstall process had issues |
| "New password in Service Info" | Reinstall reset auth to password |
| ping/SSH fail | Guest networking unconfigured |
| Firewall ACCEPT/ACCEPT | Not a hypervisor-level block |
| CPU 0-2%, mem 2% | VM idle — not crashed, just unreachable |

### What We Don't Know

1. **Was SSH ever working?** The activity log is empty — no successful SSH connections were ever recorded. The VM may have been broken from the very beginning (initial provisioning also had cloud-init failure).
2. **What's the actual password?** The reinstall set a new password, visible only in the SHC web panel's "Service Info" section (not exposed via API). The console screenshots show login attempts but nobody had the right password.
3. **Is this a known SHC issue?** We haven't checked the SHC knowledge base or opened a support ticket about Dev VPS provisioning failures.
4. **Does this affect all Dev VPS instances?** We only ordered one. It's possible this is a one-off issue or a systemic Dev VPS problem.

---

## What's Been Built (shc-toolkit repo)

### `shc_toolkit/client.py` — Full SHC API Client (637 lines)
Complete coverage of SHC v2 User API: 117 methods covering VM lifecycle, ordering, snapshots, backups, SSH keys, billing, support tickets, firewall, metrics, ISO, reverse DNS, affiliate, and more.

```python
from shc_toolkit import SHCClient
c = SHCClient()  # reads SHC_API_KEY from env
vms = c.list_vms()
c.start_vm(123)
c.create_snapshot(123, name="pre-deploy")
```

### `shc_toolkit/compute.py` — gcloud-Compute Shim (~300 lines)
**Drop-in replacement for `gcloud compute` commands** used by the tollgate cloud lab. Maps gcloud machine types to SHC Dev VPS packages:

| gcloud Machine Type | SHC Package | Specs |
|---------------------|-------------|-------|
| `n1-standard-2` | Dev VPS Standard (pkg 81) | 2C/8GB |
| `n1-standard-4` | Dev VPS Professional (pkg 82) | 4C/16GB |
| `n1-standard-8` | Dev VPS Business (pkg 83) | 8C/32GB |

Supports: `instances create/list/describe/delete/start/ssh`, `snapshots create/list`, `config get-value project`.

**Metadata**: SHC has no native instance metadata service (no `metadata.google.internal`). The shim stores metadata locally in `~/.shc-compute/metadata.json` keyed by hostname.

**IMPORTANT**: This shim has **never been tested** because we couldn't get a working VM. It needs end-to-end validation.

### `shc_toolkit/cli.py` — `shc` CLI
CLI wrapper around the client: `shc catalog`, `shc list`, `shc info <id>`, `shc order`, `shc cancel`, `shc snapshot`, etc.

### `shc_toolkit/nodns.py` — NoDNS Integration
Publishes DNS records via Nostr events (kind 11111) to `nodns.shop` domains. Verified working.

### `shc_toolkit/provision.py` — VM Provisioning
One-call setup for Caddy + HTTPS via Let's Encrypt DNS-01. Verified working on regular NVMe VPS.

### `dev-vps-plans.json` — Dev VPS Catalog
JSON dump of Dev VPS pricing plans. Contains `pricing_id` values needed for ordering.

### `tollgate/` — Cashu Tollgate (separate experiment)
A pay-per-minute SSH server that accepts Cashu ecash tokens. Not related to the cloud lab migration.

---

## GCP → SHC Migration Plan (What Needs to Happen)

The tollgate cloud lab (`physical-router-test-automation/lib/cloud_lab/`) currently uses GCP for:

1. **VM lifecycle**: `gcloud compute instances create/delete` — Create VM from snapshot, run tests, self-delete
2. **Snapshot management**: `gcloud compute snapshots create/list` — Baked snapshot with all deps pre-installed
3. **Instance metadata**: `gcloud compute instances add-metadata` — Pass GH_TOKEN, run config to VM
4. **SSH**: `gcloud compute ssh` — Connect to VM for debugging
5. **Nested virtualization flag**: `--enable-nested-virtualization` — Required for KVM-in-KVM
6. **Self-delete**: VM runs `gcloud compute instances delete` from inside itself when done
7. **Firewall rules**: GCP firewall allows SSH/HTTP from anywhere

### Key Differences: GCP vs SHC

| Feature | GCP | SHC Dev VPS |
|---------|-----|-------------|
| Nested KVM | `--enable-nested-virtualization` flag | **Built-in** (Dev VPS line) |
| Instance metadata | `metadata.google.internal` HTTP | **None** — use local JSON file |
| Self-delete from inside VM | `gcloud compute instances delete` | API call to `POST /vm/{id}/cancel` |
| Snapshots | Regional, persistent | Per-VM, 1 snapshot limit on Standard |
| Disk size | 50 GB default | **16 GB** (may be tight) |
| Billing | Per-second | Per-day with hourly refund |
| Machine type | `n1-standard-2` (2C/7.5GB) | Dev VPS Standard (2C/8GB) |
| SSH | OS Login / metadata keys | SSH key in ordering config or cloud-init |
| Firewall | GCP firewall rules | SHC firewall (ACCEPT/ACCEPT default) |
| Startup script | `gcloud compute instances create --metadata startup-script=...` | cloud-init user-data (if working) |

### Migration Steps (in order)

1. **Get a working Dev VPS** — Cancel VM 605, order fresh one, verify SSH + `/dev/kvm`
2. **Fix `compute.py` pricing_id values** — The pricing_id in compute.py (245) may be stale. Verify against current catalog.
3. **Adapt GCP-specific code in `lib/cloud_lab/`**:
   - `gcp.py` — Replace all `gcloud` subprocess calls with `shc-compute` or direct API calls
   - `constants.py` — Update `DEFAULT_DISK_SIZE_GB` (50→16), `SNAPSHOT_NAME`, zone references
   - `worker.py` — Replace metadata service reads with local JSON or env vars; replace self-delete mechanism
   - `bake-snapshot.py` — Adapt for SHC snapshot mechanism (1 snapshot limit, different API)
4. **Handle disk size**: 16 GB may be too small. The GCP snapshot is 50 GB provisioned / 3.5 GB actual. Options:
   - Order Dev VPS Professional (pkg 82, 32 GB disk, $0.96/day) for more headroom
   - Optimize the baked image to fit in 16 GB
   - Skip snapshot baking entirely and install deps on each run (slower but simpler)
5. **Handle metadata**: Replace GCP metadata service with:
   - Cloud-init user-data for startup config
   - Environment variables for secrets
   - Local JSON file for non-secret config
6. **Handle self-delete**: Replace `gcloud compute instances delete` with:
   - `curl` to SHC API `POST /vm/{id}/cancel` from inside the VM
   - Or a lease-based kill switch (host-side timer that cancels the VM)
7. **Test end-to-end**: Run a full tollgate test suite on SHC

### Relevant Files in physical-router-test-automation

| File | Lines | What It Does |
|------|-------|-------------|
| `lib/cloud_lab/gcp.py` | ~400 | GCP VM lifecycle (every `gcloud` call to shim) |
| `lib/cloud_lab/constants.py` | ~50 | GCP-specific constants (zone, machine type, snapshot name) |
| `lib/cloud_lab/worker.py` | ~800 | Cloud lab worker (boot VMs, setup mints, run tests, publish) |
| `scripts/bake-snapshot.py` | 694 | Baker (downloads OpenWrt+Debian, installs deps, snapshots disk) |
| `scripts/cloud-lab.py` | ~300 | CLI entry point for cloud lab submit/status/cleanup |

---

## Immediate Next Steps for the Next Agent

### Step 1: Cancel VM 605 (stop the bleed)

```python
from shc_toolkit.client import SHCClient
c = SHCClient()
c.cancel_vm(605)  # This requires confirmation flow
```

The cancel API also requires the `X-User-Api-Confirm` header. Handle it the same way as `submit_order()` does — catch the `confirmation_required` error, extract the confirmation_id, resend with the header.

### Step 2: Open a Support Ticket About Dev VPS Provisioning

Before ordering another VM, report the issue:

```python
c.create_support_ticket(
    subject="Dev VPS Standard (service 605) — cloud-init never completes, VM unreachable",
    message="""
VM 605 (tollgate-ci-01) was ordered as Dev VPS Standard.
After provisioning AND after a reinstall, the VM:
- Shows runtime state "running" but provisioning_state stuck at "provisioning"
- bootstrap_completed_at is null (cloud-init never completed)
- No network connectivity (ping fails, SSH fails)
- Console shows Debian 13 login prompt (OS boots fine)
- Firewall is ACCEPT/ACCEPT (not blocking)

Is this a known issue with Dev VPS cloud-init? 
Are there special steps needed for Dev VPS network configuration?
""",
    department_id=<find_from_list_support_departments>,
    priority="high",
    service_id=605,
)
```

### Step 3: Order a Fresh Dev VPS

If support is slow, order a new one and test immediately:

```python
c.submit_order(
    package_id=81,           # Dev VPS Standard
    pricing_id=245,          # daily pricing (VERIFY this is still current!)
    hostname="tollgate-ci-02",
    config_options={
        "126": "debian13-cloud",   # template
        "108": "..."               # SSH key (check config option format)
    },
)
```

**IMPORTANT**: Check the current `pricing_id` via `c.get_catalog()` before ordering. The pricing_id in `compute.py` (245) was from an earlier catalog dump and may have changed.

### Step 4: Verify the New VM Works

```bash
# Wait for provisioning (poll every 10s)
python3 -c "
from shc_toolkit.client import SHCClient
c = SHCClient()
c.wait_for_provisioning(606, timeout=600)  # new service ID
"

# Test SSH
ssh debian@<new-ip>

# Check nested KVM
ssh debian@<new-ip> "ls -la /dev/kvm && kvm-ok"

# Check disk space
ssh debian@<new-ip> "df -h /"

# Check cloud-init status
ssh debian@<new-ip> "cloud-init status --long"
```

### Step 5: If SSH Works, Proceed with Migration

Follow the migration steps above. Start by testing `compute.py` as a gcloud shim, then adapt the cloud lab code.

### Step 6: If SSH Does NOT Work

If the new VM also has the same issue (boots but unreachable):

1. **Try a different template**: Order with `debian12-cloud` or `ubuntu2404-cloud` instead
2. **Use VNC console**: The 30-second TTL makes it hard, but you can:
   - Generate a console session URL
   - Open it immediately in a browser (Playwright/browser automation)
   - Log in with the password from "Service Info" (check the web panel)
   - Run `ip addr`, `cloud-init status`, `dmesg | grep -i cloud` to diagnose
3. **Try the apply_ssh_key_live API**: `c.apply_ssh_key_live(service_id, public_key)` — this might inject a key into the running VM without needing cloud-init
4. **Check SHC KB**: `c.search_kb("Dev VPS network")` or `c.search_kb("cloud-init")`

---

## API Gotchas

### Confirmation Flow (destructive actions)
All destructive operations (reinstall, cancel, delete) require a two-step confirmation:

1. First call → HTTP 409 with `confirmation_required` error
2. Response body contains `confirmation.structuredContent.confirmation_id` (format: `cnf_...`)
3. Second call → same request + header `X-User-Api-Confirm: <confirmation_id>`

The `submit_order()` method in `client.py` handles this automatically. Other methods (reinstall, cancel) do NOT — you need to handle it manually.

```python
import requests
# Manual confirmation for any destructive action
def confirmed_call(client, method, path, data=None):
    headers = {"Authorization": f"Bearer {client.api_key}", "Content-Type": "application/json"}
    resp = requests.request(method, f"{client.base_url}{path}", json=data or {}, headers=headers)
    body = resp.json()
    if resp.status_code == 409 and body.get("confirmation", {}).get("structuredContent", {}).get("confirmation_id"):
        cid = body["confirmation"]["structuredContent"]["confirmation_id"]
        headers["X-User-Api-Confirm"] = cid
        resp = requests.request(method, f"{client.base_url}{path}", json=data or {}, headers=headers)
        return resp.json()
    return body
```

### SSH Keys Endpoint
`GET /vm/{id}/ssh-keys` returns 404 on VM 605. The endpoint may not be implemented for Dev VPS instances, or it may require a different path. The SSH key is stored in the VM's ordering config and in the top-level `ssh_key` field of the VM object.

### Snapshot Limit
Dev VPS Standard has `snapshot_limit: 1`. Only ONE snapshot per VM. The GCP baker creates snapshots freely. The SHC migration needs a different snapshot strategy:
- Option A: Bake into the single allowed snapshot, always restore from it
- Option B: Skip snapshots, install deps on each run (adds ~10-15 min per run)
- Option C: Order a higher tier (Professional has snapshot_limit: 1 too... all Dev VPS tiers have limit 1)

Actually all Dev VPS tiers have `snapshot_limit: 1`. This is a significant constraint vs GCP where you can have many snapshots.

### Console Session TTL
VNC console sessions expire in **30 seconds**. This is almost unusable for manual debugging from a terminal. Options:
- Use browser automation (Playwright) to open the console URL and interact
- Use the "Paste to VM" feature to send commands programmatically
- Open a support ticket and ask for a longer TTL

### API Key Location
The API key is in the `SHC_API_KEY` environment variable. It was set up in a previous session. The key format is `shc_live_...`.

### Activity Log May Be Empty
`GET /vm/{id}/activity` returned an empty array for VM 605. This means either:
- No events were recorded (possible SHC bug)
- Activity logging is not enabled for Dev VPS instances
- The events exist but the API doesn't expose them

Don't rely on the activity log for diagnostics.

---

## Cost Tracking

| Item | Cost |
|------|------|
| VM 605 (1 day, bricked) | $0.49 |
| Expected: Fresh VM + 30-min test run | ~$0.02 (with hourly refund) |
| Expected: Full bake + test cycle (~2h) | ~$0.04 |
| GCP equivalent (for comparison) | ~$0.05/run |

Total spent so far: $0.49 (one wasted day on the bricked VM).

---

## Console Screenshots

Seven screenshots from the previous session are in the repo root:
- `console-embedded.png` — Initial console view, login prompt
- `console-after-username.png` — Tried `debian` username
- `console-state-3.png` — Tried passphrase as username
- `console-state-4.png` — Same attempt, no password
- `console-after-login.png` — Still at password prompt
- `console-after-root.png` — Tried `root` username
- `console-after-root-password.png` — Entering password

None show a successful login. The password was never discovered (it's in the SHC web panel "Service Info" section, not accessible via API).

---

## Summary of Recommendations

1. **Cancel VM 605** — it's bricked and accruing daily charges
2. **Open a support ticket** — ask SHC about Dev VPS cloud-init issues
3. **Order a new VM** — try with different template if the same issue occurs
4. **Verify SSH + `/dev/kvm` before anything else** — don't start migration until basic VM access works
5. **Test `compute.py` shim** — it's written but never tested
6. **Plan for snapshot constraint** — only 1 snapshot per Dev VPS; may need to skip baking
7. **Fix README.md** — remove "No nested KVM" limitation (it's wrong for Dev VPS line)
8. **Update `compute.py` pricing_id values** — verify against current catalog before using

The migration is feasible but blocked on getting a working VM. The SHC API is well-documented and the toolkit is solid — the issue is specifically with Dev VPS provisioning (cloud-init not completing). This may be a platform issue worth escalating to SHC support.
