from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.list_account_managers_response_200_items_item_status_type_1 import (
    ListAccountManagersResponse200ItemsItemStatusType1,
)
from ..models.list_account_managers_response_200_items_item_status_type_2_type_1 import (
    ListAccountManagersResponse200ItemsItemStatusType2Type1,
)
from ..models.list_account_managers_response_200_items_item_status_type_3_type_1 import (
    ListAccountManagersResponse200ItemsItemStatusType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAccountManagersResponse200ItemsItem")


@_attrs_define
class ListAccountManagersResponse200ItemsItem:
    """
    Attributes:
        email (None | str):
        status (ListAccountManagersResponse200ItemsItemStatusType1 |
            ListAccountManagersResponse200ItemsItemStatusType2Type1 |
            ListAccountManagersResponse200ItemsItemStatusType3Type1 | None):  Example: active.
        permissions (list[str]):
        contact_id (int | None | Unset):  Example: 88.
        invitation_token (None | str | Unset):
        first_name (None | str | Unset):
        last_name (None | str | Unset):
        company (None | str | Unset):
    """

    email: None | str
    status: (
        ListAccountManagersResponse200ItemsItemStatusType1
        | ListAccountManagersResponse200ItemsItemStatusType2Type1
        | ListAccountManagersResponse200ItemsItemStatusType3Type1
        | None
    )
    permissions: list[str]
    contact_id: int | None | Unset = UNSET
    invitation_token: None | str | Unset = UNSET
    first_name: None | str | Unset = UNSET
    last_name: None | str | Unset = UNSET
    company: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        email: None | str
        email = self.email

        status: None | str
        if isinstance(self.status, ListAccountManagersResponse200ItemsItemStatusType1):
            status = self.status.value
        elif isinstance(
            self.status, ListAccountManagersResponse200ItemsItemStatusType2Type1
        ):
            status = self.status.value
        elif isinstance(
            self.status, ListAccountManagersResponse200ItemsItemStatusType3Type1
        ):
            status = self.status.value
        else:
            status = self.status

        permissions = self.permissions

        contact_id: int | None | Unset
        if isinstance(self.contact_id, Unset):
            contact_id = UNSET
        else:
            contact_id = self.contact_id

        invitation_token: None | str | Unset
        if isinstance(self.invitation_token, Unset):
            invitation_token = UNSET
        else:
            invitation_token = self.invitation_token

        first_name: None | str | Unset
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: None | str | Unset
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        company: None | str | Unset
        if isinstance(self.company, Unset):
            company = UNSET
        else:
            company = self.company

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "email": email,
                "status": status,
                "permissions": permissions,
            }
        )
        if contact_id is not UNSET:
            field_dict["contact_id"] = contact_id
        if invitation_token is not UNSET:
            field_dict["invitation_token"] = invitation_token
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if company is not UNSET:
            field_dict["company"] = company

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        email = _parse_email(d.pop("email"))

        def _parse_status(
            data: object,
        ) -> (
            ListAccountManagersResponse200ItemsItemStatusType1
            | ListAccountManagersResponse200ItemsItemStatusType2Type1
            | ListAccountManagersResponse200ItemsItemStatusType3Type1
            | None
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = ListAccountManagersResponse200ItemsItemStatusType1(data)

                return status_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_2_type_1 = (
                    ListAccountManagersResponse200ItemsItemStatusType2Type1(data)
                )

                return status_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_3_type_1 = (
                    ListAccountManagersResponse200ItemsItemStatusType3Type1(data)
                )

                return status_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                ListAccountManagersResponse200ItemsItemStatusType1
                | ListAccountManagersResponse200ItemsItemStatusType2Type1
                | ListAccountManagersResponse200ItemsItemStatusType3Type1
                | None,
                data,
            )

        status = _parse_status(d.pop("status"))

        permissions = cast(list[str], d.pop("permissions"))

        def _parse_contact_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        contact_id = _parse_contact_id(d.pop("contact_id", UNSET))

        def _parse_invitation_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        invitation_token = _parse_invitation_token(d.pop("invitation_token", UNSET))

        def _parse_first_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        def _parse_last_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

        def _parse_company(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        company = _parse_company(d.pop("company", UNSET))

        list_account_managers_response_200_items_item = cls(
            email=email,
            status=status,
            permissions=permissions,
            contact_id=contact_id,
            invitation_token=invitation_token,
            first_name=first_name,
            last_name=last_name,
            company=company,
        )

        return list_account_managers_response_200_items_item
