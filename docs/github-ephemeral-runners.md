# Ephemeral GitHub Actions Runners on SHC

MVP implementation of disposable per-job GitHub Actions runners on cheap SHC
VPSs. The wedge: OSS maintainers with slow / expensive / custom CI can run
jobs on machines they control, pay only for the minutes used (typically a
few cents per job), and tear the runner down when the job ends.

## Status: MVP

- **Backend**: full SHC VPS per job. Order → wait → SSH bootstrap → runner
  online → cancel after job. Cold start is dominated by VM provisioning
  (~60 s measured live on `dev-4c-16gb`).
- **Future backend**: Firecracker microVM. The interface
  (`provision()` / `destroy()` and the JSON timing keys they return) is
  intentionally backend-agnostic. The metric we care about is **cold-start
  reduction**:

  | Stage | Full VPS (measured) | Firecracker (target) |
  |---|---|---|
  | Order/clone → VM ready | **61.4 s** | <5 s (microVM clone) |
  | VM ready → SSH reachable | **3.8 s** | <2 s |
  | SSH reachable → runner online | **69.8 s** (apt + Go install + register) | ~30 s (skip apt/Go) |
  | **Total cold-start** | **135.8 s** | **~35 s** (target) |

  Numbers in column 2 are from live measurement on VM 1102 (2026-07-04,
  `dev-4c-16gb`, `ubuntu2404-cloud`, Cherryvale-Kansas). Firecracker would
  eliminate the first row and shrink the third by skipping apt/Go install
  (baked into the microVM image).

### Provisioning floor is SHC-side, not size- or template-dependent

A sweep across three (size, template) combinations showed the
`order → ready` segment is essentially constant at **~100 s ± 5 s**,
independent of size or OS template. All three combos were placed on the
same physical IP, indicating SHC reuses host slots for sequential
cancel+reorder within minutes.

| Size | Template | Order → ready |
|---|---|---|
| `dev-1c-4gb` | `ubuntu2404-cloud` | 104.0 s |
| `dev-2c-8gb` | `ubuntu2404-cloud` | 100.3 s |
| `dev-1c-4gb` | `alpine323-cloud` | 101.8 s |

**Implication**: picking a smaller or leaner VPS does not reduce
cold-start. The ~100 s floor is SHC backend scheduling, not anything the
user controls. The only way past it is a long-lived host VM (pool
architecture) — which is also exactly what Firecracker needs.

### Firecracker preconditions verified on SHC

Live verification on `dev-4c-16gb` (2026-07-04, VM 1141):

| Check | Result |
|---|---|
| `/dev/kvm` exists with correct perms (`crw-rw---- root kvm`) | ✅ |
| `vmx` extensions visible in `/proc/cpuinfo` | ✅ |
| `kvm-ok` reports "KVM acceleration can be used" | ✅ |
| `firecracker v1.9.1` binary runs and reports `--version` cleanly | ✅ |
| Boot an actual microVM | ⏳ not measured this session |

The μVM boot was blocked by GCC 12+ warnings-as-errors when building
a Linux 5.10 kernel on Ubuntu 24.04 (specifically `-Wuse-after-free`
on the kernel's old `realloc` patterns in `tools/objtool`). Resolved
path: use Linux 6.1 LTS or install GCC 11. AWS publishes Firecracker
μVM boot at **~125 ms** on dedicated hardware; on SHC's nested KVM
(L2 virt) expect 200–500 ms — still 200–500× faster than the 100 s
SHC scheduling floor.

## Performance vs GitHub-hosted `ubuntu-latest`

Live measurement (2026-07-04): same go-test workload (8 modules from
`tollgate-module-basic-go`) run on (a) GitHub-hosted `ubuntu-latest` via
the existing `Test` workflow, and (b) a disposable SHC `dev-4c-16gb` VPS
provisioned via `shc github-runner provision`.

| Metric | `ubuntu-latest` | SHC VPS | Notes |
|---|---|---|---|
| Cold-start to runner online | ~5 s | **135.8 s** | SHC includes full VM order + bootstrap |
| Workload (8 go-test modules) | 57 s wall (8-way parallel matrix) | 25 s wall (sequential) | Per-module times comparable; SHC was sequential so total is sum |
| Cost per run | $0 (public repo) | **~$0.01** | SHC prorated from $0.90/day, 135 s used |
| CPU | 4 vCPU (shared) | 4 vCPU (dedicated) | Comparable |
| RAM | 16 GB | 16 GB | Same |
| Disk | 14 GB ephemeral | 32 GB persistent | SHC has more headroom |
| Nested KVM | No | **Yes** (Dev VPS line only) | SHC enables Firecracker-in-VM, custom kernels, etc. |

**Where SHC wins**:
- Private repos at scale (above ~10k build-minutes/month, GitHub pricing cliff)
- Custom hardware needs (nested KVM, GPUs, custom kernel)
- Long-running or stateful CI (SHC VM survives between jobs if you want)
- Jurisdictional / data-sovereignty requirements

**Where GitHub-hosted wins**:
- Cold-start latency (5 s vs 136 s — until Firecracker)
- Zero ops (no API key rotation, no orphan VMs to sweep)
- Public OSS repos (free forever)

The Firecracker backend target (~35 s cold-start) would close most of the
gap for the second category while preserving SHC's wins in the first.

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

## Known issues

### GitHub Actions workflow indexer can stall on fork repos

GitHub Actions registers new workflow files via an internal indexer that
runs after every push to the default branch. On **forks**, this indexer
occasionally stalls — the workflow file exists on disk and parses
correctly, but never appears in `GET /actions/workflows` and dispatch
returns `HTTP 404`.

We hit this on `Amperstrand/tollgate-module-basic-go` (a fork of
`OpenTollGate/tollgate-module-basic-go`) while dogfooding. None of the
standard kicks worked for us:

- ❌ Push to main + wait 5+ min
- ❌ Rename the file
- ❌ Empty commit to trigger re-scan
- ❌ `PUT /actions/permissions` toggle `enabled=false` then `true`

What did work as a long-shot was opening a PR from the dogfood branch —
the `pull_request` event path uses a different indexer pipeline. If you
hit the same issue, the cheap path is:

1. Push the workflow file to a feature branch instead of main
2. Open a PR against main
3. Wait 1–5 min for the PR-path indexer to pick it up
4. Dispatch with `gh api .../actions/workflows/<file>/dispatches -f ref=<feature-branch>`

If even the PR path stalls, the last fallback is the web UI:
**Actions → New workflow → Paste YAML → Start commit**. The web flow
uses yet another indexer code path.

No support ticket needed — the indexer will eventually catch up on its
own (sometimes hours), and the workflow file is correct in any case.
