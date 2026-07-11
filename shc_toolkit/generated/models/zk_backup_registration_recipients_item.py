from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.zk_backup_registration_recipients_item_kind import (
    ZkBackupRegistrationRecipientsItemKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ZkBackupRegistrationRecipientsItem")


@_attrs_define
class ZkBackupRegistrationRecipientsItem:
    """
    Attributes:
        kind (ZkBackupRegistrationRecipientsItemKind): How this recipient's X25519 public key was derived — what the
            customer holds to unlock a restore (five-rung recovery model; any one recipient suffices): `password` — a
            passphrase (argon2id-derived key). `recovery-key` — a generated high-entropy recovery code the customer stored.
            `passkey` — a FIDO2 passkey using the PRF extension. `shamir` — one share-set of a split secret (threshold
            recovery). `ssh-ed25519` — an existing Ed25519 SSH key (converted). `secp256k1` — a secp256k1 key such as a
            Nostr identity (the input alias `nostr` is accepted and normalized to `secp256k1`). `pgp` — an OpenPGP key.
            `btc` — a Bitcoin key. `other` — any other X25519-capable material the customer manages.
        pubkey (str): X25519 public key (hex); private key never leaves the client.
        label (str | Unset):
    """

    kind: ZkBackupRegistrationRecipientsItemKind
    pubkey: str
    label: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        pubkey = self.pubkey

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "pubkey": pubkey,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = ZkBackupRegistrationRecipientsItemKind(d.pop("kind"))

        pubkey = d.pop("pubkey")

        label = d.pop("label", UNSET)

        zk_backup_registration_recipients_item = cls(
            kind=kind,
            pubkey=pubkey,
            label=label,
        )

        zk_backup_registration_recipients_item.additional_properties = d
        return zk_backup_registration_recipients_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
