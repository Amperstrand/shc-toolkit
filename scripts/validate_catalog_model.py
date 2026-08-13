#!/usr/bin/env python3
"""Validate the static catalog model against the live SHC API.

Fetches the real 10.3 MB catalog, compares prices, pricing IDs, and specs
against catalog_model.py. Exits 0 on match, 1 on drift.

Usage:
    SHC_API_KEY=shc_live_... python3 scripts/validate_catalog_model.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shc_toolkit.catalog_model import validate_against_live
from shc_toolkit.client import SHCClient


def main() -> int:
    api_key = os.environ.get("SHC_API_KEY", "")
    if not api_key:
        print("ERROR: SHC_API_KEY not set", file=sys.stderr)
        return 2

    client = SHCClient(api_key=api_key)

    print("Fetching live catalog (10.3 MB)…")
    live = client.get_catalog_live()
    print(f"  Received {len(live)} packages")

    errors = validate_against_live(live)

    if not errors:
        print("✓ Model matches live catalog perfectly.")
        return 0

    print(f"\n✗ {len(errors)} discrepancy(ies) found:\n")
    for e in errors:
        print(f"  • {e}")

    print("\nThe model in catalog_model.py needs updating.")
    print("Run: python3 scripts/generate_sizes.py  # after fixing the model")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
