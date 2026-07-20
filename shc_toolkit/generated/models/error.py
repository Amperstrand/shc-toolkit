from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.confirmation_challenge import ConfirmationChallenge
    from ..models.error_error import ErrorError


T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """
    Attributes:
        error (ErrorError):
        confirmation (ConfirmationChallenge | Unset): Present on a 409 whose error.code is `confirmation_required`. The
            action was NOT performed. Re-send the IDENTICAL request (same path, query, body and Idempotency-Key) with header
            `X-User-Api-Confirm: <confirmation_id>`. A confirmation_id is NOT permission: obtain an explicit human yes to
            THIS specific action first. The id is non-secret, single-use, and names an already-bound pending action.
    """

    error: ErrorError
    confirmation: ConfirmationChallenge | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        confirmation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.confirmation, Unset):
            confirmation = self.confirmation.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
            }
        )
        if confirmation is not UNSET:
            field_dict["confirmation"] = confirmation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.confirmation_challenge import ConfirmationChallenge
        from ..models.error_error import ErrorError

        d = dict(src_dict)
        error = ErrorError.from_dict(d.pop("error"))

        _confirmation = d.pop("confirmation", UNSET)
        confirmation: ConfirmationChallenge | Unset
        if isinstance(_confirmation, Unset):
            confirmation = UNSET
        else:
            confirmation = ConfirmationChallenge.from_dict(_confirmation)

        error = cls(
            error=error,
            confirmation=confirmation,
        )

        return error
