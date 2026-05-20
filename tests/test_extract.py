from pathlib import Path

from recipe_importer.extract import extract_snapshot
from recipe_importer.paths import KbPaths
from recipe_importer.storage import read_json, write_json, write_text


def test_extract_snapshot_writes_sections_and_evidence(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    fixture = Path("tests/fixtures/react_error_418.html").read_text(encoding="utf-8")
    write_text(snapshot_dir / "raw.html", fixture)
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-20T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
        },
    )

    result = extract_snapshot(snapshot_dir)

    sections = read_json(snapshot_dir / "sections.json")
    readable = (snapshot_dir / "readable.md").read_text(encoding="utf-8")

    assert result.source_id == "react-error-418"
    assert result.section_count == 8
    assert sections[0]["span_id"] == "react-error-418-1"
    assert sections[0]["short_excerpt"].startswith("Hydration failed")
    assert "Hydration failed" in readable
    assert sections[0]["quote_hash"].startswith("sha256:")
