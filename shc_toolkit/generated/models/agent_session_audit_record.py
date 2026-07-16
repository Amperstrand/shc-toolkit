from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_session_audit_record_data import AgentSessionAuditRecordData


T = TypeVar("T", bound="AgentSessionAuditRecord")


@_attrs_define
class AgentSessionAuditRecord:
    """
    Attributes:
        audit_id (str):
        session_id (str):
        agent_id (str):
        time (datetime.datetime):
        action (str):
        method (str):
        path (str):
        status (int):
        data (AgentSessionAuditRecordData): Includes tamperEvidence when the audit row carries prevEventHash and
            eventHash.
        traceparent (None | str | Unset):
        subject (None | str | Unset):
        message (None | str | Unset):
    """

    audit_id: str
    session_id: str
    agent_id: str
    time: datetime.datetime
    action: str
    method: str
    path: str
    status: int
    data: AgentSessionAuditRecordData
    traceparent: None | str | Unset = UNSET
    subject: None | str | Unset = UNSET
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        audit_id = self.audit_id

        session_id = self.session_id

        agent_id = self.agent_id

        time = self.time.isoformat()

        action = self.action

        method = self.method

        path = self.path

        status = self.status

        data = self.data.to_dict()

        traceparent: None | str | Unset
        if isinstance(self.traceparent, Unset):
            traceparent = UNSET
        else:
            traceparent = self.traceparent

        subject: None | str | Unset
        if isinstance(self.subject, Unset):
            subject = UNSET
        else:
            subject = self.subject

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "auditId": audit_id,
                "sessionId": session_id,
                "agentId": agent_id,
                "time": time,
                "action": action,
                "method": method,
                "path": path,
                "status": status,
                "data": data,
            }
        )
        if traceparent is not UNSET:
            field_dict["traceparent"] = traceparent
        if subject is not UNSET:
            field_dict["subject"] = subject
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_session_audit_record_data import AgentSessionAuditRecordData

        d = dict(src_dict)
        audit_id = d.pop("auditId")

        session_id = d.pop("sessionId")

        agent_id = d.pop("agentId")

        time = datetime.datetime.fromisoformat(d.pop("time"))

        action = d.pop("action")

        method = d.pop("method")

        path = d.pop("path")

        status = d.pop("status")

        data = AgentSessionAuditRecordData.from_dict(d.pop("data"))

        def _parse_traceparent(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        traceparent = _parse_traceparent(d.pop("traceparent", UNSET))

        def _parse_subject(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subject = _parse_subject(d.pop("subject", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        agent_session_audit_record = cls(
            audit_id=audit_id,
            session_id=session_id,
            agent_id=agent_id,
            time=time,
            action=action,
            method=method,
            path=path,
            status=status,
            data=data,
            traceparent=traceparent,
            subject=subject,
            message=message,
        )

        return agent_session_audit_record
