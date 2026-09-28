from enum import StrEnum


class AgentRecoveryAction(StrEnum):
    CONFIRM = "confirm"
    CONTACTSUPPORT = "contactSupport"
    FIXREQUEST = "fixRequest"
    FOLLOWNEXT = "followNext"
    POLL = "poll"
    RETRY = "retry"

    def __str__(self) -> str:
        return str(self.value)
