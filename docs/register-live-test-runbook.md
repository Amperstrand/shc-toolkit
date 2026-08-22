# Live registration test — runbook (funding day)

Goal: complete the zero-GUI onboarding proof — fresh account (client
333, context `default`) funded by a real Lightning payment, then
order → provision → cancel a VM entirely from that account.

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
   inbox for an SHC receipt → cancel (meter stopped)
3. Verify: `tail /tmp/opencode/prove-loop.log` — expect
   `FUNDED: $X.XX`, `PROOF: VM <id> provisioned, ip <ip>`,
   mail line, `cancelled`

## Tomorrow — recovery path (watcher died / machine rebooted)

The context survives in `~/.config/shc` — no re-registration needed:

```bash
cd ~/src/shc-toolkit
python3 -m shc_toolkit.cli topup --context default --amount 1.00
# pay the QR at http://127.0.0.1:8923/ (or the printed checkout URL)
# then prove the loop by hand:
python3 -m shc_toolkit.cli order --hostname proof-vm \
    --size nvme-1c-4gb --ssh-key ~/.ssh/id_ed25519.pub
python3 -m shc_toolkit.cli mail          # SHC receipt, if mailed
python3 -m shc_toolkit.cli cancel <service_id>
```

## Also ready (post-funding options)

- `shc register` on a brand-new account end-to-end (if we want a SECOND
  clean run from scratch tomorrow: fresh nsec, ~60 s to the QR)
- Eddy E2/E3 experiments: `terraform apply` in
  `lightning-playground/docker/eddy-lab/terraform` + driver — eddy-lab
  VM was destroyed after the last run (cost leak); redeploy is one
  command
- Free nomail sending: `scripts/testnut_faucet.py 100 | shc mail
  --send-to … --cashu-token "$(cat)"` (testnet ecash stamp —
  live-verified; NOTE: recipient inbox delivery is currently not
  landing, outbound shows status:sent — open question on nomail's
  ingest path)
