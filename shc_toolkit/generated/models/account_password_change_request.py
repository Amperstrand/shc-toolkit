from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_password_change_request_additional_property_type_4 import (
        AccountPasswordChangeRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="AccountPasswordChangeRequest")


@_attrs_define
class AccountPasswordChangeRequest:
    """
    Example:
        {'current_password': '<current-password>', 'new_password': '<new-password>', 'idempotency_key':
            '5f051e42-f6a0-4f4d-9b67-c444f4673dd7'}

    Attributes:
        current_password (str): The authenticated customer's current Blesta login password.
        new_password (str): The replacement password. Must satisfy the company's configured Blesta password rules.
        idempotency_key (str | Unset): Optional opaque caller-supplied key for retry-safe client bookkeeping.
    """

    current_password: str
    new_password: str
    idempotency_key: str | Unset = UNSET
    additional_properties: dict[
        str,
        AccountPasswordChangeRequestAdditionalPropertyType4
        | bool
        | float
        | int
        | list[str]
        | None
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account_password_change_request_additional_property_type_4 import (
            AccountPasswordChangeRequestAdditionalPropertyType4,
        )

        current_password = self.current_password

        new_password = self.new_password

        idempotency_key = self.idempotency_key

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, AccountPasswordChangeRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "current_password": current_password,
                "new_password": new_password,
            }
        )
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_password_change_request_additional_property_type_4 import (
            AccountPasswordChangeRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        current_password = d.pop("current_password")

        new_password = d.pop("new_password")

        idempotency_key = d.pop("idempotency_key", UNSET)

        account_password_change_request = cls(
            current_password=current_password,
            new_password=new_password,
            idempotency_key=idempotency_key,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                AccountPasswordChangeRequestAdditionalPropertyType4
                | bool
                | float
                | int
                | list[str]
                | None
                | str
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        AccountPasswordChangeRequestAdditionalPropertyType4.from_dict(
                            data
                        )
                    )

                    return additional_property_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_5 = cast(list[str], data)

                    return additional_property_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(
                    AccountPasswordChangeRequestAdditionalPropertyType4
                    | bool
                    | float
                    | int
                    | list[str]
                    | None
                    | str,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        account_password_change_request.additional_properties = additional_properties
        return account_password_change_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        AccountPasswordChangeRequestAdditionalPropertyType4
        | bool
        | float
        | int
        | list[str]
        | None
        | str
    ):
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: AccountPasswordChangeRequestAdditionalPropertyType4
        | bool
        | float
        | int
        | list[str]
        | None
        | str,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
