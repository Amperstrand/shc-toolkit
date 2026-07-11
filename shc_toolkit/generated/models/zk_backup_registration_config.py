from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.zk_backup_registration_config_alg import ZkBackupRegistrationConfigAlg
from ..models.zk_backup_registration_config_ctx import ZkBackupRegistrationConfigCtx
from ..models.zk_backup_registration_config_v import ZkBackupRegistrationConfigV

T = TypeVar("T", bound="ZkBackupRegistrationConfig")


@_attrs_define
class ZkBackupRegistrationConfig:
    """Immutable per-service KDF config; salt is 16 client-random bytes (lowercase hex).

    Attributes:
        v (ZkBackupRegistrationConfigV):
        alg (ZkBackupRegistrationConfigAlg):
        ctx (ZkBackupRegistrationConfigCtx):
        ops (int): argon2 opslimit (MODERATE)
        mem (int): argon2 memlimit bytes (MODERATE)
        salt (str):
    """

    v: ZkBackupRegistrationConfigV
    alg: ZkBackupRegistrationConfigAlg
    ctx: ZkBackupRegistrationConfigCtx
    ops: int
    mem: int
    salt: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        v = self.v.value

        alg = self.alg.value

        ctx = self.ctx.value

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        v = ZkBackupRegistrationConfigV(d.pop("v"))

        alg = ZkBackupRegistrationConfigAlg(d.pop("alg"))

        ctx = ZkBackupRegistrationConfigCtx(d.pop("ctx"))

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
