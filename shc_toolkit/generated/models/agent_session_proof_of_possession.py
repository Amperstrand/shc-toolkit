from typing import Literal

AgentSessionProofOfPossession = Literal["none", "nostr"]

AGENT_SESSION_PROOF_OF_POSSESSION_VALUES: set[AgentSessionProofOfPossession] = {
    "none",
    "nostr",
}


def check_agent_session_proof_of_possession(
    value: str,
) -> AgentSessionProofOfPossession:
    if value in AGENT_SESSION_PROOF_OF_POSSESSION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_SESSION_PROOF_OF_POSSESSION_VALUES!r}"
    )
