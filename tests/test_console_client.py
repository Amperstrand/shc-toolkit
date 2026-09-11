"""Offline proof of the headless console client: a mock RFB server served
over WebSocket, consumed through console_client's shim + asyncvnc.

Proves the transport stack (websockets -> StreamReader/Writer shim ->
asyncvnc RFB handshake with VNC auth + framebuffer decode) without SHC's
bridge — isolating the live-blocked bridge as the only untested hop
(2026-09-11: the bridge accepts the bootstrap cookie but closes the socket
without RFB bytes for the tested VM; the browser page fails identically,
so it is server-side, not client-side).
"""

import zlib

import pytest

pytest.importorskip("websockets")
pytest.importorskip("asyncvnc")
pytest.importorskip("PIL")
pytest.importorskip("numpy")

import websockets

from shc_toolkit.console_client import _ws_opener

W, H = 4, 4


async def _rfb_server(ws):
    """Minimal RFB 3.8 server: VNC auth (type 2) + one raw framebuffer."""
    await ws.send(b"RFB 003.008\n")
    await ws.recv()  # client version
    await ws.send(b"\x02\x02\x01")  # 2 types: None(1), VNC(2)
    chosen = await ws.recv()
    assert isinstance(chosen, bytes)
    if chosen[0] == 2:  # VNC auth chosen (asyncvnc prefers 1 then 2)
        challenge = b"0123456789abcdef"
        await ws.send(challenge)
        await ws.recv()  # DES response (not verified)
        await ws.send(b"\x00\x00\x00\x00")  # auth OK
    else:
        await ws.send(b"\x00\x00\x00\x00")
    # ServerInit (after ClientInit share flag)
    await ws.recv()
    init = (
        W.to_bytes(2, "big")
        + H.to_bytes(2, "big")
        + bytes([32, 24, 0, 1])  # bpp, depth, little-endian, true colour
        + (255).to_bytes(2, "big") * 3
        + bytes([0, 8, 16, 0, 0, 0])  # rgb shifts + pad
    )
    name = b"mock"
    await ws.send(init + len(name).to_bytes(4, "big") + name)
    # pixel updates: respond to any update request (incl. set-pixel-format
    # and set-encodings messages are client->server; only act on type 3)
    while True:
        msg = await ws.recv()
        if not isinstance(msg, bytes) or not msg or msg[0] != 3:
            continue
        # FramebufferUpdate, the WHOLE message: [type 0][pad][numRects 1]
        # + one zlib rect: [x:2][y:2][w:2][h:2][enc=6:4][csize:4][zlib(pixels)]
        pixels = bytes([200, 40, 80, 255] * (W * H))
        comp = zlib.compress(pixels)
        update = (
            b"\x00\x00"
            + (1).to_bytes(2, "big")
            + (0).to_bytes(2, "big")
            + (0).to_bytes(2, "big")
            + W.to_bytes(2, "big")
            + H.to_bytes(2, "big")
            + (6).to_bytes(4, "big")
            + len(comp).to_bytes(4, "big")
            + comp
        )
        await ws.send(update)


@pytest.mark.asyncio
async def test_console_client_over_mock_rfb():
    async with websockets.serve(_rfb_server, "127.0.0.1", 8791):
        import asyncvnc

        opener = await _ws_opener("ws://127.0.0.1:8791", cookie="")
        async with asyncvnc.connect(
            "mock", 5900, password="vncpass", opener=opener
        ) as vnc:
            shot = await vnc.screenshot()
            assert shot is not None
            shape = getattr(shot, "shape", None)
            if shape is not None:  # RGBA ndarray
                assert shape[:2] == (H, W)
            else:  # PIL Image
                assert shot.size == (W, H)
