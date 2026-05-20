from pathlib import Path

from recipe_importer.models import EvidenceCandidate, EvidenceRef, Recipe, RecipeStatus
from recipe_importer.storage import read_json


def _evidence_refs(snapshot_dir: Path, span_ids: list[str]) -> list[EvidenceRef]:
    sections = read_json(snapshot_dir / "sections.json")
    wanted = set(span_ids)
    selected = [item for item in sections if item["span_id"] in wanted]
    if not selected:
        selected = sections[:1]
    return [
        EvidenceRef(
            source_id=item["source_id"],
            url=item["url"],
            final_url=item["final_url"],
            source_type=item["source_type"],
            captured_at=item["captured_at"],
            section_anchor=item["section_anchor"],
            span_id=item["span_id"],
            short_excerpt=item["short_excerpt"],
            quote_hash=item["quote_hash"],
        )
        for item in selected
    ]


def normalize_recipe(candidate: EvidenceCandidate, snapshot_dir: Path, *, stack: list[str]) -> Recipe:
    return Recipe(
        id="react-hydration-mismatch",
        status=RecipeStatus.PROPOSED,
        stack=stack,
        failure_class="render/hydration",
        symptoms=candidate.symptom_quotes or ["Hydration failed"],
        fingerprints=[
            "Hydration failed",
            "server rendered HTML didn't match the client",
            "server rendered HTML did not match the client",
        ],
        first_checks=[
            "Check server/client branches such as typeof window in render output",
            "Check Date.now(), Math.random(), and locale formatting in render output",
            "Check invalid HTML nesting in the affected component",
        ],
        do_not=[
            "Do not disable SSR as the first fix",
            "Do not rewrite the component tree before locating the mismatched markup",
        ],
        evidence_needed=[
            "Identify the component producing different server and client markup",
            "Capture the browser console hydration warning",
        ],
        minimal_fix_scope=[
            "The component producing mismatched markup",
            "The server-to-client data snapshot used by that component",
        ],
        validation_ladder=[
            "Reproduce the page in development",
            "Check browser console for the hydration warning",
            "Run the related smoke test if one exists",
        ],
        regression_guard=[
            "Add or update a smoke test for the affected page or component",
        ],
        evidence_refs=_evidence_refs(snapshot_dir, candidate.section_refs),
    )
