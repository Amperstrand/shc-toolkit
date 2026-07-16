from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.zk_backup_recipient_status_kind import ZkBackupRecipientStatusKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ZkBackupRecipientStatus")


@_attrs_define
class ZkBackupRecipientStatus:
    """One public ZK backup recipient row in the verified recipient set. Public keys and fingerprints are owner-visible;
    private keys are never present.

        Attributes:
            kind (ZkBackupRecipientStatusKind):
            label (str):
            pubkey_x25519_hex (str):
            fingerprint (str):
            revoked (bool):
            created_at (datetime.datetime | None | Unset):
            revoked_at (datetime.datetime | None | Unset):
            pubkey_mlkem_hex (None | str | Unset):
            reader_id (None | str | Unset):
    """

    kind: ZkBackupRecipientStatusKind
    label: str
    pubkey_x25519_hex: str
    fingerprint: str
    revoked: bool
    created_at: datetime.datetime | None | Unset = UNSET
    revoked_at: datetime.datetime | None | Unset = UNSET
    pubkey_mlkem_hex: None | str | Unset = UNSET
    reader_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        label = self.label

        pubkey_x25519_hex = self.pubkey_x25519_hex

        fingerprint = self.fingerprint

        revoked = self.revoked

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        revoked_at: None | str | Unset
        if isinstance(self.revoked_at, Unset):
            revoked_at = UNSET
        elif isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        pubkey_mlkem_hex: None | str | Unset
        if isinstance(self.pubkey_mlkem_hex, Unset):
            pubkey_mlkem_hex = UNSET
        else:
            pubkey_mlkem_hex = self.pubkey_mlkem_hex

        reader_id: None | str | Unset
        if isinstance(self.reader_id, Unset):
            reader_id = UNSET
        else:
            reader_id = self.reader_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "label": label,
                "pubkey_x25519_hex": pubkey_x25519_hex,
                "fingerprint": fingerprint,
                "revoked": revoked,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if revoked_at is not UNSET:
            field_dict["revoked_at"] = revoked_at
        if pubkey_mlkem_hex is not UNSET:
            field_dict["pubkey_mlkem_hex"] = pubkey_mlkem_hex
        if reader_id is not UNSET:
            field_dict["reader_id"] = reader_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = ZkBackupRecipientStatusKind(d.pop("kind"))

        label = d.pop("label")

        pubkey_x25519_hex = d.pop("pubkey_x25519_hex")

        fingerprint = d.pop("fingerprint")

        revoked = d.pop("revoked")

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_revoked_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = datetime.datetime.fromisoformat(data)

                return revoked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        revoked_at = _parse_revoked_at(d.pop("revoked_at", UNSET))

        def _parse_pubkey_mlkem_hex(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pubkey_mlkem_hex = _parse_pubkey_mlkem_hex(d.pop("pubkey_mlkem_hex", UNSET))

        def _parse_reader_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reader_id = _parse_reader_id(d.pop("reader_id", UNSET))

        zk_backup_recipient_status = cls(
            kind=kind,
            label=label,
            pubkey_x25519_hex=pubkey_x25519_hex,
            fingerprint=fingerprint,
            revoked=revoked,
            created_at=created_at,
            revoked_at=revoked_at,
            pubkey_mlkem_hex=pubkey_mlkem_hex,
            reader_id=reader_id,
        )

        return zk_backup_recipient_status
