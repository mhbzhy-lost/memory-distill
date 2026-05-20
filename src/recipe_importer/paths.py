from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KbPaths:
    root: Path

    @property
    def recipe_kb_dir(self) -> Path:
        return self.root / "recipe-kb"

    @property
    def sources_dir(self) -> Path:
        return self.recipe_kb_dir / "sources"

    @property
    def snapshots_dir(self) -> Path:
        return self.recipe_kb_dir / "snapshots"

    @property
    def proposed_dir(self) -> Path:
        return self.recipe_kb_dir / "proposed"

    @property
    def accepted_dir(self) -> Path:
        return self.recipe_kb_dir / "accepted"

    @property
    def rejected_dir(self) -> Path:
        return self.recipe_kb_dir / "rejected"

    @property
    def stale_dir(self) -> Path:
        return self.recipe_kb_dir / "stale"

    @property
    def feedback_dir(self) -> Path:
        return self.recipe_kb_dir / "feedback"

    @property
    def review_dir(self) -> Path:
        return self.recipe_kb_dir / "review"

    @property
    def index_path(self) -> Path:
        return self.recipe_kb_dir / "index.json"

    def directories(self) -> list[Path]:
        return [
            self.sources_dir,
            self.snapshots_dir,
            self.proposed_dir,
            self.accepted_dir,
            self.rejected_dir,
            self.stale_dir,
            self.feedback_dir,
            self.review_dir,
        ]

    def ensure(self) -> "KbPaths":
        for directory in self.directories():
            directory.mkdir(parents=True, exist_ok=True)
        return self
