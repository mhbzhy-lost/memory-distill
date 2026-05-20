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


def test_cli_manifest_refresh_prints_prompt_revision(monkeypatch, tmp_path):
    class FakeItem:
        rev = 3

    class FakeManifest:
        prompts = {"debug_recipe_evidence": FakeItem()}

    def fake_refresh_manifest(root):
        assert root == Path.cwd()
        return FakeManifest()

    monkeypatch.setattr(recipe_importer.cli, "refresh_manifest", fake_refresh_manifest, raising=False)
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["manifest", "refresh"])

    assert result.exit_code == 0
    assert "debug_recipe_evidence rev 3" in result.stdout


def test_cli_manifest_check_exits_nonzero_when_hashes_drift(monkeypatch, tmp_path):
    monkeypatch.setattr(recipe_importer.cli, "check_manifest", lambda root: False, raising=False)
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["manifest", "check"])

    assert result.exit_code == 1


def test_cli_extract_prints_section_count(monkeypatch, tmp_path):
    class FakeExtractionResult:
        source_id = "react-error-418"
        section_count = 8

    def fake_extract_snapshot(snapshot_dir):
        assert snapshot_dir == Path("recipe-kb/snapshots/react-error-418")
        return FakeExtractionResult()

    monkeypatch.setattr(recipe_importer.cli, "extract_snapshot", fake_extract_snapshot, raising=False)
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["extract", "recipe-kb/snapshots/react-error-418"])

    assert result.exit_code == 0
    assert "react-error-418: 8 sections" in result.stdout
