from typing import Literal

ZkBackupRegistrationConfigAlg = Literal["argon2id13"]

ZK_BACKUP_REGISTRATION_CONFIG_ALG_VALUES: set[ZkBackupRegistrationConfigAlg] = {
    "argon2id13",
}


def check_zk_backup_registration_config_alg(
    value: str,
) -> ZkBackupRegistrationConfigAlg:
    if value in ZK_BACKUP_REGISTRATION_CONFIG_ALG_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ZK_BACKUP_REGISTRATION_CONFIG_ALG_VALUES!r}"
    )
