"""Localhost payment page: renders a Lightning invoice as an inline-SVG
QR (server-side, zero JS) plus a lightning: link and amount.

PaymentPage is UPDATABLE on a FIXED port: an invoice-reissue loop can
update(bolt11, amount) in place, and the page self-refreshes every 30s
so an already-open browser tab picks up the fresh invoice — the URL a
user is told about stays valid across reissues (live-earned 2026-08-22:
ephemeral ports per window made every printed pointer stale).
"""

from __future__ import annotations

import os
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DEFAULT_PORT = int(os.environ.get("SHC_PAY_PAGE_PORT", "8923"))

_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta http-equiv="refresh" content="30">
<title>SHC top-up</title>
<style>
 body{{font-family:system-ui,sans-serif;display:flex;flex-direction:column;
 align-items:center;background:#111;color:#eee;padding:2rem;gap:1rem}}
 .amt{{font-size:2rem;font-weight:700}}
 a.pay{{display:inline-block;background:#f7931a;color:#111;font-weight:700;
 padding:.9rem 2rem;border-radius:.6rem;text-decoration:none;font-size:1.1rem}}
 .uri{{font-size:.7rem;color:#888;word-break:break-all;max-width:34rem}}
</style></head><body>
<div class="amt">Top up ${amount:.2f}</div>
{svg}
<a class="pay" href="lightning:{bolt11}">Pay with Lightning</a>
<div class="uri">{bolt11}</div>
<div>Waiting for payment… page refreshes itself; it stops when the tool
exits.</div>
</body></html>"""


def _qr_svg(data: str) -> str | None:
    try:
        import qrcode
        import qrcode.image.svg
    except ImportError:
        return None
    img = qrcode.make(data, image_factory=qrcode.image.svg.SvgPathImage, box_size=12)
    import io

    buf = img.save_to_string() if hasattr(img, "save_to_string") else None
    if buf is None:
        s = io.BytesIO()  # lxml writes bytes, StringIO raises
        img.save(s)
        buf = s.getvalue()
    return buf if isinstance(buf, str) else buf.decode()


class PaymentPage:
    """Stable-port, updatable payment page served from a daemon thread."""

    def __init__(self, port: int = DEFAULT_PORT):
        self._lock = threading.Lock()
        self._html = b""
        page = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                with page._lock:
                    body = page._html
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *a):
                pass

        self._srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        self.port = self._srv.server_address[1]
        threading.Thread(target=self._srv.serve_forever, daemon=True).start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}/"

    def update(self, bolt11: str, amount_usd: float) -> None:
        svg = _qr_svg(f"lightning:{bolt11}")
        html = _PAGE.format(amount=amount_usd, svg=svg or "", bolt11=bolt11)
        with self._lock:
            self._html = html.encode()

    def close(self) -> None:
        self._srv.shutdown()


def serve_and_open(
    bolt11: str,
    *,
    amount_usd: float,
    timeout: int = 900,
    open_browser: bool = True,
    port: int = 0,
) -> None:
    """Back-compat one-shot: serve one invoice for `timeout` seconds."""
    page = PaymentPage(port=port)
    page.update(bolt11, amount_usd)
    print(f"payment page: {page.url}")
    if open_browser:
        try:
            webbrowser.open(page.url)
        except Exception:
            pass
    time.sleep(min(timeout, 3600))
    page.close()
