import logging
from pathlib import Path
from typing import Annotated, NoReturn, Optional

import typer

from recipe_importer import __version__
from recipe_importer.build_llm import deterministic_build_candidates
from recipe_importer.extract import extract_snapshot
from recipe_importer.fetch import fetch_sources
from recipe_importer.generate import generate_build_from_debug

from recipe_importer.index import IndexBuildError, list_stacks, rebuild_index
from recipe_importer.llm import deterministic_candidates
from recipe_importer.manifest import check_manifest, refresh_manifest
from recipe_importer.models import BuildRecipe, Recipe, RecipeStatus, ReviewDecision
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.publish import publish_recipe
from recipe_importer.refresh import refresh_stale_status
from recipe_importer.render import check_render_equivalence, parse_recipe_file, render_recipe_file
from recipe_importer.review import (
    ReviewSession,
    current_candidate,
    decide_current,
    load_review_session,
    next_candidate,
    previous_candidate,
    start_review,
)
from recipe_importer.schema import export_schemas
from recipe_importer.search import get_recipe, search_recipes
from recipe_importer.storage import read_json

app = typer.Typer(no_args_is_help=True)
schema_app = typer.Typer(no_args_is_help=True)
manifest_app = typer.Typer(no_args_is_help=True)
review_app = typer.Typer(no_args_is_help=False)
index_app = typer.Typer(no_args_is_help=True)
app.add_typer(schema_app, name="schema")
app.add_typer(manifest_app, name="manifest")
app.add_typer(review_app, name="review")
app.add_typer(index_app, name="index")
logger = logging.getLogger(__name__)

DEFAULT_STACK = ["react", "nextjs"]


@app.callback()
def main() -> None:
    pass


def _exit_error(message: str) -> NoReturn:
    typer.echo(message, err=True)
    raise typer.Exit(code=1)


def _snapshot_stacks(snapshot_dir: Path) -> list[str]:
    try:
        metadata = read_json(snapshot_dir / "response.json")
    except (OSError, ValueError) as exc:
        logger.warning("snapshot %s has unreadable response.json: %s", snapshot_dir, exc)
        return list(DEFAULT_STACK)
    if not isinstance(metadata, dict):
        logger.warning("snapshot %s response.json is not an object", snapshot_dir)
        return list(DEFAULT_STACK)
    stacks = metadata.get("stacks", [])
    if isinstance(stacks, list) and all(isinstance(item, str) for item in stacks) and stacks:
        return stacks
    logger.warning("snapshot %s has missing or malformed stacks", snapshot_dir)
    return list(DEFAULT_STACK)


@app.command(name="version")
def version() -> None:
    """Print the recipe importer version."""
    typer.echo(f"recipe-importer {__version__}")


@app.command()
def fetch(
    source_list: Annotated[Path, typer.Argument()] = Path("recipe-kb/sources/source-list.yml"),
) -> None:
    """Fetch configured sources and persist snapshot metadata."""
    paths = KbPaths(Path.cwd()).ensure()
    for path in fetch_sources(source_list, paths):
        typer.echo(str(path))


@schema_app.command("export")
def schema_export(
    output_dir: Annotated[Path, typer.Argument()] = Path("schemas"),
) -> None:
    """Export JSON Schemas for external adapters and review tooling."""
    for path in export_schemas(output_dir):
        typer.echo(str(path))


@manifest_app.command("refresh")
def manifest_refresh() -> None:
    """Refresh asset hashes and revisions."""
    manifest = refresh_manifest(Path.cwd())
    typer.echo(f"debug_recipe_evidence rev {manifest.prompts['debug_recipe_evidence'].rev}")


@manifest_app.command("check")
def manifest_check() -> None:
    """Check whether tracked asset hashes still match."""
    if not check_manifest(Path.cwd()):
        raise typer.Exit(code=1)
    typer.echo("manifest ok")


@app.command()
def refresh(
    refetch: Annotated[
        Path | None,
        typer.Option(help="Source list path for refetch-based stale check."),
    ] = None,
) -> None:
    """Mark accepted recipes stale when local refreshed evidence no longer matches."""
    paths = KbPaths(Path.cwd()).ensure()
    for path in refresh_stale_status(paths, source_list_path=refetch):
        typer.echo(f"stale: {path}")


@app.command()
def extract(
    snapshot_dir: Annotated[Path, typer.Argument()],
) -> None:
    """Extract readable sections from one local snapshot directory."""
    result = extract_snapshot(snapshot_dir)
    typer.echo(f"{result.source_id}: {result.section_count} sections")


@app.command(name="import-source")
def import_source(
    snapshot_dir: Annotated[Path, typer.Argument()],
    stack: Annotated[
        list[str] | None,
        typer.Option(help="Stack list. Defaults to snapshot metadata, then react/nextjs."),
    ] = None,
) -> None:
    """Create proposed recipes from one extracted snapshot."""
    paths = KbPaths(Path.cwd()).ensure()
    recipe_stack = stack if stack else _snapshot_stacks(snapshot_dir)
    produced = 0

    candidates = deterministic_candidates(snapshot_dir)
    for candidate in candidates.candidates:
        recipe = normalize_recipe(candidate, snapshot_dir, stack=recipe_stack)
        target = paths.proposed_dir / f"{recipe.id}.md"
        render_recipe_file(recipe, target)
        typer.echo(str(target))
        produced += 1

    build_recipes = deterministic_build_candidates(snapshot_dir)
    for build in build_recipes:
        target = paths.proposed_dir / f"{build.id}.md"
        render_recipe_file(build, target)
        typer.echo(str(target))
        produced += 1

    if produced == 0:
        _exit_error(
            "没有生成候选 recipe：请查看该 snapshot 的 review.md/qa.json；"
            "若 QA gate 失败，需要进入 agentic fallback 补充 extraction_profile 或 extractor。"
        )


@app.command()
def check(
    recipe: Annotated[Path, typer.Argument()],
) -> None:
    """Check that generated Markdown matches canonical YAML frontmatter."""
    if not check_render_equivalence(recipe):
        raise typer.BadParameter(f"{recipe} is not render-equivalent")
    typer.echo(f"{recipe}: ok")


def _review_session(paths: KbPaths) -> ReviewSession:
    try:
        return load_review_session(paths)
    except FileNotFoundError:
        return start_review(paths)


def _echo_current_review_candidate(paths: KbPaths, session: ReviewSession) -> None:
    try:
        candidate = current_candidate(paths, session)
    except ValueError as exc:
        _exit_error(str(exc))
    typer.echo(str(candidate))


@review_app.callback(invoke_without_command=True)
def review_start(ctx: typer.Context) -> None:
    """Start or show the review queue."""
    if ctx.invoked_subcommand is None:
        paths = KbPaths(Path.cwd()).ensure()
        _echo_current_review_candidate(paths, _review_session(paths))


@review_app.command("current")
def review_current() -> None:
    """Show the current proposed recipe."""
    paths = KbPaths(Path.cwd()).ensure()
    _echo_current_review_candidate(paths, _review_session(paths))


@review_app.command("next")
def review_next() -> None:
    """Move to the next proposed recipe."""
    paths = KbPaths(Path.cwd()).ensure()
    _echo_current_review_candidate(paths, next_candidate(paths, _review_session(paths)))


@review_app.command("prev")
def review_prev() -> None:
    """Move to the previous proposed recipe."""
    paths = KbPaths(Path.cwd()).ensure()
    _echo_current_review_candidate(paths, previous_candidate(paths, _review_session(paths)))


def _review_decide(decision: ReviewDecision, notes: str, label: str) -> None:
    paths = KbPaths(Path.cwd()).ensure()
    session = _review_session(paths)
    decide_current(paths, session, decision, notes)
    typer.echo(label)


@review_app.command("accept")
def review_accept(notes: str = "") -> None:
    """Accept the current proposed recipe."""
    _review_decide(ReviewDecision.ACCEPT, notes, "accepted")


@review_app.command("reject")
def review_reject(notes: str = "") -> None:
    """Reject the current proposed recipe."""
    _review_decide(ReviewDecision.REJECT, notes, "rejected")


@review_app.command("needs-more-evidence")
def review_needs_more_evidence(notes: str = "") -> None:
    """Mark the current proposed recipe as needing more evidence."""
    _review_decide(ReviewDecision.NEEDS_MORE_EVIDENCE, notes, "needs_more_evidence")


@app.command()
def publish(
    recipe: Annotated[Path, typer.Argument()],
) -> None:
    """Publish a proposed recipe into the accepted set."""
    paths = KbPaths(Path.cwd()).ensure()
    try:
        published = publish_recipe(recipe, paths)
    except FileNotFoundError:
        _exit_error(f"recipe file not found: {recipe}")
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(str(published))


@index_app.command("rebuild")
def index_rebuild() -> None:
    """Rebuild the deterministic recipe search index."""
    paths = KbPaths(Path.cwd()).ensure()
    try:
        index_path = rebuild_index(paths)
    except IndexBuildError as exc:
        _exit_error(str(exc))
    typer.echo(str(index_path))


@app.command(name="propose-build")
def propose_build(
    id: Annotated[str, typer.Option("--id", help="Build recipe ID (kebab-case)")],
    stack: Annotated[list[str], typer.Option(help="Stack tags")],
) -> None:
    """Create a skeleton build recipe candidate for manual editing."""
    from recipe_importer.models import EvidenceRef, TriggerSpec

    paths = KbPaths(Path.cwd()).ensure()
    target = paths.proposed_dir / f"{id}.md"
    if target.exists():
        _exit_error(f"already exists: {target}")

    ref = EvidenceRef(
        source_id="private-experience",
        url="https://example.com/placeholder",
        final_url="https://example.com/placeholder",
        source_type="private_experience",
        captured_at="PLACEHOLDER",
        section_anchor="manual",
        span_id="manual-1",
        short_excerpt="PLACEHOLDER: 替换为实际经验描述",
        quote_hash="sha256:placeholder",
    )
    build = BuildRecipe(
        id=id,
        status=RecipeStatus.PROPOSED,
        stack=stack,
        trigger=TriggerSpec(description="PLACEHOLDER: 描述触发条件"),
        correct_pattern=["PLACEHOLDER: 正确做法"],
        constraints=["PLACEHOLDER: 约束条件"],
        do_not=["PLACEHOLDER: 禁止事项"],
        validation=["PLACEHOLDER: 验证方式"],
        evidence_refs=[ref],
    )
    render_recipe_file(build, target)
    typer.echo(str(target))


@app.command(name="generate-build-recipes")
def generate_build_recipes_cmd() -> None:
    """Generate build recipe candidates from accepted debug recipes and guide snapshots."""
    paths = KbPaths(Path.cwd()).ensure()
    count = 0

    for path in sorted(paths.accepted_dir.glob("*.md")):
        recipe = parse_recipe_file(path)
        if not isinstance(recipe, Recipe):
            continue
        build = generate_build_from_debug(recipe)
        target = paths.proposed_dir / f"{build.id}.md"
        if target.exists():
            continue
        render_recipe_file(build, target)
        typer.echo(str(target))
        count += 1

    if paths.snapshots_dir.exists():
        for snapshot_dir in sorted(paths.snapshots_dir.iterdir()):
            if not snapshot_dir.is_dir():
                continue
            builds = deterministic_build_candidates(snapshot_dir)
            for build in builds:
                target = paths.proposed_dir / f"{build.id}.md"
                if target.exists():
                    continue
                render_recipe_file(build, target)
                typer.echo(str(target))
                count += 1

    if count == 0:
        typer.echo("no new build recipe candidates generated")


@app.command()
def search(
    query: Annotated[str, typer.Argument()],
    fresh_only: bool = False,
) -> None:
    """Search accepted and stale recipes."""
    paths = KbPaths(Path.cwd()).ensure()
    try:
        records = search_recipes(paths, query, fresh_only=fresh_only)
    except FileNotFoundError:
        _exit_error("recipe index not found; run `recipe-importer index rebuild`")
    except (KeyError, ValueError):
        _exit_error("recipe index is invalid; run `recipe-importer index rebuild`")
    for record in records:
        warning = " [stale]" if record["stale"] else ""
        typer.echo(f"{record['id']}{warning}")
        typer.echo(f"  summary: {record['summary']}")
        if record.get("kind") == "build-recipe":
            for item in record.get("constraints", []):
                typer.echo(f"  constraint: {item}")
            for item in record.get("correct_pattern", []):
                typer.echo(f"  pattern: {item}")
            for item in record.get("do_not", []):
                typer.echo(f"  do-not: {item}")
            for item in record.get("validation", []):
                typer.echo(f"  validate: {item}")
        else:
            for check_item in record.get("first_checks", []):
                typer.echo(f"  check: {check_item}")
            for item in record.get("do_not", []):
                typer.echo(f"  do-not: {item}")
            for validation_step in record.get("validation_ladder", []):
                typer.echo(f"  validate: {validation_step}")


@app.command(name="list")
def recipe_list(
    stack: Annotated[
        Optional[str],
        typer.Option("--stack", "-s", help="Filter by stack name"),
    ] = None,
) -> None:
    """List recipes grouped by stack."""
    paths = KbPaths(Path.cwd()).ensure()
    try:
        stacked = list_stacks(paths, stack_filter=stack)
    except FileNotFoundError:
        _exit_error("recipe index not found; run `recipe-importer index rebuild`")
    except ValueError:
        _exit_error("recipe index is invalid; run `recipe-importer index rebuild`")

    if not stacked:
        if stack:
            typer.echo(f"No recipes found for stack: {stack}")
        else:
            typer.echo("No recipes found. Run 'recipe-importer index rebuild' first.")
        return

    for stack_name in sorted(stacked.keys()):
        recipes = stacked[stack_name]
        accepted = sum(1 for r in recipes if r["status"] == "accepted")
        stale = sum(1 for r in recipes if r["stale"])

        typer.echo(f"\nStack: {stack_name} ({len(recipes)} recipes, {accepted} accepted, {stale} stale)")
        typer.echo("-" * 60)
        for recipe in recipes:
            status_indicator = "✓" if recipe["status"] == "accepted" and not recipe["stale"] else "⚠"
            typer.echo(f"  {status_indicator} {recipe['id']}")

    typer.echo()


@app.command("get")
def recipe_get(
    recipe_id: Annotated[str, typer.Argument()],
) -> None:
    """Print one recipe as canonical JSON."""
    paths = KbPaths(Path.cwd()).ensure()
    try:
        recipe = get_recipe(paths, recipe_id)
    except FileNotFoundError:
        _exit_error("recipe index not found; run `recipe-importer index rebuild`")
    except ValueError:
        _exit_error("recipe index is invalid; run `recipe-importer index rebuild`")
    except KeyError:
        _exit_error(f"recipe not found: {recipe_id}")
    typer.echo(recipe.model_dump_json(indent=2))
