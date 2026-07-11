from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountPreferencesUpdateRequest")


@_attrs_define
class AccountPreferencesUpdateRequest:
    """Update self-scoped, company-editable client preferences. PATCH semantics: only the keys present are changed; at
    least one field is required. Only fields the company has flagged editable (see GET /account/preferences `editable`)
    may be changed. `autodebit` is not writable through this API.

        Example:
            {'inv_method': 'email', 'receive_email_marketing': False}

        Attributes:
            language (str | Unset): Language code (e.g. en_us). Example: en_us.
            default_currency (str | Unset): 3-letter ISO-4217 currency code. Example: USD.
            inv_method (str | Unset): Invoice delivery method. Example: email.
            inv_address_to (int | str | Unset): Contact id to address invoices to (must be one of this client's contacts).
                Example: 88.
            tax_id (None | str | Unset): Tax id / VAT number. Example: GB123456789.
            receive_email_marketing (bool | Unset): Whether to receive marketing email. Example: True.
    """

    language: str | Unset = UNSET
    default_currency: str | Unset = UNSET
    inv_method: str | Unset = UNSET
    inv_address_to: int | str | Unset = UNSET
    tax_id: None | str | Unset = UNSET
    receive_email_marketing: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        language = self.language

        default_currency = self.default_currency

        inv_method = self.inv_method

        inv_address_to: int | str | Unset
        if isinstance(self.inv_address_to, Unset):
            inv_address_to = UNSET
        else:
            inv_address_to = self.inv_address_to

        tax_id: None | str | Unset
        if isinstance(self.tax_id, Unset):
            tax_id = UNSET
        else:
            tax_id = self.tax_id

        receive_email_marketing = self.receive_email_marketing

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if language is not UNSET:
            field_dict["language"] = language
        if default_currency is not UNSET:
            field_dict["default_currency"] = default_currency
        if inv_method is not UNSET:
            field_dict["inv_method"] = inv_method
        if inv_address_to is not UNSET:
            field_dict["inv_address_to"] = inv_address_to
        if tax_id is not UNSET:
            field_dict["tax_id"] = tax_id
        if receive_email_marketing is not UNSET:
            field_dict["receive_email_marketing"] = receive_email_marketing

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        language = d.pop("language", UNSET)

        default_currency = d.pop("default_currency", UNSET)

        inv_method = d.pop("inv_method", UNSET)

        def _parse_inv_address_to(data: object) -> int | str | Unset:
            if isinstance(data, Unset):
                return data
            return cast(int | str | Unset, data)

        inv_address_to = _parse_inv_address_to(d.pop("inv_address_to", UNSET))

        def _parse_tax_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tax_id = _parse_tax_id(d.pop("tax_id", UNSET))

        receive_email_marketing = d.pop("receive_email_marketing", UNSET)

        account_preferences_update_request = cls(
            language=language,
            default_currency=default_currency,
            inv_method=inv_method,
            inv_address_to=inv_address_to,
            tax_id=tax_id,
            receive_email_marketing=receive_email_marketing,
        )

        return account_preferences_update_request
