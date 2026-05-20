from pathlib import Path

from recipe_importer.models import RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import check_render_equivalence, parse_recipe_file, render_recipe_file


def _is_relative_to(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
    except ValueError:
        return False
    return True


def publish_recipe(proposed_path: Path, paths: KbPaths) -> Path:
    if not _is_relative_to(proposed_path, paths.proposed_dir):
        raise ValueError(f"{proposed_path} must be inside {paths.proposed_dir}")

    if not check_render_equivalence(proposed_path):
        raise ValueError(f"{proposed_path} is not render-equivalent")

    recipe = parse_recipe_file(proposed_path)
    recipe.status = RecipeStatus.ACCEPTED
    recipe.maintenance.state = RecipeStatus.ACCEPTED
    target = paths.accepted_dir / proposed_path.name
    render_recipe_file(recipe, target)
    return target
