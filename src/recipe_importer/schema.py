import json
from pathlib import Path

from recipe_importer.models import BuildRecipe, EvidenceCandidates, Recipe, ReviewRecord, SourceList

SCHEMA_TARGETS = {
    "build-recipe.schema.json": BuildRecipe,
    "debug-recipe.schema.json": Recipe,
    "source.schema.json": SourceList,
    "review.schema.json": ReviewRecord,
    "evidence-candidates.schema.json": EvidenceCandidates,
}


def export_schemas(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for filename, model in SCHEMA_TARGETS.items():
        target = output_dir / filename
        target.write_text(
            json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(target)
    return written
