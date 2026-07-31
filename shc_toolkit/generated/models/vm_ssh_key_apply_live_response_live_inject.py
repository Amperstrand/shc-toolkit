from typing import Literal

VmSshKeyApplyLiveResponseLiveInject = Literal["attempted"]

VM_SSH_KEY_APPLY_LIVE_RESPONSE_LIVE_INJECT_VALUES: set[
    VmSshKeyApplyLiveResponseLiveInject
] = {
    "attempted",
}


def check_vm_ssh_key_apply_live_response_live_inject(
    value: str,
) -> VmSshKeyApplyLiveResponseLiveInject:
    if value in VM_SSH_KEY_APPLY_LIVE_RESPONSE_LIVE_INJECT_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_SSH_KEY_APPLY_LIVE_RESPONSE_LIVE_INJECT_VALUES!r}"
    )
