#!/usr/bin/env python3
"""GitHub Actions workflow_job webhook autoscaler.

HTTP server that listens for workflow_job webhooks from GitHub and
spawns/kills Firecracker μVMs accordingly. Pairs with
scripts/firecracker_pool.py.

Architecture:
    GitHub → workflow_job webhook → this server → firecracker_pool.spawn_one()
    On 'queued' action with matching labels → spawn μVM with that label
    On 'completed' or 'in_progress' → no-op (μVM is ephemeral, self-removes)

    This replaces the in-workflow `provision-shc-runner` job in
    .github/workflows/shc-runner-benchmark.yml. The webhook-driven path
    is faster (no workflow spinup) and supports arbitrary repos.

Usage:
    sudo python3 scripts/webhook_autoscaler.py \\
        --port 8443 \\
        --webhook-secret-file /tmp/gh-webhook-secret \\
        --gh-token-file /tmp/gh-token \\
        --repo Amperstrand/tollgate-module-basic-go

Configure GitHub webhook at:
    https://github.com/<owner>/<repo>/settings/hooks/new
    - Payload URL: http://<host-vm-public-ip>:8443/github
    - Content type: application/json
    - Secret: same value as --webhook-secret-file
    - Events: just "Workflow jobs"

Test mode (no GitHub setup):
    curl -X POST -H 'X-GitHub-Event: workflow_job' \\
         -H 'X-Hub-Signature-256: sha256=<computed>' \\
         -d @test-payload.json http://localhost:8443/github
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def verify_signature(body: bytes, signature_header: str, secret: str) -> bool:
    """Verify GitHub webhook HMAC-SHA256 signature.

    Ref: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
    """
    if not signature_header.startswith("sha256="):
        return False
    expected = signature_header.removeprefix("sha256=")
    mac = hmac.new(secret.encode(), body, hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), expected)


# globals set in main()
GH_TOKEN = ""
REPO = ""
POOL_HOST_TOKEN = ""  # registration token, lazily refreshed
PRINT_LOCK = threading.Lock()


def log(msg: str) -> None:
    with PRINT_LOCK:
        print(f"[{time.strftime('%FT%TZ', time.gmtime())}] {msg}", flush=True)


def refresh_runner_token() -> str:
    """Mint a fresh repo-level runner registration token from GitHub API."""
    import urllib.request, ssl
    url = f"https://api.github.com/repos/{REPO}/actions/runners/registration-token"
    req = urllib.request.Request(
        url, method="POST",
        headers={
            "Authorization": f"Bearer {GH_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "fc-webhook-autoscaler",
        },
    )
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return json.loads(resp.read().decode())["token"]


def spawn_for_label(runner_label: str, runner_name: str) -> None:
    """Spawn a μVM with the given label (called in a thread)."""
    log(f"spawn_for_label start: name={runner_name} label={runner_label}")
    try:
        # Refresh token each spawn (safer than reusing)
        token = refresh_runner_token()
        # Import lazily so this script can run standalone for testing
        sys.path.insert(0, str(Path(__file__).parent))
        from firecracker_pool import spawn_one, kill_one
        # Static IP pool: 10.0.0.100 + counter (avoids collisions with bench IPs)
        global _ip_counter
        _ip_counter = getattr(_ip_counter_module(), "_counter", 100) + 1
        _ip_counter_module()._counter = _ip_counter
        static_ip = f"10.0.0.{_ip_counter}"
        vm = spawn_one(
            name=runner_name,
            repo=REPO, token=token,
            labels=f"shc,fc,{runner_label}",
            vcpu=2, mem_mib=2048,
            timeout_s=300,
            static_ip=static_ip,
            poll_github=True,
            github_token=GH_TOKEN,
        )
        log(f"spawn_for_label done: name={runner_name} boot={vm.boot_to_init_s}s err={vm.error}")
    except Exception as e:  # noqa: BLE001
        log(f"spawn_for_label FAILED: {type(e).__name__}: {e}")


# Cheap IP counter (module-level)
def _ip_counter_module():
    import sys
    mod = sys.modules.get("__main__")
    if not hasattr(mod, "_counter"):
        mod._counter = 100
    return mod


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/github":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b""

        # Verify signature if secret is configured
        secret = WEBHOOK_SECRET
        sig = self.headers.get("X-Hub-Signature-256", "")
        if secret:
            if not verify_signature(body, sig, secret):
                log(f"REJECT: bad signature (len={len(body)})")
                self.send_response(401)
                self.end_headers()
                return

        event = self.headers.get("X-GitHub-Event", "")
        if event != "workflow_job":
            # Acknowledge ping and other events but don't act
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"msg":"ignored"}')
            return

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        action = payload.get("action")
        job = payload.get("workflow_job", {})
        labels = job.get("labels", [])
        repo_full = payload.get("repository", {}).get("full_name", "")

        log(f"workflow_job action={action} labels={labels} repo={repo_full}")

        # Only react to 'queued' (spawn) — runner is ephemeral, self-removes
        if action == "queued":
            # Spawn only if labels include our 'shc' or 'fc' marker
            if "shc" in labels or "fc" in labels:
                # Extract a runner name from labels (unique per-run marker)
                runner_label = next(
                    (l for l in labels if l.startswith("shc-") or l.startswith("fc-")),
                    f"webhook-{int(time.time())}",
                )
                runner_name = f"auto-{runner_label}"
                threading.Thread(
                    target=spawn_for_label,
                    args=(runner_label, runner_name),
                    daemon=True,
                ).start()
                self.send_response(202)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"spawned": True, "label": runner_label,
                                "name": runner_name}).encode()
                )
                return

        # Default: ack
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"msg":"ack"}')

    def log_message(self, fmt, *args):
        # Suppress default stderr logging; we log via our own log() function
        pass


WEBHOOK_SECRET = ""


def main() -> int:
    global WEBHOOK_SECRET, GH_TOKEN, REPO

    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8443)
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--webhook-secret-file",
                    help="path to file containing the GitHub webhook secret")
    ap.add_argument("--gh-token-file", required=True,
                    help="path to file with a PAT (runners:write on repo)")
    ap.add_argument("--repo", required=True,
                    help="owner/repo (e.g. Amperstrand/tollgate-module-basic-go)")
    args = ap.parse_args()

    GH_TOKEN = Path(args.gh_token_file).read_text().strip()
    REPO = args.repo
    if args.webhook_secret_file:
        WEBHOOK_SECRET = Path(args.webhook_secret_file).read_text().strip()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    log(f"autoscaler listening on {args.host}:{args.port} (repo={REPO})")
    log(f"webhook secret: {'set' if WEBHOOK_SECRET else 'NONE (signature checks disabled)'}")
    log(f"healthz: curl http://{args.host}:{args.port}/healthz")
    log(f"endpoint: POST http://{args.host}:{args.port}/github")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("shutting down")
    return 0


if __name__ == "__main__":
    sys.exit(main())
