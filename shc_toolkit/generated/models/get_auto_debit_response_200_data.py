from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.get_auto_debit_response_200_data_type_type_1 import (
    GetAutoDebitResponse200DataTypeType1,
    check_get_auto_debit_response_200_data_type_type_1,
)
from ..models.get_auto_debit_response_200_data_type_type_2_type_1 import (
    GetAutoDebitResponse200DataTypeType2Type1,
    check_get_auto_debit_response_200_data_type_type_2_type_1,
)
from ..models.get_auto_debit_response_200_data_type_type_3_type_1 import (
    GetAutoDebitResponse200DataTypeType3Type1,
    check_get_auto_debit_response_200_data_type_type_3_type_1,
)

T = TypeVar("T", bound="GetAutoDebitResponse200Data")


@_attrs_define
class GetAutoDebitResponse200Data:
    enabled: bool
    account_id: int | None
    type_: (
        GetAutoDebitResponse200DataTypeType1
        | GetAutoDebitResponse200DataTypeType2Type1
        | GetAutoDebitResponse200DataTypeType3Type1
        | None
    )

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        account_id: int | None
        account_id = self.account_id

        type_: None | str
        if (
            isinstance(self.type_, str)
            or isinstance(self.type_, str)
            or isinstance(self.type_, str)
        ):
            type_ = self.type_
        else:
            type_ = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "enabled": enabled,
                "account_id": account_id,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        def _parse_account_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        account_id = _parse_account_id(d.pop("account_id"))

        def _parse_type_(
            data: object,
        ) -> (
            GetAutoDebitResponse200DataTypeType1
            | GetAutoDebitResponse200DataTypeType2Type1
            | GetAutoDebitResponse200DataTypeType3Type1
            | None
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_1 = check_get_auto_debit_response_200_data_type_type_1(data)

                return type_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_2_type_1 = (
                    check_get_auto_debit_response_200_data_type_type_2_type_1(data)
                )

                return type_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_3_type_1 = (
                    check_get_auto_debit_response_200_data_type_type_3_type_1(data)
                )

                return type_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                GetAutoDebitResponse200DataTypeType1
                | GetAutoDebitResponse200DataTypeType2Type1
                | GetAutoDebitResponse200DataTypeType3Type1
                | None,
                data,
            )

        type_ = _parse_type_(d.pop("type"))

        get_auto_debit_response_200_data = cls(
            enabled=enabled,
            account_id=account_id,
            type_=type_,
        )

        return get_auto_debit_response_200_data
