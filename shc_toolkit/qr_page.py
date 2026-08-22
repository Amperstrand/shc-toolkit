"""One-shot localhost payment page: renders a Lightning invoice as an
inline-SVG QR (server-side, zero JS) plus a lightning: link and amount,
auto-opens the browser, and shuts down after `timeout` seconds.
"""
from __future__ import annotations

import base64
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_PAGE = """<!doctype html><html><head><meta charset="utf-8">
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
<div>Waiting for payment… this page closes itself when done or after timeout.</div>
</body></html>"""


def _qr_svg(data: str) -> str | None:
    try:
        import qrcode
        import qrcode.image.svg
    except ImportError:
        return None
    img = qrcode.make(data, image_factory=qrcode.image.svg.SvgPathImage,
                      box_size=12)
    import io
    buf = img.save_to_string() if hasattr(img, "save_to_string") else None
    if buf is None:
        s = io.BytesIO()  # lxml writes bytes, StringIO raises
        img.save(s)
        buf = s.getvalue()
    return buf if isinstance(buf, str) else buf.decode()


def serve_and_open(bolt11: str, *, amount_usd: float, timeout: int = 900,
                   open_browser: bool = True) -> None:
    svg = _qr_svg(f"lightning:{bolt11}")
    html = _PAGE.format(amount=amount_usd, svg=svg or "", bolt11=bolt11)
    done = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            done.set()

        def log_message(self, *a):
            pass

    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    url = f"http://127.0.0.1:{srv.server_address[1]}/"
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"payment page: {url}")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    time.sleep(min(timeout, 3600))
    srv.shutdown()
