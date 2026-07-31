from typing import Literal

VmBackupCreateRequestMode = Literal["snapshot", "stop", "suspend"]

VM_BACKUP_CREATE_REQUEST_MODE_VALUES: set[VmBackupCreateRequestMode] = {
    "snapshot",
    "stop",
    "suspend",
}


def check_vm_backup_create_request_mode(value: str) -> VmBackupCreateRequestMode:
    if value in VM_BACKUP_CREATE_REQUEST_MODE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_BACKUP_CREATE_REQUEST_MODE_VALUES!r}"
    )
