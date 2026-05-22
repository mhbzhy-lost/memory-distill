from pathlib import Path

import pytest

from recipe_importer.dedupe import duplicate_hints
from recipe_importer.extract import extract_snapshot
from recipe_importer.index import rebuild_index
from recipe_importer.llm import deterministic_candidates
from recipe_importer.models import EvidenceRef, Recipe, RecipeStatus
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.publish import publish_recipe
from recipe_importer.render import parse_recipe_file, render_recipe_file
from recipe_importer.review import current_candidate, start_review
from recipe_importer.search import get_recipe, search_recipes
from recipe_importer.storage import read_json, write_json, write_text


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def proposed_recipe(paths):
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    html = (FIXTURES_DIR / "react_error_418.html").read_text(encoding="utf-8")
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
    recipe = normalize_recipe(
        deterministic_candidates(snapshot_dir).candidates[0],
        snapshot_dir,
        stack=["react", "nextjs"],
    )
    target = paths.proposed_dir / f"{recipe.id}.md"
    render_recipe_file(recipe, target)
    return target


def test_publish_rebuild_search_and_get(kb_root):
    paths = KbPaths(kb_root).ensure()
    proposed = proposed_recipe(paths)

    accepted = publish_recipe(proposed, paths)
    index_path = rebuild_index(paths)
    results = search_recipes(paths, "Hydration failed")
    tag_results = search_recipes(paths, "react")
    source_results = search_recipes(paths, "react-error-418")
    full = get_recipe(paths, "react-hydration-mismatch")

    assert accepted == paths.accepted_dir / "react-hydration-mismatch.md"
    assert index_path == paths.index_path
    assert results[0]["id"] == "react-hydration-mismatch"
    assert "Hydration failed" in results[0]["summary"]
    assert "Do not disable SSR" in "\n".join(results[0]["do_not"])
    assert results[0]["validation_ladder"]
    assert tag_results[0]["id"] == "react-hydration-mismatch"
    assert source_results[0]["id"] == "react-hydration-mismatch"
    assert source_results[0]["source_ids"] == ["react-error-418"]
    assert full.id == "react-hydration-mismatch"

    recipe = parse_recipe_file(accepted)
    assert recipe.status is RecipeStatus.ACCEPTED
    assert recipe.maintenance.state is RecipeStatus.ACCEPTED


def test_publish_rejects_non_equivalent_generated_body(kb_root):
    paths = KbPaths(kb_root).ensure()
    proposed = proposed_recipe(paths)
    proposed.write_text(proposed.read_text(encoding="utf-8") + "\nmanual semantic edit\n", encoding="utf-8")

    with pytest.raises(ValueError, match="render-equivalent"):
        publish_recipe(proposed, paths)


def test_publish_rejects_source_outside_proposed_dir(kb_root):
    paths = KbPaths(kb_root).ensure()
    outside = paths.recipe_kb_dir / "imports" / "react-hydration-mismatch.md"
    proposed = proposed_recipe(paths)
    write_text(outside, proposed.read_text(encoding="utf-8"))

    with pytest.raises(ValueError, match="proposed"):
        publish_recipe(outside, paths)


def test_search_excludes_stale_when_fresh_only(kb_root):
    paths = KbPaths(kb_root).ensure()
    proposed = proposed_recipe(paths)
    accepted = publish_recipe(proposed, paths)

    recipe = parse_recipe_file(accepted)
    recipe.status = RecipeStatus.STALE
    recipe.maintenance.state = RecipeStatus.STALE
    render_recipe_file(recipe, paths.stale_dir / accepted.name)
    accepted.unlink()

    rebuild_index(paths)
    all_results = search_recipes(paths, "Hydration failed")
    fresh_results = search_recipes(paths, "Hydration failed", fresh_only=True)

    assert len(all_results) == 1
    assert all_results[0]["stale"] is True
    assert len(fresh_results) == 0


def test_publish_replaces_same_named_stale_recipe(kb_root):
    paths = KbPaths(kb_root).ensure()
    proposed = proposed_recipe(paths)

    stale_recipe = parse_recipe_file(proposed)
    stale_recipe.status = RecipeStatus.STALE
    stale_recipe.maintenance.state = RecipeStatus.STALE
    render_recipe_file(stale_recipe, paths.stale_dir / proposed.name)

    accepted = publish_recipe(proposed, paths)
    rebuild_index(paths)
    records = read_json(paths.index_path)["recipes"]
    matching = [record for record in records if record["id"] == "react-hydration-mismatch"]

    assert accepted == paths.accepted_dir / "react-hydration-mismatch.md"
    assert not (paths.stale_dir / proposed.name).exists()
    assert len(matching) == 1
    assert matching[0]["status"] == "accepted"


def test_publish_tolerates_stale_sibling_removed_during_publish(kb_root, monkeypatch):
    paths = KbPaths(kb_root).ensure()
    proposed = proposed_recipe(paths)
    stale_path = paths.stale_dir / proposed.name

    stale_recipe = parse_recipe_file(proposed)
    stale_recipe.status = RecipeStatus.STALE
    stale_recipe.maintenance.state = RecipeStatus.STALE
    render_recipe_file(stale_recipe, stale_path)

    original_unlink = Path.unlink

    def unlink_with_stale_race(path, *args, **kwargs):
        if path == stale_path and not kwargs.get("missing_ok", False):
            original_unlink(path)
            raise FileNotFoundError(path)
        return original_unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", unlink_with_stale_race)

    accepted = publish_recipe(proposed, paths)

    assert accepted.exists()
    assert not stale_path.exists()


def test_publish_consumes_proposed_candidate(kb_root):
    paths = KbPaths(kb_root).ensure()
    proposed = proposed_recipe(paths)

    publish_recipe(proposed, paths)

    assert not proposed.exists()
    with pytest.raises(ValueError, match="review queue is empty"):
        current_candidate(paths, start_review(paths))


def _dummy_evidence_ref(source_id: str = "react-error-418") -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        url="https://react.dev/errors/418",
        final_url="https://react.dev/errors/418",
        source_type="official_error_doc",
        captured_at="2026-05-20T00:00:00Z",
        section_anchor="root",
        span_id="react-error-418-1",
        short_excerpt="Hydration failed",
        quote_hash="sha256:abc",
    )


def test_duplicate_hints_returns_deterministic_dictionaries():
    ref = _dummy_evidence_ref()

    recipe_a = Recipe(
        id="test-recipe-a",
        status=RecipeStatus.ACCEPTED,
        stack=["react", "nextjs"],
        failure_class="render/hydration",
        symptoms=["hydration mismatch"],
        fingerprints=["server rendered HTML did not match", "Hydration failed"],
        first_checks=["check typeof window"],
        do_not=["do not disable SSR"],
        evidence_needed=["find mismatched component"],
        minimal_fix_scope=["affected component"],
        validation_ladder=["smoke test"],
        regression_guard=["add regression guard"],
        evidence_refs=[ref],
    )

    recipe_b = Recipe(
        id="test-recipe-b",
        status=RecipeStatus.ACCEPTED,
        stack=["react", "vue"],
        failure_class="render/hydration",
        symptoms=["hydration mismatch"],
        fingerprints=["server rendered HTML did not match", "DOM mismatch"],
        first_checks=["check client state"],
        do_not=["do not rewrite tree"],
        evidence_needed=["find component"],
        minimal_fix_scope=["component"],
        validation_ladder=["test"],
        regression_guard=["guard"],
        evidence_refs=[ref],
    )

    recipe_c = Recipe(
        id="test-recipe-c",
        status=RecipeStatus.ACCEPTED,
        stack=["python", "django"],
        failure_class="db/connection",
        symptoms=["timeout"],
        fingerprints=["connection timeout"],
        first_checks=["check pool"],
        do_not=["do not"],
        evidence_needed=["logs"],
        minimal_fix_scope=["pool"],
        validation_ladder=["connect"],
        regression_guard=["guard"],
        evidence_refs=[ref],
    )

    hints = duplicate_hints(recipe_a, [recipe_a, recipe_b, recipe_c])

    assert len(hints) == 2

    hint_ids = {h["recipe_id"] for h in hints}
    assert "test-recipe-a" in hint_ids
    assert "test-recipe-b" in hint_ids
    assert "test-recipe-c" not in hint_ids

    for hint in hints:
        assert "recipe_id" in hint
        assert "fingerprint_overlap" in hint
        assert "stack_overlap" in hint
        assert isinstance(hint["fingerprint_overlap"], list)
        assert isinstance(hint["stack_overlap"], list)
