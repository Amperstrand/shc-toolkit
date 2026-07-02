#!/usr/bin/env python3
"""Fetch the live SHC catalog and regenerate catalog_cache.json + sizes.py.

Thin wrapper around the canonical implementation in
``shc_toolkit.generate_sizes``. Supports multiple output formats:

    python scripts/generate_sizes.py                                          # python -> shc_toolkit/sizes.py + cache
    python scripts/generate_sizes.py --format go    --output provider/sizes.go
    python scripts/generate_sizes.py --format pulumi --output src/shc_pulumi/sizes.py
    python scripts/generate_sizes.py --from-cache                             # regenerate without a live fetch
    python scripts/generate_sizes.py --check                                  # compare live vs cached, exit 1 if drift

Run locally or in CI. Requires SHC_API_KEY in env for any live fetch.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow running directly from a source checkout without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shc_toolkit.generate_sizes import main

if __name__ == "__main__":
    raise SystemExit(main())
