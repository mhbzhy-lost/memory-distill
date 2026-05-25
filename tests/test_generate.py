from pathlib import Path

import pytest

from recipe_importer.generate import generate_build_from_debug
from recipe_importer.models import EvidenceRef, Recipe, RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file, render_recipe_file


def _dummy_debug_recipe() -> Recipe:
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
    return Recipe(
        id="react-hydration-mismatch",
        status=RecipeStatus.ACCEPTED,
        stack=["react", "nextjs"],
        failure_class="render/hydration",
        symptoms=["Hydration failed because the server rendered HTML didn't match the client"],
        fingerprints=["Hydration failed", "server rendered HTML didn't match the client"],
        first_checks=[
            "Check server/client branches such as typeof window in render output",
            "Check Date.now(), Math.random(), and locale formatting in render output",
        ],
        do_not=[
            "Do not disable SSR as the first fix",
            "Do not rewrite the component tree before locating the mismatched markup",
        ],
        evidence_needed=["Identify the component producing different server and client markup"],
        minimal_fix_scope=["The component producing mismatched markup"],
        validation_ladder=[
            "Reproduce the page in development",
            "Check browser console for the hydration warning",
        ],
        regression_guard=["Add or update a smoke test for the affected page or component"],
        evidence_refs=[ref],
    )


def test_generate_build_from_debug_basic():
    debug = _dummy_debug_recipe()
    build = generate_build_from_debug(debug)

    assert build.kind == "build-recipe"
    assert build.id == "build-react-hydration-mismatch"
    assert build.status is RecipeStatus.PROPOSED
    assert build.stack == ["react", "nextjs"]
    assert build.related_debug_recipes == ["react-hydration-mismatch"]
    assert build.evidence_refs == debug.evidence_refs


def test_generate_build_constraints_from_do_not():
    debug = _dummy_debug_recipe()
    build = generate_build_from_debug(debug)

    assert len(build.constraints) >= 1
    assert len(build.do_not) == len(debug.do_not)


def test_generate_build_validation_from_debug():
    debug = _dummy_debug_recipe()
    build = generate_build_from_debug(debug)

    assert build.validation == debug.validation_ladder


def test_generate_build_trigger_from_failure_class():
    debug = _dummy_debug_recipe()
    build = generate_build_from_debug(debug)

    assert build.trigger.description != ""
    assert "render/hydration" in build.trigger.description or "hydration" in build.trigger.description.lower()


def test_generate_build_correct_pattern_empty():
    debug = _dummy_debug_recipe()
    build = generate_build_from_debug(debug)

    assert build.correct_pattern == []


def test_generate_build_recipe_file_round_trip(kb_root):
    paths = KbPaths(kb_root).ensure()
    debug = _dummy_debug_recipe()
    build = generate_build_from_debug(debug)
    target = paths.proposed_dir / f"{build.id}.md"
    render_recipe_file(build, target)

    parsed = parse_recipe_file(target)
    assert parsed.kind == "build-recipe"
    assert parsed.id == build.id
