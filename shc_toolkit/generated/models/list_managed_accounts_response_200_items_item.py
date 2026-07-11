from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.list_managed_accounts_response_200_items_item_status import (
    ListManagedAccountsResponse200ItemsItemStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListManagedAccountsResponse200ItemsItem")


@_attrs_define
class ListManagedAccountsResponse200ItemsItem:
    """
    Attributes:
        status (ListManagedAccountsResponse200ItemsItemStatus):  Example: active.
        client_id (int | None | Unset):  Example: 152.
        client_id_code (None | str | Unset):  Example: 152.
        company (None | str | Unset):
        first_name (None | str | Unset):
        last_name (None | str | Unset):
        email (None | str | Unset):
        invitation_token (None | str | Unset):
    """

    status: ListManagedAccountsResponse200ItemsItemStatus
    client_id: int | None | Unset = UNSET
    client_id_code: None | str | Unset = UNSET
    company: None | str | Unset = UNSET
    first_name: None | str | Unset = UNSET
    last_name: None | str | Unset = UNSET
    email: None | str | Unset = UNSET
    invitation_token: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        client_id: int | None | Unset
        if isinstance(self.client_id, Unset):
            client_id = UNSET
        else:
            client_id = self.client_id

        client_id_code: None | str | Unset
        if isinstance(self.client_id_code, Unset):
            client_id_code = UNSET
        else:
            client_id_code = self.client_id_code

        company: None | str | Unset
        if isinstance(self.company, Unset):
            company = UNSET
        else:
            company = self.company

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

        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        invitation_token: None | str | Unset
        if isinstance(self.invitation_token, Unset):
            invitation_token = UNSET
        else:
            invitation_token = self.invitation_token

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_id_code is not UNSET:
            field_dict["client_id_code"] = client_id_code
        if company is not UNSET:
            field_dict["company"] = company
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if invitation_token is not UNSET:
            field_dict["invitation_token"] = invitation_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ListManagedAccountsResponse200ItemsItemStatus(d.pop("status"))

        def _parse_client_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        client_id = _parse_client_id(d.pop("client_id", UNSET))

        def _parse_client_id_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        client_id_code = _parse_client_id_code(d.pop("client_id_code", UNSET))

        def _parse_company(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        company = _parse_company(d.pop("company", UNSET))

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

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_invitation_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        invitation_token = _parse_invitation_token(d.pop("invitation_token", UNSET))

        list_managed_accounts_response_200_items_item = cls(
            status=status,
            client_id=client_id,
            client_id_code=client_id_code,
            company=company,
            first_name=first_name,
            last_name=last_name,
            email=email,
            invitation_token=invitation_token,
        )

        return list_managed_accounts_response_200_items_item
