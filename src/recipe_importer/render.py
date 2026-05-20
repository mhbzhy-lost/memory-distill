from pathlib import Path

import yaml

from recipe_importer.models import Recipe


GENERATED_MARKER = "<!-- generated-from-frontmatter: do not edit semantic sections -->"


def recipe_to_frontmatter(recipe: Recipe) -> str:
    data = recipe.model_dump(mode="json")
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def render_body(recipe: Recipe) -> str:
    def bullets(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    return "\n\n".join(
        [
            GENERATED_MARKER,
            f"# {recipe.id}",
            "## Failure Class\n" + recipe.failure_class,
            "## Symptoms\n" + bullets(recipe.symptoms),
            "## Fingerprints\n" + bullets(recipe.fingerprints),
            "## First Checks\n" + bullets(recipe.first_checks),
            "## Do Not Patch Yet\n" + bullets(recipe.do_not),
            "## Evidence Needed\n" + bullets(recipe.evidence_needed),
            "## Minimal Fix Scope\n" + bullets(recipe.minimal_fix_scope),
            "## Validation Ladder\n" + bullets(recipe.validation_ladder),
            "## Regression Guard\n" + bullets(recipe.regression_guard),
            "## Reviewer Notes",
        ]
    ) + "\n"


def render_recipe_text(recipe: Recipe) -> str:
    return "---\n" + recipe_to_frontmatter(recipe) + "---\n\n" + render_body(recipe)


def render_recipe_file(recipe: Recipe, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_recipe_text(recipe), encoding="utf-8")


def parse_recipe_file(path: Path) -> Recipe:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("recipe file must start with YAML frontmatter")
    _, frontmatter, _body = text.split("---", 2)
    return Recipe.model_validate(yaml.safe_load(frontmatter))


def check_render_equivalence(path: Path) -> bool:
    recipe = parse_recipe_file(path)
    expected = render_recipe_text(recipe)
    return path.read_text(encoding="utf-8") == expected
