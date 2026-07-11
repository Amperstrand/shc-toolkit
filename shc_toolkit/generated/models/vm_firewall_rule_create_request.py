from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.vm_firewall_rule_create_request_action import (
    VmFirewallRuleCreateRequestAction,
)
from ..models.vm_firewall_rule_create_request_direction import (
    VmFirewallRuleCreateRequestDirection,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="VmFirewallRuleCreateRequest")


@_attrs_define
class VmFirewallRuleCreateRequest:
    """Create a firewall rule. `action` and `direction` are required; all other fields are optional. The raw Proxmox `type`
    key is rejected (use `direction`).

        Example:
            {'action': 'DROP', 'direction': 'in', 'source': '203.0.113.99', 'name': 'block-scanner'}

        Attributes:
            action (VmFirewallRuleCreateRequestAction): Rule action. v2.4.0: case-INSENSITIVE on input (accept/Drop/REJECT
                all valid); always canonical UPPERCASE on output. Example: DROP.
            direction (VmFirewallRuleCreateRequestDirection): Rule direction. (Security-group rules cannot be created/edited
                via the API.) Example: in.
            name (None | str | Unset): Optional rule comment / name. Example: block-scanner.
            source (None | str | Unset): Source address: IP, CIDR, or an IPSet/alias name (comma-separated tokens allowed).
                Example: 203.0.113.99.
            source_port (None | str | Unset): Source port: a port, a `lo:hi` range, a comma list, or a service name.
                Example: 1024:65535.
            dest (None | str | Unset): Destination address: IP, CIDR, or an IPSet/alias name. Example: 10.0.0.5.
            dest_port (None | str | Unset): Destination port: a port, a `lo:hi` range, a comma list, or a service name.
                Example: 22.
            protocol (None | str | Unset): Protocol name (tcp, udp, icmp, ...) or a numeric protocol id 0-255. Example: tcp.
            macro (None | str | Unset): A firewall macro name from GET /vm/{serviceId}/firewall, or `none` for no macro.
                Example: SSH.
            interface (None | str | Unset): Bind to a VM network interface name (e.g. net0). Example: net0.
            icmp_type (None | str | Unset): ICMP type, from the firewall vocabulary (GET /vm/{serviceId}/firewall
                `icmp_types`). Example: echo-request.
            enabled (bool | Unset): Whether the rule is enabled. Accepts a JSON boolean or on/off/true/false/1/0. Defaults
                to true on create; on edit, omitting it keeps the current state. Example: True.
    """

    action: VmFirewallRuleCreateRequestAction
    direction: VmFirewallRuleCreateRequestDirection
    name: None | str | Unset = UNSET
    source: None | str | Unset = UNSET
    source_port: None | str | Unset = UNSET
    dest: None | str | Unset = UNSET
    dest_port: None | str | Unset = UNSET
    protocol: None | str | Unset = UNSET
    macro: None | str | Unset = UNSET
    interface: None | str | Unset = UNSET
    icmp_type: None | str | Unset = UNSET
    enabled: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        direction = self.direction.value

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        source: None | str | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        source_port: None | str | Unset
        if isinstance(self.source_port, Unset):
            source_port = UNSET
        else:
            source_port = self.source_port

        dest: None | str | Unset
        if isinstance(self.dest, Unset):
            dest = UNSET
        else:
            dest = self.dest

        dest_port: None | str | Unset
        if isinstance(self.dest_port, Unset):
            dest_port = UNSET
        else:
            dest_port = self.dest_port

        protocol: None | str | Unset
        if isinstance(self.protocol, Unset):
            protocol = UNSET
        else:
            protocol = self.protocol

        macro: None | str | Unset
        if isinstance(self.macro, Unset):
            macro = UNSET
        else:
            macro = self.macro

        interface: None | str | Unset
        if isinstance(self.interface, Unset):
            interface = UNSET
        else:
            interface = self.interface

        icmp_type: None | str | Unset
        if isinstance(self.icmp_type, Unset):
            icmp_type = UNSET
        else:
            icmp_type = self.icmp_type

        enabled = self.enabled

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "action": action,
                "direction": direction,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if source is not UNSET:
            field_dict["source"] = source
        if source_port is not UNSET:
            field_dict["source_port"] = source_port
        if dest is not UNSET:
            field_dict["dest"] = dest
        if dest_port is not UNSET:
            field_dict["dest_port"] = dest_port
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if macro is not UNSET:
            field_dict["macro"] = macro
        if interface is not UNSET:
            field_dict["interface"] = interface
        if icmp_type is not UNSET:
            field_dict["icmp-type"] = icmp_type
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = VmFirewallRuleCreateRequestAction(d.pop("action"))

        direction = VmFirewallRuleCreateRequestDirection(d.pop("direction"))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

        def _parse_source_port(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_port = _parse_source_port(d.pop("source_port", UNSET))

        def _parse_dest(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dest = _parse_dest(d.pop("dest", UNSET))

        def _parse_dest_port(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dest_port = _parse_dest_port(d.pop("dest_port", UNSET))

        def _parse_protocol(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        protocol = _parse_protocol(d.pop("protocol", UNSET))

        def _parse_macro(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        macro = _parse_macro(d.pop("macro", UNSET))

        def _parse_interface(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        interface = _parse_interface(d.pop("interface", UNSET))

        def _parse_icmp_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        icmp_type = _parse_icmp_type(d.pop("icmp-type", UNSET))

        enabled = d.pop("enabled", UNSET)

        vm_firewall_rule_create_request = cls(
            action=action,
            direction=direction,
            name=name,
            source=source,
            source_port=source_port,
            dest=dest,
            dest_port=dest_port,
            protocol=protocol,
            macro=macro,
            interface=interface,
            icmp_type=icmp_type,
            enabled=enabled,
        )

        return vm_firewall_rule_create_request
