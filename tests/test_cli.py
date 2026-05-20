from pathlib import Path

from typer.testing import CliRunner

import recipe_importer.cli
from recipe_importer.cli import app


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "recipe-importer 0.1.0" in result.stdout


def test_cli_fetch_prints_written_snapshots(monkeypatch, tmp_path):
    def fake_fetch_sources(source_list, paths):
        assert source_list == Path("recipe-kb/sources/source-list.yml")
        return [paths.snapshots_dir / "react-error-418"]

    monkeypatch.setattr(recipe_importer.cli, "fetch_sources", fake_fetch_sources, raising=False)
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["fetch"])

    assert result.exit_code == 0
    assert "react-error-418" in result.stdout
