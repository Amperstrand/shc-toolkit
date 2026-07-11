from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vm_upgrade_preview_response_applies import VmUpgradePreviewResponseApplies
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_upgrade_preview_line import VmUpgradePreviewLine


T = TypeVar("T", bound="VmUpgradePreviewResponse")


@_attrs_define
class VmUpgradePreviewResponse:
    """Prorated quote (no charge). amount_due_now already includes any setup fee. applies is always "queued" (the change is
    created queued, awaiting payment).

        Attributes:
            service_id (int):  Example: 456.
            new_plan_label (str):  Example: SSD VPS - Professional.
            items (list[VmUpgradePreviewLine]):
            amount_due_now (str): Amount due now (includes setup fee). 0.00 when nothing is owed. Example: 8.00.
            new_recurring_amount (str): New recurring amount = base renewal + config-option recurring totals. Example:
                20.00.
            currency (str):  Example: USD.
            applies (VmUpgradePreviewResponseApplies):  Example: queued.
            discounts (list[VmUpgradePreviewLine] | Unset):
            prorate_credit (str | Unset): Prorated credit for a downgrade, only when account credit is enabled (else 0.00).
                Example: 0.00.
            setup_fee_total (str | Unset): Discrete setup-fee subtotal, only when the presenter exposes it (already in
                amount_due_now). Example: 0.00.
    """

    service_id: int
    new_plan_label: str
    items: list[VmUpgradePreviewLine]
    amount_due_now: str
    new_recurring_amount: str
    currency: str
    applies: VmUpgradePreviewResponseApplies
    discounts: list[VmUpgradePreviewLine] | Unset = UNSET
    prorate_credit: str | Unset = UNSET
    setup_fee_total: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        new_plan_label = self.new_plan_label

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        amount_due_now = self.amount_due_now

        new_recurring_amount = self.new_recurring_amount

        currency = self.currency

        applies = self.applies.value

        discounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.discounts, Unset):
            discounts = []
            for discounts_item_data in self.discounts:
                discounts_item = discounts_item_data.to_dict()
                discounts.append(discounts_item)

        prorate_credit = self.prorate_credit

        setup_fee_total = self.setup_fee_total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "new_plan_label": new_plan_label,
                "items": items,
                "amount_due_now": amount_due_now,
                "new_recurring_amount": new_recurring_amount,
                "currency": currency,
                "applies": applies,
            }
        )
        if discounts is not UNSET:
            field_dict["discounts"] = discounts
        if prorate_credit is not UNSET:
            field_dict["prorate_credit"] = prorate_credit
        if setup_fee_total is not UNSET:
            field_dict["setup_fee_total"] = setup_fee_total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_upgrade_preview_line import VmUpgradePreviewLine

        d = dict(src_dict)
        service_id = d.pop("service_id")

        new_plan_label = d.pop("new_plan_label")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = VmUpgradePreviewLine.from_dict(items_item_data)

            items.append(items_item)

        amount_due_now = d.pop("amount_due_now")

        new_recurring_amount = d.pop("new_recurring_amount")

        currency = d.pop("currency")

        applies = VmUpgradePreviewResponseApplies(d.pop("applies"))

        _discounts = d.pop("discounts", UNSET)
        discounts: list[VmUpgradePreviewLine] | Unset = UNSET
        if _discounts is not UNSET:
            discounts = []
            for discounts_item_data in _discounts:
                discounts_item = VmUpgradePreviewLine.from_dict(discounts_item_data)

                discounts.append(discounts_item)

        prorate_credit = d.pop("prorate_credit", UNSET)

        setup_fee_total = d.pop("setup_fee_total", UNSET)

        vm_upgrade_preview_response = cls(
            service_id=service_id,
            new_plan_label=new_plan_label,
            items=items,
            amount_due_now=amount_due_now,
            new_recurring_amount=new_recurring_amount,
            currency=currency,
            applies=applies,
            discounts=discounts,
            prorate_credit=prorate_credit,
            setup_fee_total=setup_fee_total,
        )

        vm_upgrade_preview_response.additional_properties = d
        return vm_upgrade_preview_response

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
