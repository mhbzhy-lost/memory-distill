from recipe_importer.models import AnyRecipe
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file
from recipe_importer.storage import read_json


def _score(record: dict, query: str) -> int:
    normalized_query = query.lower()
    fields = (
        record["stack"]
        + record.get("source_ids", [])
        + record.get("source_urls", [])
        + record.get("fingerprints", [])
        + record.get("symptoms", [])
        + record.get("constraints", [])
        + record.get("correct_pattern", [])
        + record.get("do_not", [])
        + [record.get("failure_class", ""), record["status"]]
        + [record.get("trigger_description", "")]
    )
    return sum(1 for value in fields if value and (normalized_query in value.lower() or value.lower() in normalized_query))


def search_recipes(paths: KbPaths, query: str, *, top: int = 3, fresh_only: bool = False) -> list[dict]:
    data = read_json(paths.index_path)
    records = [record for record in data["recipes"] if not (fresh_only and record["stale"])]
    scored = [(_score(record, query), record) for record in records]
    ranked = sorted(scored, key=lambda item: (-item[0], item[1]["id"]))
    return [record for score, record in ranked if score > 0][:top]


def get_recipe(paths: KbPaths, recipe_id: str) -> AnyRecipe:
    data = read_json(paths.index_path)
    for record in data["recipes"]:
        if record["id"] == recipe_id:
            return parse_recipe_file(paths.root / record["path"])
    raise KeyError(recipe_id)
