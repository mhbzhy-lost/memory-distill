from collections import defaultdict
from pathlib import Path
from typing import Optional

import yaml
from pydantic import ValidationError

from recipe_importer.models import AnyRecipe, BuildRecipe, Recipe, RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file
from recipe_importer.storage import read_json, write_json


class IndexBuildError(ValueError):
    pass


def _source_ids(recipe: AnyRecipe) -> list[str]:
    return sorted({ref.source_id for ref in recipe.evidence_refs})


def _source_urls(recipe: AnyRecipe) -> list[str]:
    urls = {str(ref.url) for ref in recipe.evidence_refs}
    urls.update(str(ref.final_url) for ref in recipe.evidence_refs)
    return sorted(urls)


def _debug_record(recipe: Recipe, path: Path, root: Path) -> dict:
    summary = f"{recipe.failure_class}: {recipe.symptoms[0]}" if recipe.symptoms else f"{recipe.failure_class}: {recipe.id}"
    return {
        "id": recipe.id,
        "kind": "debug-recipe",
        "path": str(path.relative_to(root)),
        "summary": summary,
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


def _build_record(recipe: BuildRecipe, path: Path, root: Path) -> dict:
    summary = f"[build] {recipe.constraints[0]}" if recipe.constraints else f"[build] {recipe.id}"
    return {
        "id": recipe.id,
        "kind": "build-recipe",
        "path": str(path.relative_to(root)),
        "summary": summary,
        "status": recipe.status.value,
        "stack": recipe.stack,
        "source_ids": _source_ids(recipe),
        "source_urls": _source_urls(recipe),
        "constraints": recipe.constraints,
        "correct_pattern": recipe.correct_pattern,
        "do_not": recipe.do_not,
        "validation": recipe.validation,
        "trigger_description": recipe.trigger.description,
        "related_debug_recipes": recipe.related_debug_recipes,
        "stale": recipe.status is RecipeStatus.STALE,
    }


def rebuild_index(paths: KbPaths) -> Path:
    records = []
    for directory in [paths.accepted_dir, paths.stale_dir]:
        for path in sorted(directory.glob("*.md")):
            try:
                recipe = parse_recipe_file(path)
            except (OSError, ValueError, yaml.YAMLError, ValidationError) as exc:
                raise IndexBuildError(f"failed to index {path}: {exc}") from exc
            if isinstance(recipe, BuildRecipe):
                records.append(_build_record(recipe, path, paths.root))
            else:
                records.append(_debug_record(recipe, path, paths.root))
    write_json(paths.index_path, {"recipes": records})
    return paths.index_path


def _read_index(paths: KbPaths) -> dict:
    data = read_json(paths.index_path)
    if not isinstance(data, dict):
        raise ValueError("recipe index is not an object")
    return data


def list_stacks(paths: KbPaths, stack_filter: Optional[str] = None) -> dict[str, list[dict]]:
    """Group recipes by stack, optionally filtering by stack name."""
    index = _read_index(paths)
    stacked = defaultdict(list)

    for recipe in index.get("recipes", []):
        for stack in recipe.get("stack", []):
            stacked[stack].append({
                "id": recipe["id"],
                "status": recipe["status"],
                "stale": recipe["status"] == "stale",
            })

    for stack in stacked:
        stacked[stack].sort(key=lambda r: r["id"])

    if stack_filter:
        stack_filter_lower = stack_filter.lower()
        stacked = {
            k: v for k, v in stacked.items()
            if k.lower() == stack_filter_lower
        }

    return dict(stacked)
