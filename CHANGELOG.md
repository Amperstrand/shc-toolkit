# Changelog

All notable changes to shc-toolkit are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **`shc-dns-watch.yml` — SHC DNS outage monitor (temporary, issue #40).** `sovereignhybridcompute.com` went dark on 2026-08-31 (SERVFAIL / EDE-22 "no reachable authority" from Google and Cloudflare DoH, cert-verified genuine — not a local MITM). The watch probes from GitHub's network (a vantage local middleboxes cannot touch) every 6h + on dispatch: DoH ×2, HTTP 200 on the OpenAPI spec, MCP host. While dark it logs one line and exits 0 (no red-X noise); on recovery it comments evidence on and auto-closes #40. Remove/disable after recovery.

### Changed
- **GH-side reaper eased from hourly to daily.** `reap-orphan-vms.yml` now schedules at 05:23 UTC instead of hourly: GitHub's cron skipped most hourly runs anyway (measured 4–10 executions/day), and primary cleanup now rests on the on-VM self-destruct timers plus the lab machine's local `*/30` cron — the GH workflow is a backstop, not the fast path. Reduces scheduled-workload noise against the backdrop of the org Actions outage investigation.

### Added
- **`docs/iac-lifecycle.md` — industry-aligned lifecycle vocabulary and reasoning.** Maps SHC terms onto the IaC conventions users know from AWS/GCP — *cancel* == terminate/delete, *stop* == pause (with the load-bearing divergence: a stopped SHC VM keeps billing its full daily price, unlike AWS/GCP where compute charges pause), confirm-gate == deletion protection, hourly reaper == provider test sweepers, self-destruct timer (no cloud equivalent) — with one-paragraph reasoning per design decision. README's Pulumi-bridge and proration sections now use the same terminology and link it. Canonical provider-side table: `terraform-provider-shc/docs/lifecycle-alignment.md`.

### Added
- **reap now catches stopped-but-billable zombies** (any hostname, not just test patterns). SHC bills by service existence, so a VM whose runtime is stopped keeps accruing charges until cancelled — the clboss-soak incident (2026-08-26) sat stopped-but-billable ~13h after a correct drain contract because its hostname matched no reap prefix and `shutdown` was mistaken for cleanup. Past `--max-age-hours`, ANY VM whose runtime reports stopped/shutdown is now a reap orphan (`reason: "stopped-but-billable"`); `exclude_hostnames` and `keep_patterns` always win, and a VM whose runtime cannot be probed is skipped (fail-open — never cancel what you cannot inspect). Test-pattern VMs now carry `reason: "test-pattern"` in reap output. Defaults gained the `clboss-` and `lab-` prefixes so forgotten RUNNING lab VMs are also reaped. Companion to the stop/shutdown billing warning and the on-VM self-destruct timer.
- **On-VM self-destruct — `shc_toolkit/selfdestruct.py` + `--self-destruct-minutes`.** A controller-dead failsafe: a systemd `OnBootSec` timer on the VM cancels it N minutes after boot (unlike `at` jobs, survives reboot), driven by a stdlib-python script that runs the full 409 → `X-User-Api-Confirm` cancel dance with a stable Idempotency-Key. Live-earned constraints (probed): only **full-scope** credentials can cancel (operate-scope keys and nostr operate leases 403 it — cancel is money), and Bearer keys **cannot mint keys** (Basic only). Key sources, in order: `SHC_SUICIDE_KEY` (pre-minted short-expiry secret — CI-friendly), per-run mint over Basic (`SHC_ACCOUNT_EMAIL`/`SHC_ACCOUNT_PASSWORD`, 1-day self-revoking minimum). The installer ships as one base64 SSH command so the key never hits plaintext process listings. Wired into `shc github-runner provision --self-destruct-minutes N` (fail-loud when requested but not armable) and physical-router-test-automation (which previously planted the FULL ACCOUNT KEY on every test VM — now bounded, legacy path kept as a warned fallback). **Live-fire proven**: VM ordered → 4-min timer armed → self-cancelled at T+216s, $0.01 total. Never arm on boxes running untrusted code (tollgate).

### Added
- **VM-order attribution via SSH-key comment.** `order_vm()` (and `shc order --tag`) embeds `#shc-order=<tag>` in the public key comment — tag resolution: explicit `--tag`/`tag=` → `$SHC_ORDER_TAG` env → `user@hostname`. The comment is free-form (sshd ignores it) and round-trips through `get_vm_detail().ssh_key`, so "who ordered this VM" stays answerable months later (the `devprobe-`/`lightning-playground` incidents needed manual key-fingerprint forensics). Opencode agents should `export SHC_ORDER_TAG=opencode:<session>` before ordering.

### Fixed
- **`order_vm(ssh_key=<raw string>)` silently dropped the key** — only existing file paths were honored, so string keys ordered keyless VMs without warning (live-confirmed: two test VMs provisioned with no authorized key at all, which also retroactively explains failed `ssh-key-live` injections on keyless guests). Raw key strings are now sent and tagged like file-based keys.
- **`stop_vm`/`shutdown_vm` now print a billing warning to stderr** — "VM <id> still bills while stopped (SHC charges by existence) — cancel when done". Meets agents at the moment of the classic mistake (the `clboss-soak` halt: drain contract executed, node shut down, VM left billing for 13h). Tests in `tests/test_billing_semantics.py`.

### Added
- **Customer side of the operate lane: `shc grant-operate` + `sign_operate_grant()` + `SHCClient.from_operate_grant()`.** The lane was agent-only; issuing a grant required hand-crafting a kind:30078 event in an external signer. `shc grant-operate --context <name> --service-id N --agent-npub npub… [--ttl 900]` signs the grant with the context's linked nsec and prints the signed event JSON to hand to any agent (npub or hex accepted, TTL-capped by `exp`); `sign_operate_grant()` is the programmatic form. `SHCClient.from_operate_grant(grant, nsec=…)` is the agent-side one-liner: exchange + return the operating client. Docs gain a credential-granularity matrix: per-VM scoping exists ONLY via the nostr lane (API-key `areas` are functional Blesta areas, not per-resource); per-action scoping (e.g. destroy-only) exists nowhere — an operate lease is all-ops-except-spend on one VM, with the confirm gate as the destruction control point.

### Changed
- **Removed the stale "Dev zone broken" order warning** (`_BROKEN_SIZE_PREFIXES` / `_warn_broken_zone` in `cli.py`) — issue #28 was resolved and verified 2026-08-25 (2.4.24.2); the warning contradicted the recovered reality. No behavior remains blocking `dev-*` sizes.
- **Python client now sends a versioned User-Agent.** `SHCClient` (and the standalone operate-grant exchange) send `shc-toolkit/<installed-version>` (from `importlib.metadata`, `dev` fallback) instead of httpx's bare `python-httpx/x` — parity with the Go provider's build-accurate UA fix, and lets SHC support identify toolkit traffic.

### Fixed
- **Plugin-route error bodies crashed the error mapper** (found by live negative testing). The `operate_token` plugin returns a flat `{"error": "<string>"}` (e.g. `{"error": "Grant is not bound to this agent key"}`), not the nested `{"error": {code, message}}` shape of `/user-api/v2` — `_error_from_body` raised `AttributeError` instead of the API error. It now handles both shapes and maps flat 401/403 strings to `SHCAuthError`.

### Added
- **+22 unit tests over the new corpus surface** (360 total now): User-Agent on both request paths, NIP-98 nonce/id uniqueness per request, method delegation honoring client `base_url`, default-URL targeting, grant-validation edges (non-dict, missing `aud`), invoice-poll error-path resilience, `payment_uri` edge cases (empty `payment_link` falls back to stitch, non-dict → `None`), and `register._topup` rail preference (server `payment_link` used with **zero** checkout-HTML scraping; scrape only when no rails).
- **`tests/test_nostr_operate_lane.py`** — live integration test (gated on `SHC_OPERATE_LIVE` context env, `allow_network`): customer-signed grant → lease → vm-scoped read → 403 on other service and spend. Verified live (eddy-e2e account, VM 2242) alongside negative cases: expired grant (local reject), wrong-agent grant (server: "Grant is not bound to this agent key"), forged signature (server: "Invalid grant signature"). A real `CreditTopupResponse` from a throwaway registered account also confirmed `payment_uri()` prefers the server `payment_link`.
- **Nostr operate-lane: standalone `exchange_nostr_operate_grant()` + local grant validation.** The exchange is now a module-level function (exported from `shc_toolkit`) so an agent needs **no SHC account or API key** — its nsec plus the customer's signed `kind:30078` grant are the whole credential (the method form required constructing an `SHCClient`, i.e. faking a key the lane is designed not to need). The `SHCClient` method remains and delegates. New `validate_operate_grant()` checks the corpus contract locally (kind, signature fields, `d`/`scope`/`area`/`aud`/`nbf`/`exp` with sane timing) and returns actionable problem strings, so a malformed or expired grant fails before any HTTP with "tag scope must be 'operate'" instead of an opaque server 403. Guide: `docs/nostr-operate-lane.md`.

### Fixed
- **Reaped prefix gap: `devprobe-` orphans were never cleaned up.** `scripts/dev-zone-probe.py` cancels on success, timeout, SIGINT and SIGTERM — but a SIGKILLed runner (hard tool/session timeout) leaves the probe VM alive with no key and no owner (incident 2026-08-26: `devprobe-6f9cea97` idled 7h at $0.24/day before manual cancel). Added `"devprobe-"` to `reap_orphans()` default `hostname_prefixes` so the hourly reaper collects them after the 2h age gate; test extended to pin the prefix.

## [2.4.24.3] — 2026-08-26

### Added
- **Nostr operate-lane (agent side) — `SHCClient.exchange_nostr_operate_grant()`.** Implements the `nostr-operate-lane` skill from SHC's operator-skills corpus (`https://blesta.sovereignhybridcompute.com/agent-skills/llms-full.txt`, the audit source for this release): exchanges a customer-signed `kind:30078` grant for a short-TTL (~900s), vm-scoped, cannot-spend operate Bearer via `POST /plugin/nostr_auth/main/operate_token`. Signs a NIP-98 `kind:27235` auth event with the agent nsec (`u`/`method`/fresh-`nonce` tags — server replay-checks), sends it as `Authorization: Nostr <base64>`, body `{"grant": <event>}`. Response carries `token`/`scope`/`area`/`service_id`/`expires_in`; build a follow-on client with `SHCClient(api_key=token)`. The Bearer 403s on any other service and any spend path by design; destructive ops still pass the confirmation gate.
- **BIP21 payment-URI stitching — `jit_pay.bip21_stitch()` / `jit_pay.payment_uri()`.** Implements the `shc-pay` skill table for `CreditTopupResponse`-shaped dicts: both rails → `bitcoin:<addr>?lightning=<bolt11>`, on-chain only → `bitcoin:<addr>`, Lightning only → `lightning:<bolt11>`, none → `None` (checkout_url fallback). `payment_uri()` prefers the server-provided `payment_link`, then falls back to the local stitch. `shc register`/`shc topup` now use the server-supplied `payment_link`/`bolt11`/`onchain_address` directly and only scrape the checkout page HTML when the response carries no rail; `PaymentPage.update()` renders any wallet-openable URI (bare BOLT11 still auto-prefixed).

### Fixed
- **`jit_pay.poll_shc_invoice()` polled a literal `/payment/{invoice_id}` path** — the f-prefix was stripped by an old scripted edit, so every `shc order --pay` (zero-balance jit payment) polled a nonexistent URL, swallowed the error, and reported a payment timeout even after the wallet paid. Now requests `f"/payment/{invoice_id}"` and unwraps the `data` envelope (also accepts `confirmed`/`complete`). ~15 display prints in `jit_pay.py` that lost their f-prefixes (literal `{data}`/`{mins}`/`{invoice_id}` output) restored. Found by the llms-full.txt corpus audit (lesson 19 pattern).

## [2.4.24.2] — 2026-08-26

### Changed
- **Dev zone (Cherryvale, KS) RECOVERED — all "still broken" claims corrected.** Live probe 2026-08-25: pkg 80 provisions in 85s (debian12) and 102s (**debian13 — closing the loop on lesson #13**: the old "deadlock" was purely the zone scheduler, now proven in both directions). Nested-KVM workloads (Dev plans only) available again. README/AGENTS.md updated in both repos. `dev-zone-probe.py` default template corrected debian12 → debian13 (missed in the earlier sweep — it lives in `scripts/`).

### Added
- **`shc console-session` + `SHCClient.create_console_session()`** — API-native VM console access (`POST /vm/{id}/console-session`, auto-confirm + `--ttl`).

### Changed

### Changed
- **CI trigger policy overhauled — nothing runs on push/PR anymore.** All test/lint/security workflows (`shc-tests`, `typecheck`, `coverage`, `security`, `ansible`, `cross-repo-parity`) are now `workflow_dispatch` (on demand, e.g. `gh workflow run <name>`) + tag push (`v*`, pre-release verification) + monthly schedule. `shc-tests` dropped its 6-hour schedule (monthly on the 1st). The API changes rarely; per-commit CI was noise. Hourly reaper unchanged.
- **Reaper job trimmed**: 3-minute hard timeout, pip cache, concurrency guard (cancels redundant runs), and the reap+list steps merged into one interpreter pass.

### Changed
- **All scheduled CI reduced from weekly to monthly.** The SHC API changes rarely; drift/validation/parity/live-smoke jobs now run staggered across the first week of each month: api-drift (1st, incl. catalog-model validation + live order smoke), cross-repo-parity (2nd), ansible-e2e (7th). Hourly reaper and 6h shc-tests unchanged. **ansible-e2e had failed silently every week for 4+ weeks** (it orders a Dev VPS — the broken zone); it now auto-creates a deduplicated issue whose success doubles as the Dev-zone-recovery signal for issue #28.

### Added
- **`scripts/live_smoke.py`** — Versioned live smoke: order → active+IP readiness → ssh_key persistence check → immediate cancel with refund verification. Live-verified (73s, $0.25 refund). Wired into `api-drift.yml` as a monthly `live-order-smoke` job with ephemeral SSH keygen, orphan reaping, and deduplicated auto-issue on failure. Catches regressions the unit suite can't (storefront triple, key persistence, zone health) — it's what exposed the Go balance-parse bug.

### Fixed
- **Cross-repo parity CI regressed (40 false size-map issues).** `_parse_python_sizes` imported `shc_toolkit.sizes` in-package, which triggers `__init__.py` → `import httpx` — unavailable in the bare-Python CI job. Now loads `catalog_model.py` standalone (stdlib-only, dependency-free) via importlib, so the audit works in any environment.
- **Safety scanner flagged setuptools 79.0.1 CVE (SFTY-20260721-58460).** The `pip install --upgrade setuptools>=83` pre-scan fix existed only in the pip-audit job; now applied to the safety job too.

### Changed
- **`submit_order` resolves the storefront triple statically — no more preview round-trip.** Previously called `preview_order` (live API) to resolve `order_form_id`/`package_group_id`. Now resolves all three storefront IDs (`order_form_id`, `module_group_id`, `package_group_id`) from `catalog_model._LINES`. One fewer API call per order. **Live-earned contract (from terraform-provider-shc SSH debugging, 2026-08-21):** SHC validates the triple together — the order-time `ssh_key` only survives the FULL triple; a lone form ID either 400s (form 11) or silently drops the key (forms 1/7). Verified live: order → provision 62s → ssh_key stored → cancel, refund $0.25.

### Fixed
- **Storefront triples added to `catalog_model._LINES`** (`module_group`, `package_group` keys per line) — single source of truth; `generate_sizes.py` emits all three Go maps (`lineOrderFormIDs`, `lineModuleGroupIDs`, `linePackageGroupIDs`) from the model.
- **Lint/format drift in ralph-loop-added modules** (`register.py`, `profiles.py`, `nomail.py`, `qr_page.py`, `cli.py`) — 13 ruff findings + formatting normalized; the files bypassed the pre-commit hook when committed.
- **`.mypy_cache` untracked** (was accidentally committed by a parallel agent) and added to `.gitignore`.

### Fixed
- **`_diagnose()` HEALTHY check could never fire.** Used `provisioning_state == "ready"` — which SHC VMs never report (lesson #1) — so healthy VMs fell through to `UNKNOWN`. Now: `service_status == "active"` + IP + SSH-reachable = HEALTHY, plus a new `ACTIVE_NO_SSH` diagnosis. Found by cross-repo behavioral parity audit (Prompt 1).
- **`compute.py` gcloud-compat order path sent a legacy `options` block with wrong option IDs** (126/108/167 are NVMe/gui options, not Dev's 174/198; the field was silently ignored by the API anyway). Now sends `config_options` resolved from the catalog model defaults + template, and `ssh_key` as a top-level field. Also fixed a broken f-string in the error path (`print("...{e}")` without `f`). Found by DRY audit (Prompt 3).
- **Removed dead constants** `DEV_VPS_ORDER_FORM`, `DEV_VPS_DEBIAN_OPTION`, `DEV_VPS_SSH_KEY_OPTION`, `DEV_VPS_IPV4_OPTION`.

### Changed
- **Order-form IDs moved into `catalog_model._LINES`** (`order_form` key) with an `order_form_id()` lookup — single source of truth. `generate_sizes.py` now emits Go's `lineOrderFormIDs` map from the model instead of a hand-maintained copy. Found by DRY audit (Prompt 3).
- **`generate_sizes.py` now also emits Go's `knownTemplates`** (34 templates from the model) and `dailyPriceForPackage`/`orderFormIDForPackage` helpers into sizes.go — the entire file is generated; no hand-edited sections remain.

### Added
- **Named profiles (aws/gcloud-style multi-account)** — `shc_toolkit/profiles.py` + `shc profile list|use|show`. One store at `~/.config/shc/profiles/<name>.json` (0600) unifying register contexts and the legacy contexts.json (lazily, non-destructively migrated). Identity = npub (our Nostr key IS the account identity); resolution precedence: `--api-key` > `SHC_PROFILE` > `SHC_API_KEY` > active pointer (`shc profile use`, gcloud-configurations-style persistence). `--context` remains as an alias. 6 offline tests incl. precedence matrix and 0600 enforcement.
- **AGENTS.md: Zero-GUI onboarding section + live-earned API contract table** — the whole register/topup/nostr-link/SSH-key knowledge set from the 2026-08-22/23 E2E (amount-as-string, single pending topup, async order invoices, end-of-term-cancel-voids-invoice, NIP-98 shape, apply-live newline stripping).
- **README: `shc register` framed as THE getting-started path** — first top-up QR opens in the browser by default (stable URL, auto-refresh across reissues); `--no-browser` for terminal QR.
- **Zero-GUI account onboarding: `shc register` + `shc mail`.** Register a fresh SHC account from the CLI with nothing but a Lightning payment. One locally-generated Nostr keypair is the whole identity: the account email is `npub…@nomail.name` (free cashu.email mailbox readable with the same key via `shc mail`), and the key links to the account for Nostr auth. Unattended by default (generates password/names per the API's hard minimums); `--interactive` prompts. Any `shc` command with no key on a TTY offers the wizard (`SHC_NO_REGISTER`/`--no-register` opt-out; non-TTY CI behavior unchanged). New modules: `register.py` (wizard + 0600 context store), `nomail.py` (nomail.name client — NIP-98 auth, inbox, wait-for-message, Cashu/LN sender), `qr_page.py` (stable-port updatable PaymentPage); `SHCClient` gains `register()` (anonymous), per-request `basic_auth`, `create_api_key_basic()`, `nostr_link_challenge()`/`nostr_link()` (kind-27235 + `u`/`method`/`challenge` tags), `topup_credit()`. New `[register]` extra (nostr-sdk + qrcode). Offline tests `tests/test_register.py` (10) use an echo-server with sequenced responses. Live-verified 2026-08-22 (client 331/333): register → key mint → nostr link (`status: linked` + NIP-05 name) → topup checkout → QR page → poll.
- **`docs/cross-repo-audit-prompts.md`** — Four reusable AI-agent prompts for semantic cross-repo audits: behavioral parity (defaults, readiness, retry, confirmation flow), lessons-ported (AGENTS.md cross-check), DRY boundaries (classify duplication as derivable/intentional/accidental), and live drift smoke test. Mechanical parity stays in `audit_cross_repo.py`; these prompts cover what regex can't.

- **`scripts/testnut_faucet.py`** — Mint free testnet ecash from testnut.cashu.space (FakeWallet auto-settles NUT-04 quotes; NUT-05 blind mint via electrum_ecc). cashu.email accepts any mint for its 100-sat stamp → **free real email sending**, live-verified 2026-08-22 (`ok: true`, `/api/sent` status=sent; the wallet verifies the blind signatures — a bad token 402s). cdk-mintd gotchas encoded: quote `state: "PAID"` uppercase, BlindedMessage requires keyset `id`.

- **`shc topup`** — Fund an EXISTING context's account (register only creates new ones). Recovery path for funded-account tests; reuses _topup (reissue loop, stable QR page). Runbook for the live funded test: `docs/register-live-test-runbook.md`.
### Added
- **`shc cancel --end-of-term`** — cancel at term end instead of immediately (VM keeps its paid remaining term; no renewal). Required by the 24h single-run experiment window: mid-term cancels refund partial credit that a re-order can't use and a small top-up may not clear credit_minimum.

### Fixed
- **`_topup` survives invoice expiry; QR never blocks the poll.** Live-earned 2026-08-22: BTCPay invoices expire (~15-30 min) and SHC allows ONE pending top-up per account — the original flow sat on a dead invoice until overall timeout while the synchronous QR page blocked polling. Now: non-blocking page, reissue on `expired`, single-pending 409s waited out (60 s) rather than hammered. `topup_credit` documents the single-pending contract.
- **Stable payment-page URL across reissues.** Ephemeral per-window ports made every printed payment URL stale within 25 minutes (observed: 4 different ports in one afternoon). `PaymentPage` serves a fixed port (`SHC_PAY_PAGE_PORT`, default 8923), updates content in place, and self-refreshes open tabs every 30 s.
- **`jit_pay.render_qr` survives a missing `qrencode` CLI** (FileNotFoundError was uncaught and crashed `--no-browser` runs).

### Fixed
- **`audit_cross_repo.py` resolve_addons check searched only `client.go`.** The Go client was split into domain files in v0.4.0 — `ResolveAddons` lives in `vm_client.go`. The audit now scans all non-test `provider/*.go` files. Cross-repo audit is now all-pass (5/5).

### Changed
- **Catalog is now served from a static model — zero network calls.** The `/ordering/catalog` endpoint returns 10.3 MB per call. Previously cached to disk with a 24h TTL; now replaced entirely by `shc_toolkit/catalog_model.py`, a deterministic model derived from empirical analysis of the live catalog (prices, option IDs, pricing IDs, and value lists all follow arithmetic progressions — 160/160 checks pass with 0 mismatches). `get_catalog()` returns model data instantly; `get_catalog_live()` added for validation. Weekly CI validation against the live API auto-creates an issue on drift.
- **Credit balance no longer cached.** Changes on every order/refund — caching it was incorrect.
- **API drift CI changed from daily to weekly.** The `api-drift.yml` workflow now runs weekly (Monday 08:00 UTC) and includes a catalog model validation job alongside the existing OpenAPI + llms.txt drift checks.
- **All cache infrastructure removed from SHCClient.** The `_disk_cache_*`, `_cache_get`, `_cache_set`, `_key_ttl`, `_KEY_TTL`, `_CACHE_TTL` machinery (~100 lines) is gone. The catalog model replaces caching entirely; credit was never meaningfully cached. `invalidate_cache()` kept as a no-op for backward compat.
- **`sizes.py` now derives from `catalog_model.py`.** Eliminated 200 lines of hardcoded data duplication. `SIZE_MAP` and `_PRICING_LOOKUP` are computed at import time from the model.
- **`benchmark.py` no longer fetches the 10.3 MB catalog.** Pricing comes from the static model. Removed `_extract_shc_daily_price`, `SHC_CATALOG_URL`, `SHC_DAILY_PRICE`.
- **Pre-commit hooks: flake8 replaced with ruff.** The `.pre-commit-config.yaml` now runs `ruff --fix` + `ruff-format` (v0.16.1, matching CI) instead of flake8.
- **TOOL_MAP count corrected from 156 to 157 across all docs.** The map includes `buyVirtualMachine`, giving 100% coverage (was documented as 99%).

### Fixed
- **`shc order` now sends `config_options` with every order.** Previously, orders were submitted without `config_options`, causing the SHC platform to provision VMs with minimal resources (~1GB RAM) regardless of the ordered package. Now resolves default RAM, CPU, disk, and IPv4 count from the catalog and includes them in every order submission. This fixes the long-standing issue where ordered 8GB/16GB VMs were provisioned with ~908MB RAM.
- **`submit_order` resolves `order_form_id` and `package_group_id` from preview instead of hardcoding Dev VPS defaults.** Previously, `submit_order` unconditionally injected `order_form_id=11` (Dev VPS storefront) for all orders without `config_options`, causing `validation_failed` errors for NVMe, SSD, and HDD packages which use different storefront IDs. Now calls `preview_order` to resolve the correct IDs from the package's storefront path, falling back to 11 only if preview fails.
- **debian13-cloud default restored.** The template was previously changed to debian12-cloud based on a misdiagnosed cloud-init deadlock (issue #24). The actual problem was the Dev zone scheduler hang (issue #28) — VMs in Cherryvale, KS (Dev VPS) fail to provision regardless of template. debian13-cloud works correctly on NVMe/SSD/HDD VPS in Katy, TX. **E2E verified 2026-08-13**: ordered nvme-1c-4gb with debian13-cloud, provisioned in 53s, cancelled cleanly.
- **`compute.py` field mismatch and broken f-strings.** Was reading `item.get("ram")` (non-existent key, returned empty) instead of `item.get("memory_mb")`. Two f-string literals (`"pkg-{pkg_id}"`, `"…/{item.get(...)}"`) were missing the `f` prefix and silently output literal braces.
- **`raw` property docstring corrected.** Said "149 endpoint methods" and "Pydantic type safety" → corrected to "148" and "attrs-based".

### Added
- **`shc_toolkit/catalog_model.py`** — Static model of the SHC VM catalog. Replaces the 10.3 MB `/ordering/catalog` fetch with deterministic functions for pricing (`0.22×cpu + 0.02 + nvme_disk_premium`), option IDs, pricing IDs, and upgrade value lists. 100% accuracy across 160 checks.
- **`scripts/validate_catalog_model.py`** — Fetches the live catalog and compares against the model. Exit 0 = match, exit 1 = drift.
- **`--template` flag on `shc order`** for specifying OS template at order time.
- **`get_catalog_live()` on both transports + transport Protocol.** For validation use only — returns the real API response.

## [2.4.24.1] — 2026-08-09

### Changed
- **NoDNS marked experimental**: CLI help strings for `--nodns` and `shc nodns` subcommand now say `(experimental)`. README moved NoDNS from hero section to "Experimental" with warning. Dropped false "VERIFIED 2026-06-30" claim. NoDNS is a Python-only provisioning feature that belongs at a layer above IaC tools — it has been removed from terraform-provider-shc v0.2.0.

### Added
- **`tunnel.py` — Cloudflare Quick Tunnel for SSH access when inbound traffic is blocked.** New module with `CloudflareTunnel`, `ConsoleShell`, and `ensure_ssh_access()` for establishing outbound-only SSH tunnels via Cloudflare Quick Tunnel (no account needed). Uses noVNC console automation to bootstrap cloudflared on the VM, then connects locally via `cloudflared access tcp`. Proven working during SHC inbound network outage (2026-07-20). Install: `pip install shc-toolkit[tunnel]`.
- **`scripts/openapi-client-config.yaml`** — openapi-python-client config enabling `literal_enums: true`. Documents the codegen settings that produce correct generated models (Literal type aliases instead of Enum classes, avoiding key-normalization collisions). Makes `scripts/generate_client.sh` reproducible.
- **`scripts/dev-zone-probe.py`** — Dev zone (Cherryvale, KS) health probe. Orders the smallest Dev VPS, polls for `active`+IP or timeout, then cancels. Exit 0 = zone healthy, exit 1 = broken. Used to verify whether issue #28 (Dev zone scheduler hang) is resolved. Run: `python3 scripts/dev-zone-probe.py [--template debian13-cloud] [--timeout 300]`.

### Changed
- **Regenerated client synced with current SHC spec (v2.4.24).** 741 generated files refreshed (net −596 lines — cleaner output). Notably, **issue #20 (enum collision) is resolved upstream**: the SHC spec no longer contains the duplicate `cloud_init_policy_violation` variant — only the canonical `cloud-init-policy-violation` remains. The old `fix_enums` dedup workaround in `generate_client.sh` is removed (dead code, no collision exists). Added a mypy `follow_imports = skip` override for `shc_toolkit.generated.*` so codegen template quirks don't surface as type errors.

### Fixed
- **`test_update_vm_cloud_init_uses_confirmation_flow` stale assertion (PUT → PATCH).** Commit c3febee corrected `update_vm_cloud_init` to use `PATCH` per OpenAPI spec v2.4.24, but the unit test still asserted `"PUT"`. This broke every scheduled `shc-tests.yml` run (8+ consecutive failures since 2026-07-30). Test now asserts `"PATCH"`, matching the implementation and the spec's `updateVirtualMachineCloudInit` operation.
- **Pre-existing typecheck + coverage CI failures on `main` (since 2026-07-24).** Three independent root causes, all now resolved:
  - **mypy:** `tunnel.py` declared `self._page` / `self._browser` without annotations, so mypy inferred type `None` → 19 "None has no attribute" errors. Fields now typed `Page | None` / `Browser | None` (via `TYPE_CHECKING` import — playwright stays an optional dep) with `assert self._page is not None` narrowing in the four methods that use it (`_send_text`, `login`, `verify_shell`, `run_cmd`), which also doubles as a runtime "call `connect()` first" guard.
  - **ruff (lint + format):** CI runs unpinned `pip install ruff` (now 0.16.x), which newly enforced the `I001` import-sorting rule and ~9 additional default rules. Three fixes: (1) added `[tool.ruff] extend-exclude = ["shc_toolkit/generated"]` to pyproject.toml — the 932-file auto-generated client was producing 670 spurious errors (mypy already excluded it; ruff now matches); (2) auto-fixed 59 safe findings (f-string conversions, import alphabetization in `__init__.py` + `__all__`, formatter drift in `client.py` + `tunnel.py`); (3) added a curated `[tool.ruff.lint] ignore` list for 12 rules (BLE001/S110/S112 broad-except in retry paths, PLW1510 fire-and-forget subprocess in provisioning, SIM* stylistic, plus deferred micro-optimizations) — each with an inline justification, since the codebase predates these ruff 0.16 defaults and the patterns are intentional (245 tests pass).
  - **coverage workflow:** `coverage.yml` ran `tests/test_ansible.py` (which does `import yaml`) but installed only `pytest pytest-cov`, causing a `ModuleNotFoundError: No module named 'yaml'` at collection. Added `pyyaml` to the install step.
- **Pre-existing security-scanner CI failures on `main` (since 2026-07-24):**
  - **bandit (`-ll` medium+ threshold):** 14 findings — 5× B310 (`urllib.request.urlopen`) and 9× B108 (hardcoded `/tmp/`). Every B310 hits a hardcoded HTTPS download URL (GitHub API, cloudflared, ntfy.sh, SHC catalog) where the `file://`-scheme abuse B310 warns about cannot apply; every B108 is either a remote VM path (must be `/tmp` on the Linux guest — `REMOTE_PATH`, certbot hook), a diagnostic Playwright screenshot (stable path aids debugging), or an intentional cache/default (cloudflared binary, NoDNS keypair default). Each annotated `# nosec` with per-location justification rather than a blanket `.bandit` skip, so the rationale is auditable.
  - **pip-audit:** `setuptools 79.0.1` flagged for `PYSEC-2026-3447` (fix: `83.0.0`). setuptools is a build tool, not a runtime dependency — added a `pip install --upgrade "setuptools>=83.0.0"` step to the `pip-audit` job in `security.yml` so the scanned environment has the patched version.

## [2.4.24.0] — 2026-07-20

Spec-sync release. SHC shipped API v2.4.24 on 2026-07-19 (consolidating nine
same-day iterations, v2.4.16 → v2.4.24). The drift was detected by
`shc-tests.yml` and tracked in issue #21. All changes are additive / editorial
on SHC's side; no `operationId`, path, request body, response shape, auth
requirement, or enforcement behaviour changed (per SHC's contract stability
rule). This release closes #20, closes #21, and closes customer-support
ticket #2211883 (cloud-init feature request — SHC shipped in v2.4.7, now
fully wrapped in the toolkit's REST surface).

### Added
- **Cloud-init REST wrappers on `SHCClient` + `SHCTransport` Protocol** —
  `validate_vm_cloud_init`, `update_vm_cloud_init`, `delete_vm_cloud_init`.
  SHC shipped customer cloud-init in v2.4.7 (`#cloud-config` content via a
  server-managed NoCloud ISO); the MCP transport already wrapped all three
  via `TOOL_MAP`, but the REST transport was missing them. Live-verified
  against VM 1077: `validate_vm_cloud_init` returns a structured lint report
  (`policy: shc-cloud-init-customer-v1`, `findings: []`, `accepted: true`).
  Closes the parity gap surfaced during the ticket-#2211883 audit. The
  endpoint paths use the `/virtual-machines/{virtualMachineId}/cloud-init`
  convention (distinct from most `/vm/{serviceId}` paths but the value is
  the same `service_id`).
- `.omo/llms.txt` baseline (40 lines). `api-drift.yml` references this file but
  it was missing from the repo; the workflow's first-run self-baseline path was
  silently no-op'ing the llms.txt drift check. Future llms.txt drift will now
  open an issue.
- `ConfirmationChallenge` typed model in the regenerated client. Documents the
  409 `confirmation_required` re-call flow that the hand-written `SHCClient`
  already implements via `_confirmed_request`.
- `Error.confirmation` optional field in the regenerated client (the hand-written
  client already reads `confirmation.confirmation_id`).
- **MCP coverage gap closure**: `TOOL_MAP` extended from 125 → 156 entries,
  wrapping 156/157 (99%) of all MCP-exposed ops. The 31 new entries cover VM
  power (shutdown/reset), VM data (metrics/bandwidth/network/activity/payments),
  billing (transactions/payment checkout), support departments, templates,
  firewall full CRUD, reverse-DNS full CRUD, console, ISO mount/unmount, data
  preferences, file-restore browsing, and more. The single remaining unwrapped
  op is `buyVirtualMachine` (a deprecated alias for `createVirtualMachineOrder`,
  which IS wrapped). The corresponding `SHCMCPClient` methods already existed
  with direct `call_tool()` calls — only the TOOL_MAP audit surface was missing.

### Changed
- OpenAPI spec refreshed to v2.4.24 (148 paths, 197 schemas). Path count and
  `x-shc-core` count (35) are unchanged from v2.4.15; the drift is entirely
  response-shape specifications + one new schema.
- Regenerated typed client: **729 attrs models** (was 543) across **932
  Python files** (was 906). The new response schemas are now typed end-to-end
  for anyone using `shc_toolkit.generated`. (openapi-python-client v0.29
  generates `attrs` classes — not Pydantic as previous CHANGELOG entries
  erroneously stated since v2.4.3.1.)
- 14 operations that previously returned a `"Staged contract stub"` placeholder
  now carry their real response schema. Affected: `linkNostrIdentity`,
  `unlinkNostrIdentity`, `updateNip05`, `getNostrLinkChallenge`,
  `updateContact`, `listDownloadFiles`, `updateAccountManager`, `getOrder`,
  `cancelPendingOrder`, `approveQuotation`, `submitSupportTicketFeedback`,
  `getVirtualMachineTermOptions`, `previewVirtualMachineTermChange`.
  (`changeVirtualMachineTerm` keeps its placeholder per upstream — its prorated
  invoice shape could not be verified against a live response.)
- 14 confirmation-gated operations that omitted a 409 now declare one with the
  `Error` schema. Affected: `revokeApiKey`, `updateCreditHandling`,
  `updateAccountPreferences`, `updateAffiliatePayoutDestination`,
  `createContact`, `deleteServiceSshKey`, `setServiceSshKey`,
  `closeSupportTicket`, `deleteVirtualMachineBackup`,
  `setVirtualMachineBackupProtection`, `getVirtualMachineCredentials`,
  `unmountVirtualMachineIso`, `deleteVirtualMachineSnapshot`,
  `setVirtualMachineSnapshotProtection`. The hand-written client already
  handled these via the confirmation flow; no behaviour change.
- `x-shc-mcp-exposure` annotation now present on every operation (157 `exposed`,
  20 `hidden`). `serverInfo.catalog.tool_count` now reports 157 (the actual
  tool count), not 177 (the operation count). `TOOL_MAP` grows 124 → 125
  entries (added `get_vm_credentials` → `getVirtualMachineCredentials`,
  closing the last unwrapped `x-shc-core` gap; coverage is now 35/35 = 100%
of the curated core subset and 156/157 = 99% of all MCP-exposed ops).
The single unwrapped op is `buyVirtualMachine` — a deprecated alias for
`createVirtualMachineOrder` (which IS wrapped). Live MCP server tool count
matches our drift CI baseline.
- `claimAgentKey` and `mintVmConsoleSession` moved to their correct tags
  (`Account` and `Virtual Machines`) by upstream — generated client stops
  producing near-empty extra classes.
- `pyproject.toml` version bumped 2.4.15.1 → 2.4.24.0. The `.0` patch signals
  a clean spec-sync release with no hand-written code behaviour change.
- Documentation audit: `ROADMAP.md` and `README.md` updated to v2.4.24.

### Fixed
- **Documentation: `attrs` not Pydantic.** The generated client uses
  `openapi-python-client` v0.29.0, which generates `attrs` classes (verified
  via `attrs.has(GetOrderResponse200Data) == True`, `issubclass(...,
  pydantic.BaseModel) == False`). Previous CHANGELOG / README / ROADMAP
  entries since v2.4.3.1 described these as "Pydantic models" — corrected
  across all three docs in this release.
- **`close_support_ticket` confirmation flow.** The wrapper previously called
  `_post` directly and surfaced SHC's 409 `confirmation_required` as
  `SHCConfirmationRequiredError` instead of completing the confirmation
  re-send automatically (which is the whole point of `_confirmed_request`).
  Now uses `_confirmed_request` with `*, confirm: bool = True` default,
  matching the pattern of `cancel_vm`, `delete_snapshot`, `delete_backup`,
  `reinstall_vm`, etc. Live-verified by closing customer-support ticket
  #2211883 via the fixed wrapper. The Protocol `SHCTransport.close_support_ticket`
  gains the same signature; `SHCMCPClient.close_support_ticket` accepts
  `*, confirm: bool = True` as a no-op for symmetry (MCP transport handles
  confirmation via `call_tool`).
- **Files #22 follow-up.** Audit during the same live-testing pass found 11
  more methods with the same confirmation-flow gap (e.g. `set_stored_ssh_key`,
  `set_backup_protection`, `revoke_api_key`). Tracked in issue #22 — fix is
  mechanical but voluminous and deserves its own focused PR.
- **Closes #22.** All 11 confirmation-flow gaps fixed. Each method now routes
  through `_confirmed_request` with `*, confirm: bool = True` default, matching
  the pattern of `cancel_vm`, `delete_snapshot`, `delete_backup`,
  `close_support_ticket`, etc. The 11 methods are: `update_preferences`,
  `set_credit_handling`, `revoke_api_key`, `create_contact`,
  `set_affiliate_payout_destination`, `set_snapshot_protection`,
  `set_backup_protection`, `get_vm_credentials` (the only GET — secret-read
  per v2.4.14), `set_stored_ssh_key`, `delete_stored_ssh_key`, `unmount_iso`.
  Live-verified on VM 1077: `get_vm_credentials(sid, confirm=False)` correctly
  surfaces the 409 with `confirmation_id` attached; `get_vm_credentials(sid)`
  (default `confirm=True`) auto-completes the re-send and returns credentials.
  The `SHCTransport` Protocol gains matching signatures for the 10
  MCP-reachable ops; `revoke_api_key` stays REST-only (it is identity-class
  per SHC v2.4.13: not exposed by the MCP server, verified against
  `mcp.sovereignhybridcompute.com` tool list — `revokeApiKey` absent,
  `listApiKeys` present). All `SHCMCPClient` variants accept
  `*, confirm: bool = True` as a no-op for symmetry (MCP handles confirmation
  via `call_tool`). Closes #23 (MCP drift auto-issue from an earlier draft
  that briefly added `revokeApiKey` to `TOOL_MAP`).
- **Closes #20.** Upstream removed the duplicate `Problem.x-error-code` enum
  value. Previously both `cloud-init-policy-violation` and
  `cloud_init_policy_violation` were present and normalised to the same
  `CLOUD_INIT_POLICY_VIOLATION` key, which aborted `openapi-python-client`.
  Per upstream's v2.4.24 changelog: "the removed spelling was never emitted,
  and the value the server actually returns is unchanged" — i.e. SHC kept the
  hyphenated form (the one the server emits) and removed the underscore form.
  Issue #20 had recommended the opposite (keep the underscore form to match
  the convention of the other 76 values), but upstream's choice is more
  contract-truthful: the spec now matches wire behaviour. Verified post-fix:
  enum now has 77 values (was 78), zero normalised-key collisions. The
  `openapi-python-client` regeneration that this blocked since 2026-07-16
  now runs clean. The defensive dedup step in `scripts/generate_client.sh`
  (lines 69-98) is retained as a belt-and-braces guard against future spec
  bugs of the same shape.
- **Closes #21.** API drift issue auto-created by `shc-tests.yml` on 2026-07-20.
  Resolved by this release.

### Decision: hand-written client keeps returning raw dicts

The hand-written `SHCClient` / `SHCMCPClient` continue to return raw `dict` /
`list[dict]` from JSON responses. We did **not** add dataclass / Pydantic
typed wrappers in the hand-written layer. The regenerated client
(`shc_toolkit.generated`, +729 attrs models) is the typed surface.

This follows the 2026 maintainer consensus: avoid duplicate typed surfaces
when an OpenAPI-generated Pydantic layer already exists (cf. Slothbox SDK
ADR-0001, Katana ADR-0002, Boto3's botocore/boto3 split). The hand-written
layer's value is ergonomics — retry with jitter, cost tracking, confirmation
flow, cache, MCP transport — not type safety. Re-exporting generated models
into the hand-written namespace is a future option (WorkOS-style) if users ask.

References:
- https://github.com/sloth-box/sdk-python/blob/main/docs/adr/0001-generator-choice.md
- https://github.com/dougborg/katana-openapi-client/blob/main/katana_public_api_client/docs/adr/0002-openapi-code-generation.md

---

## [2.4.15.1] — 2026-07-16

Backfilled entry. The `2.4.3.1` CHANGELOG section below was the last documented
release; this section covers everything that shipped between `v2.4.3.1` and
`v2.4.15.1` (the version in `pyproject.toml` immediately before the v2.4.24.0
bump above). The gap was a documentation miss, not a release miss.

### Added
- Adopted SHC API **v2.4.6** — agent sessions (`createAgentSession`,
  `listAgentSessions`, `getAgentSession`, `revokeAgentSession`,
  `listAgentSessionAudit`) with Nostr proof-of-possession binding.
- Adopted SHC API **v2.4.15** and wrapped **14 new MCP tools** in `TOOL_MAP` /
  `SHCMCPClient` / `SHCClient`. New upstream surfaces include:
  - **2FA enrollment** (`beginTwoFactorEnrollment`, `enableTwoFactor`,
    `disableTwoFactor`) — Basic+OTP identity ops, not API-key callable.
  - **Webhooks** (`/event-subscriptions` CRUD) with HMAC-SHA256 signed
    CloudEvents delivery.
  - **Events feed** (`GET /events`, cursor-paginated CloudEvents).
  - **Batch** (`POST /batch`, up to 25 sub-requests).
  - **VM standby/resume** (`standbyVirtualMachine`, `resumeVirtualMachine`,
    `previewVirtualMachineStandby`).
  - **Customer cloud-init** (`validateVirtualMachineCloudInit`,
    `updateVirtualMachineCloudInit`, `deleteVirtualMachineCloudInit`).
  - **ZK backup** registration / rekey / recipient management.
  - **Managed-account switch** (`switchManagedAccount`).
- **`reap_orphans()`** on `SHCClient` + `shc reap` CLI command + hourly
  `reaper.yml` workflow. Identifies VMs older than a configurable age threshold
  and cancels them, with dry-run mode, hostname-prefix filters, and exclusions.
- **`raw` property** on `SHCClient` — WorkOS-pattern POC that exposes the
  generated client (`shc_toolkit.generated.Client`) for type-safe raw API
  access without losing the hand-written ergonomics layer.
- **AGENTS.md** — maintenance guide for the three-repo SHC IaC ecosystem
  (shc-toolkit, terraform-provider-shc, shc-pulumi). Covers the drift-update
  runbook, codegen quirks, CHANGELOG discipline, CI map, known limitations.
- **Exception hierarchy** (`SHCError`, `SHCNotFoundError`, `SHCAuthError`,
  `SHCRateLimitError`, `SHCConfirmationRequiredError`, etc.) + pre-commit
  hooks (flake8, mypy).

### Changed
- **HTTP transport swap**: `SHCClient` moved from `requests` to `httpx` for the
  REST transport. `SHCMCPClient` still uses `requests` (MCP Streamable HTTP
  client requirement). The network-blocking test fixture
  (`tests/conftest.py`) patches both.
- **Cost audit redesign**: single authoritative balance-diff check at cancel
  time (was scattered across multiple points). Per-VM ledger disambiguation
  for concurrent activity. Refund tracking now first-class.
- Regenerated typed client brought up to v2.4.15: **906 Python files**, 543
  Pydantic models, 148 endpoints (was 129 paths / 718 files at v2.4.3).
- `Idempotency-Key` moved to `_confirmed_request` (fixes the confirmation flow
  when callers supply their own key). Caller-provided keys are no longer
  overwritten.
- Drift-detection CI: `confirmation_id` is now read from the correct JSON path
  (`confirmation.confirmation_id`, not the legacy nested `structuredContent`
  copy which may be absent).

### Fixed
- Removed 3 broken Nostr MCP tools (`linkNostrIdentity`, `unlinkNostrIdentity`,
  `updateNip05`) from `TOOL_MAP` — upstream v2.4.13 clarified these are
  Basic+OTP identity operations, not API-key callable. `getNostrLinkChallenge`
  stays (it is read-only).
- Confirmation flow: extract `confirmation_id` from the correct JSON path
  (was reading a legacy nested location that may be absent).
- Flake8: fixed all F-issues across the codebase. Autopep8 structural fixes.

---

## [2.4.3.1] — 2026-07-11

First release aligned with the SHC API version. Format: `<SHC_API_VERSION>.<toolkit_patch>`.
This release supports SHC API v2.4.3 (129 paths, 156 schemas).

### Added
- Auto-generated Python client from OpenAPI spec (`shc_toolkit.generated`) — 149 endpoint methods, 543 Pydantic models, 100% API coverage. Install with `pip install shc-toolkit[generated]`.
- `scripts/generate_client.sh` — regenerates the auto-generated client from the OpenAPI spec.
- 85 new MCP TOOL_MAP entries (23 → 108) — MCP coverage from 33% to 99% (141/142 server tools).
- 33 new SHCMCPClient wrapper methods for the new TOOL_MAP entries.
- 11 new SHCClient REST methods for v2.4.3 endpoints (VM term/addons, Orders).
- 11 new transport.py ABC method signatures.
- CI auto-creates deduplicated GitHub issues on API drift detection.
- Cross-repo parity CI workflow (`.github/workflows/cross-repo-parity.yml`).
- `resolve_addons` cross-repo contract parity check in `scripts/audit_cross_repo.py`.
- Network-blocking autouse fixture in `tests/conftest.py` — prevents unit tests from leaking real HTTP calls.
- `tests/test_network_fixture.py` — 4 regression tests for the network-blocking fixture.
- `tests/test_ansible.py` — 13 tests for the ansible/ subtree (inventory logic, YAML sanity, bug regressions).
- Molecule caddy scenario with `policy-rc.d` + self-signed cert `prepare.yml`.
- Weekly live E2E workflow (`.github/workflows/ansible-e2e.yml`) — runs full playbook against real SHC Dev VPS.
- 408 Request Timeout is now retried (2026 API resilience reference).
- Auto-generated `Idempotency-Key` header on all POST/PATCH/PUT/DELETE requests.
- `term` attribute on the Terraform VM resource (v2.4.3 VM term management).
- `caddy_manage_service` toggle on the caddy ansible role (for non-systemd environments).
- Pulumi Terraform Bridge migration guide (`MIGRATION-TO-BRIDGE.md` in shc-pulumi).

### Fixed
- `resolve_addons` now raises `ValueError("package_id X not found in catalog")` on unknown packages — was silently returning `{}` (Go provider already had this; Python was drifted).
- 3 flaky tests in `test_unit.py` that leaked real HTTP calls to the SHC API (`_safe_credit` cache invalidation + `get_vm_payments` unmocked path).
- `caddy_manage_service` toggle now correctly gates the `Restart caddy` handler (was only gating the explicit systemd task — handler leaked).
- TOOL_MAP duplicate key: `get_account_balance` was mapped to `getBillingBalance` (original) but overwritten to `getAccountBalance` (addition). Fixed by adding `get_billing_balance` as a separate entry.
- 4 ansible bugs: stale `inventory/shc-hosts.ini` refs, hardcoded `nsec1` prefix strip, missing OS group docs, `caddy_cert_path`/`caddy_domain`/`caddy_key_path` defaults (were defined but audit missed them).
- CI: `permissions: issues: write` was missing `contents: read`, causing `actions/checkout` to fail.
- CI: duplicate `workflow_dispatch:` key under `permissions:` block (YAML parse failure).
- CI: Python `IndentationError` in MCP drift detection script (11-space indent vs 10-space).
- API version corrected from v2.5.0 → v2.4.3 (SHC bot had prematurely labelled the spec).

### Changed
- OpenAPI spec refreshed to v2.4.3 (129 paths, 156 schemas).
- 5 ansible-lint findings fixed (3 `no-changed-when`, 1 `var-naming`, 1 `yaml[line-length]`). 6 `jinja[invalid]` false positives remain baselined.
- `shc_inventory.py` refactored: extracted pure `build_inventory(vms)` function for testability.
- `terraform-provider-shc` gained 10 new Go methods (VM term/addons + Orders).
- `ROADMAP.md` updated: API v2.4.3, 142 MCP tools, 99% coverage, 169 unit tests.
- 3 dependabot PRs merged (actions/checkout v4→v7, setup-python v5→v6, github-script v7→v9).

### Removed
- All NIP-90 DVM code paths from `physical-router-test-automation/docs/app.js` (217 lines, issue #8).
- `terraform-provider-shc/provider/sizes.go.bak` (untracked stale file).

## [0.5.0] — 2026-07-02

Initial public release with:
- SHCClient (REST), SHCMCPClient (MCP Streamable HTTP), dual transport
- VM lifecycle, ordering, snapshots, backups, firewall, rDNS, NoDNS
- CostTracker (balance-diff auditing), Cost audit
- GitHub Actions ephemeral runners
- ContextVM bootstrap
- Ansible integration (playbook + 4 roles + dynamic inventory)
- Cashu tollgate
