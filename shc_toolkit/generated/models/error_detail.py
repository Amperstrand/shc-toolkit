from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.error_detail_code import ErrorDetailCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorDetail")


@_attrs_define
class ErrorDetail:
    """Field-level validation issue.

    Attributes:
        field (str):  Example: hostname.
        issue (str):  Example: Hostname is already in use.
        code (ErrorDetailCode | Unset): Stable, machine-branchable issue code for this field. Optional; present only on
            validation branches that classify the problem. Distinct from the top-level error.code. Example: already_in_use.
        hint (str | Unset): Optional human/agent-facing remediation hint for this specific field (e.g. "Pick a different
            hostname or omit it to auto-generate."). Example: Pick a different hostname or omit it to auto-generate..
    """

    field: str
    issue: str
    code: ErrorDetailCode | Unset = UNSET
    hint: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        issue = self.issue

        code: str | Unset = UNSET
        if not isinstance(self.code, Unset):
            code = self.code.value

        hint = self.hint

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "field": field,
                "issue": issue,
            }
        )
        if code is not UNSET:
            field_dict["code"] = code
        if hint is not UNSET:
            field_dict["hint"] = hint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field")

        issue = d.pop("issue")

        _code = d.pop("code", UNSET)
        code: ErrorDetailCode | Unset
        if isinstance(_code, Unset):
            code = UNSET
        else:
            code = ErrorDetailCode(_code)

        hint = d.pop("hint", UNSET)

        error_detail = cls(
            field=field,
            issue=issue,
            code=code,
            hint=hint,
        )

        return error_detail
