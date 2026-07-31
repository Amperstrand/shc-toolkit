from typing import Literal

GetVirtualMachineBackupRestoreHintsResponse200DataSource = Literal["backup"]

GET_VIRTUAL_MACHINE_BACKUP_RESTORE_HINTS_RESPONSE_200_DATA_SOURCE_VALUES: set[
    GetVirtualMachineBackupRestoreHintsResponse200DataSource
] = {
    "backup",
}


def check_get_virtual_machine_backup_restore_hints_response_200_data_source(
    value: str,
) -> GetVirtualMachineBackupRestoreHintsResponse200DataSource:
    if (
        value
        in GET_VIRTUAL_MACHINE_BACKUP_RESTORE_HINTS_RESPONSE_200_DATA_SOURCE_VALUES
    ):
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_VIRTUAL_MACHINE_BACKUP_RESTORE_HINTS_RESPONSE_200_DATA_SOURCE_VALUES!r}"
    )
