from enum import Enum


class RekeyVirtualMachineZkBackupBodyDestroyAck(str, Enum):
    DESTROY_MY_BACKUPS = "DESTROY-MY-BACKUPS"

    def __str__(self) -> str:
        return str(self.value)
