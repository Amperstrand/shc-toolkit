from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.agent_session_proof_of_possession import AgentSessionProofOfPossession
from ..models.agent_session_scope import AgentSessionScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentSession")


@_attrs_define
class AgentSession:
    """
    Attributes:
        session_id (str):
        agent_id (str):
        agent_name (str):
        agent_purpose (str):
        key_prefix (str):
        scope (AgentSessionScope):
        proof_of_possession (AgentSessionProofOfPossession):
        created_at (datetime.datetime):
        expires_at (datetime.datetime):
        revoked_at (datetime.datetime | None):
        public_key (None | str | Unset):
        last_used_at (datetime.datetime | None | Unset):
    """

    session_id: str
    agent_id: str
    agent_name: str
    agent_purpose: str
    key_prefix: str
    scope: AgentSessionScope
    proof_of_possession: AgentSessionProofOfPossession
    created_at: datetime.datetime
    expires_at: datetime.datetime
    revoked_at: datetime.datetime | None
    public_key: None | str | Unset = UNSET
    last_used_at: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        agent_id = self.agent_id

        agent_name = self.agent_name

        agent_purpose = self.agent_purpose

        key_prefix = self.key_prefix

        scope = self.scope.value

        proof_of_possession = self.proof_of_possession.value

        created_at = self.created_at.isoformat()

        expires_at = self.expires_at.isoformat()

        revoked_at: None | str
        if isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        public_key: None | str | Unset
        if isinstance(self.public_key, Unset):
            public_key = UNSET
        else:
            public_key = self.public_key

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        elif isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "sessionId": session_id,
                "agentId": agent_id,
                "agentName": agent_name,
                "agentPurpose": agent_purpose,
                "keyPrefix": key_prefix,
                "scope": scope,
                "proofOfPossession": proof_of_possession,
                "createdAt": created_at,
                "expiresAt": expires_at,
                "revokedAt": revoked_at,
            }
        )
        if public_key is not UNSET:
            field_dict["publicKey"] = public_key
        if last_used_at is not UNSET:
            field_dict["lastUsedAt"] = last_used_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        session_id = d.pop("sessionId")

        agent_id = d.pop("agentId")

        agent_name = d.pop("agentName")

        agent_purpose = d.pop("agentPurpose")

        key_prefix = d.pop("keyPrefix")

        scope = AgentSessionScope(d.pop("scope"))

        proof_of_possession = AgentSessionProofOfPossession(d.pop("proofOfPossession"))

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))

        def _parse_revoked_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = datetime.datetime.fromisoformat(data)

                return revoked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        revoked_at = _parse_revoked_at(d.pop("revokedAt"))

        def _parse_public_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        public_key = _parse_public_key(d.pop("publicKey", UNSET))

        def _parse_last_used_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_used_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("lastUsedAt", UNSET))

        agent_session = cls(
            session_id=session_id,
            agent_id=agent_id,
            agent_name=agent_name,
            agent_purpose=agent_purpose,
            key_prefix=key_prefix,
            scope=scope,
            proof_of_possession=proof_of_possession,
            created_at=created_at,
            expires_at=expires_at,
            revoked_at=revoked_at,
            public_key=public_key,
            last_used_at=last_used_at,
        )

        return agent_session
