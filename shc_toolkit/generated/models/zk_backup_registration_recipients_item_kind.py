from typing import Literal

ZkBackupRegistrationRecipientsItemKind = Literal[
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

ZK_BACKUP_REGISTRATION_RECIPIENTS_ITEM_KIND_VALUES: set[
    ZkBackupRegistrationRecipientsItemKind
] = {
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


def check_zk_backup_registration_recipients_item_kind(
    value: str,
) -> ZkBackupRegistrationRecipientsItemKind:
    if value in ZK_BACKUP_REGISTRATION_RECIPIENTS_ITEM_KIND_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ZK_BACKUP_REGISTRATION_RECIPIENTS_ITEM_KIND_VALUES!r}"
    )
