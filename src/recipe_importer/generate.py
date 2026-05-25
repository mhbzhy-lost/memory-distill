from recipe_importer.models import BuildRecipe, Recipe, RecipeStatus, TriggerSpec


def generate_build_from_debug(recipe: Recipe) -> BuildRecipe:
    trigger_desc = f"代码可能触发 {recipe.failure_class} 类故障（{recipe.symptoms[0][:80]}）"

    return BuildRecipe(
        id=f"build-{recipe.id}",
        status=RecipeStatus.PROPOSED,
        stack=list(recipe.stack),
        trigger=TriggerSpec(description=trigger_desc),
        correct_pattern=[],
        constraints=list(recipe.do_not),
        do_not=list(recipe.do_not),
        validation=list(recipe.validation_ladder),
        related_debug_recipes=[recipe.id],
        evidence_refs=list(recipe.evidence_refs),
    )
