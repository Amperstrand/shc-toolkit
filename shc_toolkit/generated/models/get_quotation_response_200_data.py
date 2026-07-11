from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.quotation_summary_status_type_1 import QuotationSummaryStatusType1
from ..models.quotation_summary_status_type_2_type_1 import (
    QuotationSummaryStatusType2Type1,
)
from ..models.quotation_summary_status_type_3_type_1 import (
    QuotationSummaryStatusType3Type1,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_quotation_response_200_data_line_items_item import (
        GetQuotationResponse200DataLineItemsItem,
    )


T = TypeVar("T", bound="GetQuotationResponse200Data")


@_attrs_define
class GetQuotationResponse200Data:
    """
    Attributes:
        id (int):  Example: 9001.
        id_code (None | str): Formatted quotation number shown to the customer. Example: QUO-0042.
        title (None | str):  Example: Managed VPS migration.
        status (None | QuotationSummaryStatusType1 | QuotationSummaryStatusType2Type1 |
            QuotationSummaryStatusType3Type1): Quotation lifecycle state. Example: pending.
        subtotal (None | str): Quotation subtotal before tax, as a fixed-point string with two decimal places. Example:
            50.00.
        total (None | str): Quotation grand total, as a fixed-point string with two decimal places. Example: 54.13.
        currency (None | str): ISO-4217 currency code for the quotation amounts. Example: USD.
        date_created (datetime.datetime | None):
        date_expires (datetime.datetime | None):
        notes (None | str | Unset):
        line_items (list[GetQuotationResponse200DataLineItemsItem] | Unset):
    """

    id: int
    id_code: None | str
    title: None | str
    status: (
        None
        | QuotationSummaryStatusType1
        | QuotationSummaryStatusType2Type1
        | QuotationSummaryStatusType3Type1
    )
    subtotal: None | str
    total: None | str
    currency: None | str
    date_created: datetime.datetime | None
    date_expires: datetime.datetime | None
    notes: None | str | Unset = UNSET
    line_items: list[GetQuotationResponse200DataLineItemsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        id_code: None | str
        id_code = self.id_code

        title: None | str
        title = self.title

        status: None | str
        if isinstance(self.status, QuotationSummaryStatusType1):
            status = self.status.value
        elif isinstance(self.status, QuotationSummaryStatusType2Type1):
            status = self.status.value
        elif isinstance(self.status, QuotationSummaryStatusType3Type1):
            status = self.status.value
        else:
            status = self.status

        subtotal: None | str
        subtotal = self.subtotal

        total: None | str
        total = self.total

        currency: None | str
        currency = self.currency

        date_created: None | str
        if isinstance(self.date_created, datetime.datetime):
            date_created = self.date_created.isoformat()
        else:
            date_created = self.date_created

        date_expires: None | str
        if isinstance(self.date_expires, datetime.datetime):
            date_expires = self.date_expires.isoformat()
        else:
            date_expires = self.date_expires

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        line_items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.line_items, Unset):
            line_items = []
            for line_items_item_data in self.line_items:
                line_items_item = line_items_item_data.to_dict()
                line_items.append(line_items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "id_code": id_code,
                "title": title,
                "status": status,
                "subtotal": subtotal,
                "total": total,
                "currency": currency,
                "date_created": date_created,
                "date_expires": date_expires,
            }
        )
        if notes is not UNSET:
            field_dict["notes"] = notes
        if line_items is not UNSET:
            field_dict["line_items"] = line_items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_quotation_response_200_data_line_items_item import (
            GetQuotationResponse200DataLineItemsItem,
        )

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_id_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        id_code = _parse_id_code(d.pop("id_code"))

        def _parse_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        title = _parse_title(d.pop("title"))

        def _parse_status(
            data: object,
        ) -> (
            None
            | QuotationSummaryStatusType1
            | QuotationSummaryStatusType2Type1
            | QuotationSummaryStatusType3Type1
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = QuotationSummaryStatusType1(data)

                return status_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_2_type_1 = QuotationSummaryStatusType2Type1(data)

                return status_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_3_type_1 = QuotationSummaryStatusType3Type1(data)

                return status_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None
                | QuotationSummaryStatusType1
                | QuotationSummaryStatusType2Type1
                | QuotationSummaryStatusType3Type1,
                data,
            )

        status = _parse_status(d.pop("status"))

        def _parse_subtotal(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        subtotal = _parse_subtotal(d.pop("subtotal"))

        def _parse_total(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        total = _parse_total(d.pop("total"))

        def _parse_currency(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        currency = _parse_currency(d.pop("currency"))

        def _parse_date_created(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_created_type_0 = datetime.datetime.fromisoformat(data)

                return date_created_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_created = _parse_date_created(d.pop("date_created"))

        def _parse_date_expires(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_expires_type_0 = datetime.datetime.fromisoformat(data)

                return date_expires_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_expires = _parse_date_expires(d.pop("date_expires"))

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        _line_items = d.pop("line_items", UNSET)
        line_items: list[GetQuotationResponse200DataLineItemsItem] | Unset = UNSET
        if _line_items is not UNSET:
            line_items = []
            for line_items_item_data in _line_items:
                line_items_item = GetQuotationResponse200DataLineItemsItem.from_dict(
                    line_items_item_data
                )

                line_items.append(line_items_item)

        get_quotation_response_200_data = cls(
            id=id,
            id_code=id_code,
            title=title,
            status=status,
            subtotal=subtotal,
            total=total,
            currency=currency,
            date_created=date_created,
            date_expires=date_expires,
            notes=notes,
            line_items=line_items,
        )

        get_quotation_response_200_data.additional_properties = d
        return get_quotation_response_200_data

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
