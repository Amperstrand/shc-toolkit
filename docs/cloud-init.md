# SHC cloud-init behavior

Empirically verified 2026-07-02 against the live SHC API by ordering disposable
VMs on both the Dev VPS and NVMe tiers, injecting a uniquely-marked
`#cloud-config` under the `user_data` field of `POST /ordering/submit`, then
SSHing in and inspecting `/var/lib/cloud/instance/user-data.txt`,
`cloud-init status --long`, and probe marker files.

## TL;DR

SHC **does** use cloud-init (NoCloud datasource, seed CD-ROM at `/dev/sr0`)
for first-boot provisioning, but **does not expose any API mechanism to inject
custom cloud-init user-data**. The provisioning backend auto-generates a fixed
cloud-config from order fields only.

| Tier | cloud-init | Custom `user_data` honored? |
|---|---|---|
| NVMe / SSD / HDD | **enabled and running** (`enabled-by-generator`) | **No** — field silently dropped |
| Dev VPS | **disabled by marker file** (`disabled-by-marker-file`) | **No** — field silently dropped (and cloud-init doesn't run at all) |

## What cloud-init receives (the seed disk content)

`/var/lib/cloud/instance/user-data.txt` on a freshly provisioned VM contains
**only** SHC's auto-generated fields, regardless of what you pass as
`user_data`:

```yaml
#cloud-config
hostname: <your-order-hostname>
manage_etc_hosts: true
fqdn: <your-order-hostname>
user: debian
password: <$6$... randomly generated hash>
ssh_authorized_keys:
  - <your ssh_key order field, if provided>
chpasswd:
  expire: False
users:
  - default
package_upgrade: true   # NVMe/SSD/HDD only; absent on Dev VPS
```

Notable: the order-time `ssh_key` field **does** reach the seed disk on every
tier. Whether it actually gets installed depends on whether cloud-init runs:

- **NVMe/SSD/HDD**: cloud-init runs → `ssh_authorized_keys` is processed →
  the key lands in `~debian/.ssh/authorized_keys` → SSH works with no extra
  step.
- **Dev VPS**: cloud-init is disabled → the seed is written but never
  consumed → the key is **not** installed → SSH fails with
  `Permission denied (publickey)`. The documented workaround is
  `POST /vm/{service_id}/ssh-keys/apply-live` (`client.apply_ssh_key_live`),
  which appends the key to the running VM's `authorized_keys` directly,
  bypassing cloud-init.

## What was tested

The `user_data` field was passed to `POST /ordering/submit` via
`client.submit_order(..., user_data=<cloud-config>)` on:

1. **Dev VPS Starter** (`dev-1c-4gb`, package 80) — service 821
2. **NVMe VPS Starter** (`nvme-1c-4gb`, package 23) — service 822

Both VMs received a `#cloud-config` containing:

```yaml
#cloud-config
write_files:
  - path: /tmp/tollgate-cloudinit-probe
    content: "<unique-token>-writefile"
runcmd:
  - echo '<unique-token>-runcmd' > /tmp/tollgate-cloudinit-runcmd
```

**Result on both tiers**: the probe files `/tmp/tollgate-cloudinit-probe` and
`/tmp/tollgate-cloudinit-runcmd` were **absent**, and the received
`user-data.txt` showed no trace of the `write_files`/`runcmd` content — only
SHC's auto-generated fields. The `user_data` field was silently dropped by the
provisioning backend despite being accepted by the API gateway
(`VmOrderRequest` has `additionalProperties: true`).

## Why custom user-data is not supported

The SHC API surface (`openapi.json`) and live catalog were fully inspected:

- `VmOrderRequest` (the `/ordering/submit` body schema) documents:
  `package_id`, `pricing_id`, `hostname`, `module_group_id`, `user`,
  `ssh_key`/`ssh_keys`, `coupon`, `order_form_id`, `package_group_id`,
  `config_options`. **No `user_data` / `cloud_init` / `boot_script` field.**
- The live catalog's `available_config_options` across all 20 packages contain
  only: `cpu`, `disk`, `gui_choice`, `ipv4s`, `ram`, `template`, `win_edition`.
  **No user-data option.**
- `ReinstallVmRequest` (`/vm/{service_id}/reinstall`) accepts only `template`.
- No `/user-data`, `/cloud-init`, or `/metadata` endpoint exists.
- `llms.txt` mentions no cloud-init user-data mechanism.

The Blesta provisioning plugin generates the seed-disk cloud-config from the
order fields above and has no code path to merge arbitrary user content.

## Practical implications

| Goal | Approach |
|---|---|
| Set hostname, create `debian` user, set password | Handled automatically by SHC's generated cloud-config on NVMe/SSD/HDD. On Dev VPS, cloud-init is disabled so these are set by the image/proxmox template instead. |
| Inject an SSH key at order time | Pass `ssh_key` in the order. **Works on NVMe/SSD/HDD** (cloud-init installs it). **Silently ineffective on Dev VPS** — call `apply_ssh_key_live` after provisioning. |
| Run custom first-boot code | **Not supported via the API.** Use SSH-after-provisioning (the pattern in `physical-router-test-automation/lib/cloud_lab/shc_submit.py`): wait for `provisioning_state == "ready"`, then SSH in and run the bootstrap script. |
| Pass a full `#cloud-config` | Not supported. Do not add a `user_data` parameter to client wrappers expecting it to execute. |

## Related

- `docs/compute-cashu-email.md` — earlier finding ("No boot_script/user_data") that this doc refines with the full cloud-init picture.
- The Dev VPS cloud-init-disabled behavior is the root cause of the historical
  "VM unreachable after provisioning" incidents (previously tracked in the
  now-removed `HANDOVER.md`).
