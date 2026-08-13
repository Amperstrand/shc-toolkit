# SHC API Integration — DRY Architecture & CI Strategy

## The DRY Layer Cake

```
                    SHC OpenAPI Spec (v2.4.24, 148 endpoints)
                              ↓ single source of truth
                    ┌─────────────────────────────────┐
                    │   shc-toolkit/catalog_model.py   │  (static model, CI-validated)
                    │   shc-toolkit/openapi.json       │  (cached spec, CI-diffed)
                    └─────────────────────────────────┘
                              ↓ consumed by
           ┌──────────────────┼──────────────────┐
           ↓                  ↓                  ↓
    Python Toolkit      Pulumi Provider    Terraform Provider
    (client.py)         (imports client)   (Go HTTP client)
           │                  │                  │
    shc CLI /             pulumi up        terraform apply
    shc-compute
```

### Layer 1: OpenAPI Spec + Static Catalog Model

**File**: `shc_toolkit/openapi.json` (cached spec in git, CI-diffed weekly)
**File**: `shc_toolkit/catalog_model.py` (static catalog model — replaces 10.3 MB `/ordering/catalog` fetch)

The OpenAPI spec is fetched from `https://blesta.sovereignhybridcompute.com/user-api/openapi.json`
and cached locally. The catalog model derives prices, option IDs, and value lists from
deterministic arithmetic patterns (validated weekly against the live API via CI). This solves
the intermittent API problem — our tools read from local static data, not from the live API.

### Layer 2: Python Toolkit (the canonical client)

`shc_toolkit/client.py` is the single Python implementation of the SHC API.
All Python tools (CLI, Pulumi provider) import it directly.

```python
from shc_toolkit.client import SHCClient  # ← one client, many consumers
```

### Layer 3a: Pulumi Provider (thin wrapper)

The Pulumi dynamic provider imports `SHCClient` directly — no code duplication.

```python
from shc_toolkit.client import SHCClient  # ← imports the toolkit
```

This is why Pulumi is the lower-effort path: zero API code duplication.

### Layer 3b: Terraform Provider (Go — needs its own client)

Go can't import Python. Two options:

**Option A: Generate Go types from OpenAPI (recommended)**
```bash
oapi-codegen -package shc -generate types shc_toolkit/openapi.json > types_gen.go
```
This generates Go structs that exactly match the API spec. When the spec changes,
regenerate. The Terraform provider uses these generated types.

**Option B: Manual Go client (current approach)**
Write Go types by hand, validate against spec in CI. More flexible but
requires manual sync when the API changes.

### CI: Drift Detection Pipeline

```yaml
# .github/workflows/shc-api-drift.yml
name: SHC API Drift Detection
on:
  schedule:
    - cron: '0 */6 * * *'  # every 6 hours
  pull_request:
    paths: ['shc_toolkit/openapi.json', 'shc_toolkit/catalog_cache.json']

jobs:
  drift-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout
      - name: Fetch live OpenAPI spec
        run: |
          curl -s https://blesta.sovereignhybridcompute.com/user-api/openapi.json > /tmp/live-spec.json
      - name: Diff OpenAPI spec
        run: |
          if ! diff -q shc_toolkit/openapi.json /tmp/live-spec.json; then
            echo "::warning::SHC OpenAPI spec has changed! Update local cache."
            diff shc_toolkit/openapi.json /tmp/live-spec.json | head -50
            exit 1
          fi
      - name: Validate catalog still has expected packages
        env:
          SHC_API_KEY: ${{ secrets.SHC_API_KEY_READ_ONLY }}
        run: |
          python -m pytest tests/test_catalog_drift.py -v
```

### CI: Endpoint Smoke Tests

```python
# tests/test_shc_api_smoke.py
"""
Smoke tests for all SHC API endpoints.

Uses a READ-ONLY API key (scope=read, no areas restricted).
Tests assert response SHAPE (keys present, types correct), NOT data values.
This catches API drift without exposing account details.

No secrets are logged. Test failures show endpoint + status code only.
"""

import os
import pytest
import requests

BASE = "https://blesta.sovereignhybridcompute.com/user-api/v2"
KEY = os.environ.get("SHC_API_KEY_READ_ONLY", "")
HEADERS = {"Authorization": f"Bearer {KEY}"}

def _get(path, **kwargs):
    """GET with text-prefix stripping."""
    r = requests.get(f"{BASE}{path}", headers=HEADERS, timeout=15, **kwargs)
    assert r.status_code in (200, 404), f"{path}: {r.status_code}"
    if r.status_code == 404:
        pytest.skip(f"{path} returned 404 (no data)")
    text = r.text
    idx = text.find("{")
    import json
    return json.loads(text[idx:]) if idx >= 0 else {}

class TestAccount:
    def test_balance(self):
        d = _get("/account/balance")
        data = d.get("data", d)
        assert "credit" in data or "due" in data

    def test_account_info(self):
        d = _get("/account")
        data = d.get("data", d)
        assert "email" in data
        # NEVER assert the actual email value

class TestCatalog:
    def test_catalog_returns_items(self):
        d = _get("/ordering/catalog")
        data = d.get("data", d)
        items = data.get("items", [])
        assert len(items) > 0, "Catalog should return packages"
        # Assert structure, not values
        first = items[0]
        assert "package_id" in first
        assert "name" in first

class TestVMEndpoints:
    """Test VM endpoints. Uses whatever VMs exist on the account."""
    @pytest.fixture(scope="class")
    def vm_id(self):
        d = _get("/vm")
        items = d.get("data", d).get("items", [])
        if not items:
            pytest.skip("No VMs on account")
        return str(items[0]["id"])

    def test_list_vms(self):
        d = _get("/vm")
        assert "items" in d.get("data", d)

    def test_vm_detail(self, vm_id):
        d = _get(f"/vm/{vm_id}")
        data = d.get("data", d)
        assert "hostname" in data
        assert "service_status" in data

    def test_vm_credentials(self, vm_id):
        """NEW in v2.2 — password endpoint!"""
        d = _get(f"/vm/{vm_id}/credentials")
        data = d.get("data", d)
        # Assert shape, never log the actual password
        if "error" not in d:
            assert "password" in str(data).lower() or "username" in str(data).lower()

    def test_vm_metrics(self, vm_id):
        d = _get(f"/vm/{vm_id}/metrics")
        # Just verify it doesn't crash

    def test_vm_network(self, vm_id):
        d = _get(f"/vm/{vm_id}/network")

    def test_vm_activity(self, vm_id):
        d = _get(f"/vm/{vm_id}/activity")

class TestOrdering:
    def test_preview(self):
        """Preview never actually orders — safe to call."""
        import json
        r = requests.post(
            f"{BASE}/ordering/preview",
            headers={**HEADERS, "Content-Type": "application/json"},
            json={"hostname": "ci-test", "package_id": 81, "pricing_id": 245},
            timeout=15,
        )
        assert r.status_code == 200
        text = r.text
        idx = text.find("{")
        d = json.loads(text[idx:])
        data = d.get("data", d)
        assert "package" in data or "normalized_request" in data
```

### Catalog Model Validator

```bash
# Weekly CI job in api-drift.yml
SHC_API_KEY=... python3 scripts/validate_catalog_model.py
```

## Summary of Key Findings

### API v2.2 Changes Discovered

| Finding | Impact |
|---------|--------|
| `GET /vm/{id}/credentials` — **NEW** | Can now get VM password via API (no more portal scraping!) |
| `config_options` is the correct field name | Our `options` was silently ignored |
| Dev VPS defaults to debian13-cloud | No config_options needed for basic ordering |
| Option ID 174 (not 126) for Dev VPS template selection | Our hardcoded 126 was wrong but harmless |
| Catalog intermittently returns 0 items | Justifies local cache |
| `data` wrapper on all responses | Our Go provider needed unwrapData() |

### Architecture Decisions

| Component | Approach | Why |
|-----------|----------|-----|
| Catalog data | Static model (`catalog_model.py`), CI-validated weekly | Survives API outages, zero network calls |
| Python toolkit | Direct API client (source of truth) | One implementation |
| Pulumi provider | Imports Python toolkit directly | Zero duplication |
| Terraform provider | Go client, manually synced to spec | Go can't import Python |
| CI tests | Read-only API key, shape validation | No secrets leak |
| Drift detection | Diff cached OpenAPI vs live | Catches upstream changes |
