import typer

from recipe_importer import __version__

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    pass


@app.command(name="version")
def version() -> None:
    """Print the recipe importer version."""
    typer.echo(f"recipe-importer {__version__}")
