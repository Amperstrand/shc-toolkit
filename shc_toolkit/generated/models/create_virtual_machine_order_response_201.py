from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_order_submit_response import VmOrderSubmitResponse


T = TypeVar("T", bound="CreateVirtualMachineOrderResponse201")


@_attrs_define
class CreateVirtualMachineOrderResponse201:
    """
    Attributes:
        data (VmOrderSubmitResponse):  Example: {'lnvps_compatible': True, 'submitted': True, 'order': {'order_id': 901,
            'order_number': '1000901', 'status': 'accepted', 'order_form_id': 1, 'order_form_label': 'NVME',
            'package_group_id': 3}, 'invoice': {'invoice_id': 1550, 'invoice_status': 'open', 'currency': 'USD', 'total':
            '11.99', 'paid': '0.00', 'balance_due': '11.99', 'date_due': '2026-04-24T00:00:00+00:00'}, 'service_ids':
            [4012], 'virtual_machines': [{'id': 4012, 'hostname': 'demo1.example.net', 'os_user': 'debian', 'os_template':
            'debian13-cloud', 'service_status': 'pending', 'provisioning_state': 'pending', 'bootstrap_completed_at': None,
            'package': 'NVMe VPS - Starter', 'specs': {'cpu': 2, 'memory_mb': 2048, 'disk_gb': 40, 'bandwidth_gb': 2000,
            'ipv4': 1, 'ipv6': 1}, 'ips': [], 'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@laptop', 'pricing':
            {'term': 1, 'period': 'month', 'price': '11.99', 'renew': '11.99', 'currency': 'USD'}, 'date_created':
            '2026-04-17T01:23:45+00:00', 'date_renews': None, 'date_suspended': None, 'date_canceled': None}],
            'normalized_request': {'package_id': 23, 'pricing_id': 12, 'hostname': 'demo1.example.net', 'user': 'debian',
            'ssh_key_present': True, 'module_group_id': 4, 'order_form_id': 1, 'package_group_id': 3, 'coupon_present':
            False}, 'package': {'package_id': 23, 'name': 'NVMe VPS - Starter', 'template': 'debian13-cloud', 'image':
            {'name': 'debian13-cloud', 'display_name': 'Debian 13 Cloud', 'default_user': 'debian', 'cloudinit': True},
            'module_groups': [{'id': 4, 'name': 'Katy, Texas'}], 'module_group_required': False}, 'next':
            {'payment_required': True, 'checkout_url': '/payment/1550/checkout', 'manual_review': False, 'provisioning':
            'Provisioning begins after the order is accepted and the invoice is paid.'}}.
    """

    data: VmOrderSubmitResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_order_submit_response import VmOrderSubmitResponse

        d = dict(src_dict)
        data = VmOrderSubmitResponse.from_dict(d.pop("data"))

        create_virtual_machine_order_response_201 = cls(
            data=data,
        )

        create_virtual_machine_order_response_201.additional_properties = d
        return create_virtual_machine_order_response_201

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
