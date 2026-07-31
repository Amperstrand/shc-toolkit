from typing import Literal

ConsoleSessionResponseVia = Literal["secure_bridge_jwt"]

CONSOLE_SESSION_RESPONSE_VIA_VALUES: set[ConsoleSessionResponseVia] = {
    "secure_bridge_jwt",
}


def check_console_session_response_via(value: str) -> ConsoleSessionResponseVia:
    if value in CONSOLE_SESSION_RESPONSE_VIA_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CONSOLE_SESSION_RESPONSE_VIA_VALUES!r}"
    )
