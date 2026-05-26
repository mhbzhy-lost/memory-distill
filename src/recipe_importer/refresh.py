from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import httpx

from recipe_importer.fetch import sha256_text
from recipe_importer.models import RecipeStatus, Source
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file, render_recipe_file
from recipe_importer.storage import read_json, write_json, write_text


@dataclass(frozen=True)
class RefetchResult:
    source_id: str
    removed: bool
    final_url: str | None = None


def _refetch_single_source(
    source: Source,
    paths: KbPaths,
    client: httpx.Client,
) -> RefetchResult:
    try:
        response = client.get(str(source.url))
        response.raise_for_status()
    except (httpx.HTTPStatusError, httpx.HTTPError):
        return RefetchResult(source_id=source.source_id, removed=True)

    snapshot_dir = paths.snapshots_dir / source.source_id
    raw_path = snapshot_dir / "raw.html"
    metadata_path = snapshot_dir / "response.json"
    captured = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    write_text(raw_path, response.text)
    write_json(
        metadata_path,
        {
            "source_id": source.source_id,
            "url": str(source.url),
            "final_url": str(response.url),
            "source_type": source.source_type,
            "stacks": source.stacks,
            "expected_failure_hints": source.expected_failure_hints,
            "expected_build_hints": source.expected_build_hints,
            "refresh_policy": source.refresh_policy,
            "extraction_profile": source.extraction_profile.model_dump(),
            "captured_at": captured,
            "retrieved_status": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "content_hash": sha256_text(response.text),
        },
    )
    return RefetchResult(
        source_id=source.source_id,
        removed=False,
        final_url=str(response.url),
    )


def _current_quote_hashes(paths: KbPaths, source_id: str) -> dict[str, str] | None:
    sections_path = paths.snapshots_dir / source_id / "sections.json"
    if not sections_path.exists():
        return None
    return {item["span_id"]: item["quote_hash"] for item in read_json(sections_path)}


def refresh_stale_status(
    paths: KbPaths,
    source_list_path: Path | None = None,
    client: httpx.Client | None = None,
) -> list[Path]:
    from recipe_importer.sources import load_source_list

    stale_paths: list[Path] = []
    detected_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    removed_source_ids: set[str] = set()

    if source_list_path is not None:
        source_list = load_source_list(source_list_path)
        owns_client = client is None
        http = client or httpx.Client(follow_redirects=True, timeout=30.0)
        try:
            for source in source_list.sources:
                result = _refetch_single_source(source, paths, http)
                if result.removed:
                    removed_source_ids.add(source.source_id)
                else:
                    from recipe_importer.extract import extract_snapshot
                    extract_snapshot(paths.snapshots_dir / source.source_id)
        finally:
            if owns_client:
                http.close()

    for recipe_path in sorted(paths.accepted_dir.glob("*.md")):
        recipe = parse_recipe_file(recipe_path)
        stale_reasons: list[str] = []

        recipe_source_ids = {ref.source_id for ref in recipe.evidence_refs}
        if recipe_source_ids & removed_source_ids:
            stale_reasons.append("source_removed")

        hashes_by_source: dict[str, dict[str, str] | None] = {}
        for ref in recipe.evidence_refs:
            if ref.source_id in removed_source_ids:
                continue
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
