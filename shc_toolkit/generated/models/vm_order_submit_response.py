from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_detail import VmDetail
    from ..models.vm_order_invoice import VmOrderInvoice
    from ..models.vm_order_next import VmOrderNext
    from ..models.vm_order_normalized_request import VmOrderNormalizedRequest
    from ..models.vm_order_result import VmOrderResult
    from ..models.vm_order_submit_response_package import VmOrderSubmitResponsePackage


T = TypeVar("T", bound="VmOrderSubmitResponse")


@_attrs_define
class VmOrderSubmitResponse:
    """
    Example:
        {'lnvps_compatible': True, 'submitted': True, 'order': {'order_id': 901, 'order_number': '1000901', 'status':
            'accepted', 'order_form_id': 1, 'order_form_label': 'NVME', 'package_group_id': 3}, 'invoice': {'invoice_id':
            1550, 'invoice_status': 'open', 'currency': 'USD', 'total': '11.99', 'paid': '0.00', 'balance_due': '11.99',
            'date_due': '2026-04-24T00:00:00+00:00'}, 'service_ids': [4012], 'virtual_machines': [{'id': 4012, 'hostname':
            'demo1.example.net', 'os_user': 'debian', 'os_template': 'debian13-cloud', 'service_status': 'pending',
            'provisioning_state': 'pending', 'bootstrap_completed_at': None, 'package': 'NVMe VPS - Starter', 'specs':
            {'cpu': 2, 'memory_mb': 2048, 'disk_gb': 40, 'bandwidth_gb': 2000, 'ipv4': 1, 'ipv6': 1}, 'ips': [], 'ssh_key':
            'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@laptop', 'pricing': {'term': 1, 'period': 'month', 'price':
            '11.99', 'renew': '11.99', 'currency': 'USD'}, 'date_created': '2026-04-17T01:23:45+00:00', 'date_renews': None,
            'date_suspended': None, 'date_canceled': None}], 'normalized_request': {'package_id': 23, 'pricing_id': 12,
            'hostname': 'demo1.example.net', 'user': 'debian', 'ssh_key_present': True, 'module_group_id': 4,
            'order_form_id': 1, 'package_group_id': 3, 'coupon_present': False}, 'package': {'package_id': 23, 'name': 'NVMe
            VPS - Starter', 'template': 'debian13-cloud', 'image': {'name': 'debian13-cloud', 'display_name': 'Debian 13
            Cloud', 'default_user': 'debian', 'cloudinit': True}, 'module_groups': [{'id': 4, 'name': 'Katy, Texas'}],
            'module_group_required': False}, 'next': {'payment_required': True, 'checkout_url': '/payment/1550/checkout',
            'manual_review': False, 'provisioning': 'Provisioning begins after the order is accepted and the invoice is
            paid.'}}

    Attributes:
        lnvps_compatible (bool):  Example: True.
        submitted (bool):  Example: True.
        order (VmOrderResult):
        invoice (VmOrderInvoice):
        service_ids (list[int]):  Example: [4012].
        virtual_machines (list[VmDetail]):
        normalized_request (VmOrderNormalizedRequest):
        package (VmOrderSubmitResponsePackage):
        next_ (VmOrderNext):
        service_id (int | None | Unset): v2.4.0 alias (additive): the single created service id (first of service_ids; a
            VM order creates exactly one). null only if creation yielded none.
    """

    lnvps_compatible: bool
    submitted: bool
    order: VmOrderResult
    invoice: VmOrderInvoice
    service_ids: list[int]
    virtual_machines: list[VmDetail]
    normalized_request: VmOrderNormalizedRequest
    package: VmOrderSubmitResponsePackage
    next_: VmOrderNext
    service_id: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lnvps_compatible = self.lnvps_compatible

        submitted = self.submitted

        order = self.order.to_dict()

        invoice = self.invoice.to_dict()

        service_ids = self.service_ids

        virtual_machines = []
        for virtual_machines_item_data in self.virtual_machines:
            virtual_machines_item = virtual_machines_item_data.to_dict()
            virtual_machines.append(virtual_machines_item)

        normalized_request = self.normalized_request.to_dict()

        package = self.package.to_dict()

        next_ = self.next_.to_dict()

        service_id: int | None | Unset
        if isinstance(self.service_id, Unset):
            service_id = UNSET
        else:
            service_id = self.service_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lnvps_compatible": lnvps_compatible,
                "submitted": submitted,
                "order": order,
                "invoice": invoice,
                "service_ids": service_ids,
                "virtual_machines": virtual_machines,
                "normalized_request": normalized_request,
                "package": package,
                "next": next_,
            }
        )
        if service_id is not UNSET:
            field_dict["service_id"] = service_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_detail import VmDetail
        from ..models.vm_order_invoice import VmOrderInvoice
        from ..models.vm_order_next import VmOrderNext
        from ..models.vm_order_normalized_request import VmOrderNormalizedRequest
        from ..models.vm_order_result import VmOrderResult
        from ..models.vm_order_submit_response_package import (
            VmOrderSubmitResponsePackage,
        )

        d = dict(src_dict)
        lnvps_compatible = d.pop("lnvps_compatible")

        submitted = d.pop("submitted")

        order = VmOrderResult.from_dict(d.pop("order"))

        invoice = VmOrderInvoice.from_dict(d.pop("invoice"))

        service_ids = cast(list[int], d.pop("service_ids"))

        virtual_machines = []
        _virtual_machines = d.pop("virtual_machines")
        for virtual_machines_item_data in _virtual_machines:
            virtual_machines_item = VmDetail.from_dict(virtual_machines_item_data)

            virtual_machines.append(virtual_machines_item)

        normalized_request = VmOrderNormalizedRequest.from_dict(
            d.pop("normalized_request")
        )

        package = VmOrderSubmitResponsePackage.from_dict(d.pop("package"))

        next_ = VmOrderNext.from_dict(d.pop("next"))

        def _parse_service_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        service_id = _parse_service_id(d.pop("service_id", UNSET))

        vm_order_submit_response = cls(
            lnvps_compatible=lnvps_compatible,
            submitted=submitted,
            order=order,
            invoice=invoice,
            service_ids=service_ids,
            virtual_machines=virtual_machines,
            normalized_request=normalized_request,
            package=package,
            next_=next_,
            service_id=service_id,
        )

        vm_order_submit_response.additional_properties = d
        return vm_order_submit_response

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
