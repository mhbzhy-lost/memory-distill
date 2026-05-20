from pathlib import Path
from typing import Annotated, NoReturn

import typer

from recipe_importer import __version__
from recipe_importer.extract import extract_snapshot
from recipe_importer.fetch import fetch_sources

from recipe_importer.index import IndexBuildError, rebuild_index
from recipe_importer.llm import deterministic_candidates
from recipe_importer.manifest import check_manifest, refresh_manifest
from recipe_importer.models import ReviewDecision
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.publish import publish_recipe
from recipe_importer.render import check_render_equivalence, render_recipe_file
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

app = typer.Typer(no_args_is_help=True)
schema_app = typer.Typer(no_args_is_help=True)
manifest_app = typer.Typer(no_args_is_help=True)
review_app = typer.Typer(no_args_is_help=False)
index_app = typer.Typer(no_args_is_help=True)
app.add_typer(schema_app, name="schema")
app.add_typer(manifest_app, name="manifest")
app.add_typer(review_app, name="review")
app.add_typer(index_app, name="index")


@app.callback()
def main() -> None:
    pass


def _exit_error(message: str) -> NoReturn:
    typer.echo(message, err=True)
    raise typer.Exit(code=1)


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
def extract(
    snapshot_dir: Annotated[Path, typer.Argument()],
) -> None:
    """Extract readable sections from one local snapshot directory."""
    result = extract_snapshot(snapshot_dir)
    typer.echo(f"{result.source_id}: {result.section_count} sections")


@app.command(name="import-source")
def import_source(
    snapshot_dir: Annotated[Path, typer.Argument()],
    stack: Annotated[list[str], typer.Option()] = ["react", "nextjs"],
) -> None:
    """Create proposed recipes from one extracted snapshot."""
    paths = KbPaths(Path.cwd()).ensure()
    candidates = deterministic_candidates(snapshot_dir)
    for candidate in candidates.candidates:
        recipe = normalize_recipe(candidate, snapshot_dir, stack=stack)
        target = paths.proposed_dir / f"{recipe.id}.md"
        render_recipe_file(recipe, target)
        typer.echo(str(target))


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
    for record in records:
        warning = " [stale]" if record["stale"] else ""
        typer.echo(f"{record['id']}{warning}")
        typer.echo(f"  summary: {record['summary']}")
        for check_item in record["first_checks"]:
            typer.echo(f"  check: {check_item}")
        for item in record["do_not"]:
            typer.echo(f"  do-not: {item}")
        for validation_step in record["validation_ladder"]:
            typer.echo(f"  validate: {validation_step}")


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
    except KeyError:
        _exit_error(f"recipe not found: {recipe_id}")
    typer.echo(recipe.model_dump_json(indent=2))
