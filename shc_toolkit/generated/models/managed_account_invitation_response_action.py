from typing import Literal

ManagedAccountInvitationResponseAction = Literal["accepted", "declined"]

MANAGED_ACCOUNT_INVITATION_RESPONSE_ACTION_VALUES: set[
    ManagedAccountInvitationResponseAction
] = {
    "accepted",
    "declined",
}


def check_managed_account_invitation_response_action(
    value: str,
) -> ManagedAccountInvitationResponseAction:
    if value in MANAGED_ACCOUNT_INVITATION_RESPONSE_ACTION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MANAGED_ACCOUNT_INVITATION_RESPONSE_ACTION_VALUES!r}"
    )
