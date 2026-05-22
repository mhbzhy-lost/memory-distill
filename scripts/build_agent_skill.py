#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import stat
import sys
import textwrap
from pathlib import Path


SKILL_NAME = "debug-recipe-importer"
BUNDLE_DIR = Path("assets") / "recipe-importer"
DEFAULT_OUTPUT = Path("dist") / "skills" / SKILL_NAME

COPY_ENTRIES = [
    Path("pyproject.toml"),
    Path("uv.lock"),
    Path("bin"),
    Path("src"),
    Path("schemas"),
    Path("prompts"),
    Path("recipe-kb"),
]

EXCLUDED_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "dist",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def skill_markdown() -> str:
    return textwrap.dedent(
        """\
        ---
        name: debug-recipe-importer
        description: Use when an agent needs to search, inspect, or maintain the bundled memory-distill debug recipe knowledge base; includes the recipe-importer CLI, accepted recipes, JSON schemas, prompts, and source evidence snapshots.
        ---

        # Debug Recipe Importer

        Use this skill before patching a known framework or runtime failure, or when the user asks to search, inspect, import, review, publish, refresh, or maintain reviewed debug recipes.

        ## Quick Workflow

        1. Search the bundled knowledge base:
           `scripts/recipe-importer search "<error text or symptom>"`
        2. Inspect the full canonical recipe:
           `scripts/recipe-importer get <recipe-id>`
        3. Follow `first_checks` and gather `evidence_needed` before changing code.
        4. If a recipe is stale, treat it as a warning and refresh source evidence before relying on it.

        ## Bundled CLI

        The wrapper at `scripts/recipe-importer` runs the Python CLI from `assets/recipe-importer`.

        - Default root: the bundled `assets/recipe-importer` directory.
        - Project-local root: set `RECIPE_IMPORTER_ROOT=/absolute/project/root` before invoking the wrapper.
        - Network is explicit: only `fetch` and `refresh` should contact source sites.

        Useful commands:

        ```bash
        scripts/recipe-importer search "Hydration failed"
        scripts/recipe-importer get react-hydration-mismatch
        scripts/recipe-importer check recipe-kb/accepted/react-hydration-mismatch.md
        scripts/recipe-importer index rebuild
        scripts/recipe-importer manifest check
        ```

        ## Maintenance

        Generated Markdown recipe bodies are views of YAML frontmatter. Do not hand-edit semantic body sections. Update YAML or importer code, then run `check` and `index rebuild`.

        When maintaining the importer itself, document each newly discovered bug in `docs/bugs/` before fixing it. After the bug record exists, proceed with TDD and verification without waiting for another human approval.

        ## 人审文本语言

        人审的人类可读文本必须使用中文编写。适用范围包括 review summary、review checklist、面向审阅者的 CLI 提示，以及任何需要人类批准的说明文本。源证据摘录、代码标识、命令、schema 字段名和外部专有名词保持原文，避免翻译导致证据偏移。
        """
    )


def openai_yaml() -> str:
    return textwrap.dedent(
        """\
        interface:
          display_name: "Debug Recipe Importer"
          short_description: "Search reviewed debugging recipes"
          default_prompt: "Use $debug-recipe-importer to search for a reviewed debug recipe before patching this failure."
        """
    )


def wrapper_script() -> str:
    return textwrap.dedent(
        """\
        #!/usr/bin/env bash
        set -euo pipefail

        if ! command -v uv >/dev/null 2>&1; then
          echo "uv is required to run the bundled recipe-importer CLI" >&2
          exit 127
        fi

        script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
        skill_dir="$(cd -- "${script_dir}/.." && pwd)"
        bundle_dir="${skill_dir}/assets/recipe-importer"
        repo_root="${RECIPE_IMPORTER_ROOT:-${bundle_dir}}"

        cd "${repo_root}"
        exec uv run --frozen --project "${bundle_dir}" recipe-importer "$@"
        """
    )


def is_excluded(source_path: Path, repo_root: Path) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in source_path.parts):
        return True
    if source_path.suffix in EXCLUDED_SUFFIXES:
        return True

    relative = source_path.relative_to(repo_root).as_posix()
    if relative.startswith("recipe-kb/snapshots/") and relative.endswith("/raw.html"):
        return True
    return False


def copy_entry(source: Path, target: Path, repo_root: Path) -> None:
    if source.is_symlink():
        return
    if is_excluded(source, repo_root):
        return
    if source.is_dir():
        target.mkdir(parents=True, exist_ok=True)
        for child in sorted(source.iterdir()):
            copy_entry(child, target / child.name, repo_root)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def make_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_output_location(repo_root: Path, output_dir: Path) -> None:
    resolved_repo = repo_root.resolve()
    resolved_output = output_dir.resolve()
    if resolved_output in {resolved_repo, resolved_repo.parent}:
        raise ValueError(f"refusing to remove unsafe output directory: {output_dir}")

    resolved_dist = (repo_root / "dist").resolve()
    if is_relative_to(resolved_output, resolved_repo) and not is_relative_to(
        resolved_output,
        resolved_dist,
    ):
        raise ValueError(f"refusing to write inside repository outside dist/: {output_dir}")


def validate_output_target(repo_root: Path, output_dir: Path, *, force: bool) -> None:
    validate_output_location(repo_root, output_dir)
    if output_dir.exists():
        if not force:
            raise FileExistsError(f"output directory already exists: {output_dir}")
        if not output_dir.is_dir() or output_dir.is_symlink():
            raise ValueError(f"output path exists and is not a directory: {output_dir}")


def populate_skill(repo_root: Path, target_dir: Path) -> None:
    write_text(target_dir / "SKILL.md", skill_markdown())
    write_text(target_dir / "agents" / "openai.yaml", openai_yaml())

    wrapper = target_dir / "scripts" / "recipe-importer"
    write_text(wrapper, wrapper_script())
    make_executable(wrapper)

    bundle_root = target_dir / BUNDLE_DIR
    for entry in COPY_ENTRIES:
        copy_entry(repo_root / entry, bundle_root / entry, repo_root)

    make_executable(bundle_root / "bin" / "recipe-importer")


def build_skill(repo_root: Path, output_dir: Path, *, force: bool) -> Path:
    validate_output_target(repo_root, output_dir, force=force)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = output_dir.parent / f".{output_dir.name}.tmp"
    if temp_dir.exists():
        remove_path(temp_dir)

    try:
        populate_skill(repo_root, temp_dir)
        if output_dir.exists():
            remove_path(output_dir)
        temp_dir.rename(output_dir)
    except BaseException:
        if temp_dir.exists():
            remove_path(temp_dir)
        raise

    return output_dir


def iter_copy_files(source: Path, repo_root: Path):
    if source.is_symlink() or is_excluded(source, repo_root):
        return
    if source.is_dir():
        for child in sorted(source.iterdir()):
            yield from iter_copy_files(child, repo_root)
        return
    yield source.relative_to(repo_root)


def planned_skill_files(repo_root: Path) -> list[Path]:
    files = [
        Path("SKILL.md"),
        Path("agents") / "openai.yaml",
        Path("scripts") / "recipe-importer",
    ]
    for entry in COPY_ENTRIES:
        for relative_source in iter_copy_files(repo_root / entry, repo_root):
            files.append(BUNDLE_DIR / relative_source)
    return files


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the debug-recipe-importer Codex skill.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output skill directory. Defaults to {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing output directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned skill package contents without writing files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = args.output if args.output.is_absolute() else repo_root / args.output

    try:
        if args.dry_run:
            validate_output_location(repo_root, output_dir)
            print(f"would write skill: {output_dir}")
            for planned_file in planned_skill_files(repo_root):
                print(planned_file.as_posix())
            return 0

        built = build_skill(repo_root, output_dir, force=args.force)
    except (FileExistsError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(built)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
