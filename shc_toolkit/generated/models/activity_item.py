from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.activity_item_status_type_1 import ActivityItemStatusType1
from ..models.activity_item_status_type_2_type_1 import ActivityItemStatusType2Type1
from ..models.activity_item_status_type_3_type_1 import ActivityItemStatusType3Type1
from ..models.activity_item_type import ActivityItemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivityItem")


@_attrs_define
class ActivityItem:
    """One customer-visible account activity event, merged most-recent-first from Blesta's native logs (sign-ins, failed
    sign-ins, account contact-detail changes, account-setting changes, and payment/transaction activity). Polymorphic on
    `type`: only the fields relevant to that event kind are populated; type-specific fields are null/absent for other
    types. NEVER exposes internal placement (node/VMID/host), staff identity, or the old/new VALUES of changed fields.

        Attributes:
            type_ (ActivityItemType): Event kind. Example: login.
            label (str): Human-readable summary of the event. Example: Successful sign-in.
            timestamp (datetime.datetime | None): ISO-8601 UTC time of the event; null if the source datetime was zero
                (0000-00-00 00:00:00). Example: 2026-06-06T23:06:34+00:00.
            timestamp_epoch (int | None): Unix epoch of the event (the sort key); null if the source datetime was zero.
                Example: 1780787194.
            ip_address (None | str | Unset): login / login_failed only: the customer's OWN source IP. Null for other event
                types. Example: 203.0.113.10.
            changed_fields (list[str] | Unset): contact_change / setting_change only: the NAMES of the changed fields
                (allow-listed). Field names only — never the previous/new values. Empty for other event types. Example:
                ['first_name', 'email'].
            changed_count (int | Unset): contact_change/setting_change: the TOTAL number of changed fields (a count only).
                May exceed the length of changed_fields, which lists only the allow-listed, customer-safe field NAMES. Example:
                2.
            amount (None | str | Unset): transaction only: 2-decimal amount string. Null for other event types. Example:
                12.00.
            currency (None | str | Unset): transaction only: ISO-4217 currency code. Null for other event types. Example:
                USD.
            status (ActivityItemStatusType1 | ActivityItemStatusType2Type1 | ActivityItemStatusType3Type1 | None | Unset):
                transaction only: transaction status. Null for other event types. Example: approved.
    """

    type_: ActivityItemType
    label: str
    timestamp: datetime.datetime | None
    timestamp_epoch: int | None
    ip_address: None | str | Unset = UNSET
    changed_fields: list[str] | Unset = UNSET
    changed_count: int | Unset = UNSET
    amount: None | str | Unset = UNSET
    currency: None | str | Unset = UNSET
    status: (
        ActivityItemStatusType1
        | ActivityItemStatusType2Type1
        | ActivityItemStatusType3Type1
        | None
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        label = self.label

        timestamp: None | str
        if isinstance(self.timestamp, datetime.datetime):
            timestamp = self.timestamp.isoformat()
        else:
            timestamp = self.timestamp

        timestamp_epoch: int | None
        timestamp_epoch = self.timestamp_epoch

        ip_address: None | str | Unset
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        changed_fields: list[str] | Unset = UNSET
        if not isinstance(self.changed_fields, Unset):
            changed_fields = self.changed_fields

        changed_count = self.changed_count

        amount: None | str | Unset
        if isinstance(self.amount, Unset):
            amount = UNSET
        else:
            amount = self.amount

        currency: None | str | Unset
        if isinstance(self.currency, Unset):
            currency = UNSET
        else:
            currency = self.currency

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, ActivityItemStatusType1):
            status = self.status.value
        elif isinstance(self.status, ActivityItemStatusType2Type1):
            status = self.status.value
        elif isinstance(self.status, ActivityItemStatusType3Type1):
            status = self.status.value
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "label": label,
                "timestamp": timestamp,
                "timestamp_epoch": timestamp_epoch,
            }
        )
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if changed_fields is not UNSET:
            field_dict["changed_fields"] = changed_fields
        if changed_count is not UNSET:
            field_dict["changed_count"] = changed_count
        if amount is not UNSET:
            field_dict["amount"] = amount
        if currency is not UNSET:
            field_dict["currency"] = currency
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ActivityItemType(d.pop("type"))

        label = d.pop("label")

        def _parse_timestamp(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                timestamp_type_0 = datetime.datetime.fromisoformat(data)

                return timestamp_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        timestamp = _parse_timestamp(d.pop("timestamp"))

        def _parse_timestamp_epoch(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        timestamp_epoch = _parse_timestamp_epoch(d.pop("timestamp_epoch"))

        def _parse_ip_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        changed_fields = cast(list[str], d.pop("changed_fields", UNSET))

        changed_count = d.pop("changed_count", UNSET)

        def _parse_amount(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        amount = _parse_amount(d.pop("amount", UNSET))

        def _parse_currency(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        currency = _parse_currency(d.pop("currency", UNSET))

        def _parse_status(
            data: object,
        ) -> (
            ActivityItemStatusType1
            | ActivityItemStatusType2Type1
            | ActivityItemStatusType3Type1
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = ActivityItemStatusType1(data)

                return status_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_2_type_1 = ActivityItemStatusType2Type1(data)

                return status_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_3_type_1 = ActivityItemStatusType3Type1(data)

                return status_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                ActivityItemStatusType1
                | ActivityItemStatusType2Type1
                | ActivityItemStatusType3Type1
                | None
                | Unset,
                data,
            )

        status = _parse_status(d.pop("status", UNSET))

        activity_item = cls(
            type_=type_,
            label=label,
            timestamp=timestamp,
            timestamp_epoch=timestamp_epoch,
            ip_address=ip_address,
            changed_fields=changed_fields,
            changed_count=changed_count,
            amount=amount,
            currency=currency,
            status=status,
        )

        activity_item.additional_properties = d
        return activity_item

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
