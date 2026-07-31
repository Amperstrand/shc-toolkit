from typing import Literal

GetVirtualMachineSnapshotRestoreHintsResponse200DataSource = Literal["snapshot"]

GET_VIRTUAL_MACHINE_SNAPSHOT_RESTORE_HINTS_RESPONSE_200_DATA_SOURCE_VALUES: set[
    GetVirtualMachineSnapshotRestoreHintsResponse200DataSource
] = {
    "snapshot",
}


def check_get_virtual_machine_snapshot_restore_hints_response_200_data_source(
    value: str,
) -> GetVirtualMachineSnapshotRestoreHintsResponse200DataSource:
    if (
        value
        in GET_VIRTUAL_MACHINE_SNAPSHOT_RESTORE_HINTS_RESPONSE_200_DATA_SOURCE_VALUES
    ):
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_VIRTUAL_MACHINE_SNAPSHOT_RESTORE_HINTS_RESPONSE_200_DATA_SOURCE_VALUES!r}"
    )
