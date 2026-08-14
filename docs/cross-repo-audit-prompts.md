# Cross-Repo Audit Prompts — shc-toolkit ↔ terraform-provider-shc

Reusable prompts for AI agents to audit the two SHC repos against each other.
Mechanical parity (size maps, billing claims) is covered by
`python3 scripts/audit_cross_repo.py` — these prompts cover what regex can't.

Run each prompt from a checkout with both repos side by side:

```
/Users/you/src/shc-toolkit
/Users/you/src/terraform-provider-shc
```

---

## Prompt 1: Behavioral Parity Audit

```
You are auditing two repos that wrap the same HTTP API (SHC User API v2).

LEFT  = shc-toolkit (Python: shc_toolkit/)
RIGHT = terraform-provider-shc (Go: provider/)

For each behavior below, find the implementation in BOTH repos and verify
they make the SAME decision. Report a table: behavior | Python | Go | match?

1. Default OS template (should be debian13-cloud everywhere)
2. VM readiness condition (must be service_status=="active" AND ip non-empty;
   NEVER provisioning_state=="ready")
3. Retry policy: which status codes retry, max attempts, backoff base/cap,
   jitter
4. Confirmation flow: header name, auto-resend behavior, confirm=False
   probe-mode behavior
5. Idempotency-Key generation: format, length, charset, which requests
   get one
6. Credit check: minimum amount, fail-open vs fail-closed on endpoint
   error
7. Order form IDs per line (nvme=1, ssd=7, hdd=3, dev=11) — both must
   agree
8. Daily prices for all 20 packages — must be identical
9. Cancellation: immediate flag behavior, refund expectations
10. Error taxonomy: do shared error codes (not_found, invalid_token,
    confirmation_required, insufficient_credit) surface with the same
    semantics?

Exit criteria: every mismatch is reported with file:line on both sides.
```

## Prompt 2: Lessons Ported Audit

```
Read AGENTS.md in BOTH shc-toolkit and terraform-provider-shc.

shc-toolkit's AGENTS.md contains numbered lessons (1-18). For each lesson
that has cross-repo implications, verify terraform-provider-shc either:
  (a) already applies the lesson (cite file:line), or
  (b) has it documented in its own AGENTS.md, or
  (c) is immune to it (explain why — e.g. language-specific).

Flag any lesson that applies to Go but is neither implemented nor
documented. Key ones to check: batch API bare-array + Idempotency-Key,
cloud-init /virtual-machines/{id} path convention, identity-class ops
not API-key callable, "ready" never fires, Dev zone scheduler hang,
debian13-cloud correctness, __future__-equivalent import ordering issues
(N/A for Go).
```

## Prompt 3: DRY Boundary Audit

```
Find every piece of duplicated knowledge between shc-toolkit and
terraform-provider-shc. For each, classify:

  A. Derivable — one repo should generate it from the other
     (example: sizes.go is generated from catalog_model.py via
      scripts/generate_sizes.py)
  B. Intentionally duplicated — different languages need parallel
     implementations, but must be audited together
     (example: retry/backoff logic, readiness polling)
  C. Accidental — should be deleted or unified

Current known duplication: size tables (generated ✓), order-form-ID maps,
pricing formula constants, template lists, User-Agent strings, known-template
validators.

For each category-B item, check whether a mechanical parity check exists
in scripts/audit_cross_repo.py; if not, propose one as a regex/AST check.
```

## Prompt 4: Drift Smoke Test (live API required)

```
With SHC_API_KEY set, run these in order and compare outputs:

1. python3 -c "from shc_toolkit.catalog_model import validate_against_live;
   from shc_toolkit.client import SHCClient;
   import os; c=SHCClient(api_key=os.environ['SHC_API_KEY']);
   print(validate_against_live(c.get_catalog_live()))"
   → must print []

2. SHC_API_KEY=... python3 scripts/validate_catalog_model.py
   → exit 0

3. Order the cheapest VM from each repo (shc CLI / terraform apply),
   verify provision < 120s, cancel immediately, verify refund.

Report total cost — should be under $0.02.
```

---

## Maintenance

- Re-run Prompt 1 and 2 after every SHC API update (monthly cadence).
- Prompt 3 after any refactor that moves shared knowledge.
- Prompt 4 before tagging any release.
- When a new lesson is added to either AGENTS.md, add it to Prompt 2's list.
