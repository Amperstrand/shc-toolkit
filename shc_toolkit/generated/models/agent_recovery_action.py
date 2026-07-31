from typing import Literal

AgentRecoveryAction = Literal[
    "confirm", "contactSupport", "fixRequest", "followNext", "poll", "retry"
]

AGENT_RECOVERY_ACTION_VALUES: set[AgentRecoveryAction] = {
    "confirm",
    "contactSupport",
    "fixRequest",
    "followNext",
    "poll",
    "retry",
}


def check_agent_recovery_action(value: str) -> AgentRecoveryAction:
    if value in AGENT_RECOVERY_ACTION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_RECOVERY_ACTION_VALUES!r}"
    )
