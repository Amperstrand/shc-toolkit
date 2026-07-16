from enum import Enum


class AgentRecoveryAction(str, Enum):
    CONFIRM = "confirm"
    CONTACTSUPPORT = "contactSupport"
    FIXREQUEST = "fixRequest"
    FOLLOWNEXT = "followNext"
    POLL = "poll"
    RETRY = "retry"

    def __str__(self) -> str:
        return str(self.value)
