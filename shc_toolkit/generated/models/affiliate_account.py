from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.affiliate_account_stats import AffiliateAccountStats
    from ..models.affiliate_balance import AffiliateBalance
    from ..models.affiliate_program_terms import AffiliateProgramTerms


T = TypeVar("T", bound="AffiliateAccount")


@_attrs_define
class AffiliateAccount:
    """Affiliate account overview. When `enrolled` is false only `enrolled`, `status` (= "not_enrolled"), `eligible`, and
    `program` are present.

        Attributes:
            enrolled (bool):  Example: True.
            status (str): active, inactive, or not_enrolled. Example: active.
            eligible (bool | Unset): Only present when not enrolled: whether the active-service gate is met. Example: True.
            referral_code (str | Unset):  Example: cost-chimney-churn.
            referral_link (str | Unset):  Example: https://blesta.sovereignhybridcompute.com/order/forms/a/cost-chimney-
                churn.
            date_enrolled (datetime.datetime | None | Unset):
            days_active (int | Unset):  Example: 12.
            stats (AffiliateAccountStats | Unset):
            balance (AffiliateBalance | Unset):
            program (AffiliateProgramTerms | Unset): Company-level affiliate program terms (BTC-native).
    """

    enrolled: bool
    status: str
    eligible: bool | Unset = UNSET
    referral_code: str | Unset = UNSET
    referral_link: str | Unset = UNSET
    date_enrolled: datetime.datetime | None | Unset = UNSET
    days_active: int | Unset = UNSET
    stats: AffiliateAccountStats | Unset = UNSET
    balance: AffiliateBalance | Unset = UNSET
    program: AffiliateProgramTerms | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enrolled = self.enrolled

        status = self.status

        eligible = self.eligible

        referral_code = self.referral_code

        referral_link = self.referral_link

        date_enrolled: None | str | Unset
        if isinstance(self.date_enrolled, Unset):
            date_enrolled = UNSET
        elif isinstance(self.date_enrolled, datetime.datetime):
            date_enrolled = self.date_enrolled.isoformat()
        else:
            date_enrolled = self.date_enrolled

        days_active = self.days_active

        stats: dict[str, Any] | Unset = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        balance: dict[str, Any] | Unset = UNSET
        if not isinstance(self.balance, Unset):
            balance = self.balance.to_dict()

        program: dict[str, Any] | Unset = UNSET
        if not isinstance(self.program, Unset):
            program = self.program.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enrolled": enrolled,
                "status": status,
            }
        )
        if eligible is not UNSET:
            field_dict["eligible"] = eligible
        if referral_code is not UNSET:
            field_dict["referral_code"] = referral_code
        if referral_link is not UNSET:
            field_dict["referral_link"] = referral_link
        if date_enrolled is not UNSET:
            field_dict["date_enrolled"] = date_enrolled
        if days_active is not UNSET:
            field_dict["days_active"] = days_active
        if stats is not UNSET:
            field_dict["stats"] = stats
        if balance is not UNSET:
            field_dict["balance"] = balance
        if program is not UNSET:
            field_dict["program"] = program

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.affiliate_account_stats import AffiliateAccountStats
        from ..models.affiliate_balance import AffiliateBalance
        from ..models.affiliate_program_terms import AffiliateProgramTerms

        d = dict(src_dict)
        enrolled = d.pop("enrolled")

        status = d.pop("status")

        eligible = d.pop("eligible", UNSET)

        referral_code = d.pop("referral_code", UNSET)

        referral_link = d.pop("referral_link", UNSET)

        def _parse_date_enrolled(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_enrolled_type_0 = datetime.datetime.fromisoformat(data)

                return date_enrolled_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_enrolled = _parse_date_enrolled(d.pop("date_enrolled", UNSET))

        days_active = d.pop("days_active", UNSET)

        _stats = d.pop("stats", UNSET)
        stats: AffiliateAccountStats | Unset
        if isinstance(_stats, Unset):
            stats = UNSET
        else:
            stats = AffiliateAccountStats.from_dict(_stats)

        _balance = d.pop("balance", UNSET)
        balance: AffiliateBalance | Unset
        if isinstance(_balance, Unset):
            balance = UNSET
        else:
            balance = AffiliateBalance.from_dict(_balance)

        _program = d.pop("program", UNSET)
        program: AffiliateProgramTerms | Unset
        if isinstance(_program, Unset):
            program = UNSET
        else:
            program = AffiliateProgramTerms.from_dict(_program)

        affiliate_account = cls(
            enrolled=enrolled,
            status=status,
            eligible=eligible,
            referral_code=referral_code,
            referral_link=referral_link,
            date_enrolled=date_enrolled,
            days_active=days_active,
            stats=stats,
            balance=balance,
            program=program,
        )

        affiliate_account.additional_properties = d
        return affiliate_account

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
