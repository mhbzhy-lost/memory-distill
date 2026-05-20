from recipe_importer.manifest import check_manifest, refresh_manifest


def test_refresh_manifest_creates_rev_one(kb_root):
    prompt = kb_root / "prompts" / "debug_recipe_evidence.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("Extract evidence candidates.\n", encoding="utf-8")

    manifest = refresh_manifest(kb_root)

    assert manifest.prompts["debug_recipe_evidence"].rev == 1
    assert manifest.prompts["debug_recipe_evidence"].hash.startswith("sha256:")


def test_refresh_manifest_increments_rev_when_hash_changes(kb_root):
    prompt = kb_root / "prompts" / "debug_recipe_evidence.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("Extract evidence candidates.\n", encoding="utf-8")
    first = refresh_manifest(kb_root)

    prompt.write_text("Extract source-grounded evidence candidates.\n", encoding="utf-8")
    second = refresh_manifest(kb_root)

    assert (
        second.prompts["debug_recipe_evidence"].rev
        == first.prompts["debug_recipe_evidence"].rev + 1
    )


def test_check_manifest_detects_current_hash(kb_root):
    prompt = kb_root / "prompts" / "debug_recipe_evidence.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("Extract evidence candidates.\n", encoding="utf-8")
    refresh_manifest(kb_root)

    assert check_manifest(kb_root)


def test_refresh_manifest_preserves_same_rev_when_hash_unchanged(kb_root):
    prompt = kb_root / "prompts" / "debug_recipe_evidence.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("Extract evidence candidates.\n", encoding="utf-8")
    first = refresh_manifest(kb_root)

    second = refresh_manifest(kb_root)

    assert (
        second.prompts["debug_recipe_evidence"].rev
        == first.prompts["debug_recipe_evidence"].rev
    )
