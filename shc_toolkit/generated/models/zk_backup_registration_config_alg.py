from enum import Enum


class ZkBackupRegistrationConfigAlg(str, Enum):
    ARGON2ID13 = "argon2id13"

    def __str__(self) -> str:
        return str(self.value)
