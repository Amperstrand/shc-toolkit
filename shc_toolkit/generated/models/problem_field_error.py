from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.problem_field_error_type import (
    ProblemFieldErrorType,
    check_problem_field_error_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProblemFieldError")


@_attrs_define
class ProblemFieldError:
    """Typed FIELD error. Every entry names the offending request field."""

    type_: ProblemFieldErrorType
    field: str
    """ Offending field path using body/query/header/path prefixes. """
    code: str
    detail: str
    hint: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        field = self.field

        code = self.code

        detail = self.detail

        hint = self.hint

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "field": field,
                "code": code,
                "detail": detail,
            }
        )
        if hint is not UNSET:
            field_dict["hint"] = hint

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = check_problem_field_error_type(d.pop("type"))

        field = d.pop("field")

        code = d.pop("code")

        detail = d.pop("detail")

        hint = d.pop("hint", UNSET)

        problem_field_error = cls(
            type_=type_,
            field=field,
            code=code,
            detail=detail,
            hint=hint,
        )

        return problem_field_error
