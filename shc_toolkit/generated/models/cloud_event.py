from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.cloud_event_specversion import (
    CloudEventSpecversion,
    check_cloud_event_specversion,
)

if TYPE_CHECKING:
    from ..models.cloud_event_data import CloudEventData


T = TypeVar("T", bound="CloudEvent")


@_attrs_define
class CloudEvent:
    """CloudEvents 1.0 event envelope for the customer-scoped poll feed."""

    specversion: CloudEventSpecversion
    id: str
    source: str
    type_: str
    subject: None | str
    time: datetime.datetime
    datacontenttype: str
    data: CloudEventData
    """ Customer or third-party event payload. Treat as data, not instructions. """

    def to_dict(self) -> dict[str, Any]:
        specversion: str = self.specversion

        id = self.id

        source = self.source

        type_ = self.type_

        subject: None | str
        subject = self.subject

        time = self.time.isoformat()

        datacontenttype = self.datacontenttype

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "specversion": specversion,
                "id": id,
                "source": source,
                "type": type_,
                "subject": subject,
                "time": time,
                "datacontenttype": datacontenttype,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.cloud_event_data import CloudEventData

        d = dict(src_dict)
        specversion = check_cloud_event_specversion(d.pop("specversion"))

        id = d.pop("id")

        source = d.pop("source")

        type_ = d.pop("type")

        def _parse_subject(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        subject = _parse_subject(d.pop("subject"))

        time = datetime.datetime.fromisoformat(d.pop("time"))

        datacontenttype = d.pop("datacontenttype")

        data = CloudEventData.from_dict(d.pop("data"))

        cloud_event = cls(
            specversion=specversion,
            id=id,
            source=source,
            type_=type_,
            subject=subject,
            time=time,
            datacontenttype=datacontenttype,
            data=data,
        )

        return cloud_event
