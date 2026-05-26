from pathlib import Path

import yaml

from recipe_importer.models import AnyRecipe, BuildRecipe, Recipe


GENERATED_MARKER = "<!-- generated-from-frontmatter: do not edit semantic sections -->"


def recipe_to_frontmatter(recipe: AnyRecipe) -> str:
    data = recipe.model_dump(mode="json")
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def _render_debug_body(recipe: Recipe) -> str:
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


def _render_build_body(recipe: BuildRecipe) -> str:
    def bullets(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    sections = [
        GENERATED_MARKER,
        f"# {recipe.id}",
    ]

    if recipe.trigger.description:
        trigger_lines = [f"**{recipe.trigger.description}**"]
        if recipe.trigger.file_pattern:
            trigger_lines.append(f"- file pattern: `{recipe.trigger.file_pattern}`")
        for signal in recipe.trigger.code_signals:
            trigger_lines.append(f"- code signal: `{signal}`")
        sections.append("## Trigger\n" + "\n".join(trigger_lines))

    sections.append("## Correct Pattern\n" + bullets(recipe.correct_pattern))

    if recipe.decision_context:
        dc_lines = []
        for opt in recipe.decision_context:
            dc_lines.append(f"- **{opt.condition}** → {opt.recommendation}")
        sections.append("## Decision Context\n" + "\n".join(dc_lines))

    sections.append("## Constraints\n" + bullets(recipe.constraints))
    sections.append("## Do Not\n" + bullets(recipe.do_not))

    if recipe.defaults:
        sections.append("## Defaults\n" + bullets(recipe.defaults))

    sections.append("## Validation\n" + bullets(recipe.validation))

    if recipe.related_debug_recipes:
        sections.append("## Related Debug Recipes\n" + bullets(recipe.related_debug_recipes))

    sections.append("## Reviewer Notes")

    return "\n\n".join(sections) + "\n"


def render_body(recipe: AnyRecipe) -> str:
    if isinstance(recipe, BuildRecipe):
        return _render_build_body(recipe)
    return _render_debug_body(recipe)


def render_recipe_text(recipe: AnyRecipe) -> str:
    return "---\n" + recipe_to_frontmatter(recipe) + "---\n\n" + render_body(recipe)


def render_recipe_file(recipe: AnyRecipe, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_recipe_text(recipe), encoding="utf-8")


def parse_recipe_file(path: Path) -> AnyRecipe:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("recipe file must start with YAML frontmatter")
    close = text.find("\n---\n", 3)
    if close == -1:
        close = text.rfind("\n---")
    if close == -1:
        raise ValueError("recipe file missing closing frontmatter delimiter")
    frontmatter = text[4 : close + 1]
    data = yaml.safe_load(frontmatter)
    if data.get("kind") == "build-recipe":
        return BuildRecipe.model_validate(data)
    return Recipe.model_validate(data)


def check_render_equivalence(path: Path) -> bool:
    recipe = parse_recipe_file(path)
    expected = render_recipe_text(recipe)
    return path.read_text(encoding="utf-8") == expected
