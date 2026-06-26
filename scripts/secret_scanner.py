#!/usr/bin/env python3
"""Pre-commit secret scanner — blocks commits containing secrets."""

import re
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r"nsec1[023456789acdefghjklmnpqrstuvwxyz]{58}"), "nostr-nsec"),
    (re.compile(r"shc_live_[A-Za-z0-9_-]{20,}"), "shc-api-key"),
    (re.compile(r"\b(gho_|ghp_|github_pat_)[A-Za-z0-9_]{36,}\b"), "github-token"),
    (re.compile(r"\bsk-[a-zA-Z0-9]{40,}\b"), "openai-key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "pem-private-key"),
    (re.compile(r"cashu[AB][a-zA-Z0-9+/=]{20,}"), "cashu-token"),
    (re.compile(r"(?:password|passwd|pwd)\s*[=:]\s*['\"]([^'\"]{6,})['\"]", re.IGNORECASE), "password-assignment"),
    (re.compile(r"(?:NOSTR_SECRET_KEY|BOT_NSEC|nsec_hex)\s*[=:]\s*['\"]?([a-f0-9]{64})['\"]?"), "nostr-hex-key"),
    (re.compile(r"\bHCLOUD_TOKEN\s*[=:]\s*['\"]?([A-Za-z0-9]{64})['\"]?"), "hetzner-token"),
]

BLOCKLIST_FILES = {".env", "credentials.sh", ".env.local", ".env.production", "id_rsa", "id_ed25519"}
BLOCKLIST_EXTENSIONS = {".pem", ".key", ".p12", ".keystore"}


def scan_file(path: Path) -> list[str]:
    findings = []
    if path.name in BLOCKLIST_FILES or path.suffix in BLOCKLIST_EXTENSIONS:
        findings.append(f"BLOCKED: {path.name} — blocked file type")
        return findings
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return findings
    for pattern, name in PATTERNS:
        matches = pattern.findall(text)
        if matches:
            if name == "password-assignment":
                for m in matches:
                    if m and not m.startswith("$") and not m.startswith("<") and m.lower() not in ("none", "null", "true", "false", "changeme"):
                        findings.append(f"{name}: password-like assignment in {path.name}")
            else:
                findings.append(f"{name}: {path.name}")
    return findings


def main():
    staged = []
    import subprocess
    result = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"], capture_output=True, text=True)
    for line in result.stdout.strip().split("\n"):
        if line:
            staged.append(Path(line))

    all_findings = []
    for path in staged:
        if not path.exists():
            continue
        findings = scan_file(path)
        all_findings.extend(findings)

    if all_findings:
        print("🚨 PRE-COMMIT SECRET SCAN FAILED")
        print()
        for f in all_findings:
            print(f"  ❌ {f}")
        print()
        print("If these are false positives, use: git commit --no-verify")
        sys.exit(1)
    else:
        print("✅ Pre-commit scan: no secrets detected")


if __name__ == "__main__":
    main()
