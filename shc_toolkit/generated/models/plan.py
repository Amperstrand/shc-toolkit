from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.plan_pricing import PlanPricing
    from ..models.template import Template


T = TypeVar("T", bound="Plan")


@_attrs_define
class Plan:
    """Package metadata plus pricing rows returned by descriptive catalog endpoints.

    Example:
        {'package_id': 7, 'name': 'NVMe VPS - Standard', 'cpu': 2, 'memory_mb': 4096, 'disk_gb': 80, 'bandwidth_gb':
            4000, 'ipv4': 1, 'ipv6': 1, 'template': 'debian13-cloud', 'image': {'name': 'debian13-cloud', 'display_name':
            'Debian 13 Cloud', 'default_user': 'debian', 'cloudinit': True}, 'backup_limit': 3, 'snapshot_limit': 5,
            'pricing': [{'pricing_id': 12, 'term': 1, 'period': 'month', 'price': '11.99', 'renew': '11.99', 'setup_fee':
            '0.00', 'currency': 'USD'}, {'pricing_id': 13, 'term': 12, 'period': 'month', 'price': '119.00', 'renew':
            '119.00', 'setup_fee': '0.00', 'currency': 'USD'}]}

    """

    package_id: int
    """ Blesta package identifier for this plan family. """
    name: str
    """ Customer-facing package or plan name. """
    cpu: int
    """ vCPU count advertised for the package. """
    memory_mb: int
    """ Advertised memory allocation in megabytes. """
    disk_gb: int
    """ Advertised disk allocation in gigabytes. """
    bandwidth_gb: int
    """ Advertised transfer allowance in gigabytes. """
    ipv4: int
    """ Advertised IPv4 allocation count. """
    ipv6: int
    """ Advertised IPv6 allocation count. """
    template: None | str
    """ Default template identifier associated with the package, if present. """
    image: None | Template
    """ Expanded image metadata for the package template. """
    backup_limit: int
    """ Advertised backup limit for the package. """
    snapshot_limit: int
    """ Advertised snapshot limit for the package. """
    pricing: list[PlanPricing]
    """ Available billing cadences for this package. """
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
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
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

        plan = cls(
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
        )

        plan.additional_properties = d
        return plan

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
