from pathlib import Path
from typing import Annotated

import typer

from recipe_importer import __version__
from recipe_importer.fetch import fetch_sources
from recipe_importer.manifest import check_manifest, refresh_manifest
from recipe_importer.paths import KbPaths
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
