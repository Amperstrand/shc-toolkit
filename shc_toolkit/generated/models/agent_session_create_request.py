from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.agent_session_create_request_scope import AgentSessionCreateRequestScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentSessionCreateRequest")


@_attrs_define
class AgentSessionCreateRequest:
    """
    Example:
        {'agentName': 'invoice-review-agent', 'agentPurpose': 'Review invoices and open support tickets when approved.',
            'publicKey': '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef', 'scope': 'read'}

    Attributes:
        agent_name (str):
        agent_purpose (str):
        public_key (str): Required Nostr public key for proof-of-possession binding. Hex public keys and npub values are
            accepted; stored sessions verify against the hex public key.
        scope (AgentSessionCreateRequestScope | Unset): read is GET-only. operate can perform allowed non-money
            operations but cannot manage credentials, identity, billing money movement, contacts, managers, or sessions.
            Default: AgentSessionCreateRequestScope.OPERATE.
    """

    agent_name: str
    agent_purpose: str
    public_key: str
    scope: AgentSessionCreateRequestScope | Unset = (
        AgentSessionCreateRequestScope.OPERATE
    )

    def to_dict(self) -> dict[str, Any]:
        agent_name = self.agent_name

        agent_purpose = self.agent_purpose

        public_key = self.public_key

        scope: str | Unset = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agentName": agent_name,
                "agentPurpose": agent_purpose,
                "publicKey": public_key,
            }
        )
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_name = d.pop("agentName")

        agent_purpose = d.pop("agentPurpose")

        public_key = d.pop("publicKey")

        _scope = d.pop("scope", UNSET)
        scope: AgentSessionCreateRequestScope | Unset
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = AgentSessionCreateRequestScope(_scope)

        agent_session_create_request = cls(
            agent_name=agent_name,
            agent_purpose=agent_purpose,
            public_key=public_key,
            scope=scope,
        )

        return agent_session_create_request
