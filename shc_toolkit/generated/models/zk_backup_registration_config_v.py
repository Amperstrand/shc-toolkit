from typing import Literal

ZkBackupRegistrationConfigV = Literal[1]

ZK_BACKUP_REGISTRATION_CONFIG_V_VALUES: set[ZkBackupRegistrationConfigV] = {
    1,
}


def check_zk_backup_registration_config_v(value: int) -> ZkBackupRegistrationConfigV:
    if value in ZK_BACKUP_REGISTRATION_CONFIG_V_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ZK_BACKUP_REGISTRATION_CONFIG_V_VALUES!r}"
    )
