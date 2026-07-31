from typing import Literal

ListVirtualMachineJobsStatus = Literal[
    "canceled", "completed", "failed", "pending", "running"
]

LIST_VIRTUAL_MACHINE_JOBS_STATUS_VALUES: set[ListVirtualMachineJobsStatus] = {
    "canceled",
    "completed",
    "failed",
    "pending",
    "running",
}


def check_list_virtual_machine_jobs_status(value: str) -> ListVirtualMachineJobsStatus:
    if value in LIST_VIRTUAL_MACHINE_JOBS_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_VIRTUAL_MACHINE_JOBS_STATUS_VALUES!r}"
    )
