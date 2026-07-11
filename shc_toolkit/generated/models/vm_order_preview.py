from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_order_billing_preview import VmOrderBillingPreview
    from ..models.vm_order_normalized_request import VmOrderNormalizedRequest
    from ..models.vm_order_provisioning_preview import VmOrderProvisioningPreview
    from ..models.vm_order_selected_package import VmOrderSelectedPackage


T = TypeVar("T", bound="VmOrderPreview")


@_attrs_define
class VmOrderPreview:
    """
    Example:
        {'lnvps_compatible': True, 'order_submission_supported': True, 'scope_note': 'This preview validates the same
            storefront-backed order path used for live VM purchases.', 'submit_path': '/user-api/v2/ordering/submit',
            'normalized_request': {'package_id': 23, 'pricing_id': 12, 'hostname': 'demo1.example.net', 'user': 'debian',
            'ssh_key_present': True, 'module_group_id': 4, 'order_form_id': 1, 'package_group_id': 3, 'coupon_present':
            False}, 'package': {'package_id': 23, 'name': 'NVMe VPS - Starter', 'template': 'debian13-cloud', 'image':
            {'name': 'debian13-cloud', 'display_name': 'Debian 13 Cloud', 'default_user': 'debian', 'cloudinit': True},
            'specs': {'cpu': 1, 'memory_mb': 2048, 'disk_gb': 40, 'bandwidth_gb': 4000, 'ipv4': 1, 'ipv6': 1},
            'backup_limit': 3, 'snapshot_limit': 5, 'module_groups': [{'id': 4, 'name': 'Katy, Texas'}],
            'module_group_required': False, 'order_path': {'order_form_id': 1, 'order_form_label': 'NVME',
            'package_group_id': 3}}, 'billing': {'pricing_id': 12, 'term': 1, 'period': 'month', 'price': '11.99', 'renew':
            '11.99', 'setup_fee': '0.00', 'currency': 'USD', 'initial_due': '11.99', 'renewal_amount': '11.99'},
            'provisioning': {'hostname': 'demo1.example.net', 'user': 'debian', 'template': 'debian13-cloud',
            'supports_ssh_key': True, 'supports_user_override': True, 'module_group_id': 4}, 'warnings': ['This preview does
            not reserve capacity or collect payment.', 'Provisioning still waits for the created order to be accepted and
            the invoice to be paid.']}

    Attributes:
        lnvps_compatible (bool):  Example: True.
        order_submission_supported (bool):  Example: True.
        scope_note (str):  Example: This preview validates the same storefront-backed order path used for live VM
            purchases..
        submit_path (str):  Example: /user-api/v2/ordering/submit.
        normalized_request (VmOrderNormalizedRequest):
        package (VmOrderSelectedPackage):
        billing (VmOrderBillingPreview):
        provisioning (VmOrderProvisioningPreview):
        warnings (list[str]):  Example: ['This preview does not reserve capacity or collect payment.', 'Provisioning
            still waits for the created order to be accepted and the invoice to be paid.'].
    """

    lnvps_compatible: bool
    order_submission_supported: bool
    scope_note: str
    submit_path: str
    normalized_request: VmOrderNormalizedRequest
    package: VmOrderSelectedPackage
    billing: VmOrderBillingPreview
    provisioning: VmOrderProvisioningPreview
    warnings: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lnvps_compatible = self.lnvps_compatible

        order_submission_supported = self.order_submission_supported

        scope_note = self.scope_note

        submit_path = self.submit_path

        normalized_request = self.normalized_request.to_dict()

        package = self.package.to_dict()

        billing = self.billing.to_dict()

        provisioning = self.provisioning.to_dict()

        warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lnvps_compatible": lnvps_compatible,
                "order_submission_supported": order_submission_supported,
                "scope_note": scope_note,
                "submit_path": submit_path,
                "normalized_request": normalized_request,
                "package": package,
                "billing": billing,
                "provisioning": provisioning,
                "warnings": warnings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_order_billing_preview import VmOrderBillingPreview
        from ..models.vm_order_normalized_request import VmOrderNormalizedRequest
        from ..models.vm_order_provisioning_preview import VmOrderProvisioningPreview
        from ..models.vm_order_selected_package import VmOrderSelectedPackage

        d = dict(src_dict)
        lnvps_compatible = d.pop("lnvps_compatible")

        order_submission_supported = d.pop("order_submission_supported")

        scope_note = d.pop("scope_note")

        submit_path = d.pop("submit_path")

        normalized_request = VmOrderNormalizedRequest.from_dict(
            d.pop("normalized_request")
        )

        package = VmOrderSelectedPackage.from_dict(d.pop("package"))

        billing = VmOrderBillingPreview.from_dict(d.pop("billing"))

        provisioning = VmOrderProvisioningPreview.from_dict(d.pop("provisioning"))

        warnings = cast(list[str], d.pop("warnings"))

        vm_order_preview = cls(
            lnvps_compatible=lnvps_compatible,
            order_submission_supported=order_submission_supported,
            scope_note=scope_note,
            submit_path=submit_path,
            normalized_request=normalized_request,
            package=package,
            billing=billing,
            provisioning=provisioning,
            warnings=warnings,
        )

        vm_order_preview.additional_properties = d
        return vm_order_preview

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
