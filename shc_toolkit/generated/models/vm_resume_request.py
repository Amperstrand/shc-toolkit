from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="VmResumeRequest")


@_attrs_define
class VmResumeRequest:
    """Optional empty JSON object. A bodyless request is also accepted by the live handler."""

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        vm_resume_request = cls()

        return vm_resume_request
