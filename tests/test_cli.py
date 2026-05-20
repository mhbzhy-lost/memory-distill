from typer.testing import CliRunner

from recipe_importer.cli import app


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "recipe-importer 0.1.0" in result.stdout
