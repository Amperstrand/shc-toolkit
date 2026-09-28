"""Regression tests for the generated-client enum contract.

PR #34 Codex review (r3693516890): `literal_enums: true` (a workaround for
a spec duplicate that no longer exists) replaced every generated enum with
a typing.Literal alias, so consumer code like `ServiceStatus.ACTIVE` or
`ProblemXErrorCode.NOT_FOUND` broke with AttributeError on upgrade. The
generated client must expose real enum classes.
"""

import enum

from shc_toolkit.generated.models import problem_x_error_code, service_status


def test_generated_enums_are_enum_classes():
    assert issubclass(service_status.ServiceStatus, enum.Enum)
    assert issubclass(service_status.ServiceStatus, str)


def test_enum_attribute_access_works():
    # The exact consumer pattern that broke under literal_enums.
    assert service_status.ServiceStatus.ACTIVE.value == "active"
    assert problem_x_error_code.ProblemXErrorCode.NOT_FOUND.value == "not_found"


def test_the_historical_duplicate_value_is_gone_from_the_spec():
    # The collision that motivated literal_enums (issue #20):
    # "cloud-init-policy-violation" vs "cloud_init_policy_violation".
    # If the underscore variant ever reappears, fix the SPEC — not by
    # re-enabling literal_enums (breaks every consumer).
    import json
    from pathlib import Path

    spec = json.loads(
        (Path(__file__).parent.parent / "shc_toolkit" / "openapi.json").read_text()
    )
    text = json.dumps(spec)
    assert "cloud_init_policy_violation" not in text
    assert "cloud-init-policy-violation" in text
