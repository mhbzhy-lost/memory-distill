from pathlib import Path

import pytest

from recipe_importer.extract import extract_snapshot
from recipe_importer.llm import deterministic_candidates
from recipe_importer.models import (
    BuildRecipe,
    DecisionOption,
    EvidenceRef,
    RecipeStatus,
    TriggerSpec,
)
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.render import check_render_equivalence, render_recipe_file, render_recipe_text
from recipe_importer.storage import write_json, write_text


def _build_recipe_fixture() -> BuildRecipe:
    ref = EvidenceRef(
        source_id="react-error-418",
        url="https://react.dev/errors/418",
        final_url="https://react.dev/errors/418",
        source_type="official_error_doc",
        captured_at="2026-05-20T00:00:00Z",
        section_anchor="root",
        span_id="root-1",
        short_excerpt="Hydration failed.",
        quote_hash="sha256:abc",
    )
    return BuildRecipe(
        id="react-hydration-avoid-nondeterminism",
        status=RecipeStatus.PROPOSED,
        stack=["react", "nextjs"],
        trigger=TriggerSpec(
            file_pattern="app/**/*.tsx",
            code_signals=["Date.now()", "Math.random()"],
            description="Server Component 中使用了非确定性表达式",
        ),
        correct_pattern=["将时间戳从 server 作为 prop 传入"],
        decision_context=[
            DecisionOption(condition="需要显示当前时间", recommendation="从 server 传入 timestamp prop"),
        ],
        constraints=["render 路径中不得使用 Date.now() / Math.random()"],
        do_not=["不要在 Server Component render 中调用 Date.now()"],
        defaults=["默认从 server 传入时间相关数据"],
        validation=["next build 无 hydration warning"],
        related_debug_recipes=["react-hydration-mismatch"],
        evidence_refs=[ref],
    )


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


def test_deterministic_candidates_cover_first_batch_sources(kb_root):
    paths = KbPaths(kb_root).ensure()
    cases = [
        (
            "react-invalid-hook-call",
            "invalid hook call",
            "react-invalid-hook-call",
            "Hooks can only be called inside the body of a function component. "
            "You might have mismatching versions of React and React DOM. "
            "You might have more than one copy of React.",
            ["react"],
        ),
        (
            "react-use-effect-troubleshooting",
            "effect dependency rerun loop",
            "react-effect-dependency-rerun-loop",
            "My Effect keeps re-running in an infinite cycle because one of your dependencies "
            "is different on every re-render. My Effect runs twice when the component mounts. "
            "Missing cleanup function.",
            ["react"],
        ),
        (
            "react-preserving-resetting-state",
            "state reset by position or key",
            "react-state-reset-by-position-or-key",
            "State is isolated between components. You can force a subtree to reset its state "
            "by giving it a different key. Nested component definitions reset state.",
            ["react"],
        ),
        (
            "next-dynamic-server-error",
            "next dynamic server usage",
            "next-dynamic-server-usage",
            "DynamicServerError Dynamic Server Usage. cookies or headers was not bound to the "
            "same call stack. Static generation dynamic function.",
            ["react", "nextjs"],
        ),
        (
            "next-invalid-dynamic-suspense",
            "next invalid dynamic suspense",
            "next-invalid-dynamic-suspense",
            "Invalid Usage of suspense Option of next/dynamic. You are using suspense true "
            "with ssr false. You are using suspense true with loading. Next.js will use React.lazy.",
            ["react", "nextjs"],
        ),
        (
            "vite-troubleshooting",
            "vite esm-only config require",
            "vite-esm-only-config-require",
            "This package is ESM only but it was tried to load by require. Error ERR_REQUIRE_ESM "
            "from vite.config.js. Convert your config to ESM.",
            ["react", "vite"],
        ),
        (
            "tanstack-query-important-defaults",
            "tanstack query aggressive defaults",
            "tanstack-query-aggressive-defaults",
            "Query instances by default consider cached data as stale. Refetch on window focus, "
            "refetch on mount, and queries that fail are retried 3 times.",
            ["react", "tanstack-query"],
        ),
        (
            "tanstack-query-invalidation",
            "tanstack query missing invalidation",
            "tanstack-query-missing-invalidation",
            "invalidateQueries marks queries as stale. Query Matching with invalidateQueries "
            "supports partial matching after a mutation succeeds.",
            ["react", "tanstack-query"],
        ),
    ]

    for source_id, expected_label, expected_recipe_id, text, stack in cases:
        snapshot_dir = paths.snapshots_dir / source_id
        write_json(
            snapshot_dir / "sections.json",
            [
                {
                    "source_id": source_id,
                    "url": f"https://example.test/{source_id}",
                    "final_url": f"https://example.test/{source_id}",
                    "source_type": "official_doc",
                    "captured_at": "2026-05-22T00:00:00Z",
                    "section_anchor": "root",
                    "span_id": f"{source_id}-1",
                    "short_excerpt": text[:600],
                    "quote_hash": "sha256:abc",
                    "text": text,
                }
            ],
        )

        candidates = deterministic_candidates(snapshot_dir)
        recipe = normalize_recipe(candidates.candidates[0], snapshot_dir, stack=stack)

        assert candidates.candidates[0].failure_label == expected_label
        assert recipe.id == expected_recipe_id
        assert recipe.evidence_refs[0].source_id == source_id


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


def test_normalize_recipe_reports_unknown_failure_label(extracted_react_snapshot):
    candidates = deterministic_candidates(extracted_react_snapshot)
    candidate = candidates.candidates[0].model_copy(update={"failure_label": "unknown label"})

    with pytest.raises(ValueError, match="unknown failure_label"):
        normalize_recipe(candidate, extracted_react_snapshot, stack=["react"])


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


def test_render_build_recipe_text():
    build = _build_recipe_fixture()
    text = render_recipe_text(build)

    assert text.startswith("---\n")
    assert "kind: build-recipe" in text
    assert "## Correct Pattern" in text
    assert "## Constraints" in text
    assert "## Do Not" in text
    assert "## Validation" in text
    assert "## Trigger" in text
    assert "Date.now()" in text
    assert "## Reviewer Notes" in text


def test_render_build_recipe_file_round_trip(kb_root):
    paths = KbPaths(kb_root).ensure()
    build = _build_recipe_fixture()
    target = paths.proposed_dir / f"{build.id}.md"

    render_recipe_file(build, target)

    assert check_render_equivalence(target)


def test_parse_build_recipe_file(kb_root):
    paths = KbPaths(kb_root).ensure()
    build = _build_recipe_fixture()
    target = paths.proposed_dir / f"{build.id}.md"
    render_recipe_file(build, target)

    from recipe_importer.render import parse_recipe_file

    parsed = parse_recipe_file(target)
    assert parsed.kind == "build-recipe"
    assert parsed.id == build.id
    assert parsed.constraints == build.constraints
