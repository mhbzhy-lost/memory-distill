import json
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


def test_cli_refresh_prints_stale_paths(monkeypatch, tmp_path):
    def fake_refresh_stale_status(paths, source_list_path=None):
        return [paths.stale_dir / "react-hydration-mismatch.md"]

    monkeypatch.setattr(recipe_importer.cli, "refresh_stale_status", fake_refresh_stale_status, raising=False)

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["refresh"])

    assert result.exit_code == 0
    assert "stale: " in result.stdout
    assert "react-hydration-mismatch.md" in result.stdout


def test_cli_refresh_with_refetch_prints_stale(monkeypatch, tmp_path):
    received = {}

    def fake_refresh_stale_status(paths, source_list_path=None):
        received["source_list_path"] = source_list_path
        return [paths.stale_dir / "some-recipe.md"]

    monkeypatch.setattr(
        recipe_importer.cli,
        "refresh_stale_status",
        fake_refresh_stale_status,
        raising=False,
    )

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["refresh", "--refetch", "dummy-source.yml"])

    assert result.exit_code == 0
    assert "stale: " in result.stdout
    assert received["source_list_path"] == Path("dummy-source.yml")


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


def test_cli_import_source_produces_proposed_file(monkeypatch, tmp_path):
    class FakeCandidate:
        failure_label = "hydration mismatch"
        symptom_quotes = ["Hydration failed"]
        section_refs = ["react-error-418-1"]
        confidence = "high"

    class FakeCandidates:
        candidates = [FakeCandidate()]

    class FakeRecipe:
        id = "react-hydration-mismatch"

    def fake_deterministic_candidates(snapshot_dir):
        assert snapshot_dir == Path("recipe-kb/snapshots/react-error-418")
        return FakeCandidates()

    def fake_normalize_recipe(candidate, snapshot_dir, *, stack):
        assert stack == ["react", "nextjs"]
        return FakeRecipe()

    written = []

    def fake_render_recipe_file(recipe, target):
        written.append(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("---\nid: react-hydration-mismatch\n---\n\n# Body\n", encoding="utf-8")

    monkeypatch.setattr(recipe_importer.cli, "deterministic_candidates", fake_deterministic_candidates)
    monkeypatch.setattr(recipe_importer.cli, "normalize_recipe", fake_normalize_recipe)
    monkeypatch.setattr(recipe_importer.cli, "render_recipe_file", fake_render_recipe_file)

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        (tmp_path / "recipe-kb" / "proposed").mkdir(parents=True)
        result = runner.invoke(app, ["import-source", "recipe-kb/snapshots/react-error-418"])

    assert result.exit_code == 0
    assert written
    assert written[0].name == "react-hydration-mismatch.md"


def test_cli_import_source_uses_snapshot_stacks_by_default(monkeypatch, tmp_path):
    class FakeCandidate:
        failure_label = "vite esm-only config require"
        symptom_quotes = ["This package is ESM only"]
        section_refs = ["vite-troubleshooting-1"]
        confidence = "high"

    class FakeCandidates:
        candidates = [FakeCandidate()]

    class FakeRecipe:
        id = "vite-esm-only-config-require"

    monkeypatch.setattr(
        recipe_importer.cli,
        "deterministic_candidates",
        lambda snapshot_dir: FakeCandidates(),
    )

    stacks = []

    def fake_normalize_recipe(candidate, snapshot_dir, *, stack):
        stacks.append(stack)
        return FakeRecipe()

    monkeypatch.setattr(recipe_importer.cli, "normalize_recipe", fake_normalize_recipe)
    monkeypatch.setattr(
        recipe_importer.cli,
        "render_recipe_file",
        lambda recipe, target: target.parent.mkdir(parents=True, exist_ok=True)
        or target.write_text("---\nid: vite-esm-only-config-require\n---\n", encoding="utf-8"),
    )

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        snapshot = Path("recipe-kb/snapshots/vite-troubleshooting")
        snapshot.mkdir(parents=True)
        (snapshot / "response.json").write_text(
            json.dumps({"stacks": ["react", "vite"]}),
            encoding="utf-8",
        )
        result = runner.invoke(app, ["import-source", str(snapshot)])

    assert result.exit_code == 0
    assert stacks == [["react", "vite"]]


def test_cli_import_source_falls_back_when_snapshot_stacks_are_malformed(monkeypatch, tmp_path):
    class FakeCandidate:
        failure_label = "hydration mismatch"
        symptom_quotes = ["Hydration failed"]
        section_refs = ["react-error-418-1"]
        confidence = "high"

    class FakeCandidates:
        candidates = [FakeCandidate()]

    class FakeRecipe:
        id = "react-hydration-mismatch"

    monkeypatch.setattr(
        recipe_importer.cli,
        "deterministic_candidates",
        lambda snapshot_dir: FakeCandidates(),
    )

    stacks = []

    def fake_normalize_recipe(candidate, snapshot_dir, *, stack):
        stacks.append(stack)
        return FakeRecipe()

    monkeypatch.setattr(recipe_importer.cli, "normalize_recipe", fake_normalize_recipe)
    monkeypatch.setattr(
        recipe_importer.cli,
        "render_recipe_file",
        lambda recipe, target: target.parent.mkdir(parents=True, exist_ok=True)
        or target.write_text("---\nid: react-hydration-mismatch\n---\n", encoding="utf-8"),
    )

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        snapshot = Path("recipe-kb/snapshots/react-error-418")
        snapshot.mkdir(parents=True)
        (snapshot / "response.json").write_text("{not-json", encoding="utf-8")
        result = runner.invoke(app, ["import-source", str(snapshot)])

    assert result.exit_code == 0
    assert stacks == [["react", "nextjs"]]


def test_cli_import_source_falls_back_when_response_metadata_is_not_object(monkeypatch, tmp_path):
    class FakeCandidate:
        failure_label = "hydration mismatch"
        symptom_quotes = ["Hydration failed"]
        section_refs = ["react-error-418-1"]
        confidence = "high"

    class FakeCandidates:
        candidates = [FakeCandidate()]

    class FakeRecipe:
        id = "react-hydration-mismatch"

    monkeypatch.setattr(
        recipe_importer.cli,
        "deterministic_candidates",
        lambda snapshot_dir: FakeCandidates(),
    )

    stacks = []

    def fake_normalize_recipe(candidate, snapshot_dir, *, stack):
        stacks.append(stack)
        return FakeRecipe()

    monkeypatch.setattr(recipe_importer.cli, "normalize_recipe", fake_normalize_recipe)
    monkeypatch.setattr(
        recipe_importer.cli,
        "render_recipe_file",
        lambda recipe, target: target.parent.mkdir(parents=True, exist_ok=True)
        or target.write_text("---\nid: react-hydration-mismatch\n---\n", encoding="utf-8"),
    )

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        snapshot = Path("recipe-kb/snapshots/react-error-418")
        snapshot.mkdir(parents=True)
        (snapshot / "response.json").write_text("[]", encoding="utf-8")
        result = runner.invoke(app, ["import-source", str(snapshot)])

    assert result.exit_code == 0
    assert stacks == [["react", "nextjs"]]


def test_cli_import_source_reports_empty_candidates(monkeypatch, tmp_path):
    class FakeCandidates:
        candidates = []

    monkeypatch.setattr(
        recipe_importer.cli,
        "deterministic_candidates",
        lambda snapshot_dir: FakeCandidates(),
    )

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        (tmp_path / "recipe-kb" / "proposed").mkdir(parents=True)
        result = runner.invoke(app, ["import-source", "recipe-kb/snapshots/react-error-418"])

    assert result.exit_code == 1
    assert "没有生成候选 recipe" in result.stderr
    assert "agentic fallback" in result.stderr


def test_cli_check_passes_when_equivalent(monkeypatch, tmp_path):
    def fake_check_render_equivalence(recipe):
        assert recipe == Path("recipe-kb/proposed/test.md")
        return True

    monkeypatch.setattr(recipe_importer.cli, "check_render_equivalence", fake_check_render_equivalence)

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        (tmp_path / "recipe-kb" / "proposed").mkdir(parents=True)
        (tmp_path / "recipe-kb" / "proposed" / "test.md").write_text(
            "---\nid: test\n---\n\n# Body\n", encoding="utf-8"
        )
        result = runner.invoke(app, ["check", "recipe-kb/proposed/test.md"])

    assert result.exit_code == 0
    assert ": ok" in result.stdout


def test_cli_check_fails_when_not_equivalent(monkeypatch, tmp_path):
    def fake_check_render_equivalence(recipe):
        return False

    monkeypatch.setattr(recipe_importer.cli, "check_render_equivalence", fake_check_render_equivalence)

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        (tmp_path / "recipe-kb" / "proposed").mkdir(parents=True)
        result = runner.invoke(app, ["check", "recipe-kb/proposed/broken.md"])

    assert result.exit_code != 0


def test_cli_review_start_next_accept_uses_persisted_cursor(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        proposed = Path("recipe-kb/proposed")
        proposed.mkdir(parents=True)
        (proposed / "a.md").write_text("---\nid: a\n---\n", encoding="utf-8")
        (proposed / "b.md").write_text("---\nid: b\n---\n", encoding="utf-8")

        start = runner.invoke(app, ["review"])
        move = runner.invoke(app, ["review", "next"])
        current = runner.invoke(app, ["review"])
        decision = runner.invoke(app, ["review", "accept", "--notes", "looks good"])
        decisions = json.loads(Path("recipe-kb/review/decisions.json").read_text(encoding="utf-8"))

    assert start.exit_code == 0
    assert "a.md" in start.stdout
    assert move.exit_code == 0
    assert "b.md" in move.stdout
    assert current.exit_code == 0
    assert "b.md" in current.stdout
    assert decision.exit_code == 0
    assert "accepted" in decision.stdout
    assert decisions[0]["candidate_id"] == "b"


def test_cli_review_empty_queue_reports_clean_error(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["review"])

    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert "review queue is empty" in result.stderr


def test_cli_publish_index_search_and_get(monkeypatch, tmp_path):
    def fake_publish_recipe(recipe, paths):
        assert recipe == Path("recipe-kb/proposed/react-hydration-mismatch.md")
        return paths.accepted_dir / recipe.name

    def fake_rebuild_index(paths):
        return paths.index_path

    def fake_search_recipes(paths, query, *, fresh_only=False):
        assert query == "Hydration failed"
        assert fresh_only is True
        return [
            {
                "id": "react-hydration-mismatch",
                "summary": "render/hydration: Hydration failed",
                "stale": False,
                "first_checks": ["Check browser-only branches"],
                "do_not": ["Do not disable SSR"],
                "validation_ladder": ["Reproduce the affected route"],
            }
        ]

    class FakeRecipe:
        def model_dump_json(self, indent):
            assert indent == 2
            return '{\n  "id": "react-hydration-mismatch"\n}'

    def fake_get_recipe(paths, recipe_id):
        assert recipe_id == "react-hydration-mismatch"
        return FakeRecipe()

    monkeypatch.setattr(recipe_importer.cli, "publish_recipe", fake_publish_recipe, raising=False)
    monkeypatch.setattr(recipe_importer.cli, "rebuild_index", fake_rebuild_index, raising=False)
    monkeypatch.setattr(recipe_importer.cli, "search_recipes", fake_search_recipes, raising=False)
    monkeypatch.setattr(recipe_importer.cli, "get_recipe", fake_get_recipe, raising=False)

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        publish = runner.invoke(app, ["publish", "recipe-kb/proposed/react-hydration-mismatch.md"])
        rebuild = runner.invoke(app, ["index", "rebuild"])
        search = runner.invoke(app, ["search", "Hydration failed", "--fresh-only"])
        get = runner.invoke(app, ["get", "react-hydration-mismatch"])

    assert publish.exit_code == 0
    assert "recipe-kb/accepted/react-hydration-mismatch.md" in publish.stdout
    assert rebuild.exit_code == 0
    assert "recipe-kb/index.json" in rebuild.stdout
    assert search.exit_code == 0
    assert "react-hydration-mismatch" in search.stdout
    assert "summary: render/hydration: Hydration failed" in search.stdout
    assert "check: Check browser-only branches" in search.stdout
    assert "do-not: Do not disable SSR" in search.stdout
    assert "validate: Reproduce the affected route" in search.stdout
    assert get.exit_code == 0
    assert '"id": "react-hydration-mismatch"' in get.stdout


def test_cli_publish_reports_render_equivalence_error(monkeypatch, tmp_path):
    def fake_publish_recipe(recipe, paths):
        raise ValueError(f"{recipe} is not render-equivalent")

    monkeypatch.setattr(recipe_importer.cli, "publish_recipe", fake_publish_recipe, raising=False)

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["publish", "recipe-kb/proposed/broken.md"])

    assert result.exit_code != 0
    assert "not render-equivalent" in result.stderr


def test_cli_publish_reports_missing_file(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["publish", "recipe-kb/proposed/missing.md"])

    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert "recipe file not found" in result.stderr


def test_cli_search_reports_missing_index(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["search", "Hydration failed"])

    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert "run `recipe-importer index rebuild`" in result.stderr


def test_cli_search_reports_invalid_index(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        recipe_kb = Path("recipe-kb")
        recipe_kb.mkdir()
        (recipe_kb / "index.json").write_text('{"not_recipes": []}\n', encoding="utf-8")

        result = runner.invoke(app, ["search", "Hydration failed"])

    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert "recipe index is invalid" in result.stderr


def test_cli_get_reports_unknown_recipe(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        recipe_kb = Path("recipe-kb")
        recipe_kb.mkdir()
        (recipe_kb / "index.json").write_text('{"recipes": []}\n', encoding="utf-8")

        result = runner.invoke(app, ["get", "missing-recipe"])

    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert "recipe not found: missing-recipe" in result.stderr


def test_cli_index_rebuild_reports_malformed_recipe(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        accepted = Path("recipe-kb/accepted")
        accepted.mkdir(parents=True)
        (accepted / "broken.md").write_text("not a recipe\n", encoding="utf-8")

        result = runner.invoke(app, ["index", "rebuild"])

    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert "broken.md" in result.stderr
