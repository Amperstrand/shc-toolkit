# IaC Lifecycle Semantics — How SHC Maps to Industry Terms

SHC's lifecycle differs from the big clouds in two load-bearing ways, and
the whole toolkit + Terraform provider + Pulumi bridge encode them. This
guide gives the vocabulary mapping and the reasoning; the provider-side
canonical doc with the full design table is
[terraform-provider-shc/docs/lifecycle-alignment.md](https://github.com/Amperstrand/terraform-provider-shc/blob/main/docs/lifecycle-alignment.md).

## Vocabulary

| Industry term | AWS / GCP | SHC term | Where it lives here |
|---|---|---|---|
| terminate / delete (billing ends) | `TerminateInstances` / instance delete | **cancel** (`cancel_vm(immediate=True)`) | `SHCClient.cancel_vm`, TF `Delete()`, `shc cancel` |
| stop / pause (billing usually pauses — **not on SHC**) | stop / `desired_status=TERMINATED` | stop / shutdown | `SHCClient.stop_vm/shutdown_vm`, TF `power_state="stopped"` |
| desired power state | GCP `desired_status` | — | TF `power_state` attribute |
| observed state (drift) | `instance_state` / `current_status` | `service_status` + `provisioning_state` | computed attrs, `shc list/info` |
| deletion protection | `disable_api_termination` / `deletion_policy` | **confirm-gate** (409 + single-use `confirmation_id` → `X-User-Api-Confirm`) | both transports, `_confirmed_request` |
| orphan cleanup | provider test **sweepers** | hourly **reaper** | `reap_orphans()`, `reap-orphan-vms.yml` |
| — (no cloud equivalent) | — | **self-destruct timer** (on-VM cancel at boot+Nmin) | `shc_toolkit/selfdestruct.py` |
| billing period | per-second, running only | **daily term**, renewed from credit, by existence | `term`, `auto_cancel` |

## The two divergences that matter

1. **Stopped ≠ free.** AWS/GCP stop compute charges when stopped (disks
   keep billing). SHC charges the **full daily price while the service
   exists**, regardless of power state. `stop`/`shutdown` are a pause;
   only `cancel` ends billing (with a prorated refund of the unused day).
   Every teardown path in our tooling — CI `if: always()` steps, the
   reaper, the self-destruct timer, `terraform destroy` — fires **cancel,
   never stop**. The Python client prints a "still bills while stopped"
   warning on `stop_vm`/`shutdown_vm`; the TF provider warns at apply and
   in the `power_state` schema description at plan time.
2. **Ephemeral by default.** Clouds renew instances; our tooling defaults
   to destroy-at-term (`auto_cancel = true`, `cancel --end-of-term`
   patterns) so nothing outlives its paid term by accident. Earned from
   leaked-VM incidents (AGENTS.md lessons).

## Reasoning, one paragraph each

- **Destroy = terminate**: same as every major cloud; on SHC it is also the
  only way to stop billing, so nothing weaker is ever used for teardown.
- **Power state as a TF attribute** (GCP `desired_status` pattern, not
  AWS action-resources): one resource owns the lifecycle; power diffs show
  in `terraform plan`.
- **No `deletion_protection` attribute**: SHC's server-side confirm-gate on
  every destructive op + Terraform-native `prevent_destroy` already cover
  both sides; AWS needs its attribute only because raw EC2 has no gate.
- **Readiness = active + IP, never `provisioning_state == ready`**: SHC's
  `provisioning_state` stays `provisioning` forever on real VMs; a status
  field is a claim, active + assigned IP (+ reachable SSH) is proof.
- **Self-destruct timer**: no cloud needs it (per-second billing); SHC's
  daily-term-by-existence billing makes a controller-dead leak expensive
  enough to warrant an on-VM failsafe. Bounded full-scope key (only full
  can cancel — money class), systemd timer (survives reboot, unlike `at`).
