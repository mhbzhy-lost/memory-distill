import hashlib
from datetime import UTC, datetime
from pathlib import Path

import httpx

from recipe_importer.paths import KbPaths
from recipe_importer.sources import load_source_list
from recipe_importer.storage import write_json, write_text


def sha256_text(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()


def fetch_sources(
    source_list_path: Path,
    paths: KbPaths,
    *,
    client: httpx.Client | None = None,
    captured_at: str | None = None,
) -> list[Path]:
    source_list = load_source_list(source_list_path)
    owns_client = client is None
    http = client or httpx.Client(follow_redirects=True, timeout=30.0)
    captured = captured_at or datetime.now(UTC).isoformat().replace("+00:00", "Z")
    written: list[Path] = []
    try:
        for source in source_list.sources:
            response = http.get(str(source.url))
            response.raise_for_status()
            snapshot_dir = paths.snapshots_dir / source.source_id
            raw_path = snapshot_dir / "raw.html"
            metadata_path = snapshot_dir / "response.json"
            write_text(raw_path, response.text)
            write_json(
                metadata_path,
                {
                    "source_id": source.source_id,
                    "url": str(source.url),
                    "final_url": str(response.url),
                    "source_type": source.source_type,
                    "captured_at": captured,
                    "retrieved_status": response.status_code,
                    "content_type": response.headers.get("content-type", ""),
                    "content_hash": sha256_text(response.text),
                },
            )
            written.append(snapshot_dir)
    finally:
        if owns_client:
            http.close()
    return written
