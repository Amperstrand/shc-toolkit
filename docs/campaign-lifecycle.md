# Campaign Lifecycle — Ephemeral VM Work With Receipts

Every ephemeral-VM project (fuzz campaigns, trace-repro loops, soak tests,
one-off benchmarks) re-derives the same lifecycle: order → provision → run
→ exfiltrate → close. This guide is the encoded version, earned across the
2026-09 lightning-playground campaigns (net spend $0.04 for a full
validation arc — the discipline below is why it stayed there).

The universal rules that make a campaign cheap and safe:

1. **Cancel, never stop.** A stopped VM bills its full daily price (see
   [iac-lifecycle.md](iac-lifecycle.md)); only `cancel` (immediate) ends
   billing with a prorated refund. Minimum charge is 1 hour.
2. **Tag for the reaper before you need it.** `--reap 8h` (or a
   `-reap<deadline>` hostname tag) makes the VM clean itself up even if
   your session dies. Deadline-tagged reaping sizes the reap to the work.
3. **Reachability is not `provisioning_state`.** The only health signal
   that means anything is TCP/22 answering. `active` + an IP is a billing
   state, not a network state (issue #39: weeks of billing-active,
   unroutable Dev VMs).
4. **Spend is the human's call.** Order and pay are confirm-gated
   server-side; the toolkit's `--confirm` flags are the explicit yes.

## The loop, with the toolkit

```bash
# 0. Pick a facility that actually routes to you (Katy lines: nvme/hdd).
shc sizes --available          # facility + reachability flags + live stock

# 1. Order — zone-guarded (refuses ssd-*/dev-* unless --allow-unstable-zone),
#    reaper-tagged, and reachability-gated: if TCP/22 never opens, the VM
#    is cancelled immediately (prorated refund) and the command exits 1.
shc order --hostname fuzz-reap6h --size nvme-2c-8gb \
  --ssh-key ~/.ssh/id_ed25519.pub \
  --reap 6h --pay --verify-reachability

# 2. Provision — the wait ends on active+IP, then TCP/22 (sshd may lag
#    ~120s behind 'ready'; cloud-init even longer — wait before assuming
#    full configuration).
shc info <service_id>

# 3. Run — stamp artifacts, keep the run resumable. If the box runs
#    untrusted code, do NOT arm self-destruct there (the planted key is
#    account-wide spend for its lifetime).

# 4. Exfiltrate — ship completion artifacts before teardown. A
#    completion-watcher + pull survives `kill -9` of the driving session.

# 5. Close — guards → pull → verify → cancel:
shc cancel <service_id>        # immediate; prorated refund
shc reap --dry-run             # confirm nothing leaked
```

## Guards, in order of when they save you

| Guard | Fires when | Cost if missing |
|---|---|---|
| `--allow-unstable-zone` refusal (order-time) | facility flagged unroutable (#39) | paid VM, hours of diagnosis |
| `--verify-reachability` (post-provision) | active+IP but TCP/22 dark | billing until manual cancel |
| `--reap <deadline>` / `-reap` hostname tag | session dies mid-campaign | VM bills for days |
| self-destruct timer (`selfdestruct.py`) | controller dead, VM reachable | same — needs a bounded full-scope key |
| daily reaper (`reap-orphan-vms.yml`) | everything above failed | capped at age + prefixes |
| `shc reap --dry-run` (session end) | your own sloppiness | caught before it costs |

## The receipts

A campaign is closed when you can show, from real command output:

- the order id + hostname + size (what existed),
- the cancel confirmation (billing ended),
- `shc reap --dry-run` → no orphans (nothing leaked),
- the exfiltrated artifacts (the work survived the teardown).

Anything less — "it should have cancelled", "stop will hold it" — is an
open incident. See `lightning-playground` docs/LESSONS-2026-09-02 for the
campaign this was extracted from, and AGENTS.md lesson 25 (the 13-hour
stopped-but-billable VM) for what skipping step 5 costs.
