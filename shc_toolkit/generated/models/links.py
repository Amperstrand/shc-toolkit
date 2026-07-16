from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link_target import LinkTarget


T = TypeVar("T", bound="Links")


@_attrs_define
class Links:
    """Hypermedia links keyed by IANA-registered link relation names.

    Attributes:
        self_ (LinkTarget | Unset): Typed hypermedia target. Relation names are carried by the containing Links object
            and use IANA-registered rels.
        next_ (LinkTarget | Unset): Typed hypermedia target. Relation names are carried by the containing Links object
            and use IANA-registered rels.
        related (list[LinkTarget] | Unset):
        status (LinkTarget | Unset): Typed hypermedia target. Relation names are carried by the containing Links object
            and use IANA-registered rels.
        about (LinkTarget | Unset): Typed hypermedia target. Relation names are carried by the containing Links object
            and use IANA-registered rels.
        help_ (LinkTarget | Unset): Typed hypermedia target. Relation names are carried by the containing Links object
            and use IANA-registered rels.
    """

    self_: LinkTarget | Unset = UNSET
    next_: LinkTarget | Unset = UNSET
    related: list[LinkTarget] | Unset = UNSET
    status: LinkTarget | Unset = UNSET
    about: LinkTarget | Unset = UNSET
    help_: LinkTarget | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        self_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.self_, Unset):
            self_ = self.self_.to_dict()

        next_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_, Unset):
            next_ = self.next_.to_dict()

        related: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.related, Unset):
            related = []
            for related_item_data in self.related:
                related_item = related_item_data.to_dict()
                related.append(related_item)

        status: dict[str, Any] | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        about: dict[str, Any] | Unset = UNSET
        if not isinstance(self.about, Unset):
            about = self.about.to_dict()

        help_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.help_, Unset):
            help_ = self.help_.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if next_ is not UNSET:
            field_dict["next"] = next_
        if related is not UNSET:
            field_dict["related"] = related
        if status is not UNSET:
            field_dict["status"] = status
        if about is not UNSET:
            field_dict["about"] = about
        if help_ is not UNSET:
            field_dict["help"] = help_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.link_target import LinkTarget

        d = dict(src_dict)
        _self_ = d.pop("self", UNSET)
        self_: LinkTarget | Unset
        if isinstance(_self_, Unset):
            self_ = UNSET
        else:
            self_ = LinkTarget.from_dict(_self_)

        _next_ = d.pop("next", UNSET)
        next_: LinkTarget | Unset
        if isinstance(_next_, Unset):
            next_ = UNSET
        else:
            next_ = LinkTarget.from_dict(_next_)

        _related = d.pop("related", UNSET)
        related: list[LinkTarget] | Unset = UNSET
        if _related is not UNSET:
            related = []
            for related_item_data in _related:
                related_item = LinkTarget.from_dict(related_item_data)

                related.append(related_item)

        _status = d.pop("status", UNSET)
        status: LinkTarget | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = LinkTarget.from_dict(_status)

        _about = d.pop("about", UNSET)
        about: LinkTarget | Unset
        if isinstance(_about, Unset):
            about = UNSET
        else:
            about = LinkTarget.from_dict(_about)

        _help_ = d.pop("help", UNSET)
        help_: LinkTarget | Unset
        if isinstance(_help_, Unset):
            help_ = UNSET
        else:
            help_ = LinkTarget.from_dict(_help_)

        links = cls(
            self_=self_,
            next_=next_,
            related=related,
            status=status,
            about=about,
            help_=help_,
        )

        return links
