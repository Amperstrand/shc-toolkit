# Live registration test — runbook (funding day)

Goal: complete the zero-GUI onboarding proof — fresh account funded by a
single real Lightning payment, then a 24h experiment window: order →
provision → run eddy (plus E2/E3 re-runs) → tidy end-of-term.

**VM policy (owner decision 2026-08-23): single-run VM, leave RUNNING the
full 24h paid term — do NOT cancel mid-term.** Rationale: cancelling
after ~1h refunds ~$0.47 as credit; a re-order needs the full $0.49
again and topping up the gap risks the server-side credit_minimum —
stranding the refund. The paid term is the experiment window: every
re-run (E2 random-skew, E3 5-node churn) rides the same invoice. To
prevent a surprise day-2 renewal charge, schedule end-of-term
cancellation right after ordering: `shc cancel <id> --end-of-term`.

## State as of 2026-08-22 23:xx (pre-funding)

- Account registered, full-scope key minted, nostr linked (NIP-05 name
  assigned), context saved at `~/.config/shc/contexts/default.json`
- Completion watcher RUNNING (`/tmp/opencode/prove-loop.py`, pid file
  `/tmp/opencode/prove-loop.pid`): re-issues the topup invoice every
  25 min and serves a STABLE QR page at **http://127.0.0.1:8923/**
  (auto-refreshes; always shows the current payable invoice)
- Credit: 0.00 — awaiting payment
- Proof path dry-run PASSED on the main account (VM 2224: ordered,
  provisioned in 79 s, SSH OK, cancelled — ~1¢)

## Tomorrow — normal path (watcher alive)

1. Open http://127.0.0.1:8923/ — pay the QR (~$1.00) with any wallet
2. Watcher detects funding within ~20 s and runs the proof
   automatically: order nvme-1c-4gb → wait provisioning → check nomail
   inbox for an SHC receipt → NOTE: watcher cancels immediately — for
   the fresh-account 24h run below, drive it manually instead
3. Verify: `tail /tmp/opencode/prove-loop.log` — expect
   `FUNDED: $X.XX`, `PROOF: VM <id> provisioned, ip <ip>`, mail line

## Tomorrow — the fresh-account 24h E2E (the real test)

0. Stop the old watcher (frees port 8923 for the fresh run's QR page):
   `kill $(cat /tmp/opencode/prove-loop.pid)`
1. Register + fund in one pass:
   `shc register --context eddy-e2e --amount 1.00 --timeout 1800`
   → pay the ONE invoice at http://127.0.0.1:8923/ (~$1.00; covers the
   $0.49 nvme-2c-8gb day + slack; if credit_minimum rejects a later
   smaller topup, that slack is what keeps the window usable)
2. Order the experiment VM from credit (NO new invoice):
   `shc order --hostname eddy-e2e-vm --size nvme-2c-8gb \
      --ssh-key ~/.ssh/id_ed25519.pub --pay`
3. IMMEDIATELY prevent renewal (VM keeps its paid 24h):
   `shc cancel <service_id> --end-of-term`
4. Bootstrap + run eddy:
   `scp docker/eddy-lab/provision.sh debian@<ip>:/tmp/ && \
    ssh debian@<ip> sudo bash /tmp/provision.sh`
   `puppets/experiments/eddy.py --host debian@<ip>`  (~35–50 min)
5. Use the remaining window for E2 (`--skew-mode random`, N reps) and
   E3 (5-node) on the SAME VM — zero extra cost
6. Closeout (no cancel — end-of-term is already scheduled):
   `shc balance` (credit accounting), `shc mail` (receipt check)
   Optionally snapshot before the term lapses if the state is precious:
   `shc snapshot-create <id> -n eddy-e2e-final`

## Recovery path (watcher died / machine rebooted)

The context survives in `~/.config/shc` — no re-registration needed:

```bash
cd ~/src/shc-toolkit
python3 -m shc_toolkit.cli topup --context eddy-e2e --amount 1.00
# pay the QR at http://127.0.0.1:8923/ (or the printed checkout URL)
# then continue at step 2 above
```

## Also ready (post-funding options)

- `shc register` on a brand-new account end-to-end (if we want a SECOND
  clean run from scratch: fresh nsec, ~60 s to the QR)
- Free nomail sending: `scripts/testnut_faucet.py 100 | shc mail
  --send-to … --cashu-token "$(cat)"` (testnet ecash stamp —
  live-verified; NOTE: recipient inbox delivery is currently not
  landing, outbound shows status:sent — open question on nomail's
  ingest path)
