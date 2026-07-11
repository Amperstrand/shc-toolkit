from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vm_order_result_status import VmOrderResultStatus

T = TypeVar("T", bound="VmOrderResult")


@_attrs_define
class VmOrderResult:
    """
    Attributes:
        order_id (int):  Example: 901.
        order_number (str):  Example: 1000901.
        status (VmOrderResultStatus): Order lifecycle state from Blesta's order engine. Distinct from service status,
            runtime status, and invoice status. Example: accepted.
        order_form_id (int):  Example: 1.
        order_form_label (str):  Example: NVME.
        package_group_id (int):  Example: 3.
    """

    order_id: int
    order_number: str
    status: VmOrderResultStatus
    order_form_id: int
    order_form_label: str
    package_group_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        order_id = self.order_id

        order_number = self.order_number

        status = self.status.value

        order_form_id = self.order_form_id

        order_form_label = self.order_form_label

        package_group_id = self.package_group_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "order_id": order_id,
                "order_number": order_number,
                "status": status,
                "order_form_id": order_form_id,
                "order_form_label": order_form_label,
                "package_group_id": package_group_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        order_id = d.pop("order_id")

        order_number = d.pop("order_number")

        status = VmOrderResultStatus(d.pop("status"))

        order_form_id = d.pop("order_form_id")

        order_form_label = d.pop("order_form_label")

        package_group_id = d.pop("package_group_id")

        vm_order_result = cls(
            order_id=order_id,
            order_number=order_number,
            status=status,
            order_form_id=order_form_id,
            order_form_label=order_form_label,
            package_group_id=package_group_id,
        )

        vm_order_result.additional_properties = d
        return vm_order_result

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
