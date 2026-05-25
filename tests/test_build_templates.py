from pathlib import Path

from recipe_importer.build_llm import deterministic_build_candidates
from recipe_importer.build_templates import BUILD_TEMPLATES_BY_SOURCE
from recipe_importer.models import RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import check_render_equivalence, render_recipe_file
from recipe_importer.storage import write_json


def test_build_templates_registry_has_entries():
    assert len(BUILD_TEMPLATES_BY_SOURCE) >= 1
    assert "nextjs-rendering-server-components" in BUILD_TEMPLATES_BY_SOURCE


def test_deterministic_build_candidates_from_guide_snapshot(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "nextjs-rendering-server-components"
    write_json(
        snapshot_dir / "sections.json",
        [
            {
                "source_id": "nextjs-rendering-server-components",
                "url": "https://nextjs.org/docs/app/building-your-application/rendering/server-components",
                "final_url": "https://nextjs.org/docs/app/building-your-application/rendering/server-components",
                "source_type": "official_guide",
                "captured_at": "2026-05-25T00:00:00Z",
                "section_anchor": "root",
                "span_id": "nextjs-rendering-server-components-1",
                "short_excerpt": "Server Components allow you to render on the server.",
                "quote_hash": "sha256:test",
                "text": (
                    "By default, Next.js uses Server Components. "
                    "To use Client Components, you can add the 'use client' directive. "
                    "Server Components cannot use hooks like useState or useEffect. "
                    "You should use Client Components when you need interactivity."
                ),
            },
            {
                "source_id": "nextjs-rendering-server-components",
                "url": "https://nextjs.org/docs/app/building-your-application/rendering/server-components",
                "final_url": "https://nextjs.org/docs/app/building-your-application/rendering/server-components",
                "source_type": "official_guide",
                "captured_at": "2026-05-25T00:00:00Z",
                "section_anchor": "root",
                "span_id": "nextjs-rendering-server-components-2",
                "short_excerpt": "When to use Server vs Client Components.",
                "quote_hash": "sha256:test2",
                "text": (
                    "Use Server Components for fetching data and accessing backend resources. "
                    "Use Client Components for onClick, onChange, useState, useEffect, "
                    "browser-only APIs. Keep Client Components at the leaves of your component tree."
                ),
            },
        ],
    )

    results = deterministic_build_candidates(snapshot_dir)

    assert len(results) >= 1
    build = results[0]
    assert build.kind == "build-recipe"
    assert build.status is RecipeStatus.PROPOSED
    assert "react" in build.stack or "nextjs" in build.stack
    assert len(build.correct_pattern) > 0
    assert len(build.constraints) > 0
    assert len(build.do_not) > 0
    assert build.trigger.description != ""
    assert len(build.evidence_refs) > 0
    assert build.related_debug_recipes


def test_deterministic_build_candidates_returns_empty_for_unknown_source(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "unknown-source"
    write_json(
        snapshot_dir / "sections.json",
        [
            {
                "source_id": "unknown-source",
                "url": "https://example.com",
                "final_url": "https://example.com",
                "source_type": "official_guide",
                "captured_at": "2026-05-25T00:00:00Z",
                "section_anchor": "root",
                "span_id": "unknown-1",
                "short_excerpt": "Some text.",
                "quote_hash": "sha256:x",
                "text": "Some unrelated content.",
            }
        ],
    )

    results = deterministic_build_candidates(snapshot_dir)
    assert results == []


def test_build_candidate_renders_and_round_trips(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "nextjs-rendering-server-components"
    write_json(
        snapshot_dir / "sections.json",
        [
            {
                "source_id": "nextjs-rendering-server-components",
                "url": "https://nextjs.org/docs/app/building-your-application/rendering/server-components",
                "final_url": "https://nextjs.org/docs/app/building-your-application/rendering/server-components",
                "source_type": "official_guide",
                "captured_at": "2026-05-25T00:00:00Z",
                "section_anchor": "root",
                "span_id": "nextjs-rendering-server-components-1",
                "short_excerpt": "Server Components.",
                "quote_hash": "sha256:test",
                "text": "Server Components cannot use hooks. Use 'use client' for interactivity.",
            }
        ],
    )

    results = deterministic_build_candidates(snapshot_dir)
    assert results
    build = results[0]
    target = paths.proposed_dir / f"{build.id}.md"
    render_recipe_file(build, target)

    assert check_render_equivalence(target)
