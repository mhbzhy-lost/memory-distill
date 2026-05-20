import json

import pytest
from pydantic import ValidationError

from recipe_importer.models import (
    EvidenceCandidate,
    EvidenceRef,
    Recipe,
    RecipeStatus,
    Source,
)
from recipe_importer.schema import export_schemas


def test_recipe_requires_evidence_for_core_fields():
    ref = EvidenceRef(
        source_id="react-error-418",
        url="https://react.dev/errors/418",
        final_url="https://react.dev/errors/418",
        source_type="official_error_doc",
        captured_at="2026-05-20T00:00:00Z",
        section_anchor="root",
        span_id="root-1",
        short_excerpt="Hydration failed because the server rendered HTML did not match.",
        quote_hash="sha256:abc",
    )

    recipe = Recipe(
        id="react-hydration-mismatch",
        status=RecipeStatus.PROPOSED,
        stack=["react", "nextjs"],
        failure_class="render/hydration",
        symptoms=["Hydration failed"],
        fingerprints=["server rendered HTML did not match the client"],
        first_checks=["Check browser-only branches in render output"],
        do_not=["Do not disable SSR as the first fix"],
        evidence_needed=["Component output must be compared server vs client"],
        minimal_fix_scope=["The component producing mismatched markup"],
        validation_ladder=["Reproduce the page and inspect console warning"],
        regression_guard=["Add a smoke test for the affected page"],
        evidence_refs=[ref],
    )

    assert recipe.id == "react-hydration-mismatch"
    assert recipe.status is RecipeStatus.PROPOSED


def test_recipe_rejects_missing_evidence_refs():
    with pytest.raises(ValidationError):
        Recipe(
            id="react-hydration-mismatch",
            status=RecipeStatus.PROPOSED,
            stack=["react"],
            failure_class="render/hydration",
            symptoms=["Hydration failed"],
            fingerprints=["server rendered HTML did not match the client"],
            first_checks=["Check Date.now usage"],
            do_not=["Do not rewrite the app"],
            evidence_needed=["Source evidence is required"],
            minimal_fix_scope=["Affected component"],
            validation_ladder=["Run related smoke test"],
            regression_guard=["Add regression guard"],
            evidence_refs=[],
        )


def test_source_model_has_stable_id():
    source = Source(
        source_id="react-error-418",
        url="https://react.dev/errors/418",
        source_type="official_error_doc",
        stacks=["react", "nextjs"],
        expected_failure_hints=["hydration mismatch"],
        refresh_policy="monthly",
    )

    assert source.source_id == "react-error-418"


def test_evidence_candidate_schema_is_narrow():
    candidate = EvidenceCandidate(
        failure_label="hydration mismatch",
        symptom_quotes=["Hydration failed"],
        cause_quotes=["Date.now() in render"],
        avoidance_quotes=["Do not disable SSR"],
        validation_quotes=["Check browser console"],
        section_refs=["react-error-418#root-1"],
        confidence="medium",
    )

    assert candidate.confidence == "medium"


def test_export_schemas(tmp_path):
    export_schemas(tmp_path)

    exported = sorted(path.name for path in tmp_path.iterdir())
    assert exported == [
        "debug-recipe.schema.json",
        "evidence-candidates.schema.json",
        "review.schema.json",
        "source.schema.json",
    ]

    recipe_schema = json.loads((tmp_path / "debug-recipe.schema.json").read_text())
    assert recipe_schema["title"] == "Recipe"
