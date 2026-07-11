from enum import Enum


class GetVirtualMachineSnapshotRestoreHintsResponse200DataSource(str, Enum):
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
