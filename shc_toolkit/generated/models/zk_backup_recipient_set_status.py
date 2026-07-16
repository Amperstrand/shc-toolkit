from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.zk_backup_recipient_status import ZkBackupRecipientStatus


T = TypeVar("T", bound="ZkBackupRecipientSetStatus")


@_attrs_define
class ZkBackupRecipientSetStatus:
    """Verified owner-visible ZK backup recipient set, including revoked recipients. SHC ZK backup is genuine self-custody,
    the same model as Bitcoin: your keys, your data. Backups already sealed to a recovery key stay openable by that key
    until you rotate forward and re-upload the backups you care about; that is the sovereignty property. If a recovery
    key is exposed, register a fresh recipient set and re-upload replacement backups, like sweeping a Bitcoin key to a
    fresh address. SHC cannot re-seal, claw back, or reach into existing backup data; that inability is the guarantee.

        Attributes:
            zk_enabled (bool):
            revocation_guarantee (str):  Example: SHC ZK backup is genuine self-custody, the same model as Bitcoin: your
                keys, your data. Backups already sealed to a recovery key stay openable by that key until you rotate forward and
                re-upload the backups you care about; that is the sovereignty property. If a recovery key is exposed, register a
                fresh recipient set and re-upload replacement backups, like sweeping a Bitcoin key to a fresh address. SHC
                cannot re-seal, claw back, or reach into existing backup data; that inability is the guarantee..
            recipients (list[ZkBackupRecipientStatus]):
            generation (int | None | Unset):
            config_hash (None | str | Unset):
            recipient_set_hash (None | str | Unset):
            active_seal_digest (None | str | Unset):
    """

    zk_enabled: bool
    revocation_guarantee: str
    recipients: list[ZkBackupRecipientStatus]
    generation: int | None | Unset = UNSET
    config_hash: None | str | Unset = UNSET
    recipient_set_hash: None | str | Unset = UNSET
    active_seal_digest: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        zk_enabled = self.zk_enabled

        revocation_guarantee = self.revocation_guarantee

        recipients = []
        for recipients_item_data in self.recipients:
            recipients_item = recipients_item_data.to_dict()
            recipients.append(recipients_item)

        generation: int | None | Unset
        if isinstance(self.generation, Unset):
            generation = UNSET
        else:
            generation = self.generation

        config_hash: None | str | Unset
        if isinstance(self.config_hash, Unset):
            config_hash = UNSET
        else:
            config_hash = self.config_hash

        recipient_set_hash: None | str | Unset
        if isinstance(self.recipient_set_hash, Unset):
            recipient_set_hash = UNSET
        else:
            recipient_set_hash = self.recipient_set_hash

        active_seal_digest: None | str | Unset
        if isinstance(self.active_seal_digest, Unset):
            active_seal_digest = UNSET
        else:
            active_seal_digest = self.active_seal_digest

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "zk_enabled": zk_enabled,
                "revocation_guarantee": revocation_guarantee,
                "recipients": recipients,
            }
        )
        if generation is not UNSET:
            field_dict["generation"] = generation
        if config_hash is not UNSET:
            field_dict["config_hash"] = config_hash
        if recipient_set_hash is not UNSET:
            field_dict["recipient_set_hash"] = recipient_set_hash
        if active_seal_digest is not UNSET:
            field_dict["active_seal_digest"] = active_seal_digest

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.zk_backup_recipient_status import ZkBackupRecipientStatus

        d = dict(src_dict)
        zk_enabled = d.pop("zk_enabled")

        revocation_guarantee = d.pop("revocation_guarantee")

        recipients = []
        _recipients = d.pop("recipients")
        for recipients_item_data in _recipients:
            recipients_item = ZkBackupRecipientStatus.from_dict(recipients_item_data)

            recipients.append(recipients_item)

        def _parse_generation(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        generation = _parse_generation(d.pop("generation", UNSET))

        def _parse_config_hash(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        config_hash = _parse_config_hash(d.pop("config_hash", UNSET))

        def _parse_recipient_set_hash(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recipient_set_hash = _parse_recipient_set_hash(
            d.pop("recipient_set_hash", UNSET)
        )

        def _parse_active_seal_digest(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        active_seal_digest = _parse_active_seal_digest(
            d.pop("active_seal_digest", UNSET)
        )

        zk_backup_recipient_set_status = cls(
            zk_enabled=zk_enabled,
            revocation_guarantee=revocation_guarantee,
            recipients=recipients,
            generation=generation,
            config_hash=config_hash,
            recipient_set_hash=recipient_set_hash,
            active_seal_digest=active_seal_digest,
        )

        return zk_backup_recipient_set_status
