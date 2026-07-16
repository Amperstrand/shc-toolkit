from enum import Enum


class ZkBackupRecipientStatusKind(str, Enum):
    BTC = "btc"
    OTHER = "other"
    PASSKEY = "passkey"
    PASSWORD = "password"
    PGP = "pgp"
    PQ_HYBRID = "pq-hybrid"
    RECOVERY_KEY = "recovery-key"
    SECP256K1 = "secp256k1"
    SHAMIR = "shamir"
    SSH_ED25519 = "ssh-ed25519"

    def __str__(self) -> str:
        return str(self.value)
