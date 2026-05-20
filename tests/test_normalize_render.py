from pathlib import Path

import pytest

from recipe_importer.extract import extract_snapshot
from recipe_importer.llm import deterministic_candidates
from recipe_importer.models import RecipeStatus
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.render import check_render_equivalence, render_recipe_file, render_recipe_text
from recipe_importer.storage import write_json, write_text


@pytest.fixture
def extracted_react_snapshot(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    html = Path("tests/fixtures/react_error_418.html").read_text(encoding="utf-8")
    write_text(snapshot_dir / "raw.html", html)
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-20T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
        },
    )
    extract_snapshot(snapshot_dir)
    return snapshot_dir


def test_deterministic_candidates_find_hydration(extracted_react_snapshot):
    candidates = deterministic_candidates(extracted_react_snapshot)

    assert candidates.candidates[0].failure_label == "hydration mismatch"
    assert candidates.candidates[0].confidence == "high"


def test_normalize_recipe_from_candidates(extracted_react_snapshot):
    candidates = deterministic_candidates(extracted_react_snapshot)
    recipe = normalize_recipe(
        candidates.candidates[0],
        extracted_react_snapshot,
        stack=["react", "nextjs"],
    )

    assert recipe.id == "react-hydration-mismatch"
    assert recipe.status is RecipeStatus.PROPOSED
    assert "Hydration failed" in recipe.symptoms[0]
    assert recipe.evidence_refs[0].source_id == "react-error-418"


def test_render_recipe_file_round_trip(extracted_react_snapshot, kb_root):
    paths = KbPaths(kb_root).ensure()
    recipe = normalize_recipe(
        deterministic_candidates(extracted_react_snapshot).candidates[0],
        extracted_react_snapshot,
        stack=["react", "nextjs"],
    )
    target = paths.proposed_dir / "react-hydration-mismatch.md"

    render_recipe_file(recipe, target)

    assert check_render_equivalence(target)
    text = target.read_text(encoding="utf-8")
    assert "## First Checks" in text
    assert "Do not disable SSR as the first fix" in text


def test_render_recipe_text_has_no_trailing_blank_line(extracted_react_snapshot):
    recipe = normalize_recipe(
        deterministic_candidates(extracted_react_snapshot).candidates[0],
        extracted_react_snapshot,
        stack=["react", "nextjs"],
    )

    assert render_recipe_text(recipe).endswith("\n")
    assert not render_recipe_text(recipe).endswith("\n\n")


def test_check_render_equivalence_detects_body_drift(extracted_react_snapshot, kb_root):
    paths = KbPaths(kb_root).ensure()
    recipe = normalize_recipe(
        deterministic_candidates(extracted_react_snapshot).candidates[0],
        extracted_react_snapshot,
        stack=["react", "nextjs"],
    )
    target = paths.proposed_dir / "react-hydration-mismatch.md"
    render_recipe_file(recipe, target)

    target.write_text(target.read_text(encoding="utf-8") + "\nmanual edit\n", encoding="utf-8")

    assert not check_render_equivalence(target)
