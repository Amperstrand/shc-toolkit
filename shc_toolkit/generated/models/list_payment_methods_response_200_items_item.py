from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.list_payment_methods_response_200_items_item_status import (
    ListPaymentMethodsResponse200ItemsItemStatus,
    check_list_payment_methods_response_200_items_item_status,
)
from ..models.list_payment_methods_response_200_items_item_type import (
    ListPaymentMethodsResponse200ItemsItemType,
    check_list_payment_methods_response_200_items_item_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListPaymentMethodsResponse200ItemsItem")


@_attrs_define
class ListPaymentMethodsResponse200ItemsItem:
    id: int
    type_: ListPaymentMethodsResponse200ItemsItemType
    account_type: str
    """ Card brand (visa, mc, amex, ...) for cc, or checking/savings for ach. """
    last4: None | str
    contact_id: int
    status: ListPaymentMethodsResponse200ItemsItemStatus
    expiration: None | str | Unset = UNSET
    """ Card expiration (cc only), masked/encrypted-at-rest source. """
    name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str = self.type_

        account_type = self.account_type

        last4: None | str
        last4 = self.last4

        contact_id = self.contact_id

        status: str = self.status

        expiration: None | str | Unset
        if isinstance(self.expiration, Unset):
            expiration = UNSET
        else:
            expiration = self.expiration

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "type": type_,
                "account_type": account_type,
                "last4": last4,
                "contact_id": contact_id,
                "status": status,
            }
        )
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_list_payment_methods_response_200_items_item_type(d.pop("type"))

        account_type = d.pop("account_type")

        def _parse_last4(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last4 = _parse_last4(d.pop("last4"))

        contact_id = d.pop("contact_id")

        status = check_list_payment_methods_response_200_items_item_status(
            d.pop("status")
        )

        def _parse_expiration(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        expiration = _parse_expiration(d.pop("expiration", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        list_payment_methods_response_200_items_item = cls(
            id=id,
            type_=type_,
            account_type=account_type,
            last4=last4,
            contact_id=contact_id,
            status=status,
            expiration=expiration,
            name=name,
        )

        return list_payment_methods_response_200_items_item
