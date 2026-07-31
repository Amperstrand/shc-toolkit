from typing import Literal

VmResumeResponseState = Literal["active"]

VM_RESUME_RESPONSE_STATE_VALUES: set[VmResumeResponseState] = {
    "active",
}


def check_vm_resume_response_state(value: str) -> VmResumeResponseState:
    if value in VM_RESUME_RESPONSE_STATE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_RESUME_RESPONSE_STATE_VALUES!r}"
    )
