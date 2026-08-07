"""
BDD Steps for sot-registry-guardian feature.
"""

from behave import given, when, then
from pathlib import Path


@given("known_repositories.yaml avec un repo valide")
def step_given_sot(context):
    context.sot_path = Path(context.tempdir) / "known_repositories.yaml"
    context.sot_path.write_text("""
repositories:
  - full_name: gerivdb/GeriCode
    local_path: D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/
    layer: L2-PLATFORM
""")
    context.original = context.sot_path.read_text()


@when("le local_path diffère du remote")
def step_when_mismatch(context):
    context.error = None
    try:
        from sot_registry_guardian import validate_repo_path
        validate_repo_path(
            "gerivdb/GeriCode",
            "D:/DO/WEB/TOOLS/L4-TOOLS/GeriCode/",
        )
    except ValueError as e:
        context.error = e


@then("une erreur de validation est remontée")
def step_then_validation_error(context):
    assert context.error is not None
    assert "mismatch" in str(context.error).lower()


@then("le rapport de drift est généré")
def step_then_drift_report(context):
    # placeholder
    assert context.error is not None


@when("je valide la strate")
def step_when_validate_layer(context):
    context.error = None
    try:
        from sot_registry_guardian import validate_strate
        validate_strate("D:\\DO\\WEB\\TOOLS\\BAD")
    except ValueError as e:
        context.error = e


@then("`ValueError` est levé")
def step_then_value_error(context):
    assert context.error is not None
    assert isinstance(context.error, ValueError)


@then("le repo est marqué INVALIDE")
def step_then_invalid(context):
    assert context.error is not None
