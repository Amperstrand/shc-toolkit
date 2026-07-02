# compute.cashu.email — Lightning-Powered VPS

Pay-to-provision VPS service built as a Cloudflare Worker. Users pay a Lightning invoice, get root SSH access to a dedicated SHC VM in seconds.

## Architecture

```
User Browser → compute.cashu.email Worker → SHC API
                    ↓                          ↓
              KV (order state)         BTCPay Server
                    ↓                          ↓
              Balance polling            Lightning Network
                    ↓                          ↓
              VM ready detected         User pays invoice
```

### Flow
1. User visits compute.cashu.email, selects tier, clicks Order
2. Worker calls `POST /account/credit` (with idempotency_key + auto-confirmation)
3. SHC returns `checkout_url` + `bolt11` (or `payment_link` with LNURL) directly
4. Worker stores `credit_before` balance + invoice data in KV
5. User pays Lightning invoice (QR code or BTCPay checkout link)
6. Worker polls `GET /account/balance` every 3s (frontend-initiated)
7. When `balance > credit_before` → payment detected
8. Worker calls `POST /ordering/submit` → VM created
9. Worker calls `POST /vm/{id}/cancel` with `{}` → end-of-term cancel scheduled
10. Worker polls `GET /vm/{id}` until `provisioning_state: "ready"`
11. If SSH key provided: `POST /vm/{id}/ssh-keys/apply-live` → key injected
12. Worker returns `ssh debian@<IP>` to frontend

### Files
```
/Users/macbook/src/vps-on-demand/
  src/
    index.ts    — Worker router + order lifecycle state machine
    shc.ts      — SHC API client (TypeScript port)
  index.html    — Frontend (3-tier selector, QR, polling, SSH result)
  wrangler.jsonc — KV binding + custom domain route
  tests/
    full-flow.spec.ts — 28 Playwright tests (27 pass, 1 skip)
```

## Deployment

### Prerequisites
- Cloudflare account with Workers + KV
- `cashu.email` DNS zone on Cloudflare
- SHC API key (`shc_live_...`)
- Wrangler CLI authenticated

### Deploy
```bash
cd /Users/macbook/src/vps-on-demand
npx wrangler kv namespace create VPS_ORDERS  # already done: dea6b148906e4acc8d5a2650660e2796
npx wrangler deploy
echo "$SHC_API_KEY" | npx wrangler secret put SHC_API_KEY
```

### Test
```bash
# Health check
curl https://compute.cashu.email/api/health
# → {"status":"ok","time":...}

# Order (creates real Lightning invoice)
curl -X POST https://compute.cashu.email/api/order \
  -H "Content-Type: application/json" \
  -d '{"tier":"standard"}'
# → {"order_id":"...","bolt11":"lnbc...","checkout_url":"..."}

# Poll status
curl https://compute.cashu.email/api/status/<order_id>
# → {"status":"awaiting_payment"} → {"status":"provisioning"} → {"status":"ready","ssh":"ssh debian@<IP>"}
```

## Key API Findings

### SHC API quirks discovered during development

1. **"Authorized access only" prefix**: SHC API responses start with `Authorized access only. All activity is monitored and logged.\n` before the JSON. The Worker must strip this with `rawText.indexOf('{')` before parsing.

2. **addCredit requires idempotency_key**: `POST /account/credit` body must include `idempotency_key` (16-128 chars, `[A-Za-z0-9_-]`). Without it: `validation_failed`.

3. **addCredit returns checkout data directly**: The response includes `checkout_url`, `bolt11` (sometimes null), and `payment_link` (LNURL with `lightning:` prefix). No separate `triggerCheckout` call needed.

4. **Payment detection via balance polling**: `GET /account/balance` returns current credit. Compare before/after to detect payment. No invoice_id needed.

5. **apply_ssh_key_live field name**: `POST /vm/{id}/ssh-keys/apply-live` expects `{"ssh_key": "..."}` NOT `{"public_key": "..."}`. Response: `{"live_inject": "attempted", "key_fingerprint": "SHA256:..."}`.

6. **VM password NOT in API**: Password is only available on the portal web page at `/client/services/manage/{id}/` in `<input placeholder="Server password">`. No API endpoint returns it. Use `console.py` (Playwright scraper) to retrieve it.

7. **No boot_script/user_data**: `POST /ordering/submit` does not accept a custom cloud-init user-data field — the backend auto-generates a fixed cloud-config from order fields only (hostname/user/password/ssh_key). The `user_data` kwarg is accepted by the API gateway (`additionalProperties: true`) but silently dropped by the provisioning backend. Empirically verified on both Dev VPS and NVMe tiers (2026-07-02); see [`docs/cloud-init.md`](cloud-init.md) for the full picture. Note: cloud-init itself **does** run on NVMe/SSD/HDD (the order `ssh_key` gets installed automatically); on Dev VPS cloud-init is **disabled by a marker file**, so the `ssh_key` reaches the seed but is never consumed — use `apply_ssh_key_live` as the workaround.

8. **SSH keys inject for `debian` user**: `apply_ssh_key_live` injects the key for the `debian` user, NOT `root`. Use `sudo -i` for root access.

9. **End-of-term cancel**: `POST /vm/{id}/cancel` with body `{}` schedules end-of-term cancel. With `{"immediate": true}` for immediate cancel with prorata refund.

10. **Confirmation flow**: Money-spending API calls return `confirmation_required` (HTTP 409) with a `confirmation_id`. Resubmit with `X-User-Api-Confirm: <id>` header to execute.

### SHC package IDs (Dev VPS)

| Package | ID | Pricing ID | CPU | RAM | Disk | $/day |
|---------|----|-----------|-----|-----|------|-------|
| Standard | 81 | 245 | 2 vCPU | 8 GB | 16 GB | $0.49 |
| Professional | 82 | 249 | 4 vCPU | 16 GB | 32 GB | $0.96 |
| Business | 83 | 253 | 8 vCPU | 32 GB | 64 GB | $1.91 |

Markup: 10% → Standard $0.54, Professional $1.06, Business $2.10 per 24h.

## Known Issues

1. **QR code CDN unreliable**: The `qrcode@1.5.3` library from jsdelivr CDN sometimes fails to load. Fallback: show invoice string + BTCPay checkout link. TODO: use inline QR generation or more reliable CDN.

2. **SHC provisioning delays**: VMs sometimes take 5-60+ minutes to provision. The Worker polls indefinitely. Frontend shows elapsed timer.

3. **One pending topup at a time**: SHC only allows one pending credit topup. If an invoice expires unpaid, it blocks new orders until SHC clears it (~15-30 min).

4. **Balance polling can false-positive**: If multiple credit sources exist, balance increase might not be from the Lightning payment. For production: use invoice-specific tracking (BTCPay webhooks or idempotency replay).

5. **Provisioning log spam**: Fixed — was logging every 3s poll. Now logs once with elapsed timer.

## E2E Test Results (2026-06-24)

- VM 615: Ordered directly via Python client. Provisioned in 5 min. SSH key injected. SSH verified. Cancelled. ✅
- VM 616: Ordered by Worker (simulated payment). Provisioning stuck 18+ min. Cancelled. ✅ (chain proven)
- VM 619: Ordered by Worker after real Lightning payment ($0.54). Provisioned in ~2 hours (SHC infra delay). SSH key injected. SSH verified. Cancelled. ✅ (full E2E)

### Bugs fixed during testing
1. `addCredit` missing `idempotency_key` → validation_failed
2. `apply_ssh_key_live` field name `public_key` → should be `ssh_key`
3. BOLT11 empty → `payment_link` LNURL fallback
4. JSON parsing → SHC "Authorized access" prefix stripped
5. QR CDN race condition → retry mechanism added
6. Log spam → single entry + elapsed timer
7. SSH user `root` → should be `debian` (key injects for debian)
