from typing import Literal

VmOrderResultStatus = Literal["accepted", "canceled", "fraud", "pending"]

VM_ORDER_RESULT_STATUS_VALUES: set[VmOrderResultStatus] = {
    "accepted",
    "canceled",
    "fraud",
    "pending",
}


def check_vm_order_result_status(value: str) -> VmOrderResultStatus:
    if value in VM_ORDER_RESULT_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_ORDER_RESULT_STATUS_VALUES!r}"
    )
