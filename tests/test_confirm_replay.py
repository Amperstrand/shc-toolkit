"""Reproduction: _confirmed_request auto-confirm replay diverges from the
server's confirmation contract (found live 2026-09-06 while ordering).

The SHC confirmation gate requires the resend to be byte-identical to the
gated request. Live evidence: a manual session.post(json=body, headers={...})
replay passes the gate, while _confirmed_request's replay re-triggers a fresh
409 (new request id) — its resend is NOT identical.
"""

import httpx
import pytest

from shc_toolkit.client import SHCClient


class _GateTransport(httpx.MockTransport):
    """Implements the SHC confirmation-gate contract.

    - First POST to /ordering/submit with this idempotency key: 409 with the
      confirmation_id in BOTH the prose text (as the live server does) and
      structuredContent.
    - A POST carrying X-User-Api-Confirm == the issued cid AND the identical
      body+idempotency key: 201.
    - A POST carrying a WRONG/stale cid, or a body that differs from the one
      the cid was issued for: fresh 409 (new cid) — the observed live
      behavior for non-identical replays.
    """

    def __init__(self):
        self.requests = []
        self._issued = {}  # idem_key -> (cid, body_bytes)
        self._n = 0
        super().__init__(self._handler)

    def _cid(self):
        self._n += 1
        return f"cnf_{self._n:032x}"

    def _handler(self, request: httpx.Request) -> httpx.Response:
        if request.url.path != "/user-api/v2/ordering/submit":
            return httpx.Response(404, json={"error": {"code": "not_found"}})

        body = request.content
        idem = request.headers.get("Idempotency-Key", "")
        confirm = request.headers.get("X-User-Api-Confirm", "")
        self.requests.append((idem, confirm, body))

        if confirm:
            rec = self._issued.get(idem)
            if rec and confirm == rec[0] and body == rec[1]:
                return httpx.Response(
                    201,
                    json={"data": {"submitted": True, "order": {"order_id": 1}}},
                )
            # non-identical or unknown confirm: fresh gate
            cid = self._cid()
            self._issued[idem] = (cid, body)
            return self._gate(cid)

        cid = self._cid()
        self._issued[idem] = (cid, body)
        return self._gate(cid)

    def _gate(self, cid: str) -> httpx.Response:
        return httpx.Response(
            409,
            json={
                "error": {
                    "code": "confirmation_required",
                    "message": (
                        "This action requires confirmation and was NOT performed. "
                        f"Re-send with header X-User-Api-Confirm: {cid}"
                    ),
                },
                "confirmation": {
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "STOP -- re-send the IDENTICAL request with header "
                                f"'X-User-Api-Confirm: {cid}' only after an explicit "
                                "human yes."
                            ),
                        }
                    ],
                    "isError": False,
                    "structuredContent": {"status": "confirmation_required"},
                },
            },
        )


@pytest.fixture()
def gated_client(monkeypatch):
    transport = _GateTransport()
    client = SHCClient(api_key="k" * 32)
    # swap the session while keeping the client's header defaults
    old = client.session
    client.session = httpx.Client(
        transport=transport,
        headers={"Authorization": old.headers.get("Authorization", "")},
        timeout=5.0,
    )
    client._transport = transport
    return client


def test_confirmed_request_replay_passes_gate(gated_client):
    """The auto-confirm resend must be identical: same body bytes, same
    idempotency key, cid header — and exactly TWO server hits (409 + 201)."""
    result = gated_client.submit_order(
        idempotency_key="order-repro-1",
        package_id=23,
        pricing_id=55,
        hostname="repro",
        check_credit=False,
    )
    assert result["submitted"] is True
    t = gated_client._transport
    assert len(t.requests) == 2, f"expected 2 requests, got {len(t.requests)}"
    idem1, conf1, body1 = t.requests[0]
    idem2, conf2, body2 = t.requests[1]
    assert idem1 == idem2 and body1 == body2, "replay must be identical"
    assert conf1 == "" and conf2.startswith("cnf_")


def test_prose_cid_is_extracted(gated_client):
    """The live server embeds the cid in prose text; extraction must find it
    even when structuredContent lacks a confirmation_id field."""
    import pytest as _pytest
    from shc_toolkit.client import SHCConfirmationRequiredError

    with _pytest.raises(SHCConfirmationRequiredError) as ei:
        gated_client._confirmed_request(
            "POST",
            "/ordering/submit",
            json={"package_id": 23, "pricing_id": 55, "hostname": "repro2"},
            confirm=False,
        )
    cid = getattr(ei.value, "confirmation_id", None)
    assert cid and cid.startswith("cnf_"), (
        f"cid not extracted from prose-only 409: cid={cid!r}"
    )
