from typing import Literal

AgentSessionScope = Literal["operate", "read"]

AGENT_SESSION_SCOPE_VALUES: set[AgentSessionScope] = {
    "operate",
    "read",
}


def check_agent_session_scope(value: str) -> AgentSessionScope:
    if value in AGENT_SESSION_SCOPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_SESSION_SCOPE_VALUES!r}"
    )
