#!/usr/bin/env python3
"""Mint free testnet ecash from testnut.cashu.space.

The mint runs cdk-mintd with a FakeWallet — mint quotes auto-settle, so
NUT-04 (quote) + NUT-05 (blind mint) over electrum_ecc point math yields
a cashuA (v3) token at zero cost. cashu.email accepts ANY mint for its
100-sat send stamp, so a token from here sends real mail for free:

    python3 scripts/testnut_faucet.py 100 | xargs -I{} \
        shc mail --send-to you@example.com --subject hi --text hi --cashu-token {}

cdk-mintd specifics handled: quote state is {"state": "PAID"} (uppercase,
not a `paid` bool) and each BlindedMessage must carry the keyset `id`.
"""

import base64
import hashlib
import json
import secrets
import sys
import time

import httpx
from electrum_ecc import ECPubkey

MINT = "https://testnut.cashu.space"
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def hash_to_curve(secret: bytes) -> ECPubkey:
    e = hashlib.sha256(secret).digest()
    while True:
        try:
            return ECPubkey(b"\x02" + e)  # even-y per NUT-00
        except Exception:
            e = hashlib.sha256(e).digest()


def mint_token(amount_sats: int) -> str:
    c = httpx.Client(timeout=30)

    keys_resp = c.get(f"{MINT}/v1/keys").raise_for_status().json()
    ks = next(
        k
        for k in keys_resp["keysets"]
        if k.get("unit") == "sat" and k.get("active", True)
    )
    keyset_id = ks["id"]

    quote = (
        c.post(
            f"{MINT}/v1/mint/quote/bolt11", json={"amount": amount_sats, "unit": "sat"}
        )
        .raise_for_status()
        .json()
    )
    qid = quote["quote"]
    for _ in range(60):
        st = c.get(f"{MINT}/v1/mint/quote/bolt11/{qid}").raise_for_status().json()
        # cdk-mintd reports {"state": "PAID"} — NOT a lowercase `paid` bool
        # (the exact gotcha cashu.email's llms.txt documents)
        if st.get("state") == "PAID" or st.get("paid"):
            break
        time.sleep(2)
    else:
        raise RuntimeError(f"quote never paid: {st}")

    # amount split into powers of two, one blinded message each
    amounts, rest = [], amount_sats
    while rest:
        p = 1 << (rest.bit_length() - 1)
        amounts.append(p)
        rest -= p

    outputs, blindings = [], {}
    for a in amounts:
        secret = secrets.token_hex(16)
        P = hash_to_curve(secret.encode())
        r = secrets.randbelow(N - 1) + 1
        B_ = P * pow(r, -1, N)
        blindings[a] = (secret, r, P)
        outputs.append(
            {
                "amount": a,
                "id": keyset_id,
                "B_": B_.get_public_key_bytes(compressed=True).hex(),
            }
        )

    sigs = (
        c.post(f"{MINT}/v1/mint/bolt11", json={"quote": qid, "outputs": outputs})
        .raise_for_status()
        .json()["signatures"]
    )

    proofs = []
    for s in sigs:
        a = int(s["amount"])
        secret, r, P = blindings[a]
        C_ = ECPubkey(bytes.fromhex(s["C_"]))
        C = C_ * r
        assert C.get_public_key_bytes(compressed=True) != b"\x00"  # point exists
        proofs.append(
            {
                "amount": a,
                "secret": secret,
                "C": C.get_public_key_bytes(compressed=True).hex(),
            }
        )

    token = {
        "token": [{"mint": MINT, "proofs": proofs}],
        "unit": "sat",
        "memo": "shc-toolkit testnut faucet",
    }
    return "cashuA" + base64.b64encode(json.dumps(token).encode()).decode()


if __name__ == "__main__":
    amt = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(mint_token(amt))
