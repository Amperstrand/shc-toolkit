# SHC Webhooks (Event Subscriptions)

SHC v2.4.8 ships push-based event delivery. Instead of polling `GET /events`,
you register an HTTPS endpoint and SHC pushes CloudEvents 1.0 payloads to you
as they happen. Each delivery is HMAC-SHA256 signed so you can verify it came
from SHC.

## Push vs poll

| Approach | Endpoint | Trade-off |
|---|---|---|
| **Poll** | `GET /events` | Simple, works everywhere, but wastes requests during quiet periods and has inherent latency. |
| **Push** | `POST /event-subscriptions` | Near-real-time delivery, no polling overhead, but you need a publicly reachable HTTPS endpoint. |

Both consume the same underlying event feed. If you subscribe to webhooks,
you can still poll `GET /events` as a fallback or for debugging.

## Event type taxonomy

The events feed uses a dot-separated type taxonomy. The supported top-level
categories and their wildcards:

| Type pattern | What it matches |
|---|---|
| `service.lifecycle.*` | VM provisioning, suspension, termination, snapshot/backup events |
| `billing.order.*` | Order creation, cancellation, status changes |
| `billing.invoice.*` | Invoice generation, payment, overdue events |
| `module.vm.*` | VM module-level events (reinstall, template change) |
| `gateway.payment.*` | Payment gateway events |

Subscriptions use exact types or suffix wildcards (e.g. `service.lifecycle.*`
catches all lifecycle events). Up to 32 filters per subscription.

## Creating a subscription

### Via the toolkit (REST client)

Event subscription methods live on `SHCMCPClient` (MCP transport). The REST
`SHCClient` does not currently wrap these endpoints, so use the MCP transport
or call the REST API directly via `client._request()`:

```python
from shc_toolkit import create_client
import uuid

c = create_client(transport="mcp")

result = c.create_event_subscription(
    url="https://hooks.example.com/shc/webhooks",
    eventTypes=[
        "service.lifecycle.*",
        "billing.invoice.*",
    ],
    # Idempotency-Key is required by the API
    _idempotency_key=str(uuid.uuid4()),
)
```

The 201 response includes the signing secret **exactly once**:

```json
{
  "data": {
    "eventSubscriptionId": "evsub_0123456789abcdef0123456789abcdef",
    "url": "https://hooks.example.com/shc/webhooks",
    "eventTypes": ["service.lifecycle.*", "billing.invoice.*"],
    "signingAlgorithm": "HMAC-SHA256",
    "signatureHeader": "X-SHC-Webhook-Signature",
    "timestampHeader": "X-SHC-Webhook-Timestamp",
    "eventIdHeader": "X-SHC-Webhook-Event-Id",
    "deliveryIdHeader": "X-SHC-Webhook-Delivery-Id",
    "status": "active",
    "secretPreview": "whsec_abc123...",
    "secret": "whsec_0123456789abcdef0123456789abcdef0123456789ab",
    "createdAt": "2026-07-13T22:30:00Z",
    "updatedAt": "2026-07-13T22:30:00Z",
    "lastDeliveryAt": null,
    "deadLetterCount": 0
  }
}
```

**Store the `secret` immediately.** It is never returned again on subsequent
GET, list, or idempotent replay (200) responses. The `secretPreview` field is a
display-only prefix, not enough to verify signatures.

### Via curl

```bash
curl -X POST https://blesta.sovereignhybridcompute.com/user-api/v2/event-subscriptions \
  -H "Authorization: Bearer shc_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{
    "url": "https://hooks.example.com/shc/webhooks",
    "eventTypes": ["service.lifecycle.*", "billing.invoice.*"]
  }'
```

### Idempotency

The `Idempotency-Key` header (16-128 chars, alphanumeric/dash/underscore) is
required. The API uses it to deduplicate create requests:

| Scenario | Result |
|---|---|
| First request with a given key + body | 201 with `secret` |
| Replay same key + same body | 200, **no `secret`** |
| Replay same key + different body | 422 `idempotency_key_conflict` |

Generate a fresh UUID per subscription. Replaying the same key is only useful
for network retries during the same create call.

## HMAC-SHA256 signature verification

Every webhook delivery includes these headers:

| Header | Purpose |
|---|---|
| `X-SHC-Webhook-Signature` | HMAC-SHA256 digest, format `sha256=<hex>` |
| `X-SHC-Webhook-Timestamp` | Delivery timestamp (ISO 8601) |
| `X-SHC-Webhook-Event-Id` | The event's unique ID (deduplication key) |
| `X-SHC-Webhook-Delivery-Id` | Unique per delivery attempt (tracks retries) |

The signature covers the **exact raw request body bytes**. Compute it yourself
and compare with constant-time comparison to prevent timing attacks:

```python
import hashlib
import hmac
import time

def verify_webhook(
    raw_body: bytes,
    signature_header: str,
    timestamp_header: str,
    secret: str,
    tolerance_seconds: int = 300,
) -> bool:
    """Verify an SHC webhook delivery.

    Returns True only if the HMAC matches AND the timestamp is fresh.
    Reject stale deliveries to prevent replay attacks.
    """
    # Check timestamp freshness
    try:
        timestamp = time.mktime(
            time.strptime(timestamp_header, "%Y-%m-%dT%H:%M:%SZ")
        )
    except (ValueError, OverflowError):
        return False

    now = time.time()
    if abs(now - timestamp) > tolerance_seconds:
        return False

    # Parse the signature header: "sha256=<hex>"
    if not signature_header.startswith("sha256="):
        return False
    expected = signature_header[len("sha256="):]

    # Compute HMAC-SHA256 over the raw body
    computed = hmac.new(
        secret.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    # Constant-time comparison — always compare full length
    return hmac.compare_digest(computed, expected)
```

## Example receiver: Flask

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
WEBHOOK_SECRET = "whsec_0123456789abcdef0123456789abcdef0123456789ab"

# Track processed event IDs to handle at-least-once deduplication
seen_events: set[str] = set()


@app.route("/shc/webhooks", methods=["POST"])
def handle_webhook():
    signature = request.headers.get("X-SHC-Webhook-Signature", "")
    timestamp = request.headers.get("X-SHC-Webhook-Timestamp", "")
    event_id = request.headers.get("X-SHC-Webhook-Event-Id", "")
    delivery_id = request.headers.get("X-SHC-Webhook-Delivery-Id", "")

    raw_body = request.get_data()

    if not verify_webhook(raw_body, signature, timestamp, WEBHOOK_SECRET):
        return jsonify({"error": "invalid signature"}), 401

    # Deduplicate: at-least-once means you may see the same event twice
    if event_id in seen_events:
        return jsonify({"status": "duplicate"}), 200
    seen_events.add(event_id)

    event = request.get_json()
    event_type = event.get("type")
    print(f"Event {event_id}: {event_type}")

    # Process based on type...
    # {
    #   "specversion": "1.0",
    #   "id": "evt_...",
    #   "source": "/user-api/v2",
    #   "type": "service.lifecycle.provisioned",
    #   "time": "2026-07-13T22:31:00Z",
    #   "data": { ... },
    #   "shcdeliveryid": "...",
    #   "shcsubscriptionid": "evsub_...",
    #   "shcattempt": 1,
    #   "shcwebhookversion": "1"
    # }

    return jsonify({"status": "accepted"}), 200
```

## Example receiver: FastAPI

```python
from fastapi import FastAPI, Request, Response
import json

app = FastAPI()
WEBHOOK_SECRET = "whsec_0123456789abcdef0123456789abcdef0123456789ab"
seen_events: set[str] = set()


@app.post("/shc/webhooks")
async def handle_webhook(request: Request) -> Response:
    signature = request.headers.get("x-shc-webhook-signature", "")
    timestamp = request.headers.get("x-shc-webhook-timestamp", "")
    event_id = request.headers.get("x-shc-webhook-event-id", "")
    raw_body = await request.body()

    if not verify_webhook(raw_body, signature, timestamp, WEBHOOK_SECRET):
        return Response(content='{"error":"invalid signature"}',
                        status_code=401, media_type="application/json")

    if event_id in seen_events:
        return Response(content='{"status":"duplicate"}',
                        status_code=200, media_type="application/json")
    seen_events.add(event_id)

    event = json.loads(raw_body)
    print(f"Event {event_id}: {event['type']}")

    return Response(content='{"status":"accepted"}',
                    status_code=200, media_type="application/json")
```

## Listing and managing subscriptions

### List all subscriptions

```python
# MCP transport
subs = c.list_event_subscriptions()
for sub in subs:
    print(f"{sub['eventSubscriptionId']} → {sub['url']} ({sub['status']})")
```

```bash
curl -H "Authorization: Bearer shc_live_YOUR_KEY" \
  "https://blesta.sovereignhybridcompute.com/user-api/v2/event-subscriptions"
```

### Get a single subscription

```python
sub = c.get_event_subscription("evsub_0123456789abcdef0123456789abcdef")
print(sub["status"], sub["deadLetterCount"])
```

```bash
curl -H "Authorization: Bearer shc_live_YOUR_KEY" \
  "https://blesta.sovereignhybridcompute.com/user-api/v2/event-subscriptions/evsub_0123456789abcdef0123456789abcdef"
```

### Delete a subscription

```python
c.delete_event_subscription("evsub_0123456789abcdef0123456789abcdef")
```

```bash
curl -X DELETE -H "Authorization: Bearer shc_live_YOUR_KEY" \
  "https://blesta.sovereignhybridcompute.com/user-api/v2/event-subscriptions/evsub_0123456789abcdef0123456789abcdef"
```

Deletion stops all future delivery attempts and removes queued and
dead-lettered artifacts for that subscription.

## Delivery semantics

| Property | Value |
|---|---|
| **Delivery guarantee** | At-least-once. Your receiver may see the same event more than once. Deduplicate by `X-SHC-Webhook-Event-Id`. |
| **Retry policy** | Bounded exponential backoff, up to 3 attempts per event |
| **Dead lettering** | Enabled. After 3 failed attempts, the event is dead-lettered. The subscription's `deadLetterCount` tracks how many events have dead-lettered. |
| **Payload format** | [CloudEvents 1.0](https://cloudevents.io/) JSON envelope with SHC extension attributes |

Each delivery body includes these CloudEvents extensions:

| Extension attribute | Meaning |
|---|---|
| `shcdeliveryid` | Unique delivery attempt ID (matches `X-SHC-Webhook-Delivery-Id` header) |
| `shcsubscriptionid` | The subscription that triggered this delivery |
| `shcattempt` | Delivery attempt number (1, 2, or 3) |
| `shcwebhookversion` | Webhook protocol version |

## Security constraints

SHC enforces strict outbound webhook policies to prevent SSRF and data exfiltration:

**Registration and delivery-time validation** (both checks run):

| Check | Rule |
|---|---|
| Scheme | HTTPS only |
| Port | 443 (standard port only) |
| Host | Must resolve to a public IP address |
| Private networks | Rejected: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.0.0/16`, `::1`, `fc00::/7` |
| Local domains | `*.local` rejected |
| Metadata targets | Cloud provider metadata endpoints rejected |
| DNS rebinding | Host is re-resolved and validated before every delivery |
| Redirects | Not followed (3xx responses from your endpoint do not trigger a redirect) |

In practice, this means:

- Your webhook URL must be `https://` on port 443 with a publicly resolvable
  hostname.
- `http://`, custom ports, and IP addresses in private ranges will be rejected
  at registration time.
- If your DNS changes between registration and delivery to point at a private
  IP, the delivery is dropped (not retried against the new IP).

## Subscription statuses

| Status | Meaning |
|---|---|
| `active` | Deliveries are being attempted |
| `paused` | Deliveries suspended (not currently documented as user-triggerable) |
| `deadLettered` | Too many consecutive failures; deliveries stopped |

Check `deadLetterCount` on your subscription to monitor delivery health. A
non-zero count means events were lost after exhausting retries.

## Polling the events feed (without webhooks)

If you don't want to expose an endpoint, you can poll `GET /events` directly:

```python
from shc_toolkit import SHCClient

c = SHCClient()
events = c.list_events(limit=50)
for event in events:
    print(f"{event.get('type')}: {event.get('id')}")
```

```bash
curl -H "Authorization: Bearer shc_live_YOUR_KEY" \
  "https://blesta.sovereignhybridcompute.com/user-api/v2/events?limit=50"
```

The events feed supports cursor-based pagination (`cursor` query param) and
optional VM filtering (`virtualMachineId` query param).

## Common patterns and pitfalls

**1. Save the secret on create.** The `secret` field appears only in the 201
response. If you lose it, delete the subscription and create a new one. There
is no "rotate secret" endpoint.

**2. Use constant-time comparison.** Never compare HMAC digests with `==`. Use
`hmac.compare_digest()` or an equivalent constant-time function. The example
code above shows the correct approach.

**3. Reject stale timestamps.** Check `X-SHC-Webhook-Timestamp` and reject
deliveries older than 5 minutes to prevent replay attacks. The example code
includes this check.

**4. Deduplicate events.** At-least-once delivery means duplicates happen. Track
`X-SHC-Webhook-Event-Id` in a set (or database) and skip events you have
already processed.

**5. Return 200 quickly.** SHC treats non-2xx responses as delivery failures that
count toward the retry limit. If your processing is slow, return 200 immediately
and process asynchronously.

**6. Use the Idempotency-Key.** The create endpoint requires it. Generate a fresh
UUID per subscription attempt. Don't reuse keys across different subscription
configurations or you will get 422.

**7. HTTPS-only, public host, port 443.** The SSRF protection is strict. Don't
try to register `http://` URLs, non-standard ports, or private IPs. The API
rejects them at registration and re-validates the DNS at delivery time.

**8. Monitor dead letter count.** A rising `deadLetterCount` means your receiver
is failing. Check your endpoint logs and fix the receiver before events are
permanently lost.

## Related

- [SHC User API docs](https://blesta.sovereignhybridcompute.com/user-api/docs/)
- [OpenAPI spec](https://blesta.sovereignhybridcompute.com/user-api/openapi.json)
- [CloudEvents 1.0 specification](https://cloudevents.io/)
- [OWASP Webhook Security Guidelines](https://owasp.org/www-community/attacks/Webhook)
- [Agent Sessions](agent-sessions.md) — scoped, short-lived identity for automated agents
