from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateContactBody")


@_attrs_define
class UpdateContactBody:
    """
    Attributes:
        first_name (str | Unset):
        last_name (str | Unset):
        email (str | Unset):
        company (str | Unset):
        title (str | Unset):
        address1 (str | Unset):
        address2 (str | Unset):
        city (str | Unset):
        state (str | Unset):
        zip_ (str | Unset):
        country (str | Unset):
        phone (str | Unset):
        permissions (list[str] | Unset):
        enable_login (bool | Unset):
        username (str | Unset):
        new_password (str | Unset):
        confirm_password (str | Unset):
    """

    first_name: str | Unset = UNSET
    last_name: str | Unset = UNSET
    email: str | Unset = UNSET
    company: str | Unset = UNSET
    title: str | Unset = UNSET
    address1: str | Unset = UNSET
    address2: str | Unset = UNSET
    city: str | Unset = UNSET
    state: str | Unset = UNSET
    zip_: str | Unset = UNSET
    country: str | Unset = UNSET
    phone: str | Unset = UNSET
    permissions: list[str] | Unset = UNSET
    enable_login: bool | Unset = UNSET
    username: str | Unset = UNSET
    new_password: str | Unset = UNSET
    confirm_password: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        first_name = self.first_name

        last_name = self.last_name

        email = self.email

        company = self.company

        title = self.title

        address1 = self.address1

        address2 = self.address2

        city = self.city

        state = self.state

        zip_ = self.zip_

        country = self.country

        phone = self.phone

        permissions: list[str] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        enable_login = self.enable_login

        username = self.username

        new_password = self.new_password

        confirm_password = self.confirm_password

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if company is not UNSET:
            field_dict["company"] = company
        if title is not UNSET:
            field_dict["title"] = title
        if address1 is not UNSET:
            field_dict["address1"] = address1
        if address2 is not UNSET:
            field_dict["address2"] = address2
        if city is not UNSET:
            field_dict["city"] = city
        if state is not UNSET:
            field_dict["state"] = state
        if zip_ is not UNSET:
            field_dict["zip"] = zip_
        if country is not UNSET:
            field_dict["country"] = country
        if phone is not UNSET:
            field_dict["phone"] = phone
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if enable_login is not UNSET:
            field_dict["enableLogin"] = enable_login
        if username is not UNSET:
            field_dict["username"] = username
        if new_password is not UNSET:
            field_dict["newPassword"] = new_password
        if confirm_password is not UNSET:
            field_dict["confirmPassword"] = confirm_password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        email = d.pop("email", UNSET)

        company = d.pop("company", UNSET)

        title = d.pop("title", UNSET)

        address1 = d.pop("address1", UNSET)

        address2 = d.pop("address2", UNSET)

        city = d.pop("city", UNSET)

        state = d.pop("state", UNSET)

        zip_ = d.pop("zip", UNSET)

        country = d.pop("country", UNSET)

        phone = d.pop("phone", UNSET)

        permissions = cast(list[str], d.pop("permissions", UNSET))

        enable_login = d.pop("enableLogin", UNSET)

        username = d.pop("username", UNSET)

        new_password = d.pop("newPassword", UNSET)

        confirm_password = d.pop("confirmPassword", UNSET)

        update_contact_body = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company=company,
            title=title,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_=zip_,
            country=country,
            phone=phone,
            permissions=permissions,
            enable_login=enable_login,
            username=username,
            new_password=new_password,
            confirm_password=confirm_password,
        )

        return update_contact_body
