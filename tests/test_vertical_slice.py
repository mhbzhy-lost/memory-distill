from pathlib import Path

from typer.testing import CliRunner

from recipe_importer.cli import app
from recipe_importer.paths import KbPaths
from recipe_importer.storage import write_json, write_text, write_yaml


def test_vertical_slice_without_network(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    monkeypatch.chdir(repo)
    paths = KbPaths(repo).ensure()
    (repo / "prompts").mkdir()
    write_text(repo / "prompts" / "debug_recipe_evidence.md", "Extract evidence candidates.\n")
    write_yaml(
        paths.sources_dir / "source-list.yml",
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
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    html = Path(__file__).parent.joinpath("fixtures/react_error_418.html").read_text(encoding="utf-8")
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
    runner = CliRunner()

    assert runner.invoke(app, ["extract", str(snapshot_dir)]).exit_code == 0
    assert runner.invoke(app, ["import-source", str(snapshot_dir)]).exit_code == 0
    recipe_path = paths.proposed_dir / "react-hydration-mismatch.md"
    assert runner.invoke(app, ["check", str(recipe_path)]).exit_code == 0
    assert runner.invoke(app, ["publish", str(recipe_path)]).exit_code == 0
    assert runner.invoke(app, ["index", "rebuild"]).exit_code == 0
    search_result = runner.invoke(app, ["search", "Hydration failed"])
    get_result = runner.invoke(app, ["get", "react-hydration-mismatch"])

    assert search_result.exit_code == 0
    assert "react-hydration-mismatch" in search_result.stdout
    assert "Do not disable SSR" in search_result.stdout
    assert get_result.exit_code == 0
    assert '"id": "react-hydration-mismatch"' in get_result.stdout
