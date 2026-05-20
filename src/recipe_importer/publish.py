from pathlib import Path

from recipe_importer.models import RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import check_render_equivalence, parse_recipe_file, render_recipe_file


def publish_recipe(proposed_path: Path, paths: KbPaths) -> Path:
    if not check_render_equivalence(proposed_path):
        raise ValueError(f"{proposed_path} is not render-equivalent")

    recipe = parse_recipe_file(proposed_path)
    recipe.status = RecipeStatus.ACCEPTED
    recipe.maintenance.state = RecipeStatus.ACCEPTED
    target = paths.accepted_dir / proposed_path.name
    render_recipe_file(recipe, target)
    return target
