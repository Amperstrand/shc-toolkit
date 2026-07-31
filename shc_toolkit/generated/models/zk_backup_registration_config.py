from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.zk_backup_registration_config_alg import (
    ZkBackupRegistrationConfigAlg,
    check_zk_backup_registration_config_alg,
)
from ..models.zk_backup_registration_config_ctx import (
    ZkBackupRegistrationConfigCtx,
    check_zk_backup_registration_config_ctx,
)
from ..models.zk_backup_registration_config_v import (
    ZkBackupRegistrationConfigV,
    check_zk_backup_registration_config_v,
)

T = TypeVar("T", bound="ZkBackupRegistrationConfig")


@_attrs_define
class ZkBackupRegistrationConfig:
    """Immutable per-service KDF config; salt is 16 client-random bytes (lowercase hex)."""

    v: ZkBackupRegistrationConfigV
    alg: ZkBackupRegistrationConfigAlg
    ctx: ZkBackupRegistrationConfigCtx
    ops: int
    """ argon2 opslimit (MODERATE) """
    mem: int
    """ argon2 memlimit bytes (MODERATE) """
    salt: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        v: int = self.v

        alg: str = self.alg

        ctx: str = self.ctx

        ops = self.ops

        mem = self.mem

        salt = self.salt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "v": v,
                "alg": alg,
                "ctx": ctx,
                "ops": ops,
                "mem": mem,
                "salt": salt,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        v = check_zk_backup_registration_config_v(d.pop("v"))

        alg = check_zk_backup_registration_config_alg(d.pop("alg"))

        ctx = check_zk_backup_registration_config_ctx(d.pop("ctx"))

        ops = d.pop("ops")

        mem = d.pop("mem")

        salt = d.pop("salt")

        zk_backup_registration_config = cls(
            v=v,
            alg=alg,
            ctx=ctx,
            ops=ops,
            mem=mem,
            salt=salt,
        )

        zk_backup_registration_config.additional_properties = d
        return zk_backup_registration_config

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
