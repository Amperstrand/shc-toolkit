from typing import Literal

VmStandbyResponseState = Literal["standby"]

VM_STANDBY_RESPONSE_STATE_VALUES: set[VmStandbyResponseState] = {
    "standby",
}


def check_vm_standby_response_state(value: str) -> VmStandbyResponseState:
    if value in VM_STANDBY_RESPONSE_STATE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_STANDBY_RESPONSE_STATE_VALUES!r}"
    )
