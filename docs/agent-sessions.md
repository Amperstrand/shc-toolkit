# SHC Agent Sessions

SHC v2.4.6 ships native agent session identity. An agent session is a
short-lived, scoped token that lets automated tools (CI runners, monitoring
bots, policy agents) call the SHC API on your behalf without giving them your
root credentials. Each session is bound to a Nostr key via proof-of-possession,
so the token alone is not enough to authenticate: every request must carry a
cryptographic proof that the caller holds the private key.

## Why agent sessions instead of API keys?

| Mechanism | Scope control | Proof-of-possession | Key rotation | Typical use |
|---|---|---|---|---|
| **API key** (`shc_live_`) | scope (read/operate/full) + optional area restriction | No — key alone authenticates | Manual revoke at `/account/api-keys` | Long-lived integrations, Terraform provider |
| **Agent session** (`shc_agent_`) | scope (read/operate) only | Yes — every request must carry a NIP-98 proof signed by the bound Nostr key | Revocation at `/agent-sessions/{id}` | Short-lived automation, CI jobs, ephemeral agents |

Agent sessions are designed for scenarios where the credential itself needs to
be tied to a specific identity (the Nostr keypair). An API key is a bearer
token: anyone who has it can use it. An agent session token is also a bearer
token, but every API call with it must prove the caller holds the corresponding
private key. If the token leaks, the attacker cannot make API calls without the
private key.

## The flow in four steps

1. **You create an agent session** with your root credentials (Basic+OTP or
   `shc_live_` key). You provide a Nostr public key. SHC returns a
   `shc_agent_` token.
2. **The agent claims its API key** (optional). You can mint a separate
   `shc_live_` key scoped to the agent and hand the agent only a single-use
   claim code. The agent exchanges the code for the key.
3. **The agent makes API calls** using the `shc_agent_` token in the
   `Authorization` header, plus a NIP-98 proof-of-possession event in the
   `X-User-Api-Agent-Proof` header.
4. **You revoke the session** when the agent's work is done.

## Creating an agent session

### Via the toolkit

```python
from shc_toolkit import SHCClient
import uuid

c = SHCClient()

session = c.create_agent_session(
    agentName="ci-deploy-bot",
    agentPurpose="Deploy VMs for integration testing and tear them down after.",
    publicKey="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    scope="operate",  # or "read"
)
```

The 201 response includes the token **exactly once**:

```json
{
  "data": {
    "sessionId": "ags_abc123def456ghi789jkl012mno345pqr678",
    "agentId": "agent_ci-deploy-bot_20260720",
    "token": "shc_agent_...returned-once...",
    "keyPrefix": "shc_agent_Ab1",
    "scope": "operate",
    "expiresAt": "2026-07-21T00:00:00Z"
  }
}
```

**Store the `token` immediately.** It is never returned again on subsequent GET
or list calls.

### Via curl

```bash
curl -X POST https://blesta.sovereignhybridcompute.com/user-api/v2/agent-sessions \
  -H "Authorization: Bearer shc_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{
    "agentName": "ci-deploy-bot",
    "agentPurpose": "Deploy VMs for integration testing and tear them down after.",
    "publicKey": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    "scope": "operate"
  }'
```

### Request fields

| Field | Type | Required | Description |
|---|---|---|---|
| `agentName` | string | Yes | Human-readable name for the agent (1-128 chars) |
| `agentPurpose` | string | Yes | What the agent does (1-512 chars) |
| `publicKey` | string | Yes | Nostr public key. Hex (`02...` or `03...`) or npub format accepted. |
| `scope` | enum | No (default: `operate`) | `read` (GET only) or `operate` (allowed non-money operations) |

### Idempotency

Like event subscriptions, `Idempotency-Key` is required (16-128 chars). Same key
+ same body returns 201. Same key + different body returns 422.

## Session scope

| Scope | Can do | Cannot do |
|---|---|---|
| `read` | GET any endpoint the account can access | Anything that writes, creates, or modifies |
| `operate` | Read + allowed write operations | Manage credentials, identity, billing money movement, contacts, managers, agent sessions, API keys, passwords, 2FA |

`operate` sessions are useful for CI runners that need to order/destroy VMs but
should never touch billing or account settings. `read` sessions are for
monitoring bots that only need to inspect state.

The hard boundaries (never reachable by any agent session, regardless of scope):
credentials (`/account/api-keys`, `/account/password`, `/account/2fa`),
identity (`PATCH /account`, `/account/contact`), billing money movement,
contacts, managers, and agent-session management endpoints.

## NIP-98 proof-of-possession

Every API request authenticated with a `shc_agent_` token must include a
cryptographic proof that the caller holds the private key bound to the session.
SHC uses [NIP-98](https://github.com/nostr-protocol/nips/blob/master/98.md)
(kind 27235) for this.

### The proof header

The proof goes in the `X-User-Api-Agent-Proof` header as a base64url-encoded
Nostr event:

```
X-User-Api-Agent-Proof: <base64url-encoded NIP-98 event>
```

### NIP-98 event structure (kind 27235)

```json
{
  "kind": 27235,
  "created_at": 1721510400,
  "tags": [
    ["u", "https://blesta.sovereignhybridcompute.com/user-api/v2/vm"],
    ["method", "GET"],
    ["challenge", ""]
  ],
  "content": "",
  "pubkey": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
```

| Tag | Value |
|---|---|
| `u` | The full URL of the API endpoint being called (e.g. `https://blesta.sovereignhybridcompute.com/user-api/v2/vm`) |
| `method` | The HTTP method (GET, POST, DELETE, etc.) |
| `challenge` | Empty string for agent sessions (challenges are for the account-level Nostr link flow, not agent sessions) |

The event must be:
- Signed by the private key corresponding to the session's `publicKey`
- Less than 600 seconds old (SHC rejects stale proofs)

### Constructing the proof in Python

```python
import json
import base64
import time
import hashlib
from pathlib import Path

# Using nostr-sdk or a manual secp256k1 signing library.
# This example shows the structure; adapt the signing to your library.

def build_nip98_proof(
    private_key_hex: str,
    method: str,
    url: str,
) -> str:
    """Build a base64url-encoded NIP-98 kind 27235 proof event.

    Args:
        private_key_hex: The Nostr private key (hex) that matches the session's publicKey.
        method: HTTP method (GET, POST, etc.)
        url: Full URL of the API endpoint.

    Returns:
        Base64url-encoded signed event for X-User-Api-Agent-Proof header.
    """
    pubkey = get_public_key(private_key_hex)  # derive or lookup

    event_template = {
        "kind": 27235,
        "created_at": int(time.time()),
        "tags": [
            ["u", url],
            ["method", method],
            ["challenge", ""],
        ],
        "content": "",
        "pubkey": pubkey,
    }

    event_id = compute_event_id(event_template)
    sig = sign_event_id(event_id, private_key_hex)

    event_template["id"] = event_id
    event_template["sig"] = sig

    serialized = json.dumps(event_template, separators=(",", ":"),
                             ensure_ascii=False)
    return base64.urlsafe_b64encode(serialized.encode()).rstrip(b"=").decode()
```

### Making an authenticated request

```python
import requests

AGENT_TOKEN = "shc_agent_..."
PRIVATE_KEY_HEX = "..."
BASE = "https://blesta.sovereignhybridcompute.com/user-api/v2"

url = f"{BASE}/vm"
proof = build_nip98_proof(PRIVATE_KEY_HEX, "GET", url)

resp = requests.get(
    url,
    headers={
        "Authorization": f"Bearer {AGENT_TOKEN}",
        "X-User-Api-Agent-Proof": proof,
    },
)
print(resp.json())
```

## Claiming an agent key (bootstrap flow)

The `POST /agent-keys/claim` endpoint is **public** (no authentication required).
Its purpose is to let an agent bootstrap its own credentials without ever
holding root-level keys.

The flow:
1. You (the account owner) mint a scoped API key via your account settings or
   the toolkit.
2. SHC gives you a single-use claim code (not the key itself).
3. You hand only the claim code to the agent.
4. The agent calls `claim_agent_key` with the code and receives the plaintext
   `shc_live_` key.

The code is burned on success. If it fails (unknown, expired, already claimed),
SHC returns a uniform 404 to prevent enumeration.

### Via the toolkit

```python
from shc_toolkit.client import SHCClient

# Static method — no SHCClient instance needed
result = SHCClient.claim_agent_key("u_XcVb12mN0pQrStUvWxYz")

# result: {"key": "shc_live_...", "key_prefix": "shc_live_Ab1", "scope": "operate", "expires_at": "2026-07-09T00:00:00+00:00"}
```

The returned key has its own scope and expiry. The claim itself is now spent.

### Via curl

```bash
curl -X POST https://blesta.sovereignhybridcompute.com/user-api/v2/agent-keys/claim \
  -H "Content-Type: application/json" \
  -d '{"code": "u_XcVb12mN0pQrStUvWxYz"}'
```

### Error behavior

| Status | Meaning |
|---|---|
| 200 | Claimed. The key is shown once. |
| 404 | Unknown, expired, or already-claimed code. Indistinguishable by design. |
| 422 | Malformed request (code too short, bad characters). |
| 429 | Rate limited (30 requests per IP per 10 min, 10 per code per 10 min). |

## Listing and inspecting sessions

### List active sessions

```python
from shc_toolkit import SHCClient

c = SHCClient()
sessions = c.list_agent_sessions()
for s in sessions:
    print(f"{s['sessionId']} — {s['agentName']} ({s['scope']})")
```

```bash
curl -H "Authorization: Bearer shc_live_YOUR_KEY" \
  "https://blesta.sovereignhybridcompute.com/user-api/v2/agent-sessions"
```

### Get a single session

```python
s = c.get_agent_session("ags_abc123def456ghi789jkl012mno345pqr678")
print(s["scope"], s["proofOfPossession"], s["lastUsedAt"])
```

The session object:

| Field | Type | Description |
|---|---|---|
| `sessionId` | string | Session identifier (`ags_...`) |
| `agentId` | string | Agent identity ID |
| `agentName` | string | Human-readable agent name |
| `agentPurpose` | string | What the agent does |
| `keyPrefix` | string | Token prefix for identification (never the full token) |
| `scope` | enum | `read` or `operate` |
| `publicKey` | string or null | The bound Nostr public key (may be null if redacted) |
| `proofOfPossession` | enum | `nostr` (current) or `none` (legacy) |
| `createdAt` | datetime | When the session was created |
| `expiresAt` | datetime | When the session expires |
| `lastUsedAt` | datetime or null | Last API call timestamp |
| `revokedAt` | datetime or null | Revocation timestamp (null if active) |

## Revoking a session

Revocation is **confirm-gated**: you must send `X-User-Api-Confirm` with a
valid challenge token. The toolkit's `_confirmed_request` handles this
automatically:

```python
# The toolkit's delete_agent_session maps to DELETE, which is the revoke endpoint
c.delete_agent_session("ags_abc123def456ghi789jkl012mno345pqr678")
```

For the REST API directly, the revocation requires a confirmation flow:

```bash
# Step 1: POST to get a challenge
curl -X POST \
  -H "Authorization: Bearer shc_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  "https://blesta.sovereignhybridcompute.com/user-api/v2/agent-sessions/ags_abc123def456ghi789jkl012mno345pqr678" \
  -d '{}'
# → 409 Conflict with challenge token

# Step 2: DELETE with the confirm header
curl -X DELETE \
  -H "Authorization: Bearer shc_live_YOUR_KEY" \
  -H "X-User-Api-Confirm: <challenge-token>" \
  "https://blesta.sovereignhybridcompute.com/user-api/v2/agent-sessions/ags_abc123def456ghi789jkl012mno345pqr678"
```

After revocation, the `shc_agent_` token is immediately invalid. Any in-flight
requests using that token will receive 401.

## Reading audit logs

Every API call made with an agent session is audited. You can retrieve the audit
trail:

```python
audit = c.get_agent_session_audit("ags_abc123def456ghi789jkl012mno345pqr678")
for record in audit.get("items", []):
    print(f"{record['time']} {record['method']} {record['path']} → {record['status']}")
```

```bash
curl -H "Authorization: Bearer shc_live_YOUR_KEY" \
  "https://blesta.sovereignhybridcompute.com/user-api/v2/agent-sessions/ags_abc123def456ghi789jkl012mno345pqr678/audit"
```

Audit record fields:

| Field | Type | Description |
|---|---|---|
| `auditId` | string | Unique audit record ID |
| `sessionId` | string | The agent session that made the call |
| `agentId` | string | Agent identity |
| `traceparent` | string or null | W3C trace context, if the caller supplied one |
| `time` | datetime | When the call happened |
| `action` | string | Action label |
| `method` | string | HTTP method |
| `path` | string | API path called |
| `status` | int | HTTP response status code |
| `subject` | string or null | Resource affected |
| `message` | string or null | Human-readable description |
| `data` | object | Additional structured data (includes `tamperEvidence` hashes when present) |

The `data` field may include `prevEventHash` and `eventHash` for tamper-evident
audit records, letting you verify the audit log has not been altered.

## Security model

### What agent sessions can never do

These endpoints have `x-required-area: __identity__` and are blocked to all
agent sessions regardless of scope:

- `/account/api-keys/*` — API key management
- `/account/password` — Password changes
- `/account/2fa/*` — Two-factor authentication
- `/account/contact` — Contact information
- `PATCH /account` — Account identity changes
- `/agent-sessions` (POST, DELETE) — Agent session creation/revocation (by the agent itself)

### What `read` scope can do

GET any endpoint that the account owner can access. That includes VM listings,
billing summaries, and all read operations.

### What `operate` scope can do

Everything `read` can do, plus write operations that do not involve:
- Money movement (payments, credits, refunds)
- Credential management
- Account identity
- Contacts and managers
- Other agent sessions

In practice, an `operate` agent can order VMs, cancel VMs, create snapshots,
manage firewall rules, and perform other infrastructure operations. It cannot
pay invoices, change passwords, or create new agent sessions.

### Proof-of-possession binding

The Nostr key binding adds a second factor to every API call. Even if an
attacker obtains the `shc_agent_` token (e.g. from a leaked environment
variable), they cannot make authenticated API calls without the private key.
The proof is per-request, bound to the exact method and URL, and expires after
600 seconds.

### Anti-enumeration on key claims

The `claim_agent_key` endpoint returns a uniform 404 for all miss cases
(unknown, expired, already-claimed). This prevents attackers from probing which
claim codes exist. The response time is also uniform (floor enforced) to prevent
timing-based enumeration.

## Common patterns and pitfalls

**1. Save the token on create.** The `shc_agent_` token appears only in the
201 response. There is no way to retrieve it later. If you lose it, revoke the
session and create a new one.

**2. Keep the Nostr private key secure.** The agent session is bound to a Nostr
keypair. If the private key is compromised, the attacker can forge
proof-of-possession headers. Revoke the session and rotate the keypair.

**3. Build the proof per-request.** The `u` tag must match the exact URL being
called, and the proof expires after 600 seconds. You cannot reuse proofs across
different endpoints or after the window closes.

**4. The `challenge` tag is empty for agent sessions.** NIP-98's `challenge`
tag is used in the account-level Nostr link flow. For agent session proofs,
it is an empty string.

**5. Claim codes are single-use and non-recoverable.** If you lose a claim code
before the agent uses it, the underlying key is stuck. Mint a new key with a
new claim code.

**6. Agent sessions are not MCP-exposed.** The `createAgentSession`,
`listAgentSessions`, `getAgentSession`, `revokeAgentSession`, and
`listAgentSessionAudit` operations have `x-shc-mcp-exposure: hidden`. They
are REST-only. Use `SHCClient` (REST transport) to manage them.

**7. The claim endpoint is also not MCP-exposed.** `claimAgentKey` is
intentionally excluded from the MCP surface because it is a public credential
bootstrap endpoint with no authentication.

**8. Revocation is confirm-gated.** Deleting (revoking) an agent session
requires the `X-User-Api-Confirm` challenge flow. The toolkit's
`delete_agent_session` method handles this, but if you call the REST API
directly you need to do the two-step confirm dance.

**9. Audit logs are your forensic trail.** If something goes wrong, pull the
audit logs for the affected session. Every API call (successful or not) is
recorded with timestamps, paths, and status codes.

## Related

- [SHC User API docs](https://blesta.sovereignhybridcompute.com/user-api/docs/)
- [OpenAPI spec](https://blesta.sovereignhybridcompute.com/user-api/openapi.json)
- [NIP-98: HTTP Auth](https://github.com/nostr-protocol/nips/blob/master/98.md)
- [Nostr protocol](https://nostr.com/)
- [Webhooks (Event Subscriptions)](webhooks.md) — push-based event delivery
