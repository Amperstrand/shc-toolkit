from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.provisioning_state import ProvisioningState
from ..models.service_status import ServiceStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cancel_vm_credit import CancelVmCredit
    from ..models.ip_address import IpAddress
    from ..models.vm_pricing import VmPricing
    from ..models.vm_specs import VmSpecs


T = TypeVar("T", bound="CancelVmResponseData")


@_attrs_define
class CancelVmResponseData:
    """VmDetail extended with `cancel_credit` when the cancel was immediate. End-of-term cancels return the bare VmDetail
    shape (no `cancel_credit`). v2.4.0: top-level expected_refund + transaction_id mirrors are always present on cancel
    responses.

        Attributes:
            id (int):  Example: 353.
            hostname (None | str):  Example: my-vps.
            os_user (None | str):  Example: debian.
            os_template (None | str): Machine-stable OS template identifier the service was last provisioned with. Resolved
                against the customer's eligible plan and the live /ordering/catalog `template` option (e.g. debian13-cloud,
                debian12-cloud, ubuntu2404-cloud, ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud, almalinux9-cloud,
                alpine323-cloud, devuan5-cloud, openbsd79-cloud, windows2022-byol). null when not yet known. Example:
                debian13-cloud.
            service_status (ServiceStatus): Blesta service lifecycle state. Example: active.
            provisioning_state (ProvisioningState): Derived customer-facing provisioning readiness state. Example:
                provisioning.
            bootstrap_completed_at (datetime.datetime | None): When the provisioning watcher confirmed guest-agent
                readiness, IPv4 assignment, and SSH reachability. Example: 2026-02-01T07:59:12+00:00.
            package (str): Customer-facing package name currently attached to the service. Example: NVMe VPS - Standard.
            specs (VmSpecs): Package-derived resource profile for a VM service or plan. Example: {'cpu': 2, 'memory_mb':
                4096, 'disk_gb': 80, 'bandwidth_gb': 4000, 'ipv4': 1, 'ipv6': 1}.
            ips (list[IpAddress]):
            ssh_key (None | str): Stored SSH public key that will be applied on reinstall, if present. Example: ssh-ed25519
                AAAAC3NzaC1lZDI1NTE5AAAA....
            pricing (VmPricing): Current billing cadence and pricing for one owned service. Example: {'term': 1, 'period':
                'month', 'price': '11.99', 'renew': '11.99', 'currency': 'USD'}.
            date_created (datetime.datetime | None):  Example: 2026-02-01T07:57:55+00:00.
            date_renews (datetime.datetime | None): Next renewal timestamp recorded for the service. Example:
                2027-02-01T07:57:55+00:00.
            date_suspended (datetime.datetime | None):  Example: 2026-03-01T10:15:00+00:00.
            date_canceled (datetime.datetime | None):  Example: 2026-03-15T10:15:00+00:00.
            has_active_job (bool | Unset): True when the VM has a backup/snapshot/restore/reinstall/provision job that is
                pending or running. When true, poll /vm/{service_id}/jobs/{job_id} before mutating.
            cancel_credit (CancelVmCredit | Unset): Financial outcome of an immediate cancellation. Only present on
                `immediate: true` responses. `issued: false` means the auto-credit was either zero (no unused-paid time) or that
                the in_house_credit transaction failed to land — check the customer's billing history for ground truth. Example:
                {'amount': 12.47, 'currency': 'USD', 'transaction_id': 8412, 'issued': True}.
            expected_refund (float | Unset): v2.4.0 (additive, top-level mirror): the issued unused-time credit in the
                billing currency, computed by the SAME shared cancel-credit model as cancel_credit.amount (see the refund
                formula in the API description). 0 for end-of-term cancels and when nothing was due.
            transaction_id (int | None | Unset): v2.4.0 (additive, top-level mirror of cancel_credit.transaction_id): the
                in_house_credit transaction id, null when no credit was issued or the cancel was end-of-term.
    """

    id: int
    hostname: None | str
    os_user: None | str
    os_template: None | str
    service_status: ServiceStatus
    provisioning_state: ProvisioningState
    bootstrap_completed_at: datetime.datetime | None
    package: str
    specs: VmSpecs
    ips: list[IpAddress]
    ssh_key: None | str
    pricing: VmPricing
    date_created: datetime.datetime | None
    date_renews: datetime.datetime | None
    date_suspended: datetime.datetime | None
    date_canceled: datetime.datetime | None
    has_active_job: bool | Unset = UNSET
    cancel_credit: CancelVmCredit | Unset = UNSET
    expected_refund: float | Unset = UNSET
    transaction_id: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        hostname: None | str
        hostname = self.hostname

        os_user: None | str
        os_user = self.os_user

        os_template: None | str
        os_template = self.os_template

        service_status = self.service_status.value

        provisioning_state = self.provisioning_state.value

        bootstrap_completed_at: None | str
        if isinstance(self.bootstrap_completed_at, datetime.datetime):
            bootstrap_completed_at = self.bootstrap_completed_at.isoformat()
        else:
            bootstrap_completed_at = self.bootstrap_completed_at

        package = self.package

        specs = self.specs.to_dict()

        ips = []
        for ips_item_data in self.ips:
            ips_item = ips_item_data.to_dict()
            ips.append(ips_item)

        ssh_key: None | str
        ssh_key = self.ssh_key

        pricing = self.pricing.to_dict()

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

        date_suspended: None | str
        if isinstance(self.date_suspended, datetime.datetime):
            date_suspended = self.date_suspended.isoformat()
        else:
            date_suspended = self.date_suspended

        date_canceled: None | str
        if isinstance(self.date_canceled, datetime.datetime):
            date_canceled = self.date_canceled.isoformat()
        else:
            date_canceled = self.date_canceled

        has_active_job = self.has_active_job

        cancel_credit: dict[str, Any] | Unset = UNSET
        if not isinstance(self.cancel_credit, Unset):
            cancel_credit = self.cancel_credit.to_dict()

        expected_refund = self.expected_refund

        transaction_id: int | None | Unset
        if isinstance(self.transaction_id, Unset):
            transaction_id = UNSET
        else:
            transaction_id = self.transaction_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "hostname": hostname,
                "os_user": os_user,
                "os_template": os_template,
                "service_status": service_status,
                "provisioning_state": provisioning_state,
                "bootstrap_completed_at": bootstrap_completed_at,
                "package": package,
                "specs": specs,
                "ips": ips,
                "ssh_key": ssh_key,
                "pricing": pricing,
                "date_created": date_created,
                "date_renews": date_renews,
                "date_suspended": date_suspended,
                "date_canceled": date_canceled,
            }
        )
        if has_active_job is not UNSET:
            field_dict["has_active_job"] = has_active_job
        if cancel_credit is not UNSET:
            field_dict["cancel_credit"] = cancel_credit
        if expected_refund is not UNSET:
            field_dict["expected_refund"] = expected_refund
        if transaction_id is not UNSET:
            field_dict["transaction_id"] = transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cancel_vm_credit import CancelVmCredit
        from ..models.ip_address import IpAddress
        from ..models.vm_pricing import VmPricing
        from ..models.vm_specs import VmSpecs

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

        def _parse_os_template(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        os_template = _parse_os_template(d.pop("os_template"))

        service_status = ServiceStatus(d.pop("service_status"))

        provisioning_state = ProvisioningState(d.pop("provisioning_state"))

        def _parse_bootstrap_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                bootstrap_completed_at_type_0 = datetime.datetime.fromisoformat(data)

                return bootstrap_completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        bootstrap_completed_at = _parse_bootstrap_completed_at(
            d.pop("bootstrap_completed_at")
        )

        package = d.pop("package")

        specs = VmSpecs.from_dict(d.pop("specs"))

        ips = []
        _ips = d.pop("ips")
        for ips_item_data in _ips:
            ips_item = IpAddress.from_dict(ips_item_data)

            ips.append(ips_item)

        def _parse_ssh_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        ssh_key = _parse_ssh_key(d.pop("ssh_key"))

        pricing = VmPricing.from_dict(d.pop("pricing"))

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

        def _parse_date_suspended(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_suspended_type_0 = datetime.datetime.fromisoformat(data)

                return date_suspended_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_suspended = _parse_date_suspended(d.pop("date_suspended"))

        def _parse_date_canceled(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_canceled_type_0 = datetime.datetime.fromisoformat(data)

                return date_canceled_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_canceled = _parse_date_canceled(d.pop("date_canceled"))

        has_active_job = d.pop("has_active_job", UNSET)

        _cancel_credit = d.pop("cancel_credit", UNSET)
        cancel_credit: CancelVmCredit | Unset
        if isinstance(_cancel_credit, Unset):
            cancel_credit = UNSET
        else:
            cancel_credit = CancelVmCredit.from_dict(_cancel_credit)

        expected_refund = d.pop("expected_refund", UNSET)

        def _parse_transaction_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        transaction_id = _parse_transaction_id(d.pop("transaction_id", UNSET))

        cancel_vm_response_data = cls(
            id=id,
            hostname=hostname,
            os_user=os_user,
            os_template=os_template,
            service_status=service_status,
            provisioning_state=provisioning_state,
            bootstrap_completed_at=bootstrap_completed_at,
            package=package,
            specs=specs,
            ips=ips,
            ssh_key=ssh_key,
            pricing=pricing,
            date_created=date_created,
            date_renews=date_renews,
            date_suspended=date_suspended,
            date_canceled=date_canceled,
            has_active_job=has_active_job,
            cancel_credit=cancel_credit,
            expected_refund=expected_refund,
            transaction_id=transaction_id,
        )

        cancel_vm_response_data.additional_properties = d
        return cancel_vm_response_data

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
