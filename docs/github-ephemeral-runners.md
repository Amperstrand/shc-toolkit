# Ephemeral GitHub Actions Runners on SHC

MVP implementation of disposable per-job GitHub Actions runners on cheap SHC
VPSs. The wedge: OSS maintainers with slow / expensive / custom CI can run
jobs on machines they control, pay only for the minutes used (typically a
few cents per job), and tear the runner down when the job ends.

## Status: MVP

- **Backend**: full SHC VPS per job. Order → wait → SSH bootstrap → runner
  online → cancel after job. Cold start is dominated by VM provisioning
  (~3–5 min on SHC).
- **Future backend**: Firecracker microVM. The interface
  (`provision()` / `destroy()` and the JSON timing keys they return) is
  intentionally backend-agnostic. The metric we care about is **cold-start
  reduction**:

  | Stage | Full VPS | Firecracker (target) |
  |---|---|---|
  | Provisioning | 180–300 s | <5 s (clone) |
  | SSH reachable | +15–60 s | +1–2 s |
  | Runner online | +30–90 s | +30–90 s (same) |

  Firecracker eliminates the first two rows. The third is GitHub-side
  registration overhead and is unaffected by backend.

## CLI

```bash
export SHC_API_KEY="shc_live_..."
export SHC_GITHUB_ADMIN_TOKEN="ghp_..."   # PAT with repo admin / runners:write

shc github-runner provision \
  --repo Amperstrand/tollgate-module-basic-go \
  --size dev-4c-16gb \
  --template ubuntu2404-cloud \
  --labels shc-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}
```

Output is always JSON:

```json
{
  "ok": true,
  "service_id": 1234,
  "ip": "1.2.3.4",
  "runner_name": "shc-abc123",
  "runner_label": "shc-42-1",
  "labels": ["self-hosted", "linux", "x64", "shc", "shc-42-1"],
  "backend": "shc-vps",
  "created_at": "2026-07-04T12:00:00Z",
  "timings": {
    "t0_started":        {"iso": "...", "epoch": 1783000000.0},
    "t1_order_submitted":{"iso": "...", "epoch": 1783000000.5},
    "t2_vm_ready":       {"iso": "...", "epoch": 1783000180.0},
    "t3_ssh_reachable":  {"iso": "...", "epoch": 1783000200.0},
    "t4_runner_configured": {"iso": "...", "epoch": 1783000260.0},
    "t5_runner_online":  {"iso": "...", "epoch": 1783000290.0},
    "t6_finished":       {"iso": "...", "epoch": 1783000290.5},
    "durations": {
      "order_to_ready_s": 179.5,
      "ready_to_ssh_s": 20.0,
      "ssh_to_online_s": 90.0,
      "total_s": 290.5
    }
  }
}
```

Destroy is idempotent — re-running it on an already-canceled VM returns
`{"ok": true, "action": "already-cancelled"}` rather than failing:

```bash
shc github-runner destroy --service-id 1234
```

## SSH key strategy

The provision command needs to SSH into the VM to bootstrap the runner.

- **Default**: ephemeral ed25519 keypair generated per run, written to a
  0700 temp dir, used for one SSH bootstrap, then reaped with `/tmp`.
- **Escape hatch**: `--ssh-public-key ~/.ssh/id_ed25519.pub
  --ssh-private-key ~/.ssh/id_ed25519`. Useful for local debugging or
  long-lived test VMs.

The workflow at
[`.github/workflows/shc-runner-benchmark.yml`](https://github.com/Amperstrand/tollgate-module-basic-go/blob/dogfood/shc-runner-benchmark/.github/workflows/shc-runner-benchmark.yml)
in the Amperstrand fork of `tollgate-module-basic-go` uses the default.

## Secrets required

| Name | Used by | Notes |
|---|---|---|
| `SHC_API_KEY` | provision | SHC user API key. The default `GITHUB_TOKEN` cannot do this. |
| `SHC_GITHUB_ADMIN_TOKEN` | provision | PAT with `repo` scope (classic) or `Administration: read+write` (fine-grained) on the target repo. Mint one at `https://github.com/settings/tokens`. |

Never hardcode these in workflow YAML, commit them, or log them.

## Python API

```python
from shc_toolkit.github_runner import (
    ProvisionRequest, provision, destroy,
)

req = ProvisionRequest(
    repo="Amperstrand/tollgate-module-basic-go",
    github_token=os.environ["SHC_GITHUB_ADMIN_TOKEN"],
    size="dev-4c-16gb",
    template="ubuntu2404-cloud",
    labels=["shc-42-1"],
)
result = provision(req)
print(result.to_dict())

# Later — always runs, even on cancel
destroy(result.service_id)
```

## Timing instrumentation

The `t0`–`t6` markers and the derived `durations` are stable keys. Do not
rename without also updating the dogfood workflow summary job and any
dashboards that consume them. These are the points used to compare
backends:

- `t0_started` → `t1_order_submitted`: token + URL resolution (small)
- `t1_order_submitted` → `t2_vm_ready`: VM provisioning (the wedge)
- `t2_vm_ready` → `t3_ssh_reachable`: SSH come-up (small for Firecracker)
- `t3_ssh_reachable` → `t5_runner_online`: bootstrap + register (same across backends)
- `t0_started` → `t6_finished`: total cold start

## Roadmap (not in this MVP)

1. **Webhook autoscaler** — `workflow_job` webhook → provision-on-demand,
   no `provision` job in the workflow itself.
2. **Firecracker backend** — microVM clone replaces `t1`→`t3`. The
   `provision()` signature stays the same; only the implementation swaps.
3. **Sweeper** — `shc github-runner sweep --older-than 1h` for orphaned
   VMs left over from hard cancels.
4. **Pool mode** — keep N warm runners, hand them out, replenish async.
