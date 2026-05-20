from recipe_importer.models import Recipe


def duplicate_hints(candidate: Recipe, existing: list[Recipe]) -> list[dict]:
    hints: list[dict] = []
    candidate_fingerprints = set(candidate.fingerprints)
    candidate_stack = set(candidate.stack)
    for recipe in existing:
        overlap = candidate_fingerprints.intersection(recipe.fingerprints)
        stack_overlap = candidate_stack.intersection(recipe.stack)
        if candidate.id == recipe.id or (overlap and stack_overlap):
            hints.append(
                {
                    "recipe_id": recipe.id,
                    "fingerprint_overlap": sorted(overlap),
                    "stack_overlap": sorted(stack_overlap),
                }
            )
    return hints
