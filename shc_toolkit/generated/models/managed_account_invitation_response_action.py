from enum import StrEnum


class ManagedAccountInvitationResponseAction(StrEnum):
    ACCEPTED = "accepted"
    DECLINED = "declined"

    def __str__(self) -> str:
        return str(self.value)
