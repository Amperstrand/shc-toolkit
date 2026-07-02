# SHC Cloud-Init Seed Security Audit

**Date:** 2026-07-02
**Scope:** Passive analysis of the NoCloud seed disk (`/dev/sr0`) attached to customer-provisioned VMs on the Dev VPS and NVMe tiers. All data examined is exposed to every customer who provisions a VM — no hypervisor-side or out-of-scope access was used.
**Purpose:** Responsible-disclosure feedback to help SHC harden their cloud-init provisioning.
**Method:** Ordered disposable VMs on both tiers, mounted the seed disk, and analyzed `user-data`, `vendor-data`, `meta-data`, and `network-config`.

## Executive summary

The seed disk does **not** expose hypervisor credentials, Proxmox API tokens, or a viable VM-breakout path. The findings are information-leakage and **inconsistent-hardening** issues, the most significant being that the Dev VPS tier ships without its own security baseline due to a cloud-init disable marker.

| # | Finding | Severity | Tier |
|---|---|---|---|
| 1 | Dev VPS cloud-init disabled → vendor-data hardening never runs | **MEDIUM** | Dev VPS |
| 2 | `ssh_deletekeys: false` — potential SSH host-key duplication across VMs | LOW-MEDIUM | Both |
| 3 | Internal site/cluster naming leaked in `network-config` search domain | LOW | Both |
| 4 | Internal documentation references in `vendor-data` comments | LOW | Both |
| 5 | Password hash exposed in world-readable seed `user-data` | LOW (standard cloud-init) | Both |

## Finding 1 — Dev VPS ships without its own security hardening (MEDIUM)

**Observation:** The Dev VPS template includes `/etc/cloud/cloud-init.disabled` (an empty marker file). Cloud-init reports `status: disabled`, `boot_status_code: disabled-by-marker-file`. The NVMe tier has no marker and cloud-init runs normally (`enabled-by-generator`).

**Impact:** The Dev VPS seed disk contains a 7.5 KB `vendor-data` that would:
- Install and enable `auditd` with command-execution logging (`-a always,exit -S execve -k shc_exec`)
- Enable `qemu-guest-agent` verbose logging for auditability
- Harden SSH (disable password auth when keys are present)
- Run `package_upgrade` for security patches

**None of this runs on Dev VPS** because cloud-init is disabled. A customer who provisions a Dev VPS gets a VM without the audit logging, guest-agent auditing, or SSH hardening that SHC evidently intended to apply. This is an inconsistent security posture across tiers that customers cannot detect without inspecting the seed disk themselves.

**Likely root cause:** The marker was probably added to the Dev VPS template to skip the slow `package_upgrade` on the cheap tier (reducing first-boot time), but it also disables all the other hardening in the vendor-data.

**Recommendation:** If the goal is to skip `package_upgrade` on Dev VPS, set `package_upgrade: false` in the Dev VPS vendor-data (which is already the case) and **remove the marker file** so the rest of the hardening (auditd, guest-agent, SSH) still applies. Alternatively, move the hardening out of cloud-init into the image-bake process so it's present regardless of the cloud-init enable state.

## Finding 2 — `ssh_deletekeys: false` (LOW-MEDIUM)

**Observation:** Both tiers' `vendor-data` sets `ssh_deletekeys: false` (cloud-init's default is `true`). This tells cloud-init NOT to regenerate SSH host keys on first boot.

**Impact:** If the base image was not properly prepared (i.e., host keys were not regenerated at image-bake time), multiple VMs from the same template could share identical SSH host keys. Shared host keys defeat SSH host-key verification, enabling man-in-the-middle attacks between VMs or against clients that pin host keys.

**Caveat:** If SHC's image-bake process regenerates host keys per-image (via `ssh-keygen` or `virt-sysprep --ssh-inject`), this finding is mitigated. The cloud-init output log on the test VMs *did* show host-key generation, but it was unclear whether that was the initial image creation or a per-boot regeneration. SHC should confirm host keys are unique per deployed VM.

**Recommendation:** Either (a) restore `ssh_deletekeys: true` (let cloud-init guarantee uniqueness), or (b) confirm the image-bake pipeline regenerates host keys and document that decision.

## Finding 3 — Internal naming leaked in network-config (LOW)

**Observation:** The `network-config` sets a DNS search domain of `cv1.ks.sovereignhybridcompute.com`. This reveals:
- `cv1` — likely an internal cluster/site code ("compute virtualization 1")
- `ks` — likely a datacenter/location code (Kansas)
- The gateway and DNS resolver are both `66.92.204.1` (single device serving both roles — flat network)

**Impact:** Low. This reveals SHC's internal naming convention and confirms a flat /24 network topology with static IP allocation (no DHCP). An attacker who provisions a VM learns the subnet structure and can infer the addressing scheme of other VMs. This is common across VPS providers and not exploitable on its own, but reducing the information in the search domain (e.g., using a generic `sovereignhybridcompute.com`) would reduce reconnaissance value.

## Finding 4 — Internal documentation references in vendor-data comments (LOW)

**Observation:** The NVMe `vendor-data` contains detailed troubleshooting comments that reference internal infrastructure knowledge:
- `"proven on Ubuntu 26.04 — coordination.md"` — references an internal document
- Detailed explanation of an SSH drop-in ordering bug they hit (`50-cloud-init.conf` overriding `00-` prefixes)
- Mentions of "Blesta" (their billing/provisioning platform) in comments

**Impact:** Low information disclosure. A sophisticated attacker learns SHC's internal tooling (Blesta), the OS versions they've tested, and the specific bugs they've worked through. This could aid targeted attacks (e.g., known Blesta CVEs). The comments are helpful for SHC's own engineers but shouldn't ship in production vendor-data.

**Recommendation:** Strip internal commentary from production vendor-data, or move it to an internal documentation system.

## Finding 5 — Password hash in seed user-data (LOW)

**Observation:** The seed `user-data` contains the `debian` user's password as a SHA-512 crypt hash (`password: $6$...`). This is standard cloud-init practice (`chpasswd`), and the password is randomly generated per-VM.

**Impact:** Low. Anyone who can read the seed disk (the VM owner) can attempt offline cracking. Since the password is random and sufficiently long, this is not practically exploitable. Noted for completeness — this is how every cloud-init provider works.

## Breakout assessment

**No viable VM-breakout path was identified in the seed data.** Specifically:
- No hypervisor credentials, Proxmox API tokens, or internal service credentials are present in any seed file.
- No PCI passthrough, shared filesystems, or host-mount exposure is evident.
- The `network-config` shows standard flat tenant networking with no route to management networks beyond the gateway.
- The `qemu-guest-agent` runs as root in the guest and can execute commands triggered by the Proxmox host, but this is a standard Proxmox feature not exploitable by the tenant (it's a host→guest channel, not guest→host).

The seed data exposes **information about SHC's infrastructure** (naming, tooling, topology) but not **access to it**.

## What we could NOT test from the tenant vantage point

- Whether the Proxmox host exposes the QMP/guest-agent socket to tenants (would require hypervisor-side access)
- Whether the flat /24 has any isolation between tenant VMs (ARP spoofing, L2 attacks) — would require active testing against other tenants, which is out of scope
- Whether the static IP allocation could be abused (IP squatting, gateway impersonation) — active test, out of scope
- Image-bake host-key uniqueness (Finding 2) — requires comparing host keys across multiple VMs from the same template

## Recommended disclosure

These findings are suitable for submission via SHC's support ticketing system (`POST /support/tickets`). Finding 1 (Dev VPS hardening gap) is the most actionable and should be reported first.
