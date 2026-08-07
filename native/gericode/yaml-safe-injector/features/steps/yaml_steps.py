"""
BDD Steps for yaml-safe-injector feature.
"""

from behave import given, when, then
from pathlib import Path
from yaml_safe_injector import inject_yaml


@given("un fichier YAML avec ancres `&id001`")
def step_given_yaml_file(context):
    context.temp_path = Path(context.tempdir) / "test.yaml"
    context.temp_path.write_text("""
defaults: &defaults
  layer: L2-PLATFORM
  citizen: DEV-EXPERIENCE

repo1:
  <<: *defaults
  verse_mapping: verse
""")
    context.original_content = context.temp_path.read_text()


@when("j'injecte `verse_mapping: verse` pour `VERSES`")
def step_when_inject(context):
    context.result_path, context.diff = inject_yaml(
        context.temp_path, {"verse_mapping": "verse"}, dry_run=False
    )


@then("la structure YAML est préservée")
def step_then_structure_preserved(context):
    import yaml
    with open(context.result_path) as f:
        data = yaml.safe_load(f)
    assert data["repo1"]["layer"] == "L2-PLATFORM"


@then("le diff est minimal")
def step_then_diff_minimal(context):
    assert len(context.diff) < 200


@when("j'appelle `inject_yaml` avec ce chemin")
def step_when_bad_path(context):
    from yaml_safe_injector import inject_yaml
    context.error = None
    try:
        inject_yaml(Path("D:\\DO\\WEB\\TOOLS\\BAD"), {})
    except ValueError as e:
        context.error = e


@then("l'erreur `ValueError` est levée")
def step_then_value_error(context):
    assert context.error is not None
    assert isinstance(context.error, ValueError)


@then("le fichier n'est pas modifié")
def step_then_not_modified(context):
    import yaml
    with open(context.temp_path) as f:
        data = yaml.safe_load(f)
    assert "verse_mapping" not in data.get("repo1", {})
