"""
BDD Steps for Meta Coherence Validator.

Gherkin step definitions for behave tests.
"""

from behave import given, when, then
from pathlib import Path
from unittest.mock import MagicMock
from application.services.meta_coherence_service import MetaCoherenceService
from infrastructure.adapters.out.filesystem_adapter import (
    FilesystemPrdMocReader,
    FilesystemReferenceChecker,
)


@given("a set of PRD MOC documents with valid references")
def step_impl(context):
    context.prd_moc_paths = [Path("/fake/test.md")]
    context.prd_moc_content = "References: `design:foo.yaml` `concept:bar`"


@given("a set of PRD MOC documents with missing references")
def step_impl(context):
    context.prd_moc_paths = [Path("/fake/test.md")]
    context.prd_moc_content = "References: `design:missing.yaml`"


@when("I validate meta coherence")
def step_impl(context):
    mock_reader = MagicMock()
    mock_reader.read_prd_mocs.return_value = [
        {
            "path": "test.md",
            "title": "Test",
            "content": context.prd_moc_content,
        }
    ]

    mock_checker = MagicMock()
    if "missing" in context.prd_moc_content:
        mock_checker.check_design_exists.return_value = False
    else:
        mock_checker.check_design_exists.return_value = True
    mock_checker.check_concept_exists.return_value = True
    mock_checker.check_skill_exists.return_value = True
    mock_checker.check_citizen_exists.return_value = True
    mock_checker.check_boot_step_exists.return_value = True
    mock_checker.check_prd_moc_exists.return_value = True
    mock_checker.check_adr_exists.return_value = True
    mock_checker.check_ontology_file_exists.return_value = True

    service = MetaCoherenceService(
        prd_moc_reader=mock_reader,
        reference_checker=mock_checker,
        base_path=Path("/fake"),
    )
    context.report = service.validate(
        prd_moc_paths=context.prd_moc_paths,
        unified_design_path=Path("/designs"),
        ontology_path=Path("/ontology"),
        skills_registry=Path("/skills/REGISTRY.yaml"),
        boot_sequence_path=Path("/boot.md"),
    )


@then("the global score should be >= 0.8")
def step_impl(context):
    assert context.report["global_score"] >= 0.8


@then("the validation should not be blocked")
def step_impl(context):
    assert context.report["blocked"] is False


@then("the global score should be < 0.8")
def step_impl(context):
    assert context.report["global_score"] < 0.8


@then("the validation should be blocked")
def step_impl(context):
    assert context.report["blocked"] is True


@then("missing references should be reported")
def step_impl(context):
    assert len(context.report["details"][0]["missing_references"]) > 0
