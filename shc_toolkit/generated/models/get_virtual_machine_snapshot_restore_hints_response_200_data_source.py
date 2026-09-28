from enum import StrEnum


class GetVirtualMachineSnapshotRestoreHintsResponse200DataSource(StrEnum):
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
