from enum import StrEnum


class ManagedAccountInvitationRequestAction(StrEnum):
    ACCEPT = "accept"
    DECLINE = "decline"

    def __str__(self) -> str:
        return str(self.value)
