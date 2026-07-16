from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.cloud_init_apply_result_format import CloudInitApplyResultFormat
from ..models.cloud_init_apply_result_volume_label import (
    CloudInitApplyResultVolumeLabel,
)

if TYPE_CHECKING:
    from ..models.cloud_init_attached_drive import CloudInitAttachedDrive
    from ..models.lint_report import LintReport


T = TypeVar("T", bound="CloudInitApplyResult")


@_attrs_define
class CloudInitApplyResult:
    """
    Attributes:
        service_id (int):
        accepted (bool):
        lint_report (LintReport):
        iso_name (str):  Example: cloud-init-seed.iso.
        volume_label (CloudInitApplyResultVolumeLabel):
        format_ (CloudInitApplyResultFormat):
        storage (str):  Example: local.
        attached (CloudInitAttachedDrive):
        removed_generated_cloud_init (bool):
        single_cidata_source (bool):
    """

    service_id: int
    accepted: bool
    lint_report: LintReport
    iso_name: str
    volume_label: CloudInitApplyResultVolumeLabel
    format_: CloudInitApplyResultFormat
    storage: str
    attached: CloudInitAttachedDrive
    removed_generated_cloud_init: bool
    single_cidata_source: bool

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        accepted = self.accepted

        lint_report = self.lint_report.to_dict()

        iso_name = self.iso_name

        volume_label = self.volume_label.value

        format_ = self.format_.value

        storage = self.storage

        attached = self.attached.to_dict()

        removed_generated_cloud_init = self.removed_generated_cloud_init

        single_cidata_source = self.single_cidata_source

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "accepted": accepted,
                "lintReport": lint_report,
                "isoName": iso_name,
                "volumeLabel": volume_label,
                "format": format_,
                "storage": storage,
                "attached": attached,
                "removedGeneratedCloudInit": removed_generated_cloud_init,
                "singleCidataSource": single_cidata_source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_init_attached_drive import CloudInitAttachedDrive
        from ..models.lint_report import LintReport

        d = dict(src_dict)
        service_id = d.pop("service_id")

        accepted = d.pop("accepted")

        lint_report = LintReport.from_dict(d.pop("lintReport"))

        iso_name = d.pop("isoName")

        volume_label = CloudInitApplyResultVolumeLabel(d.pop("volumeLabel"))

        format_ = CloudInitApplyResultFormat(d.pop("format"))

        storage = d.pop("storage")

        attached = CloudInitAttachedDrive.from_dict(d.pop("attached"))

        removed_generated_cloud_init = d.pop("removedGeneratedCloudInit")

        single_cidata_source = d.pop("singleCidataSource")

        cloud_init_apply_result = cls(
            service_id=service_id,
            accepted=accepted,
            lint_report=lint_report,
            iso_name=iso_name,
            volume_label=volume_label,
            format_=format_,
            storage=storage,
            attached=attached,
            removed_generated_cloud_init=removed_generated_cloud_init,
            single_cidata_source=single_cidata_source,
        )

        return cloud_init_apply_result
