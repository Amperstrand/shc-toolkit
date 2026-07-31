from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="ClaimAgentKeyBody")


@_attrs_define
class ClaimAgentKeyBody:
    code: str
    """ The single-use claim code (base64url, 22-128 chars). Burned on success. """

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = d.pop("code")

        claim_agent_key_body = cls(
            code=code,
        )

        return claim_agent_key_body
