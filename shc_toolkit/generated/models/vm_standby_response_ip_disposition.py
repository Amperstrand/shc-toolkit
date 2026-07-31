from typing import Literal

VmStandbyResponseIpDisposition = Literal["kept", "released"]

VM_STANDBY_RESPONSE_IP_DISPOSITION_VALUES: set[VmStandbyResponseIpDisposition] = {
    "kept",
    "released",
}


def check_vm_standby_response_ip_disposition(
    value: str,
) -> VmStandbyResponseIpDisposition:
    if value in VM_STANDBY_RESPONSE_IP_DISPOSITION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_STANDBY_RESPONSE_IP_DISPOSITION_VALUES!r}"
    )
