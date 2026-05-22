from pathlib import Path

from recipe_importer.models import EvidenceCandidate, EvidenceRef, Recipe, RecipeStatus
from recipe_importer.recipe_templates import TEMPLATES_BY_LABEL
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
    template = TEMPLATES_BY_LABEL.get(candidate.failure_label)
    if template is None:
        raise ValueError(f"unknown failure_label: {candidate.failure_label}")
    return Recipe(
        id=template.recipe_id,
        status=RecipeStatus.PROPOSED,
        stack=stack,
        failure_class=template.failure_class,
        symptoms=template.symptoms,
        fingerprints=template.fingerprints,
        first_checks=template.first_checks,
        do_not=template.do_not,
        evidence_needed=template.evidence_needed,
        minimal_fix_scope=template.minimal_fix_scope,
        validation_ladder=template.validation_ladder,
        regression_guard=template.regression_guard,
        evidence_refs=_evidence_refs(snapshot_dir, candidate.section_refs),
    )
