from enum import StrEnum


class ZkBackupRegistrationConfigAlg(StrEnum):
    ARGON2ID13 = "argon2id13"

    def __str__(self) -> str:
        return str(self.value)
