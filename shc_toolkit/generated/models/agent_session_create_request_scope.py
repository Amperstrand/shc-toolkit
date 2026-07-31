from typing import Literal

AgentSessionCreateRequestScope = Literal["operate", "read"]

AGENT_SESSION_CREATE_REQUEST_SCOPE_VALUES: set[AgentSessionCreateRequestScope] = {
    "operate",
    "read",
}


def check_agent_session_create_request_scope(
    value: str,
) -> AgentSessionCreateRequestScope:
    if value in AGENT_SESSION_CREATE_REQUEST_SCOPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_SESSION_CREATE_REQUEST_SCOPE_VALUES!r}"
    )
