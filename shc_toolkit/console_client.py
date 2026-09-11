"""Headless Blesta console client — VM screen + keyboard without SSH or a
browser.

Reverses SHC's ``proxmoxbridge`` (2026-09-11): the noVNC web page does
exactly two things a Python program can do itself —

1. ``POST /proxmoxbridge/console/bootstrap`` with ``{"token": <JWT>}``
   (the JWT comes from ``SHCClient.create_console_session``) →
   ``{"ws_url": "wss://…", "vnc_password": "…"}``
2. speak RFB (VNC) over that WebSocket, authenticating with the returned
   password.

``asyncvnc`` implements RFB with an injectable transport (``opener=``), so
a WebSocket wrapped in ``asyncio.StreamReader``/``StreamWriter`` shims is
the entire bridge — no Playwright, no browser, no portal login.

The console is hypervisor-side: it works even when the guest's network is
broken (the dev-zone boxes SSH can't reach) as long as the VM is registered
with the management plane.

Requires the ``console`` extra: ``pip install shc-toolkit[console]``.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from .client import SHCClient

log = logging.getLogger(__name__)

BOOTSTRAP_PATH = "/proxmoxbridge/console/bootstrap"


async def bootstrap_console(token: str, base_url: str) -> tuple[str, str, str]:
    """Exchange the single-use console JWT for (ws_url, vnc_password, cookie).

    The bootstrap may return a relative ws path (the web page resolves it
    against its origin with wss:) — do the same here. Any Set-Cookie must
    ride the WebSocket upgrade ("Missing bridge session" without it).
    """
    api_origin = base_url.split("/user-api")[0]
    async with httpx.AsyncClient(timeout=30) as http:
        r = await http.post(
            f"{api_origin}{BOOTSTRAP_PATH}",
            json={"token": token},
            headers={"Content-Type": "application/json"},
        )
    if r.status_code != 200:
        raise RuntimeError(
            f"console bootstrap failed ({r.status_code}): {r.text[:200]}"
        )
    payload = r.json()
    ws_url = str(payload.get("ws_url") or "")
    vnc_password = str(payload.get("vnc_password") or "")
    if ws_url.startswith("/"):
        scheme = "wss" if api_origin.startswith("https") else "ws"
        ws_url = scheme + "://" + api_origin.split("://", 1)[1] + ws_url
    cookie = "; ".join(f"{k}={v}" for k, v in r.cookies.items())
    if not ws_url or not vnc_password:
        raise RuntimeError(f"bootstrap incomplete: {payload!r}")
    return ws_url, vnc_password, cookie


class _WebSocketWriterShim:
    """asyncio.StreamWriter-compatible facade over a websockets connection.

    asyncvnc only uses write()/close()/wait_closed(); write() is sync, so
    bytes go through a queue drained by an ordered sender task — VNC is a
    byte stream, and key events are two write() calls that must stay in
    order.
    """

    def __init__(self, ws: Any, loop: asyncio.AbstractEventLoop):
        self._ws = ws
        self._loop = loop
        self._queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._closed = asyncio.Event()
        self._drain = loop.create_task(self._drain_loop())

    async def _drain_loop(self) -> None:
        while True:
            data = await self._queue.get()
            if data is None:
                return
            try:
                await self._ws.send(data)
            except Exception as e:  # connection closed mid-send
                log.debug("console ws send failed: %s", e)
                return

    def write(self, data: bytes) -> None:
        if not self._closed.is_set():
            self._queue.put_nowait(bytes(data))

    def close(self) -> None:
        self._queue.put_nowait(None)  # type: ignore[arg-type]

    async def wait_closed(self) -> None:
        self._queue.put_nowait(None)  # type: ignore[arg-type]
        await self._drain
        try:
            await self._ws.close()
        except Exception:
            pass
        self._closed.set()


async def _ws_opener(ws_url: str, cookie: str = ""):
    """opener(host, port) -> (reader, writer) over a WebSocket connection."""

    async def _open(_host: str, _port: int):
        import websockets

        headers = {"Cookie": cookie} if cookie else {}
        ws = await websockets.connect(
            ws_url, max_size=None, ping_interval=20, extra_headers=headers
        )
        loop = asyncio.get_running_loop()
        reader: asyncio.StreamReader = asyncio.StreamReader(limit=2**24)

        async def _pump() -> None:
            try:
                async for message in ws:
                    reader.feed_data(
                        message if isinstance(message, bytes) else message.encode()
                    )
            except Exception as e:  # closed
                log.debug("console ws pump ended: %s", e)
            finally:
                reader.feed_eof()

        loop.create_task(_pump())
        return reader, _WebSocketWriterShim(ws, loop)

    return _open


async def open_console(client: SHCClient, service_id: int, *, ttl: int = 60) -> Any:
    """Async context manager: a connected asyncvnc Client for the VM console.

    Usage::

        async with await open_console(c, 2542) as vnc:
            await vnc.screenshot(...)  # asyncvnc API
    """
    import asyncvnc

    session = client.create_console_session(service_id, ttl=ttl)
    token = (session.get("data", session) or {}).get("console_url", "")
    token = token.split("#token=")[-1].strip()
    if not token or token == session.get("data", session).__str__():
        raise RuntimeError(f"no console token for {service_id}: {session!r}")
    ws_url, vnc_password, cookie = await bootstrap_console(token, client.base_url)

    opener = await _ws_opener(ws_url, cookie)
    reader, writer = await opener("console", 0)
    vnc = await asyncvnc.Client.create(reader, writer, password=vnc_password)

    class _Ctx:
        async def __aenter__(self):
            return vnc

        async def __aexit__(self, *exc):
            writer.close()
            await writer.wait_closed()

    return _Ctx()


def screenshot(client: SHCClient, service_id: int, path: str, *, ttl: int = 60) -> str:
    """Capture the VM's console screen to a PNG file (sync facade)."""

    async def _run() -> None:
        async with await open_console(client, service_id, ttl=ttl) as vnc:
            vnc.video.refresh()
            shot = await vnc.screenshot()
            if hasattr(shot, "save"):  # PIL Image
                shot.save(path)
            else:  # asyncvnc may hand back an RGBA ndarray
                from PIL import Image

                Image.fromarray(shot).save(path)

    asyncio.run(_run())
    return path


def type_text(
    client: SHCClient, service_id: int, text: str, *, ttl: int = 60, enter: bool = False
) -> None:
    """Type text into the VM's console (sync facade). Types literally; the
    guest sees it on whatever screen it is showing (login prompt, shell,
    editor...)."""

    async def _run() -> None:
        async with await open_console(client, service_id, ttl=ttl) as vnc:
            vnc.keyboard.write(text)
            if enter:
                vnc.keyboard.press("Return")

    asyncio.run(_run())


def console_command(
    client: SHCClient,
    service_id: int,
    command: str,
    *,
    login_user: str | None = None,
    login_password: str | None = None,
    settle: float = 3.0,
    ttl: int = 120,
) -> tuple[str, str]:
    """Run a command on the VM's console and capture before/after screens.

    The SSH-free control plane (live-proven 2026-09-11): logs in via the
    console if credentials are given (requires a cloud-init-set root
    password), types the command, waits, and captures screenshots of the
    output. Returns (pre_screenshot_path, post_screenshot_path) — the
    screenshots ARE the output (VNC gives you the screen, not stdout).

    If login_user is None, assumes the console is already at a shell prompt
    (a previous console_command session leaves it logged in).
    """
    import tempfile

    async def _run() -> tuple[str, str]:
        async with await open_console(client, service_id, ttl=ttl) as vnc:
            pre = tempfile.mktemp(suffix=".png", prefix="console-pre-")
            post = tempfile.mktemp(suffix=".png", prefix="console-post-")

            def _save(shot: Any, path: str) -> None:
                if hasattr(shot, "save"):
                    shot.save(path)
                else:
                    from PIL import Image

                    Image.fromarray(shot).save(path)

            if login_user and login_password:
                vnc.keyboard.press("Return")
                await asyncio.sleep(1.5)
                vnc.keyboard.write(login_user)
                vnc.keyboard.press("Return")
                await asyncio.sleep(settle)
                vnc.keyboard.write(login_password)
                vnc.keyboard.press("Return")
                await asyncio.sleep(settle)

            vnc.video.refresh()
            _save(await vnc.screenshot(), pre)

            vnc.keyboard.write(command)
            vnc.keyboard.press("Return")
            await asyncio.sleep(settle)
            vnc.video.refresh()
            _save(await vnc.screenshot(), post)
            return pre, post

    return asyncio.run(_run())
