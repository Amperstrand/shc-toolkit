from typing import Literal

ListVirtualMachineJobsType = Literal[
    "backup", "provision", "reinstall", "restore", "snapshot"
]

LIST_VIRTUAL_MACHINE_JOBS_TYPE_VALUES: set[ListVirtualMachineJobsType] = {
    "backup",
    "provision",
    "reinstall",
    "restore",
    "snapshot",
}


def check_list_virtual_machine_jobs_type(value: str) -> ListVirtualMachineJobsType:
    if value in LIST_VIRTUAL_MACHINE_JOBS_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_VIRTUAL_MACHINE_JOBS_TYPE_VALUES!r}"
    )
