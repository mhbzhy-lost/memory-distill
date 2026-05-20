from pathlib import Path

from recipe_importer.models import RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file
from recipe_importer.storage import write_json


def _summary(recipe_id: str, failure_class: str, symptoms: list[str]) -> str:
    if symptoms:
        return f"{failure_class}: {symptoms[0]}"
    return f"{failure_class}: {recipe_id}"


def _source_ids(recipe) -> list[str]:
    return sorted({ref.source_id for ref in recipe.evidence_refs})


def _source_urls(recipe) -> list[str]:
    urls = {str(ref.url) for ref in recipe.evidence_refs}
    urls.update(str(ref.final_url) for ref in recipe.evidence_refs)
    return sorted(urls)


def rebuild_index(paths: KbPaths) -> Path:
    records = []
    for directory in [paths.accepted_dir, paths.stale_dir]:
        for path in sorted(directory.glob("*.md")):
            recipe = parse_recipe_file(path)
            records.append(
                {
                    "id": recipe.id,
                    "path": str(path.relative_to(paths.root)),
                    "summary": _summary(recipe.id, recipe.failure_class, recipe.symptoms),
                    "status": recipe.status.value,
                    "stack": recipe.stack,
                    "source_ids": _source_ids(recipe),
                    "source_urls": _source_urls(recipe),
                    "failure_class": recipe.failure_class,
                    "symptoms": recipe.symptoms,
                    "fingerprints": recipe.fingerprints,
                    "first_checks": recipe.first_checks,
                    "do_not": recipe.do_not,
                    "validation_ladder": recipe.validation_ladder,
                    "stale": recipe.status is RecipeStatus.STALE,
                }
            )
    write_json(paths.index_path, {"recipes": records})
    return paths.index_path
