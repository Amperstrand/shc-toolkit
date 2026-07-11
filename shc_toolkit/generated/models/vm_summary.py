from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.provisioning_state import ProvisioningState
from ..models.service_status import ServiceStatus

if TYPE_CHECKING:
    from ..models.ip_address import IpAddress


T = TypeVar("T", bound="VmSummary")


@_attrs_define
class VmSummary:
    """Compact inventory view for one owned VM service.

    Example:
        {'id': 353, 'hostname': 'edge-app-01', 'os_user': 'debian', 'package': 'NVMe VPS - Standard', 'service_status':
            'active', 'provisioning_state': 'ready', 'ips': [{'ip': '23.182.128.79', 'cidr': '23.182.128.79/24', 'gateway':
            '23.182.128.1', 'type': 'v4'}], 'date_created': '2026-02-01T07:57:55+00:00', 'date_renews':
            '2027-02-01T07:57:55+00:00'}

    Attributes:
        id (int):  Example: 353.
        hostname (None | str):  Example: my-vps.
        os_user (None | str):  Example: debian.
        package (str): Customer-facing package name associated with the service. Example: NVMe VPS - Standard.
        service_status (ServiceStatus): Blesta service lifecycle state. Example: active.
        provisioning_state (ProvisioningState): Derived customer-facing provisioning readiness state. Example:
            provisioning.
        ips (list[IpAddress]):
        date_created (datetime.datetime | None):  Example: 2026-02-01T07:57:55+00:00.
        date_renews (datetime.datetime | None): Next renewal timestamp recorded for the service. Example:
            2027-02-01T07:57:55+00:00.
    """

    id: int
    hostname: None | str
    os_user: None | str
    package: str
    service_status: ServiceStatus
    provisioning_state: ProvisioningState
    ips: list[IpAddress]
    date_created: datetime.datetime | None
    date_renews: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        hostname: None | str
        hostname = self.hostname

        os_user: None | str
        os_user = self.os_user

        package = self.package

        service_status = self.service_status.value

        provisioning_state = self.provisioning_state.value

        ips = []
        for ips_item_data in self.ips:
            ips_item = ips_item_data.to_dict()
            ips.append(ips_item)

        date_created: None | str
        if isinstance(self.date_created, datetime.datetime):
            date_created = self.date_created.isoformat()
        else:
            date_created = self.date_created

        date_renews: None | str
        if isinstance(self.date_renews, datetime.datetime):
            date_renews = self.date_renews.isoformat()
        else:
            date_renews = self.date_renews

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "hostname": hostname,
                "os_user": os_user,
                "package": package,
                "service_status": service_status,
                "provisioning_state": provisioning_state,
                "ips": ips,
                "date_created": date_created,
                "date_renews": date_renews,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ip_address import IpAddress

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_hostname(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        hostname = _parse_hostname(d.pop("hostname"))

        def _parse_os_user(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        os_user = _parse_os_user(d.pop("os_user"))

        package = d.pop("package")

        service_status = ServiceStatus(d.pop("service_status"))

        provisioning_state = ProvisioningState(d.pop("provisioning_state"))

        ips = []
        _ips = d.pop("ips")
        for ips_item_data in _ips:
            ips_item = IpAddress.from_dict(ips_item_data)

            ips.append(ips_item)

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

        def _parse_date_renews(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_renews_type_0 = datetime.datetime.fromisoformat(data)

                return date_renews_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_renews = _parse_date_renews(d.pop("date_renews"))

        vm_summary = cls(
            id=id,
            hostname=hostname,
            os_user=os_user,
            package=package,
            service_status=service_status,
            provisioning_state=provisioning_state,
            ips=ips,
            date_created=date_created,
            date_renews=date_renews,
        )

        vm_summary.additional_properties = d
        return vm_summary

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
