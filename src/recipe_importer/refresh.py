from datetime import UTC, datetime
from pathlib import Path

from recipe_importer.models import RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file, render_recipe_file
from recipe_importer.storage import read_json


def _current_quote_hashes(paths: KbPaths, source_id: str) -> dict[str, str] | None:
    sections_path = paths.snapshots_dir / source_id / "sections.json"
    if not sections_path.exists():
        return None
    return {item["span_id"]: item["quote_hash"] for item in read_json(sections_path)}


def refresh_stale_status(paths: KbPaths) -> list[Path]:
    stale_paths: list[Path] = []
    detected_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    for recipe_path in sorted(paths.accepted_dir.glob("*.md")):
        recipe = parse_recipe_file(recipe_path)
        stale_reasons: list[str] = []
        hashes_by_source: dict[str, dict[str, str] | None] = {}
        for ref in recipe.evidence_refs:
            if ref.source_id not in hashes_by_source:
                hashes_by_source[ref.source_id] = _current_quote_hashes(paths, ref.source_id)
            current_hashes = hashes_by_source[ref.source_id]
            if current_hashes is None:
                continue
            if current_hashes.get(ref.span_id) != ref.quote_hash:
                stale_reasons.append("source_quote_hash_changed")

        if stale_reasons:
            recipe.status = RecipeStatus.STALE
            recipe.maintenance.state = RecipeStatus.STALE
            recipe.maintenance.stale_reason = sorted(set(stale_reasons))
            recipe.maintenance.stale_detected_at = detected_at
            target = paths.stale_dir / recipe_path.name
            render_recipe_file(recipe, target)
            recipe_path.unlink()
            stale_paths.append(target)
    return stale_paths
