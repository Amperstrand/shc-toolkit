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
        first_name (str | Unset): Contact first name.
        last_name (str | Unset): Contact last name.
        email (str | Unset): Contact email address; changed email values are verification-gated.
        title (str | Unset): Contact title.
        company (str | Unset): Contact company name.
        address1 (str | Unset): First street address line.
        address2 (str | Unset): Second street address line.
        city (str | Unset): Contact city.
        state (str | Unset): Contact state or region.
        zip_ (str | Unset): Contact postal code.
        country (str | Unset): ISO 3166-1 alpha-2 country code.
        phone (str | Unset): Single E.164 phone number; an empty string clears phone rows.
        permissions (list[str] | Unset): Full replacement list of contact permission area keys.
        enable_login (bool | Unset): Whether to create, keep/update, or remove this contact's portal login.
        username (str | Unset): Username used only when creating a new login.
        new_password (str | Unset): New portal login password when enabling login or changing an existing login
            password.
        confirm_password (str | Unset): Confirmation for new_password; defaults to new_password when omitted.
    """

    first_name: str | Unset = UNSET
    last_name: str | Unset = UNSET
    email: str | Unset = UNSET
    title: str | Unset = UNSET
    company: str | Unset = UNSET
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

        title = self.title

        company = self.company

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
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if title is not UNSET:
            field_dict["title"] = title
        if company is not UNSET:
            field_dict["company"] = company
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
            field_dict["enable_login"] = enable_login
        if username is not UNSET:
            field_dict["username"] = username
        if new_password is not UNSET:
            field_dict["new_password"] = new_password
        if confirm_password is not UNSET:
            field_dict["confirm_password"] = confirm_password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        email = d.pop("email", UNSET)

        title = d.pop("title", UNSET)

        company = d.pop("company", UNSET)

        address1 = d.pop("address1", UNSET)

        address2 = d.pop("address2", UNSET)

        city = d.pop("city", UNSET)

        state = d.pop("state", UNSET)

        zip_ = d.pop("zip", UNSET)

        country = d.pop("country", UNSET)

        phone = d.pop("phone", UNSET)

        permissions = cast(list[str], d.pop("permissions", UNSET))

        enable_login = d.pop("enable_login", UNSET)

        username = d.pop("username", UNSET)

        new_password = d.pop("new_password", UNSET)

        confirm_password = d.pop("confirm_password", UNSET)

        update_contact_body = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            title=title,
            company=company,
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
