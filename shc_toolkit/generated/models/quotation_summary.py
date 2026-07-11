from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.quotation_summary_status_type_1 import QuotationSummaryStatusType1
from ..models.quotation_summary_status_type_2_type_1 import (
    QuotationSummaryStatusType2Type1,
)
from ..models.quotation_summary_status_type_3_type_1 import (
    QuotationSummaryStatusType3Type1,
)

T = TypeVar("T", bound="QuotationSummary")


@_attrs_define
class QuotationSummary:
    """Compact view of one quotation owned by the authenticated client. Money fields are formatted as fixed-point strings
    (two decimal places) to preserve precision. Returned directly in the GET /quotations list; the GET
    /quotations/{quotationId} detail response composes this summary with notes and line_items via allOf.

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

        field_dict: dict[str, Any] = {}

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
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

        quotation_summary = cls(
            id=id,
            id_code=id_code,
            title=title,
            status=status,
            subtotal=subtotal,
            total=total,
            currency=currency,
            date_created=date_created,
            date_expires=date_expires,
        )

        return quotation_summary
