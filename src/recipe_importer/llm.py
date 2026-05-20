from pathlib import Path

from recipe_importer.models import EvidenceCandidate, EvidenceCandidates
from recipe_importer.storage import read_json


def deterministic_candidates(snapshot_dir: Path) -> EvidenceCandidates:
    sections = read_json(snapshot_dir / "sections.json")
    joined = "\n".join(item["text"] for item in sections)
    if "Hydration failed" not in joined:
        return EvidenceCandidates(candidates=[])

    section_refs = [
        item["span_id"]
        for item in sections
        if "Hydration" in item["text"] or "Date.now" in item["text"]
    ]
    return EvidenceCandidates(
        candidates=[
            EvidenceCandidate(
                failure_label="hydration mismatch",
                symptom_quotes=[
                    "Hydration failed because the server rendered HTML didn't match the client"
                ],
                cause_quotes=[
                    "server/client branch",
                    "Date.now() or Math.random()",
                    "Date formatting in a user's locale",
                    "Invalid HTML tag nesting",
                ],
                avoidance_quotes=["Do not disable SSR as the first fix"],
                validation_quotes=["Reproduce the page and inspect browser console hydration warning"],
                section_refs=section_refs,
                confidence="high",
            )
        ]
    )
