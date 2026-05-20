from pathlib import Path
from typing import Annotated

import typer

from recipe_importer import __version__
from recipe_importer.extract import extract_snapshot
from recipe_importer.fetch import fetch_sources
from recipe_importer.llm import deterministic_candidates
from recipe_importer.manifest import check_manifest, refresh_manifest
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.render import check_render_equivalence, render_recipe_file
from recipe_importer.schema import export_schemas

app = typer.Typer(no_args_is_help=True)
schema_app = typer.Typer(no_args_is_help=True)
manifest_app = typer.Typer(no_args_is_help=True)
app.add_typer(schema_app, name="schema")
app.add_typer(manifest_app, name="manifest")


@app.callback()
def main() -> None:
    pass


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
