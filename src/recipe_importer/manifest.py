import hashlib
from pathlib import Path

from pydantic import BaseModel, Field

from recipe_importer.storage import read_yaml, write_yaml


class ManifestItem(BaseModel):
    rev: int
    path: str | None = None
    files: list[str] | None = None
    hash: str


class Manifest(BaseModel):
    prompts: dict[str, ManifestItem] = Field(default_factory=dict)
    schemas: dict[str, ManifestItem] = Field(default_factory=dict)
    extractors: dict[str, ManifestItem] = Field(default_factory=dict)


def _hash_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest_path(root: Path) -> Path:
    return root / "recipe-kb" / "manifest.yml"


def _load_existing(root: Path) -> Manifest:
    path = _manifest_path(root)
    if not path.exists():
        return Manifest()
    return Manifest.model_validate(read_yaml(path))


def refresh_manifest(root: Path) -> Manifest:
    existing = _load_existing(root)
    prompt_path = root / "prompts" / "debug_recipe_evidence.md"
    prompt_hash = _hash_file(prompt_path)
    previous = existing.prompts.get("debug_recipe_evidence")
    rev = (
        previous.rev
        if previous and previous.hash == prompt_hash
        else (previous.rev + 1 if previous else 1)
    )
    manifest = Manifest(
        prompts={
            "debug_recipe_evidence": ManifestItem(
                rev=rev,
                path="prompts/debug_recipe_evidence.md",
                hash=prompt_hash,
            )
        },
        schemas=existing.schemas,
        extractors=existing.extractors,
    )
    write_yaml(_manifest_path(root), manifest.model_dump(mode="json"))
    return manifest


def check_manifest(root: Path) -> bool:
    manifest = _load_existing(root)
    item = manifest.prompts.get("debug_recipe_evidence")
    if item is None:
        return False
    file_path = root / item.path if item.path else None
    if file_path is None or not file_path.exists():
        return False
    return item.hash == _hash_file(file_path)
