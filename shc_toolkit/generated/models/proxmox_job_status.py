from typing import Literal

ProxmoxJobStatus = Literal["canceled", "completed", "failed", "pending", "running"]

PROXMOX_JOB_STATUS_VALUES: set[ProxmoxJobStatus] = {
    "canceled",
    "completed",
    "failed",
    "pending",
    "running",
}


def check_proxmox_job_status(value: str) -> ProxmoxJobStatus:
    if value in PROXMOX_JOB_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROXMOX_JOB_STATUS_VALUES!r}"
    )
