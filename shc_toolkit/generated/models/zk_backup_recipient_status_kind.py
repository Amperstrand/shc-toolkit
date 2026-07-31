from typing import Literal

ZkBackupRecipientStatusKind = Literal[
    "btc",
    "other",
    "passkey",
    "password",
    "pgp",
    "pq-hybrid",
    "recovery-key",
    "secp256k1",
    "shamir",
    "ssh-ed25519",
]

ZK_BACKUP_RECIPIENT_STATUS_KIND_VALUES: set[ZkBackupRecipientStatusKind] = {
    "btc",
    "other",
    "passkey",
    "password",
    "pgp",
    "pq-hybrid",
    "recovery-key",
    "secp256k1",
    "shamir",
    "ssh-ed25519",
}


def check_zk_backup_recipient_status_kind(value: str) -> ZkBackupRecipientStatusKind:
    if value in ZK_BACKUP_RECIPIENT_STATUS_KIND_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ZK_BACKUP_RECIPIENT_STATUS_KIND_VALUES!r}"
    )
