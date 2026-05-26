from pathlib import Path

from recipe_importer.models import EvidenceCandidate, EvidenceCandidates
from recipe_importer.recipe_templates import TEMPLATES_BY_SOURCE
from recipe_importer.storage import read_json


def deterministic_candidates(snapshot_dir: Path) -> EvidenceCandidates:
    sections = read_json(snapshot_dir / "sections.json")
    source_id = sections[0]["source_id"] if sections else snapshot_dir.name
    templates = TEMPLATES_BY_SOURCE.get(source_id, [])
    candidates: list[EvidenceCandidate] = []

    for template in templates:
        lower_terms = [term.lower() for term in template.match_terms]
        section_refs = [
            item["span_id"]
            for item in sections
            if any(term in item["text"].lower() for term in lower_terms)
        ]
        if not section_refs:
            continue

        candidates.append(
            EvidenceCandidate(
                failure_label=template.failure_label,
                symptom_quotes=template.symptoms,
                cause_quotes=template.fingerprints,
                avoidance_quotes=template.do_not,
                validation_quotes=template.validation_ladder,
                section_refs=section_refs,
                confidence="high",
            )
        )

    return EvidenceCandidates(candidates=candidates)
