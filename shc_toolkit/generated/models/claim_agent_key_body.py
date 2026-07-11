from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ClaimAgentKeyBody")


@_attrs_define
class ClaimAgentKeyBody:
    """
    Attributes:
        code (str): The single-use claim code (base64url, 22-128 chars). Burned on success.
    """

    code: str

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        claim_agent_key_body = cls(
            code=code,
        )

        return claim_agent_key_body
