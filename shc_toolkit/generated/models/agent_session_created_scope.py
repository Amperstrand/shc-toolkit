from typing import Literal

AgentSessionCreatedScope = Literal["operate", "read"]

AGENT_SESSION_CREATED_SCOPE_VALUES: set[AgentSessionCreatedScope] = {
    "operate",
    "read",
}


def check_agent_session_created_scope(value: str) -> AgentSessionCreatedScope:
    if value in AGENT_SESSION_CREATED_SCOPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_SESSION_CREATED_SCOPE_VALUES!r}"
    )
