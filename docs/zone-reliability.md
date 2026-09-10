# Zone & Reliability Map — Every SHC Facility, What's Verified, What Guards It

Live-earned 2026-09-09/10 while investigating the dev-zone EU/US asymmetry.
Everything below is evidence from probes, not vendor claims. When any cell
here matters to a decision, re-earn it — the map describes a moment, not a
law. Last full re-verification: 2026-09-10 (~07:30 UTC).

## The facilities

| Zone | Module group | Catalog lines | Nested KVM | BGP (RIS view) |
|---|---|---|---|---|
| **Katy, Texas** | g4 | `nvme-*` | ❌ (probed 2026-07-20: no `vmx/svm`, no `/dev/kvm`) | ✅ `23.182.128.0/24` announced (AS401933 HASHIT) |
| **Katy, Texas (HDD)** | g8 | `hdd-*` | ❌ | ✅ (same facility, different disk class) |
| **Cherryvale, Kansas** | g7 | `ssd-*`, `dev-*` | ✅ **dev only** (pkg 80–84) | ❌ **`64.188.7.0/24` has NO covering announcement** — absent from the global table (RIPEstat, 2026-09-10) |

## Reachability matrix (the 2026-09-10 live probe, VM 2490 @ 64.188.7.239)

| Vantage | TCP/22 to dev zone | Notes |
|---|---|---|
| EU lab (Norway) | ❌ timeout; ICMP 100% loss | stable since 2026-08-27 |
| check-host.net ×15 (BR/DE/ES/FI/HU/ID/IR/JP/MD/PL/PT/RU/SG/UK/VN) | ❌ all timeout or `Network is unreachable` | includes **their US node** — this is not "US vs EU" |
| **GitHub Actions (Azure US)** | ✅ **OPEN in 0.07s** | repeatedly: 2026-09-09 18:50 + 2026-09-10 07:19 |
| **Cross-zone from a Katy VM** | ❌ `Network is unreachable` | gateway (23.182.128.1) has no route to 64.188.7.0/24 — ICMP-unreachable back to the guest; re-verified 2026-09-10 after the Azure path healed (same as 2026-08-28) |

**Conclusion (narrower than "EU dark"):** the dev subnet is reachable only
through one narrow path (whatever transit Azure/GitHub rides — SHC-side
private peering or partial announcement invisible to RIS). The global DFZ
does not carry it, and SHC's own zones can't route to it. Practical
read: **dev zone is unusable except from GitHub runners** — do not build on
that path (one routing change away from dark).

**So: can we reach the dev zone through SHC's other sites? No.** A Katy
bastion does not unlock Cherryvale — tested live 2026-09-10. (If SHC ever
adds the internal route, the same one-liner from the runbook below
re-answers the question in 30 seconds.)

## Egress: dev-zone VMs have NO outgoing internet (2026-09-10, VM 2527)

SSH'd from the GitHub/US vantage INTO a fresh dev VM and ran the battery
inside (`egress-probe.yml`, sid 2527 @ 64.188.7.240):

| Probe (inside the VM) | Result |
|---|---|
| `ping 1.1.1.1` | ❌ 100% loss |
| DNS (`getent deb.debian.org`) | ❌ FAIL |
| HTTP (`curl https://ifconfig.me`) | ❌ timeout |
| HTTPS (`curl -I https://example.com`) | ❌ resolve failure |
| `traceroute -n 1.1.1.1` | hop 1 `64.188.7.1` → hop 2 **`66.92.204.1`** (the OLD subnet's gateway) → `* * *` dead |

**The fabric still routes dev-zone egress via the decommissioned
`66.92.204.0/24` range.** Inbound TCP/22 on the narrow Azure path is the
only working network path. Practical consequences: cloud-init network
fetches, apt, DNS-dependent anything — all dead inside the zone; a dev VM
is an island reachable only from specific shores. Re-test any time:
`gh workflow run egress-probe.yml` (~$0.01). Console lane (noVNC via
blesta) is independent of the VM's network and was healthy the same day
(mint + bootstrap 200 via curl; headless-browser bootstrap rejected —
fingerprint-level; untested from a human browser).

## Predicted reliability, per zone

| Zone | Provisioning | Reachability | Verdict for workloads |
|---|---|---|---|
| Katy nvme/hdd | ⚠️ **flake class** — ~50% of fresh orders dead >600s on 2026-09-09/10 (issue #47); historically ~60–90s | ✅ globally announced, verified from EU + 15 nodes | default choice; use `--verify-reachability`, retry once on provision-timeout, never widen timeouts |
| Cherryvale ssd | scheduler OK | same fabric gap as dev (unreachable from EU since 2026-09-01) | refuse-by-default (`shc order` guard) |
| Cherryvale dev | scheduler fixed (#28, 2026-08-25); VMs attach + answer **only** on the Azure path (#39) | see matrix above | nested-KVM workloads blocked from the EU lab; GitHub-runner-driven CI is the only live consumer — at your own risk |

## The vantage-check runbook (how to re-earn any cell)

Semantics first: probe a **live** VM (a cancelled VM's IP gives firewall-drop
timeouts that are indistinguishable from no-route). With a live target:
`connection refused` = route exists, no listener; `timeout` = route missing
or firewall; `Network is unreachable` = your gateway has no route (strongest
no-route signal).

1. **BGP visibility (zero cost, no VM):**
   `curl -sS "https://stat.ripe.net/data/prefix-overview/data.json?resource=64.188.7.0/24"`
   — empty `asns` = the DFZ doesn't carry it (control: Katy's /24 shows
   AS401933).
2. **15-country TCP matrix (zero cost, needs live VM):**
   `https://check-host.net/check-tcp?host=<IP>:22&max_nodes=16` → poll
   `check-result/<request_id>` (~20s). One open node = narrow path, not a
   recovered zone (earned: their US node was dark while Azure was open).
3. **GitHub/Azure vantage (needs live VM):**
   `gh workflow run "Dev Zone Watch" -f target_ip=<IP>` — TCP/22 + tracepath
   from the runner, orders nothing, comments nothing.
4. **EU lab side:** TCP/22 + ICMP + `tracepath -n <IP>` locally.
5. **Cross-zone (Katy→Cherryvale):** order the bastion with an
   **order-time** `--ssh-key` (apply-live is unreliable — API records the
   key, guest never gets it; verified 2026-09-10), then
   `ssh debian@<katy-ip> 'timeout 8 bash -c "exec 3<>/dev/tcp/<dev-ip>/22 && head -c 40 <&3"'`
   — banner text = real sshd answered.
6. **Verdict rule (lesson 30):** "recovered" requires green from **two+
   independent vantages** — never close on one route's PASS. The
   dev-zone-watch enforces this: PASS posts evidence, only a human closes.

## What guards each failure class

| Failure class | Guard |
|---|---|
| Ordering into an unreachable facility | `shc order` refusal on flagged sizes + `--dry-run` |
| Billing-active-but-unroutable VM | `shc order --verify-reachability` (cancels, refund) |
| Zone-wide regression | `dev-zone-watch.yml` weekly (US vantage) + this runbook |
| **Longitudinal zone health (all four lines)** | **monthly multi-zone smoke** (`scripts/live_smoke.py --zone all`, in `api-drift.yml`): stable lines hard-fail, watch lines log-only, stock-outs warn, Katy→Cherryvale bastion canary built in (unreachable = expected; open = internal route arrived — report on #39) |
| Katy provision-timeout flake | fail-loudly + retry-once discipline (#47); never widen timeouts |
| Leaked test VMs | reaper prefixes incl. `ansible-demo-`, `-reap<deadline>` tags, `shc reap --dry-run` at session end |
