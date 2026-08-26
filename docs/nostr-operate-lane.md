# Nostr Operate Lane — one VM, no shared key

A customer can hand an agent operation of **one specific VM** without giving
it an account-wide API key and without touching a website. The customer signs
a Nostr grant; the agent exchanges it for a short-TTL, vm-scoped,
cannot-spend Bearer. This is the agent-side counterpart of SHC's
`nostr-operate-lane` operator skill (see the
[operator-skills corpus](https://blesta.sovereignhybridcompute.com/agent-skills/llms-full.txt)).

Distinguish it from [agent sessions](agent-sessions.md): an agent session is
minted by the **account owner** for one of their own agents. The operate lane
is signed by the **customer** for an agent they trust with exactly one VM —
no account-level credential is ever shared, in either direction.

## What the lease is

| Property | Value |
|---|---|
| TTL | ~15 minutes (`expires_in: 900`); re-mint from the same grant |
| Scope | `operate` — read + VM ops on `/vm/<service_id>/...` for the ONE granted VM |
| Spend | **impossible** — every spend path 403s (an `operate` key cannot spend) |
| Destructive ops | still confirm-gated (reinstall, restore/delete backup, …) |
| Other services / non-VM routes | 403 by design |

## The customer's step (they sign, you never do)

The customer signs a Nostr **`kind:30078`** event with these tags in their own
signer (NIP-07 extension, NIP-46 bunker, …) and sends you the full signed
event:

| tag | value |
|---|---|
| `d` | `shc:agent:<YOUR_AGENT_PUBKEY>` |
| `scope` | `operate` |
| `area` | `vm:<service_id>` |
| `aud` | `shc:https://blesta.sovereignhybridcompute.com` |
| `nbf` | unix seconds (now) |
| `exp` | unix seconds (now + ≤ ~15 min) — required |

## The agent's step (this toolkit)

```python
from shc_toolkit import exchange_nostr_operate_grant, SHCClient

# grant = the customer's full signed kind:30078 event (a dict)
# nsec  = YOUR agent key — the one named in the grant's d tag
lease = exchange_nostr_operate_grant(grant, nsec=nsec)   # no SHC account needed

vm = SHCClient(api_key=lease["token"])                   # the 64-hex operate Bearer
vm.restart_vm(lease["service_id"])                       # routine op — no confirm
```

The function:

1. **Validates the grant locally** (`validate_operate_grant`) — kind, signature
   fields, and every tag above with sane `nbf`/`exp` timing. A malformed or
   expired grant fails immediately with an actionable message ("tag scope must
   be 'operate'", "grant is expired — ask for a re-sign") instead of an opaque
   server 403. `validate_operate_grant(grant)` is also exported if you want to
   check a grant before asking the customer to re-sign.
2. **Signs a NIP-98 `kind:27235` request event** with your nsec — `u` bound to
   `https://…/plugin/nostr_auth/main/operate_token`, `method=POST`, a fresh
   `nonce` (the server replay-checks; a reused request 401s).
3. **POSTs** it as `Authorization: Nostr <base64 event>` with body
   `{"grant": <event>}` and returns the lease (`token`, `scope`, `area`,
   `service_id`, `expires_in`).

`SHCClient.exchange_nostr_operate_grant(grant, nsec=…)` also exists as a
method (same behavior, uses the client's `base_url`) — but prefer the module
function: it needs no SHC account or API key, which is the whole point of the
lane. Requires `pip install shc-toolkit[register]` (nostr-sdk).

## Operating under the lease

- Routine ops (power, restart, mount ISO, add/edit firewall rule, set rDNS,
  create backup/snapshot, **add** SSH key) need **no** confirmation.
- Destructive ops (reinstall, restore/delete backup or snapshot, delete
  firewall rule/SSH key, cancel) hit the same confirmation gate as always:
  the first call 409s with a single-use `confirmation_id`; after the
  customer's explicit yes, re-send the identical request with header
  `X-User-Api-Confirm`. `SHCClient` handles this automatically.
- Any spend path 403s — that is correct; do not go looking for a broader key.
- Lease expired (401)? Re-run the exchange with the same grant if it is still
  unexpired; otherwise ask the customer to re-sign — it is cheap.

## Common rejections

| code | meaning | action |
|---|---|---|
| `401` | NIP-98 header missing/malformed, or replayed | re-sign a fresh `kind:27235` (new nonce, `created_at`=now) |
| `403` "Invalid grant" | forged / expired / wrong `d`/`scope`/`aud`/`area` | re-check locally with `validate_operate_grant`; ask for a corrected re-sign |
| `403` "Grant signer is not a linked customer" | signer's key isn't linked to an SHC account | customer links their Nostr key first |
| `403` on a `/vm/...` call | used the Bearer on another service or a spend path | only call the granted VM |
| `409` `confirmation_required` | destructive op without the gate | get the customer's yes, re-send with `X-User-Api-Confirm` |
