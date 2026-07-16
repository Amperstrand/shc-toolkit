from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="UpdateNip05Body")


@_attrs_define
class UpdateNip05Body:
    """
    Attributes:
        nip05_name (float | str): Desired NIP-05 local name, lowercased by the handler and limited to a-z, 0-9, dot,
            hyphen, and underscore.
    """

    nip05_name: float | str

    def to_dict(self) -> dict[str, Any]:
        nip05_name: float | str
        nip05_name = self.nip05_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "nip05_name": nip05_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_nip05_name(data: object) -> float | str:
            return cast(float | str, data)

        nip05_name = _parse_nip05_name(d.pop("nip05_name"))

        update_nip_05_body = cls(
            nip05_name=nip05_name,
        )

        return update_nip_05_body
