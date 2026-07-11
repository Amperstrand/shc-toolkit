from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.module_group_choice import ModuleGroupChoice
    from ..models.template import Template


T = TypeVar("T", bound="VmOrderSubmitResponsePackage")


@_attrs_define
class VmOrderSubmitResponsePackage:
    """
    Attributes:
        package_id (int):  Example: 23.
        name (str):  Example: NVMe VPS - Starter.
        template (None | str):  Example: debian13-cloud.
        image (None | Template):
        module_groups (list[ModuleGroupChoice]):
        module_group_required (bool):
    """

    package_id: int
    name: str
    template: None | str
    image: None | Template
    module_groups: list[ModuleGroupChoice]
    module_group_required: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.template import Template

        package_id = self.package_id

        name = self.name

        template: None | str
        template = self.template

        image: dict[str, Any] | None
        if isinstance(self.image, Template):
            image = self.image.to_dict()
        else:
            image = self.image

        module_groups = []
        for module_groups_item_data in self.module_groups:
            module_groups_item = module_groups_item_data.to_dict()
            module_groups.append(module_groups_item)

        module_group_required = self.module_group_required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "package_id": package_id,
                "name": name,
                "template": template,
                "image": image,
                "module_groups": module_groups,
                "module_group_required": module_group_required,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.module_group_choice import ModuleGroupChoice
        from ..models.template import Template

        d = dict(src_dict)
        package_id = d.pop("package_id")

        name = d.pop("name")

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

        module_groups = []
        _module_groups = d.pop("module_groups")
        for module_groups_item_data in _module_groups:
            module_groups_item = ModuleGroupChoice.from_dict(module_groups_item_data)

            module_groups.append(module_groups_item)

        module_group_required = d.pop("module_group_required")

        vm_order_submit_response_package = cls(
            package_id=package_id,
            name=name,
            template=template,
            image=image,
            module_groups=module_groups,
            module_group_required=module_group_required,
        )

        vm_order_submit_response_package.additional_properties = d
        return vm_order_submit_response_package

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
