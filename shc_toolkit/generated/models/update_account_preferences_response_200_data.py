from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.update_account_preferences_response_200_data_editable import (
        UpdateAccountPreferencesResponse200DataEditable,
    )


T = TypeVar("T", bound="UpdateAccountPreferencesResponse200Data")


@_attrs_define
class UpdateAccountPreferencesResponse200Data:
    """
    Attributes:
        language (None | str):  Example: en_us.
        default_currency (None | str):  Example: USD.
        inv_method (None | str):  Example: email.
        inv_address_to (None | str):  Example: 88.
        tax_id (None | str):
        receive_email_marketing (bool | None):  Example: True.
        autodebit (bool | None):  Example: True.
        editable (UpdateAccountPreferencesResponse200DataEditable):  Example: {'autodebit': True, 'inv_address_to':
            True, 'tax_id': False, 'default_currency': False, 'inv_method': False, 'language': False,
            'receive_email_marketing': True}.
    """

    language: None | str
    default_currency: None | str
    inv_method: None | str
    inv_address_to: None | str
    tax_id: None | str
    receive_email_marketing: bool | None
    autodebit: bool | None
    editable: UpdateAccountPreferencesResponse200DataEditable

    def to_dict(self) -> dict[str, Any]:
        language: None | str
        language = self.language

        default_currency: None | str
        default_currency = self.default_currency

        inv_method: None | str
        inv_method = self.inv_method

        inv_address_to: None | str
        inv_address_to = self.inv_address_to

        tax_id: None | str
        tax_id = self.tax_id

        receive_email_marketing: bool | None
        receive_email_marketing = self.receive_email_marketing

        autodebit: bool | None
        autodebit = self.autodebit

        editable = self.editable.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "language": language,
                "default_currency": default_currency,
                "inv_method": inv_method,
                "inv_address_to": inv_address_to,
                "tax_id": tax_id,
                "receive_email_marketing": receive_email_marketing,
                "autodebit": autodebit,
                "editable": editable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_account_preferences_response_200_data_editable import (
            UpdateAccountPreferencesResponse200DataEditable,
        )

        d = dict(src_dict)

        def _parse_language(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        language = _parse_language(d.pop("language"))

        def _parse_default_currency(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        default_currency = _parse_default_currency(d.pop("default_currency"))

        def _parse_inv_method(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        inv_method = _parse_inv_method(d.pop("inv_method"))

        def _parse_inv_address_to(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        inv_address_to = _parse_inv_address_to(d.pop("inv_address_to"))

        def _parse_tax_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        tax_id = _parse_tax_id(d.pop("tax_id"))

        def _parse_receive_email_marketing(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        receive_email_marketing = _parse_receive_email_marketing(
            d.pop("receive_email_marketing")
        )

        def _parse_autodebit(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        autodebit = _parse_autodebit(d.pop("autodebit"))

        editable = UpdateAccountPreferencesResponse200DataEditable.from_dict(
            d.pop("editable")
        )

        update_account_preferences_response_200_data = cls(
            language=language,
            default_currency=default_currency,
            inv_method=inv_method,
            inv_address_to=inv_address_to,
            tax_id=tax_id,
            receive_email_marketing=receive_email_marketing,
            autodebit=autodebit,
            editable=editable,
        )

        return update_account_preferences_response_200_data
