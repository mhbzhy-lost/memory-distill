from pathlib import Path
from unittest.mock import MagicMock

import httpx
import yaml

from recipe_importer.extract import extract_snapshot
from recipe_importer.index import rebuild_index
from recipe_importer.llm import deterministic_candidates
from recipe_importer.models import Source
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.publish import publish_recipe
from recipe_importer.refresh import _refetch_single_source, RefetchResult, refresh_stale_status
from recipe_importer.render import parse_recipe_file, render_recipe_file
from recipe_importer.storage import read_json, write_json, write_text


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _published_recipe(paths: KbPaths) -> tuple[Path, Path]:
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    html = (FIXTURES_DIR / "react_error_418.html").read_text(encoding="utf-8")
    write_text(snapshot_dir / "raw.html", html)
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
    extract_snapshot(snapshot_dir)
    recipe = normalize_recipe(
        deterministic_candidates(snapshot_dir).candidates[0],
        snapshot_dir,
        stack=["react", "nextjs"],
    )
    proposed = paths.proposed_dir / "react-hydration-mismatch.md"
    render_recipe_file(recipe, proposed)
    return publish_recipe(proposed, paths), snapshot_dir


def test_refresh_marks_recipe_stale_when_quote_hash_changes(kb_root):
    paths = KbPaths(kb_root).ensure()
    accepted, snapshot_dir = _published_recipe(paths)

    sections_path = snapshot_dir / "sections.json"
    sections = read_json(sections_path)
    sections[0]["quote_hash"] = "sha256:changed"
    write_json(sections_path, sections)

    stale_paths = refresh_stale_status(paths)
    rebuild_index(paths)

    stale_path = paths.stale_dir / "react-hydration-mismatch.md"
    recipe = parse_recipe_file(stale_path)

    assert stale_paths == [stale_path]
    assert stale_path.exists()
    assert not accepted.exists()
    assert recipe.status == "stale"
    assert recipe.maintenance.state == "stale"
    assert recipe.maintenance.stale_reason == ["source_quote_hash_changed"]


def test_refresh_uses_referenced_span_not_source_wide_hash(kb_root):
    paths = KbPaths(kb_root).ensure()
    accepted, snapshot_dir = _published_recipe(paths)
    recipe = parse_recipe_file(accepted)
    old_hash = recipe.evidence_refs[0].quote_hash
    old_span_id = recipe.evidence_refs[0].span_id

    sections_path = snapshot_dir / "sections.json"
    sections = read_json(sections_path)
    assert sections[0]["span_id"] == old_span_id
    sections[0]["quote_hash"] = "sha256:changed"
    sections[1]["quote_hash"] = old_hash
    write_json(sections_path, sections)

    stale_paths = refresh_stale_status(paths)

    assert stale_paths == [paths.stale_dir / "react-hydration-mismatch.md"]
    assert not accepted.exists()


def test_refresh_skips_missing_local_sections_without_state_change(kb_root):
    paths = KbPaths(kb_root).ensure()
    accepted, snapshot_dir = _published_recipe(paths)
    (snapshot_dir / "sections.json").unlink()

    stale_paths = refresh_stale_status(paths)

    assert stale_paths == []
    assert accepted.exists()
    assert not (paths.stale_dir / accepted.name).exists()


def test_refresh_keeps_recipe_accepted_when_quote_hash_matches(kb_root):
    paths = KbPaths(kb_root).ensure()
    accepted, _snapshot_dir = _published_recipe(paths)

    stale_paths = refresh_stale_status(paths)

    assert stale_paths == []
    assert accepted.exists()


def test_refetch_single_source_writes_metadata(kb_root):
    paths = KbPaths(kb_root).ensure()

    fake_response = MagicMock(spec=httpx.Response)
    fake_response.status_code = 200
    fake_response.url = "https://react.dev/errors/418"
    fake_response.text = "<html><body>hydration mismatch</body></html>"
    fake_response.headers = {"content-type": "text/html"}
    fake_response.raise_for_status = MagicMock()

    class FakeClient:
        def get(self, url, **kwargs):
            return fake_response
        def close(self):
            pass

    source = Source(
        source_id="react-error-418",
        url="https://react.dev/errors/418",
        source_type="official_error_doc",
        stacks=["react"],
    )
    result = _refetch_single_source(source, paths, FakeClient())

    assert result.removed is False
    assert result.source_id == "react-error-418"
    assert result.final_url == "https://react.dev/errors/418"
    raw_html = (paths.snapshots_dir / "react-error-418" / "raw.html").read_text(encoding="utf-8")
    assert "hydration mismatch" in raw_html
    metadata = read_json(paths.snapshots_dir / "react-error-418" / "response.json")
    assert metadata["source_id"] == "react-error-418"
    assert metadata["final_url"] == "https://react.dev/errors/418"
    assert metadata["content_hash"].startswith("sha256:")


def test_refetch_single_source_removed_on_404(kb_root):
    paths = KbPaths(kb_root).ensure()

    class Fake404Client:
        def get(self, url, **kwargs):
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 404
            resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                request=MagicMock(), response=resp, message="Client error"
            )
            return resp
        def close(self):
            pass

    source = Source(
        source_id="dead-source",
        url="https://example.com/dead",
        source_type="official_error_doc",
        stacks=["react"],
    )
    result = _refetch_single_source(source, paths, Fake404Client())
    assert result.removed is True
    assert result.final_url is None


def test_refetch_single_source_removed_on_network_error(kb_root):
    paths = KbPaths(kb_root).ensure()

    class FakeNetworkError:
        def get(self, url, **kwargs):
            raise httpx.ConnectError("connection refused")
        def close(self):
            pass

    source = Source(
        source_id="timeout-source",
        url="https://example.com/timeout",
        source_type="official_error_doc",
        stacks=["react"],
    )
    result = _refetch_single_source(source, paths, FakeNetworkError())
    assert result.removed is True
    assert result.final_url is None


def test_refresh_marks_recipe_stale_when_source_removed(kb_root):
    paths = KbPaths(kb_root).ensure()
    accepted, snapshot_dir = _published_recipe(paths)

    source_list_path = paths.sources_dir / "source-list.yml"
    source_list_path.write_text(
        yaml.safe_dump({
            "sources": [{
                "source_id": "react-error-418",
                "url": "https://react.dev/errors/418",
                "source_type": "official_error_doc",
                "stacks": ["react", "nextjs"],
            }]
        }),
        encoding="utf-8",
    )

    class Fake404Client:
        def get(self, url, **kwargs):
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 404
            resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                request=MagicMock(), response=resp, message="404"
            )
            return resp
        def close(self):
            pass

    stale_paths = refresh_stale_status(paths, source_list_path, Fake404Client())

    stale_path = paths.stale_dir / "react-hydration-mismatch.md"
    assert stale_paths == [stale_path]
    recipe = parse_recipe_file(stale_path)
    assert "source_removed" in recipe.maintenance.stale_reason
