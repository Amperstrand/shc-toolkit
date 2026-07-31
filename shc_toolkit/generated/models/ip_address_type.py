from typing import Literal

IpAddressType = Literal["v4", "v6"]

IP_ADDRESS_TYPE_VALUES: set[IpAddressType] = {
    "v4",
    "v6",
}


def check_ip_address_type(value: str) -> IpAddressType:
    if value in IP_ADDRESS_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {IP_ADDRESS_TYPE_VALUES!r}"
    )
