from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.contact_create_request_contact_type_type_0 import (
    ContactCreateRequestContactTypeType0,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContactCreateRequest")


@_attrs_define
class ContactCreateRequest:
    """Fields for creating a client-owned contact. Mirrors the portal add-contact form.

    Example:
        {'first_name': 'Jane', 'last_name': 'Roe', 'email': 'jane.roe@example.com', 'contact_type': 'billing'}

    Attributes:
        first_name (str):  Example: Jane.
        last_name (str):  Example: Roe.
        email (str):  Example: jane.roe@example.com.
        contact_type (ContactCreateRequestContactTypeType0 | int | Unset): Non-primary contact type: 'billing'
            (default), 'other', or a numeric custom contact-type id (stored as 'other'). Default:
            ContactCreateRequestContactTypeType0.BILLING. Example: billing.
        title (str | Unset):
        company (str | Unset):
        address1 (str | Unset):
        address2 (str | Unset):
        city (str | Unset):
        state (str | Unset): ISO 3166-2 subdivision code, where applicable.
        zip_ (str | Unset):
        country (str | Unset): ISO 3166-1 alpha-2 country code. Defaults to the account's own country if omitted.
            Example: US.
        phone (str | Unset): Optional single phone number in E.164 format (e.g. +15125550123). Example: +15125550123.
        permissions (list[str] | Unset): Permission area keys to grant this contact. Unknown keys are ignored. See GET
            /contacts/permission-options. Example: ['client_invoices', 'client_services'].
        enable_login (bool | Unset): Create a portal login for this contact. When true, new_password is required (and
            confirm_password must match if supplied). Default: False.
        username (str | Unset): Login username when enable_login is true (defaults to the email). Only valid with
            enable_login.
        new_password (str | Unset): Password for the contact's portal login. Required when enable_login is true; only
            valid with enable_login. Must satisfy the company password policy.
        confirm_password (str | Unset): Must equal new_password. Defaults to new_password if omitted. Only valid with
            enable_login.
    """

    first_name: str
    last_name: str
    email: str
    contact_type: ContactCreateRequestContactTypeType0 | int | Unset = (
        ContactCreateRequestContactTypeType0.BILLING
    )
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
    enable_login: bool | Unset = False
    username: str | Unset = UNSET
    new_password: str | Unset = UNSET
    confirm_password: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        first_name = self.first_name

        last_name = self.last_name

        email = self.email

        contact_type: int | str | Unset
        if isinstance(self.contact_type, Unset):
            contact_type = UNSET
        elif isinstance(self.contact_type, ContactCreateRequestContactTypeType0):
            contact_type = self.contact_type.value
        else:
            contact_type = self.contact_type

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

        field_dict.update(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
            }
        )
        if contact_type is not UNSET:
            field_dict["contact_type"] = contact_type
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
        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        email = d.pop("email")

        def _parse_contact_type(
            data: object,
        ) -> ContactCreateRequestContactTypeType0 | int | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                contact_type_type_0 = ContactCreateRequestContactTypeType0(data)

                return contact_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ContactCreateRequestContactTypeType0 | int | Unset, data)

        contact_type = _parse_contact_type(d.pop("contact_type", UNSET))

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

        contact_create_request = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact_type=contact_type,
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

        return contact_create_request
