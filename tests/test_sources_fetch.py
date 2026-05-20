import httpx

from recipe_importer.fetch import fetch_sources
from recipe_importer.paths import KbPaths
from recipe_importer.sources import load_source_list
from recipe_importer.storage import read_json, write_yaml


def test_load_source_list(kb_root):
    path = kb_root / "recipe-kb" / "sources" / "source-list.yml"
    write_yaml(
        path,
        {
            "sources": [
                {
                    "source_id": "react-error-418",
                    "url": "https://react.dev/errors/418",
                    "source_type": "official_error_doc",
                    "stacks": ["react", "nextjs"],
                    "expected_failure_hints": ["hydration mismatch"],
                    "refresh_policy": "monthly",
                }
            ]
        },
    )

    source_list = load_source_list(path)

    assert source_list.sources[0].source_id == "react-error-418"
    assert source_list.sources[0].stacks == ["react", "nextjs"]


def test_fetch_sources_writes_metadata_and_readable_seed(kb_root):
    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://react.dev/errors/418"
        return httpx.Response(
            200,
            headers={"content-type": "text/html"},
            text="<html><body><h1>Hydration failed</h1><p>server rendered HTML did not match</p></body></html>",
        )

    source_path = kb_root / "recipe-kb" / "sources" / "source-list.yml"
    write_yaml(
        source_path,
        {
            "sources": [
                {
                    "source_id": "react-error-418",
                    "url": "https://react.dev/errors/418",
                    "source_type": "official_error_doc",
                    "stacks": ["react"],
                    "expected_failure_hints": ["hydration mismatch"],
                    "refresh_policy": "monthly",
                }
            ]
        },
    )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    paths = KbPaths(kb_root).ensure()
    written = fetch_sources(source_path, paths, client=client, captured_at="2026-05-20T00:00:00Z")

    assert len(written) == 1
    metadata = read_json(paths.snapshots_dir / "react-error-418" / "response.json")
    html = (paths.snapshots_dir / "react-error-418" / "raw.html").read_text(encoding="utf-8")

    assert metadata["source_id"] == "react-error-418"
    assert metadata["retrieved_status"] == 200
    assert metadata["captured_at"] == "2026-05-20T00:00:00Z"
    assert "Hydration failed" in html
