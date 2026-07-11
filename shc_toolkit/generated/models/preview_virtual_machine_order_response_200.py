from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_order_preview import VmOrderPreview


T = TypeVar("T", bound="PreviewVirtualMachineOrderResponse200")


@_attrs_define
class PreviewVirtualMachineOrderResponse200:
    """
    Attributes:
        data (VmOrderPreview):  Example: {'lnvps_compatible': True, 'order_submission_supported': True, 'scope_note':
            'This preview validates the same storefront-backed order path used for live VM purchases.', 'submit_path':
            '/user-api/v2/ordering/submit', 'normalized_request': {'package_id': 23, 'pricing_id': 12, 'hostname':
            'demo1.example.net', 'user': 'debian', 'ssh_key_present': True, 'module_group_id': 4, 'order_form_id': 1,
            'package_group_id': 3, 'coupon_present': False}, 'package': {'package_id': 23, 'name': 'NVMe VPS - Starter',
            'template': 'debian13-cloud', 'image': {'name': 'debian13-cloud', 'display_name': 'Debian 13 Cloud',
            'default_user': 'debian', 'cloudinit': True}, 'specs': {'cpu': 1, 'memory_mb': 2048, 'disk_gb': 40,
            'bandwidth_gb': 4000, 'ipv4': 1, 'ipv6': 1}, 'backup_limit': 3, 'snapshot_limit': 5, 'module_groups': [{'id': 4,
            'name': 'Katy, Texas'}], 'module_group_required': False, 'order_path': {'order_form_id': 1, 'order_form_label':
            'NVME', 'package_group_id': 3}}, 'billing': {'pricing_id': 12, 'term': 1, 'period': 'month', 'price': '11.99',
            'renew': '11.99', 'setup_fee': '0.00', 'currency': 'USD', 'initial_due': '11.99', 'renewal_amount': '11.99'},
            'provisioning': {'hostname': 'demo1.example.net', 'user': 'debian', 'template': 'debian13-cloud',
            'supports_ssh_key': True, 'supports_user_override': True, 'module_group_id': 4}, 'warnings': ['This preview does
            not reserve capacity or collect payment.', 'Provisioning still waits for the created order to be accepted and
            the invoice to be paid.']}.
    """

    data: VmOrderPreview
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
        from ..models.vm_order_preview import VmOrderPreview

        d = dict(src_dict)
        data = VmOrderPreview.from_dict(d.pop("data"))

        preview_virtual_machine_order_response_200 = cls(
            data=data,
        )

        preview_virtual_machine_order_response_200.additional_properties = d
        return preview_virtual_machine_order_response_200

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
