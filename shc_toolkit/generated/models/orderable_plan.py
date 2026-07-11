from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.module_group_choice import ModuleGroupChoice
    from ..models.order_path_summary import OrderPathSummary
    from ..models.plan_pricing import PlanPricing
    from ..models.template import Template


T = TypeVar("T", bound="OrderablePlan")


@_attrs_define
class OrderablePlan:
    """
    Example:
        {'package_id': 23, 'name': 'NVMe VPS - Starter', 'cpu': 1, 'memory_mb': 2048, 'disk_gb': 40, 'bandwidth_gb':
            4000, 'ipv4': 1, 'ipv6': 1, 'template': 'debian13-cloud', 'image': {'name': 'debian13-cloud', 'display_name':
            'Debian 13 Cloud', 'default_user': 'debian', 'cloudinit': True}, 'backup_limit': 3, 'snapshot_limit': 5,
            'pricing': [{'pricing_id': 12, 'term': 1, 'period': 'month', 'price': '11.99', 'renew': '11.99', 'setup_fee':
            '0.00', 'currency': 'USD'}], 'module_groups': [{'id': 4, 'name': 'Katy, Texas'}], 'default_module_group_id': 4,
            'module_group_required': False, 'order_form_id': 1, 'order_form_label': 'NVME', 'package_group_id': 3,
            'order_paths': [{'order_form_id': 1, 'order_form_label': 'NVME', 'package_group_id': 3}]}

    Attributes:
        package_id (int): Blesta package identifier for this plan family. Example: 7.
        name (str): Customer-facing package or plan name. Example: NVMe VPS - Standard.
        cpu (int): vCPU count advertised for the package. Example: 2.
        memory_mb (int): Advertised memory allocation in megabytes. Example: 4096.
        disk_gb (int): Advertised disk allocation in gigabytes. Example: 80.
        bandwidth_gb (int): Advertised transfer allowance in gigabytes. Example: 4000.
        ipv4 (int): Advertised IPv4 allocation count. Example: 1.
        ipv6 (int): Advertised IPv6 allocation count. Example: 1.
        template (None | str): Default template identifier associated with the package, if present. Example:
            debian13-cloud.
        image (None | Template): Expanded image metadata for the package template.
        backup_limit (int): Advertised backup limit for the package. Example: 3.
        snapshot_limit (int): Advertised snapshot limit for the package. Example: 5.
        pricing (list[PlanPricing]): Available billing cadences for this package.
        module_groups (list[ModuleGroupChoice]): Selectable location or module-group choices for this package.
        default_module_group_id (int | None): Default module-group selection when the plan only exposes one location or
            has a package default. Example: 4.
        module_group_required (bool): Whether the caller must supply `module_group_id` to disambiguate multiple
            locations.
        order_form_id (int | None): Preferred order form chosen for this package when one is available. Example: 1.
        order_form_label (None | str): Preferred order form label chosen for this package. Example: NVME.
        package_group_id (int | None): Preferred package group used to route the order. Example: 3.
        order_paths (list[OrderPathSummary]): Available storefront paths for this package.
    """

    package_id: int
    name: str
    cpu: int
    memory_mb: int
    disk_gb: int
    bandwidth_gb: int
    ipv4: int
    ipv6: int
    template: None | str
    image: None | Template
    backup_limit: int
    snapshot_limit: int
    pricing: list[PlanPricing]
    module_groups: list[ModuleGroupChoice]
    default_module_group_id: int | None
    module_group_required: bool
    order_form_id: int | None
    order_form_label: None | str
    package_group_id: int | None
    order_paths: list[OrderPathSummary]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.template import Template

        package_id = self.package_id

        name = self.name

        cpu = self.cpu

        memory_mb = self.memory_mb

        disk_gb = self.disk_gb

        bandwidth_gb = self.bandwidth_gb

        ipv4 = self.ipv4

        ipv6 = self.ipv6

        template: None | str
        template = self.template

        image: dict[str, Any] | None
        if isinstance(self.image, Template):
            image = self.image.to_dict()
        else:
            image = self.image

        backup_limit = self.backup_limit

        snapshot_limit = self.snapshot_limit

        pricing = []
        for pricing_item_data in self.pricing:
            pricing_item = pricing_item_data.to_dict()
            pricing.append(pricing_item)

        module_groups = []
        for module_groups_item_data in self.module_groups:
            module_groups_item = module_groups_item_data.to_dict()
            module_groups.append(module_groups_item)

        default_module_group_id: int | None
        default_module_group_id = self.default_module_group_id

        module_group_required = self.module_group_required

        order_form_id: int | None
        order_form_id = self.order_form_id

        order_form_label: None | str
        order_form_label = self.order_form_label

        package_group_id: int | None
        package_group_id = self.package_group_id

        order_paths = []
        for order_paths_item_data in self.order_paths:
            order_paths_item = order_paths_item_data.to_dict()
            order_paths.append(order_paths_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "package_id": package_id,
                "name": name,
                "cpu": cpu,
                "memory_mb": memory_mb,
                "disk_gb": disk_gb,
                "bandwidth_gb": bandwidth_gb,
                "ipv4": ipv4,
                "ipv6": ipv6,
                "template": template,
                "image": image,
                "backup_limit": backup_limit,
                "snapshot_limit": snapshot_limit,
                "pricing": pricing,
                "module_groups": module_groups,
                "default_module_group_id": default_module_group_id,
                "module_group_required": module_group_required,
                "order_form_id": order_form_id,
                "order_form_label": order_form_label,
                "package_group_id": package_group_id,
                "order_paths": order_paths,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.module_group_choice import ModuleGroupChoice
        from ..models.order_path_summary import OrderPathSummary
        from ..models.plan_pricing import PlanPricing
        from ..models.template import Template

        d = dict(src_dict)
        package_id = d.pop("package_id")

        name = d.pop("name")

        cpu = d.pop("cpu")

        memory_mb = d.pop("memory_mb")

        disk_gb = d.pop("disk_gb")

        bandwidth_gb = d.pop("bandwidth_gb")

        ipv4 = d.pop("ipv4")

        ipv6 = d.pop("ipv6")

        def _parse_template(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        template = _parse_template(d.pop("template"))

        def _parse_image(data: object) -> None | Template:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                image_type_0 = Template.from_dict(data)

                return image_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Template, data)

        image = _parse_image(d.pop("image"))

        backup_limit = d.pop("backup_limit")

        snapshot_limit = d.pop("snapshot_limit")

        pricing = []
        _pricing = d.pop("pricing")
        for pricing_item_data in _pricing:
            pricing_item = PlanPricing.from_dict(pricing_item_data)

            pricing.append(pricing_item)

        module_groups = []
        _module_groups = d.pop("module_groups")
        for module_groups_item_data in _module_groups:
            module_groups_item = ModuleGroupChoice.from_dict(module_groups_item_data)

            module_groups.append(module_groups_item)

        def _parse_default_module_group_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        default_module_group_id = _parse_default_module_group_id(
            d.pop("default_module_group_id")
        )

        module_group_required = d.pop("module_group_required")

        def _parse_order_form_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        order_form_id = _parse_order_form_id(d.pop("order_form_id"))

        def _parse_order_form_label(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        order_form_label = _parse_order_form_label(d.pop("order_form_label"))

        def _parse_package_group_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        package_group_id = _parse_package_group_id(d.pop("package_group_id"))

        order_paths = []
        _order_paths = d.pop("order_paths")
        for order_paths_item_data in _order_paths:
            order_paths_item = OrderPathSummary.from_dict(order_paths_item_data)

            order_paths.append(order_paths_item)

        orderable_plan = cls(
            package_id=package_id,
            name=name,
            cpu=cpu,
            memory_mb=memory_mb,
            disk_gb=disk_gb,
            bandwidth_gb=bandwidth_gb,
            ipv4=ipv4,
            ipv6=ipv6,
            template=template,
            image=image,
            backup_limit=backup_limit,
            snapshot_limit=snapshot_limit,
            pricing=pricing,
            module_groups=module_groups,
            default_module_group_id=default_module_group_id,
            module_group_required=module_group_required,
            order_form_id=order_form_id,
            order_form_label=order_form_label,
            package_group_id=package_group_id,
            order_paths=order_paths,
        )

        orderable_plan.additional_properties = d
        return orderable_plan

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
