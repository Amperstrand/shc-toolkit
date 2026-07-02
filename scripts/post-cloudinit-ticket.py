"""Post the cloud-init user-data feature request to SHC support.

Message 1 (ticket): the primary ask — custom cloud-init user-data.
Message 2 (reply): FYI observations from testing — not blockers.

Saves exact posted text to notes/posted-ticket-<timestamp>/ for the record.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from shc_toolkit import SHCClient

NOTES = Path(__file__).resolve().parent.parent / "notes"

SUBJECT = "Feature request: custom cloud-init user-data / first-boot scripts"

MESSAGE_1 = """Hi SHC team,

We've been integrating SHC into our automated test infrastructure (we maintain the shc-toolkit Python client and the Pulumi/Terraform providers for SHC) and have a feature request.

## The request

We'd like to be able to pass a custom cloud-init script (user-data) when ordering a VM, so it runs automatically on first boot. Currently, as far as we can tell from the API (POST /ordering/submit and the config_options catalog), there's no field for custom user-data or a startup script.

This means our provisioning flow has to: create the VM, wait for it to become ready, SSH in, and then manually run our deploy script. It works, but it means the orchestrator has to stay alive between creation and deployment, and it adds latency.

If we could pass user-data at order time (like Hetzner, GCP, AWS, and Azure all support), our VMs could be truly fire-and-forget.

## Suggested implementation

Since SHC runs Proxmox, the natural mechanism is `qm set <vmid> --cicustom` with separate vendor and user snippets:

- vendor= : SHC's own provisioning (user creation, SSH keys, audit rules — what's currently in the auto-generated vendor-data)
- user= : the customer's custom script

Cloud-init runs vendor-data first, then user-data, so customer scripts would execute AFTER SHC's own setup. The implementation would be: accept a `user_data` string field on the order API, write it to a Proxmox snippet, reference it via cicustom when generating the cloud-init drive.

We've confirmed that cloud-init does run on the NVMe tier (takes about 80 seconds after the VM boots) and that the NoCloud seed disk is fully populated — so the infrastructure is already in place, it just needs the API field to let customers inject their own config.

This is not a blocker for us — just something we'd find very useful as we scale our automation.

## Secondary observations

While testing VM provisioning across tiers, we collected some observations (cloud-init behavior differences between Dev VPS and NVMe, SSH configuration posture, etc.). These are not blockers or urgent issues — just things we noticed during our integration work that you might find interesting to audit against. Details are in the follow-up message.

Thanks for the great service!
"""

MESSAGE_2 = """FYI observations from our integration testing — these are not blockers or urgent issues, just things we came across while building our automation. We thought they might be interesting for your team to audit against.

This report was prepared with AI assistance for the analysis. I supervised the testing process but have not independently verified every technical detail — please treat these as preliminary observations rather than definitive findings.

## 1. Cloud-init behavior differs between Dev VPS and NVMe

We tested provisioning on both tiers and inspected the NoCloud seed disk (/dev/sr0):

- **NVMe**: cloud-init runs on first boot (~80 seconds to complete). The vendor-data installs auditd, qemu-guest-agent, and hardens SSH. Works as expected once cloud-init finishes.
- **Dev VPS**: cloud-init is disabled via a marker file (/etc/cloud/cloud-init.disabled). However, the hardening (auditd, guest-agent) appears to be baked into the Dev VPS image directly, so it's present regardless.

One operational note: the `provisioning_state: ready` signal appears to fire when the VM boots, not when cloud-init finishes. On NVMe, there's roughly an 80-second window where the VM is "ready" but cloud-init is still installing packages. Automation that SSHes in immediately after "ready" may find packages not yet installed. Polling `cloud-init status` before assuming full configuration would be more reliable.

## 2. SSH posture differs between tiers

- **Dev VPS**: PasswordAuthentication yes + PermitRootLogin yes (set via a 00-shc-root-login.conf drop-in baked into the image)
- **NVMe**: PasswordAuthentication no (hardened by cloud-init's vendor-data after ~80s)

This is presumably intentional (the SHC portal provides the root password for Dev VPS access), but the inconsistent posture between tiers is worth noting.

## 3. SSH host keys are unique per VM

We ordered two NVMe VMs from the same template and compared SSH host key fingerprints — they were different, confirming host keys are regenerated per-VM despite `ssh_deletekeys: false` in the vendor-data. No issue here.

## 4. Positive security observations

- No metadata service at 169.254.169.254 (no SSRF attack surface — SHC uses the NoCloud seed disk instead)
- No L2 neighbor visibility between tenant VMs (tenant isolation appears effective)
- No credentials or secrets found in any seed disk file
- qemu-guest-agent runs with verbose logging (good for auditability)
- Minimal attack surface: only SSH (port 22) exposed externally

## 5. Vendor-data comments reference internal docs

The NVMe vendor-data contains detailed troubleshooting comments that reference internal documentation (e.g., "coordination.md") and internal infrastructure details (the Blesta platform, specific OS version findings). These are visible to any customer who inspects their seed disk. Low severity, but you may want to strip internal commentary from production vendor-data.

## Artifacts

We have saved the full seed disk contents (user-data, vendor-data, meta-data, network-config) from both tiers, plus system reconnaissance data, in our local notes. Happy to share specific files if useful.
"""


def main():
    c = SHCClient()
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    outdir = NOTES / f"posted-ticket-{ts}"
    outdir.mkdir(parents=True, exist_ok=True)

    # Save what we're about to post
    (outdir / "subject.txt").write_text(SUBJECT)
    (outdir / "message-1.txt").write_text(MESSAGE_1)
    (outdir / "message-2.txt").write_text(MESSAGE_2)

    print("=== creating support ticket ===")
    result = c.create_support_ticket(
        subject=SUBJECT,
        message=MESSAGE_1,
        department_id=1,
        priority="medium",
    )
    ticket_id = result.get("ticket_id") or result.get("id")
    print(f"ticket created: id={ticket_id}")
    print(f"  result: {json.dumps(result, indent=2)[:400]}")
    (outdir / "create-result.json").write_text(json.dumps(result, indent=2))

    if ticket_id:
        print(f"\n=== posting follow-up reply (message 2) ===")
        reply = c.reply_support_ticket(ticket_id, MESSAGE_2)
        print(f"reply posted: {json.dumps(reply, indent=2)[:200]}")
        (outdir / "reply-result.json").write_text(json.dumps(reply, indent=2))

    print(f"\n=== done. artifacts in {outdir} ===")
    print(f"ticket URL: https://blesta.sovereignhybridcompute.com/client/support/tickets/{ticket_id}/")
    return 0


if __name__ == "__main__":
    main()
