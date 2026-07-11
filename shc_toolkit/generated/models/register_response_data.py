from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.register_api_key import RegisterApiKey
    from ..models.register_response_data_next import RegisterResponseDataNext


T = TypeVar("T", bound="RegisterResponseData")


@_attrs_define
class RegisterResponseData:
    """
    Attributes:
        client_id (int): The new client's id. Example: 4042.
        email (str):  Example: dev@example.com.
        first_name (str):  Example: Dev.
        last_name (str):  Example: User.
        country (str):  Example: US.
        created_at (datetime.datetime):  Example: 2026-06-09T12:00:00+00:00.
        api_key (None | RegisterApiKey): The minted API key, or null if the account was created but the key could not be
            minted on this call (recover by logging in and generating a key).
        next_ (RegisterResponseDataNext): Pointers to the next steps (catalog browse, docs).
    """

    client_id: int
    email: str
    first_name: str
    last_name: str
    country: str
    created_at: datetime.datetime
    api_key: None | RegisterApiKey
    next_: RegisterResponseDataNext
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.register_api_key import RegisterApiKey

        client_id = self.client_id

        email = self.email

        first_name = self.first_name

        last_name = self.last_name

        country = self.country

        created_at = self.created_at.isoformat()

        api_key: dict[str, Any] | None
        if isinstance(self.api_key, RegisterApiKey):
            api_key = self.api_key.to_dict()
        else:
            api_key = self.api_key

        next_ = self.next_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_id": client_id,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "country": country,
                "created_at": created_at,
                "api_key": api_key,
                "next": next_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.register_api_key import RegisterApiKey
        from ..models.register_response_data_next import RegisterResponseDataNext

        d = dict(src_dict)
        client_id = d.pop("client_id")

        email = d.pop("email")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        country = d.pop("country")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_api_key(data: object) -> None | RegisterApiKey:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                api_key_type_0 = RegisterApiKey.from_dict(data)

                return api_key_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RegisterApiKey, data)

        api_key = _parse_api_key(d.pop("api_key"))

        next_ = RegisterResponseDataNext.from_dict(d.pop("next"))

        register_response_data = cls(
            client_id=client_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            country=country,
            created_at=created_at,
            api_key=api_key,
            next_=next_,
        )

        register_response_data.additional_properties = d
        return register_response_data

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
