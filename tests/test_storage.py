from recipe_importer.paths import KbPaths
from recipe_importer.storage import read_json, read_yaml, write_json, write_text, write_yaml


def test_kb_paths_create_expected_directories(kb_root):
    paths = KbPaths(kb_root)
    result = paths.ensure()

    assert result is paths
    assert paths.sources_dir.exists()
    assert paths.snapshots_dir.exists()
    assert paths.proposed_dir.exists()
    assert paths.accepted_dir.exists()
    assert paths.rejected_dir.exists()
    assert paths.stale_dir.exists()
    assert paths.feedback_dir.exists()
    assert paths.review_dir.exists()


def test_yaml_json_text_round_trip(kb_root):
    paths = KbPaths(kb_root).ensure()

    yaml_path = paths.sources_dir / "source-list.yml"
    json_path = paths.snapshots_dir / "metadata.json"
    text_path = paths.proposed_dir / "recipe.md"

    write_yaml(yaml_path, {"sources": [{"source_id": "react-error-418"}]})
    write_json(json_path, {"source_id": "react-error-418"})
    write_text(text_path, "# Recipe\n")

    assert read_yaml(yaml_path)["sources"][0]["source_id"] == "react-error-418"
    assert read_json(json_path)["source_id"] == "react-error-418"
    assert text_path.read_text(encoding="utf-8") == "# Recipe\n"
