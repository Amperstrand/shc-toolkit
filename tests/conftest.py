import os
import time

import pytest

from shc_toolkit.client import SHCClient
from shc_toolkit import create_client

_created_service_ids = []


@pytest.fixture(scope="session")
def client():
    transport = os.environ.get("SHC_TEST_TRANSPORT", "rest")
    try:
        c = create_client(transport=transport)
    except (ValueError, ImportError) as e:
        pytest.skip(f"Cannot create {transport} client: {e}")
    try:
        c.get_account_balance()
    except Exception as e:
        pytest.skip(f"SHC API is not accessible via {transport}: {e}")
    return c


@pytest.fixture(scope="session")
def vm(client):
    try:
        result = client.submit_order(
            package_id=81, pricing_id=245, hostname="pytest-test-vm"
        )
    except Exception as e:
        pytest.skip(f"Failed to submit VM order: {e}")

    service_ids = result.get("service_ids", [])
    sid = (
        service_ids[0]
        if service_ids
        else result.get("service_id") or result.get("id")
    )
    if not sid:
        pytest.skip(f"No service_id in order response: {list(result.keys())}")

    sid = int(sid)
    _created_service_ids.append(sid)

    try:
        client._confirmed_request("POST", f"/vm/{sid}/cancel", json={})
    except Exception:
        pass

    deadline = time.time() + 300
    vm_data = None
    while time.time() < deadline:
        try:
            vm_data = client.get_vm(sid)
            prov = vm_data.get("provisioning_state", "")
            if prov == "ready":
                break
            if prov in ("failed", "error"):
                pytest.skip(f"VM provisioning failed: state={prov}")
        except Exception:
            pass
        time.sleep(5)

    if not vm_data or vm_data.get("provisioning_state") != "ready":
        pytest.skip(f"VM {sid} did not become ready within 300s")

    ips = vm_data.get("ips", [])
    ip = ips[0]["ip"] if ips else vm_data.get("ipv4") or vm_data.get("ip")
    hostname = vm_data.get("hostname", "pytest-test-vm")

    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
    if os.path.exists(ssh_key_path):
        try:
            with open(ssh_key_path) as f:
                pubkey = f.read().strip()
            if pubkey:
                client.apply_ssh_key_live(sid, pubkey)
        except Exception:
            pass

    return {"service_id": sid, "ip": ip, "hostname": hostname}


@pytest.fixture(scope="session", autouse=True)
def _cleanup_vms():
    yield
    try:
        c = SHCClient()
    except Exception:
        return
    for sid in list(_created_service_ids):
        try:
            c.cancel_vm(sid, immediate=True)
        except Exception:
            pass
