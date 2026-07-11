from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.error_error import ErrorError


T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """
    Attributes:
        error (ErrorError):
    """

    error: ErrorError

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_error import ErrorError

        d = dict(src_dict)
        error = ErrorError.from_dict(d.pop("error"))

        error = cls(
            error=error,
        )

        return error
