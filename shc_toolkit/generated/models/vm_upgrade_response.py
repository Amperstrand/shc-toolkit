from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vm_upgrade_response_change import VmUpgradeResponseChange
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.next_checkout import NextCheckout
    from ..models.vm_upgrade_response_amount_due import VmUpgradeResponseAmountDue


T = TypeVar("T", bound="VmUpgradeResponse")


@_attrs_define
class VmUpgradeResponse:
    """Result of an accepted (queued) package change. change is always "queued"; the prorated invoice_id is awaiting
    payment and the change is applied by cron once that invoice is paid.

        Attributes:
            service_id (int):  Example: 456.
            change (VmUpgradeResponseChange):  Example: queued.
            invoice_id (int): The prorated invoice awaiting payment. Example: 9012.
            amount_due (VmUpgradeResponseAmountDue):
            new_plan_label (str):  Example: SSD VPS - Professional.
            new_recurring_amount (str): New recurring amount (base + ALL merged config-option recurring). Example: 20.00.
            next_ (NextCheckout | Unset): Checkout pointer for a payment-gated, queued change (package upgrade).
    """

    service_id: int
    change: VmUpgradeResponseChange
    invoice_id: int
    amount_due: VmUpgradeResponseAmountDue
    new_plan_label: str
    new_recurring_amount: str
    next_: NextCheckout | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        change = self.change.value

        invoice_id = self.invoice_id

        amount_due = self.amount_due.to_dict()

        new_plan_label = self.new_plan_label

        new_recurring_amount = self.new_recurring_amount

        next_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_, Unset):
            next_ = self.next_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "change": change,
                "invoice_id": invoice_id,
                "amount_due": amount_due,
                "new_plan_label": new_plan_label,
                "new_recurring_amount": new_recurring_amount,
            }
        )
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.next_checkout import NextCheckout
        from ..models.vm_upgrade_response_amount_due import VmUpgradeResponseAmountDue

        d = dict(src_dict)
        service_id = d.pop("service_id")

        change = VmUpgradeResponseChange(d.pop("change"))

        invoice_id = d.pop("invoice_id")

        amount_due = VmUpgradeResponseAmountDue.from_dict(d.pop("amount_due"))

        new_plan_label = d.pop("new_plan_label")

        new_recurring_amount = d.pop("new_recurring_amount")

        _next_ = d.pop("next", UNSET)
        next_: NextCheckout | Unset
        if isinstance(_next_, Unset):
            next_ = UNSET
        else:
            next_ = NextCheckout.from_dict(_next_)

        vm_upgrade_response = cls(
            service_id=service_id,
            change=change,
            invoice_id=invoice_id,
            amount_due=amount_due,
            new_plan_label=new_plan_label,
            new_recurring_amount=new_recurring_amount,
            next_=next_,
        )

        vm_upgrade_response.additional_properties = d
        return vm_upgrade_response

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
