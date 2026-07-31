from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.agent_session_created_scope import (
    AgentSessionCreatedScope,
    check_agent_session_created_scope,
)

T = TypeVar("T", bound="AgentSessionCreated")


@_attrs_define
class AgentSessionCreated:
    session_id: str
    agent_id: str
    token: str
    """ Plaintext shc_agent_ token returned once. """
    key_prefix: str
    scope: AgentSessionCreatedScope
    expires_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        agent_id = self.agent_id

        token = self.token

        key_prefix = self.key_prefix

        scope: str = self.scope

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "sessionId": session_id,
                "agentId": agent_id,
                "token": token,
                "keyPrefix": key_prefix,
                "scope": scope,
                "expiresAt": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        session_id = d.pop("sessionId")

        agent_id = d.pop("agentId")

        token = d.pop("token")

        key_prefix = d.pop("keyPrefix")

        scope = check_agent_session_created_scope(d.pop("scope"))

        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))

        agent_session_created = cls(
            session_id=session_id,
            agent_id=agent_id,
            token=token,
            key_prefix=key_prefix,
            scope=scope,
            expires_at=expires_at,
        )

        return agent_session_created
