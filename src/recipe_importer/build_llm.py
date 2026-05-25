from pathlib import Path

from recipe_importer.build_templates import BUILD_TEMPLATES_BY_SOURCE
from recipe_importer.models import BuildRecipe, EvidenceRef, RecipeStatus
from recipe_importer.storage import read_json


def deterministic_build_candidates(snapshot_dir: Path) -> list[BuildRecipe]:
    sections_path = snapshot_dir / "sections.json"
    if not sections_path.exists():
        return []
    sections = read_json(sections_path)
    if not sections:
        return []

    source_id = sections[0]["source_id"]
    template = BUILD_TEMPLATES_BY_SOURCE.get(source_id)
    if template is None:
        return []

    lower_terms = [term.lower() for term in template.match_terms]
    matched_sections = [
        item for item in sections
        if any(term in item["text"].lower() for term in lower_terms)
    ]
    if not matched_sections:
        return []

    evidence_refs = [
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
        for item in matched_sections
    ]

    return [
        BuildRecipe(
            id=template.recipe_id,
            status=RecipeStatus.PROPOSED,
            stack=list(template.stack),
            trigger=template.trigger,
            correct_pattern=list(template.correct_pattern),
            decision_context=list(template.decision_context),
            constraints=list(template.constraints),
            do_not=list(template.do_not),
            defaults=list(template.defaults),
            validation=list(template.validation),
            related_debug_recipes=list(template.related_debug_recipes),
            evidence_refs=evidence_refs,
        )
    ]
