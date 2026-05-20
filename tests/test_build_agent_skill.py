import os
import stat
import subprocess
import sys
import importlib.util
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGER = REPO_ROOT / "scripts" / "build_agent_skill.py"


def load_packager_module():
    spec = importlib.util.spec_from_file_location("build_agent_skill", PACKAGER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_packager(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PACKAGER), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_build_agent_skill_packages_cli_code_and_static_assets(tmp_path):
    output_dir = tmp_path / "debug-recipe-importer"

    result = run_packager("--output", str(output_dir))

    assert result.returncode == 0, result.stderr
    assert (output_dir / "SKILL.md").is_file()
    assert (output_dir / "agents" / "openai.yaml").is_file()
    wrapper = output_dir / "scripts" / "recipe-importer"
    assert wrapper.is_file()
    assert wrapper.stat().st_mode & stat.S_IXUSR
    assert "--frozen" in wrapper.read_text(encoding="utf-8")

    bundle = output_dir / "assets" / "recipe-importer"
    for packaged_path in [
        "pyproject.toml",
        "uv.lock",
        "src/recipe_importer/cli.py",
        "bin/recipe-importer",
        "schemas/debug-recipe.schema.json",
        "prompts/debug_recipe_evidence.md",
        "recipe-kb/accepted/react-hydration-mismatch.md",
        "recipe-kb/index.json",
        "recipe-kb/snapshots/react-error-418/sections.json",
    ]:
        assert (bundle / packaged_path).exists()

    assert not list(bundle.glob("recipe-kb/snapshots/**/raw.html"))


def test_generated_skill_wrapper_runs_against_bundled_kb(tmp_path):
    output_dir = tmp_path / "debug-recipe-importer"
    result = run_packager("--output", str(output_dir))
    assert result.returncode == 0, result.stderr

    wrapper = output_dir / "scripts" / "recipe-importer"
    env = {
        **os.environ,
        "UV_OFFLINE": "1",
        "UV_PROJECT_ENVIRONMENT": str(tmp_path / "venv"),
    }
    version = subprocess.run(
        [str(wrapper), "version"],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    assert version.returncode == 0, version.stderr
    assert "recipe-importer 0.1.0" in version.stdout

    search = subprocess.run(
        [str(wrapper), "search", "Hydration failed"],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    assert search.returncode == 0, search.stderr
    assert "react-hydration-mismatch" in search.stdout
    assert "Do not disable SSR as the first fix" in search.stdout


def test_build_agent_skill_refuses_existing_output_without_force(tmp_path):
    output_dir = tmp_path / "debug-recipe-importer"
    first = run_packager("--output", str(output_dir))
    assert first.returncode == 0, first.stderr

    second = run_packager("--output", str(output_dir))
    assert second.returncode != 0
    assert "already exists" in second.stderr

    forced = run_packager("--output", str(output_dir), "--force")
    assert forced.returncode == 0, forced.stderr


def test_build_agent_skill_force_replaces_directory_but_refuses_file(tmp_path):
    output_dir = tmp_path / "debug-recipe-importer"
    output_dir.mkdir()
    stale_file = output_dir / "stale.txt"
    stale_file.write_text("old", encoding="utf-8")

    forced = run_packager("--output", str(output_dir), "--force")

    assert forced.returncode == 0, forced.stderr
    assert not stale_file.exists()
    assert (output_dir / "SKILL.md").is_file()

    file_output = tmp_path / "not-a-directory"
    file_output.write_text("keep", encoding="utf-8")
    refused = run_packager("--output", str(file_output), "--force")

    assert refused.returncode != 0
    assert "not a directory" in refused.stderr
    assert file_output.read_text(encoding="utf-8") == "keep"


def test_build_agent_skill_excludes_cache_and_raw_artifacts():
    packager = load_packager_module()

    excluded = [
        "src/recipe_importer/__pycache__/cli.cpython-312.pyc",
        "src/recipe_importer/.mypy_cache/module.json",
        "src/recipe_importer/.pytest_cache/README.md",
        "src/recipe_importer/.venv/pyvenv.cfg",
        "src/recipe_importer/cache.pyo",
        "recipe-kb/snapshots/react-error-418/raw.html",
    ]

    for relative_path in excluded:
        assert packager.is_excluded(REPO_ROOT / relative_path, REPO_ROOT)


def test_build_agent_skill_skips_symlinks(tmp_path):
    packager = load_packager_module()
    repo = tmp_path / "repo"
    source = repo / "src"
    source.mkdir(parents=True)
    secret = tmp_path / "secret.txt"
    secret.write_text("do not package", encoding="utf-8")
    link = source / "linked-secret.txt"
    try:
        link.symlink_to(secret)
    except OSError:
        pytest.skip("symlinks are not supported on this filesystem")

    target = tmp_path / "out" / "src"
    packager.copy_entry(source, target, repo)

    assert not (target / "linked-secret.txt").exists()


def test_build_agent_skill_blocks_repo_internal_output_except_dist():
    packager = load_packager_module()

    packager.validate_output_target(
        REPO_ROOT,
        REPO_ROOT / "dist" / "skills" / "debug-recipe-importer",
        force=True,
    )
    with pytest.raises(ValueError, match="inside repository"):
        packager.validate_output_target(REPO_ROOT, REPO_ROOT / "src", force=True)


def test_build_agent_skill_dry_run_does_not_write_output(tmp_path):
    output_dir = tmp_path / "debug-recipe-importer"

    result = run_packager("--output", str(output_dir), "--dry-run")

    assert result.returncode == 0, result.stderr
    assert "would write skill" in result.stdout
    assert "assets/recipe-importer/src/recipe_importer/cli.py" in result.stdout
    assert not output_dir.exists()
