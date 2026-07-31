from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="ChangeVirtualMachineTermBody")


@_attrs_define
class ChangeVirtualMachineTermBody:
    pricing_id: int | str
    """ Required target package_pricing ID for the new term. """
    idempotency_key: str
    """ Replay key required by the live route body idempotency gate. """

    def to_dict(self) -> dict[str, Any]:
        pricing_id: int | str
        pricing_id = self.pricing_id

        idempotency_key = self.idempotency_key

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "pricing_id": pricing_id,
                "idempotency_key": idempotency_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_pricing_id(data: object) -> int | str:
            return cast(int | str, data)

        pricing_id = _parse_pricing_id(d.pop("pricing_id"))

        idempotency_key = d.pop("idempotency_key")

        change_virtual_machine_term_body = cls(
            pricing_id=pricing_id,
            idempotency_key=idempotency_key,
        )

        return change_virtual_machine_term_body
