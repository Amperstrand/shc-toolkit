from typing import Literal

ClaimAgentKeyResponse200DataScope = Literal["full", "operate", "read"]

CLAIM_AGENT_KEY_RESPONSE_200_DATA_SCOPE_VALUES: set[
    ClaimAgentKeyResponse200DataScope
] = {
    "full",
    "operate",
    "read",
}


def check_claim_agent_key_response_200_data_scope(
    value: str,
) -> ClaimAgentKeyResponse200DataScope:
    if value in CLAIM_AGENT_KEY_RESPONSE_200_DATA_SCOPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CLAIM_AGENT_KEY_RESPONSE_200_DATA_SCOPE_VALUES!r}"
    )
