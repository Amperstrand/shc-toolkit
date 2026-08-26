"""Live integration test for the nostr operate-lane (agent side).

Exercises the real plugin endpoint end-to-end: a customer-signed
kind:30078 grant is exchanged for a vm-scoped operate lease, the lease
reads the granted VM, and other-service + spend paths 403.

Requirements (skipped otherwise):
- ``SHC_OPERATE_LIVE``: name of a context in ``~/.config/shc/contexts/``
  whose account OWNS at least one VM and whose nsec is linked to the
  account (register-created contexts satisfy both).

Run: ``SHC_OPERATE_LIVE=eddy-e2e pytest tests/test_nostr_operate_lane.py -v``
"""

import json
import os
import time

import pytest

from shc_toolkit.client import SHCAuthError, SHCClient, SHCError
from shc_toolkit.register import load_context

pytestmark = pytest.mark.skipif(
    not os.environ.get("SHC_OPERATE_LIVE"),
    reason="SHC_OPERATE_LIVE (context name owning a VM) not set",
)

AUD = "shc:https://blesta.sovereignhybridcompute.com"


def _make_grant(customer_keys, agent_pub_hex: str, service_id: int, ttl: int = 900) -> dict:
    from nostr_sdk import EventBuilder, Kind, Tag

    now = int(time.time())
    event = (
        EventBuilder(Kind(30078), "")
        .tags(
            [
                Tag.parse(["d", f"shc:agent:{agent_pub_hex}"]),
                Tag.parse(["scope", "operate"]),
                Tag.parse(["area", f"vm:{service_id}"]),
                Tag.parse(["aud", AUD]),
                Tag.parse(["nbf", str(now)]),
                Tag.parse(["exp", str(now + ttl)]),
            ]
        )
        .sign_with_keys(customer_keys)
    )
    return json.loads(event.as_json())


@pytest.mark.allow_network
def test_operate_lane_grant_to_lease():
    from nostr_sdk import Keys

    from shc_toolkit.client import exchange_nostr_operate_grant, validate_operate_grant

    ctx = load_context(os.environ["SHC_OPERATE_LIVE"])
    assert ctx and ctx.get("nsec"), "context must carry an nsec"

    customer = SHCClient(api_key=ctx["api_key"])
    vms = customer.list_vms()
    assert vms, "context account must own at least one VM for this test"
    service_id = int(vms[0].get("service_id") or vms[0].get("id"))

    agent = Keys.generate()
    grant = _make_grant(customer_keys=Keys.parse(ctx["nsec"]),
                        agent_pub_hex=agent.public_key().to_hex(), service_id=service_id)
    assert validate_operate_grant(grant, expected_aud=AUD) == []

    lease = exchange_nostr_operate_grant(grant, nsec=agent.secret_key().to_bech32())
    assert lease["scope"] == "operate"
    assert lease["area"] == f"vm:{service_id}"
    assert len(lease["token"]) == 64

    vmc = SHCClient(api_key=lease["token"])
    vm = vmc.get_vm(service_id)
    assert vm.get("service_id") or vm.get("id")

    with pytest.raises(SHCError):
        vmc.get_vm(service_id + 1)

    with pytest.raises((SHCError, SHCAuthError)):
        vmc.topup_credit("1.00")
