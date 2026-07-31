from typing import Literal

ProxmoxJobType = Literal["backup", "provision", "reinstall", "restore", "snapshot"]

PROXMOX_JOB_TYPE_VALUES: set[ProxmoxJobType] = {
    "backup",
    "provision",
    "reinstall",
    "restore",
    "snapshot",
}


def check_proxmox_job_type(value: str) -> ProxmoxJobType:
    if value in PROXMOX_JOB_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROXMOX_JOB_TYPE_VALUES!r}"
    )
