from typing import Literal

ZkBackupRegistrationConfigCtx = Literal["shc-vps-backup-v1"]

ZK_BACKUP_REGISTRATION_CONFIG_CTX_VALUES: set[ZkBackupRegistrationConfigCtx] = {
    "shc-vps-backup-v1",
}


def check_zk_backup_registration_config_ctx(
    value: str,
) -> ZkBackupRegistrationConfigCtx:
    if value in ZK_BACKUP_REGISTRATION_CONFIG_CTX_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ZK_BACKUP_REGISTRATION_CONFIG_CTX_VALUES!r}"
    )
