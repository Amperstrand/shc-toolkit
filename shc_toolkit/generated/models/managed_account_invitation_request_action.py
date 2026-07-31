from typing import Literal

ManagedAccountInvitationRequestAction = Literal["accept", "decline"]

MANAGED_ACCOUNT_INVITATION_REQUEST_ACTION_VALUES: set[
    ManagedAccountInvitationRequestAction
] = {
    "accept",
    "decline",
}


def check_managed_account_invitation_request_action(
    value: str,
) -> ManagedAccountInvitationRequestAction:
    if value in MANAGED_ACCOUNT_INVITATION_REQUEST_ACTION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MANAGED_ACCOUNT_INVITATION_REQUEST_ACTION_VALUES!r}"
    )
