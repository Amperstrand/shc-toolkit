from typing import Literal

VmResumeResponseLifecycleState = Literal["active"]

VM_RESUME_RESPONSE_LIFECYCLE_STATE_VALUES: set[VmResumeResponseLifecycleState] = {
    "active",
}


def check_vm_resume_response_lifecycle_state(
    value: str,
) -> VmResumeResponseLifecycleState:
    if value in VM_RESUME_RESPONSE_LIFECYCLE_STATE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_RESUME_RESPONSE_LIFECYCLE_STATE_VALUES!r}"
    )
