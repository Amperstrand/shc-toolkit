from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmFirewallRule")


@_attrs_define
class VmFirewallRule:
    """A single firewall rule. Field names mirror the Proxmox rule object as consumed by the client portal; 'type' is the
    rule direction (in/out).

        Attributes:
            pos (int | None | Unset): Rule position (ordering key). Positions renumber when a rule is deleted.
            type_ (None | str | Unset): Rule direction (in or out).
            action (None | str | Unset): Rule action (ACCEPT, DROP, or REJECT).
            comment (None | str | Unset): Rule comment / name.
            enable (int | None | Unset): 1 if the rule is enabled, 0 otherwise.
            macro (None | str | Unset): Applied macro, if any.
            iface (None | str | Unset): Bound network interface, if any.
            proto (None | str | Unset): Protocol, if any.
            source (None | str | Unset): Source address/CIDR, if any.
            sport (None | str | Unset): Source port, if any.
            dest (None | str | Unset): Destination address/CIDR, if any.
            dport (None | str | Unset): Destination port, if any.
            icmp_type (None | str | Unset): ICMP type, if any.
    """

    pos: int | None | Unset = UNSET
    type_: None | str | Unset = UNSET
    action: None | str | Unset = UNSET
    comment: None | str | Unset = UNSET
    enable: int | None | Unset = UNSET
    macro: None | str | Unset = UNSET
    iface: None | str | Unset = UNSET
    proto: None | str | Unset = UNSET
    source: None | str | Unset = UNSET
    sport: None | str | Unset = UNSET
    dest: None | str | Unset = UNSET
    dport: None | str | Unset = UNSET
    icmp_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pos: int | None | Unset
        if isinstance(self.pos, Unset):
            pos = UNSET
        else:
            pos = self.pos

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        action: None | str | Unset
        if isinstance(self.action, Unset):
            action = UNSET
        else:
            action = self.action

        comment: None | str | Unset
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        enable: int | None | Unset
        if isinstance(self.enable, Unset):
            enable = UNSET
        else:
            enable = self.enable

        macro: None | str | Unset
        if isinstance(self.macro, Unset):
            macro = UNSET
        else:
            macro = self.macro

        iface: None | str | Unset
        if isinstance(self.iface, Unset):
            iface = UNSET
        else:
            iface = self.iface

        proto: None | str | Unset
        if isinstance(self.proto, Unset):
            proto = UNSET
        else:
            proto = self.proto

        source: None | str | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        sport: None | str | Unset
        if isinstance(self.sport, Unset):
            sport = UNSET
        else:
            sport = self.sport

        dest: None | str | Unset
        if isinstance(self.dest, Unset):
            dest = UNSET
        else:
            dest = self.dest

        dport: None | str | Unset
        if isinstance(self.dport, Unset):
            dport = UNSET
        else:
            dport = self.dport

        icmp_type: None | str | Unset
        if isinstance(self.icmp_type, Unset):
            icmp_type = UNSET
        else:
            icmp_type = self.icmp_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pos is not UNSET:
            field_dict["pos"] = pos
        if type_ is not UNSET:
            field_dict["type"] = type_
        if action is not UNSET:
            field_dict["action"] = action
        if comment is not UNSET:
            field_dict["comment"] = comment
        if enable is not UNSET:
            field_dict["enable"] = enable
        if macro is not UNSET:
            field_dict["macro"] = macro
        if iface is not UNSET:
            field_dict["iface"] = iface
        if proto is not UNSET:
            field_dict["proto"] = proto
        if source is not UNSET:
            field_dict["source"] = source
        if sport is not UNSET:
            field_dict["sport"] = sport
        if dest is not UNSET:
            field_dict["dest"] = dest
        if dport is not UNSET:
            field_dict["dport"] = dport
        if icmp_type is not UNSET:
            field_dict["icmp-type"] = icmp_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_pos(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        pos = _parse_pos(d.pop("pos", UNSET))

        def _parse_type_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_action(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        action = _parse_action(d.pop("action", UNSET))

        def _parse_comment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        comment = _parse_comment(d.pop("comment", UNSET))

        def _parse_enable(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        enable = _parse_enable(d.pop("enable", UNSET))

        def _parse_macro(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        macro = _parse_macro(d.pop("macro", UNSET))

        def _parse_iface(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        iface = _parse_iface(d.pop("iface", UNSET))

        def _parse_proto(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        proto = _parse_proto(d.pop("proto", UNSET))

        def _parse_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

        def _parse_sport(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sport = _parse_sport(d.pop("sport", UNSET))

        def _parse_dest(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dest = _parse_dest(d.pop("dest", UNSET))

        def _parse_dport(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dport = _parse_dport(d.pop("dport", UNSET))

        def _parse_icmp_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        icmp_type = _parse_icmp_type(d.pop("icmp-type", UNSET))

        vm_firewall_rule = cls(
            pos=pos,
            type_=type_,
            action=action,
            comment=comment,
            enable=enable,
            macro=macro,
            iface=iface,
            proto=proto,
            source=source,
            sport=sport,
            dest=dest,
            dport=dport,
            icmp_type=icmp_type,
        )

        vm_firewall_rule.additional_properties = d
        return vm_firewall_rule

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
