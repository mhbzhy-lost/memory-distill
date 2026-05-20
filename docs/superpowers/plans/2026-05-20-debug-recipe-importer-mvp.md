# Debug Recipe Importer MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first end-to-end CLI-first debug recipe importer vertical slice for React hydration mismatch.

**Architecture:** The importer is a Python CLI backed by file-based storage. Pydantic models define canonical data, generated Markdown is a review view, and derived artifacts such as `index.json` are rebuilt from accepted recipes. The first slice uses deterministic extraction from local/static source data; LLM extraction is represented by a narrow `evidence_candidates` interface but does not call a real provider.

**Tech Stack:** Python 3.12, uv, Typer, Pydantic v2, PyYAML, httpx, BeautifulSoup, lxml/html5lib, pytest.

---

## Confirmed Scope

This plan implements the MVP described in [debug-recipe-importer-mvp.md](/Users/mhbzhy/memory-distill/docs/design/debug-recipe-importer-mvp.md).

The first completed vertical slice must support:

```text
source-list.yml
  -> fetch source
  -> save snapshot metadata + readable sections + evidence refs
  -> extract narrow evidence candidates
  -> normalize to proposed recipe
  -> render Markdown from canonical YAML
  -> review via inbox-first CLI session
  -> publish accepted recipe
  -> rebuild deterministic index
  -> search/get accepted recipe
  -> refresh and mark stale when evidence changes
```

MVP intentionally does not implement:

- Embeddings.
- SQLite.
- Browser-rendered extraction.
- A real LLM provider call.
- Automatic dedupe merge.
- Full feedback command loop.

## External Documentation Checked

Use these as implementation references:

- uv project/package commands: https://docs.astral.sh/uv/reference/cli/
- Typer CLI testing with `CliRunner`: https://typer.tiangolo.com/tutorial/testing/
- Pydantic JSON Schema export: https://docs.pydantic.dev/latest/concepts/json_schema/
- Beautiful Soup parsing and traversal: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## File Structure

Create and maintain these files:

```text
bin/
  recipe-importer
pyproject.toml
README.md
src/
  recipe_importer/
    __init__.py
    cli.py
    dedupe.py
    extract.py
    fetch.py
    index.py
    llm.py
    manifest.py
    models.py
    normalize.py
    paths.py
    publish.py
    refresh.py
    render.py
    review.py
    schema.py
    search.py
    sources.py
    storage.py
recipe-kb/
  sources/source-list.yml
  feedback/.gitkeep
prompts/
  debug_recipe_evidence.md
schemas/
  debug-recipe.schema.json
  evidence-candidates.schema.json
  review.schema.json
  source.schema.json
tests/
  conftest.py
  fixtures/react_error_418.html
  test_cli.py
  test_models_schema.py
  test_storage.py
  test_sources_fetch.py
  test_extract.py
  test_normalize_render.py
  test_manifest.py
  test_review.py
  test_publish_index_search.py
  test_refresh.py
  test_vertical_slice.py
```

### File Responsibilities

- `cli.py`: Typer command tree and CLI I/O only.
- `models.py`: Pydantic domain models and enums.
- `paths.py`: repository-relative KB paths.
- `storage.py`: YAML/JSON/Markdown file I/O helpers.
- `sources.py`: parse and validate `source-list.yml`.
- `fetch.py`: explicit network fetch and snapshot metadata writing.
- `extract.py`: HTML-to-section extraction and evidence ref generation.
- `llm.py`: narrow evidence candidate interfaces and deterministic MVP extractor.
- `normalize.py`: convert evidence candidates to canonical recipe models.
- `render.py`: canonical YAML to generated Markdown body, plus equivalence check.
- `schema.py`: export JSON Schemas from Pydantic models.
- `manifest.py`: hash/rev manifest check and refresh.
- `review.py`: inbox-first review session state and decisions.
- `dedupe.py`: deterministic duplicate candidate hints.
- `publish.py`: state transition from proposed to accepted/rejected/stale/deprecated.
- `index.py`: rebuild derived search index from accepted/stale recipes.
- `search.py`: deterministic search and recipe get.
- `refresh.py`: compare stored evidence hashes with current explicit snapshot data.

## DAG And Parallelization

```text
Task 1: scaffold
  -> Task 2: models/schema
  -> Task 3: storage/paths
      -> Task 4: sources/fetch
      -> Task 5: extract/evidence
          -> Task 6: normalize/render/check
              -> Task 8: review
              -> Task 9: publish/index/search
                  -> Task 10: refresh
                  -> Task 11: vertical slice
      -> Task 7: manifest
```

Parallel-ready sets after dependencies are satisfied:

```text
After Task 3:
  - Task 4 and Task 7 can run independently.

After Task 6:
  - Task 8 and Task 9 can be prepared independently if write scopes are split.

After Task 9:
  - Task 10 and Task 11 can be verified independently, then integrated.
```

Because this plan will be implemented in the main session unless the user explicitly requests subagents, do not spawn subagents from this plan by default.

## Verification Summary

Default verification:

```bash
uv run pytest -q
uv run recipe-importer check recipe-kb/proposed/react-hydration-mismatch.md
uv run recipe-importer index rebuild
uv run recipe-importer search "Hydration failed"
git diff --check
```

Network verification is explicit:

```bash
uv run recipe-importer fetch recipe-kb/sources/source-list.yml
```

Do not make default tests depend on live React documentation. Use `tests/fixtures/react_error_418.html` for stable tests.

## Task 1: Project Scaffold And CLI Smoke

**Files:**
- Create: `pyproject.toml`
- Create: `bin/recipe-importer`
- Create: `src/recipe_importer/__init__.py`
- Create: `src/recipe_importer/cli.py`
- Create: `tests/test_cli.py`
- Create: `README.md`

- [ ] **Step 1: Write the failing CLI smoke test**

Create `tests/test_cli.py`:

```python
from typer.testing import CliRunner

from recipe_importer.cli import app


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "recipe-importer 0.1.0" in result.stdout
```

- [ ] **Step 2: Add project metadata and dependencies**

Create `pyproject.toml`:

```toml
[project]
name = "recipe-importer"
version = "0.1.0"
description = "CLI-first importer for reviewed debug recipes"
requires-python = ">=3.12"
dependencies = [
  "beautifulsoup4>=4.12",
  "html5lib>=1.1",
  "httpx>=0.27",
  "lxml>=5.0",
  "pydantic>=2.8",
  "pyyaml>=6.0",
  "typer>=0.12",
]

[project.scripts]
recipe-importer = "recipe_importer.cli:app"

[dependency-groups]
dev = [
  "pytest>=8.2",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

- [ ] **Step 3: Add the Typer app**

Create `src/recipe_importer/__init__.py`:

```python
__version__ = "0.1.0"
```

Create `src/recipe_importer/cli.py`:

```python
import typer

from recipe_importer import __version__

app = typer.Typer(no_args_is_help=True)


@app.command()
def version() -> None:
    """Print the recipe importer version."""
    typer.echo(f"recipe-importer {__version__}")
```

Create `bin/recipe-importer`:

```python
#!/usr/bin/env python3
from recipe_importer.cli import app


if __name__ == "__main__":
    app()
```

Create `README.md`:

```markdown
# Recipe Importer

CLI-first importer for reviewed, source-grounded debug recipes.

The MVP imports official troubleshooting/error documentation into a local
file-based recipe knowledge base. Accepted recipes are reviewed before agent
consumption.
```

- [ ] **Step 4: Run the CLI smoke test**

Run:

```bash
uv run pytest tests/test_cli.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml bin/recipe-importer src/recipe_importer/__init__.py src/recipe_importer/cli.py tests/test_cli.py README.md
git commit -m "feat(cli): 搭建 importer CLI 骨架"
```

## Task 2: Domain Models And JSON Schema Export

**Files:**
- Create: `src/recipe_importer/models.py`
- Create: `src/recipe_importer/schema.py`
- Create: `tests/test_models_schema.py`
- Create/Update generated by command: `schemas/debug-recipe.schema.json`
- Create/Update generated by command: `schemas/source.schema.json`
- Create/Update generated by command: `schemas/review.schema.json`
- Create/Update generated by command: `schemas/evidence-candidates.schema.json`

- [ ] **Step 1: Write failing model/schema tests**

Create `tests/test_models_schema.py`:

```python
import json

import pytest
from pydantic import ValidationError

from recipe_importer.models import (
    EvidenceCandidate,
    EvidenceRef,
    Recipe,
    RecipeStatus,
    Source,
)
from recipe_importer.schema import export_schemas


def test_recipe_requires_evidence_for_core_fields():
    ref = EvidenceRef(
        source_id="react-error-418",
        url="https://react.dev/errors/418",
        final_url="https://react.dev/errors/418",
        source_type="official_error_doc",
        captured_at="2026-05-20T00:00:00Z",
        section_anchor="root",
        span_id="root-1",
        short_excerpt="Hydration failed because the server rendered HTML did not match.",
        quote_hash="sha256:abc",
    )

    recipe = Recipe(
        id="react-hydration-mismatch",
        status=RecipeStatus.PROPOSED,
        stack=["react", "nextjs"],
        failure_class="render/hydration",
        symptoms=["Hydration failed"],
        fingerprints=["server rendered HTML did not match the client"],
        first_checks=["Check browser-only branches in render output"],
        do_not=["Do not disable SSR as the first fix"],
        evidence_needed=["Component output must be compared server vs client"],
        minimal_fix_scope=["The component producing mismatched markup"],
        validation_ladder=["Reproduce the page and inspect console warning"],
        regression_guard=["Add a smoke test for the affected page"],
        evidence_refs=[ref],
    )

    assert recipe.id == "react-hydration-mismatch"
    assert recipe.status is RecipeStatus.PROPOSED


def test_recipe_rejects_missing_evidence_refs():
    with pytest.raises(ValidationError):
        Recipe(
            id="react-hydration-mismatch",
            status=RecipeStatus.PROPOSED,
            stack=["react"],
            failure_class="render/hydration",
            symptoms=["Hydration failed"],
            fingerprints=["server rendered HTML did not match the client"],
            first_checks=["Check Date.now usage"],
            do_not=["Do not rewrite the app"],
            evidence_needed=["Source evidence is required"],
            minimal_fix_scope=["Affected component"],
            validation_ladder=["Run related smoke test"],
            regression_guard=["Add regression guard"],
            evidence_refs=[],
        )


def test_source_model_has_stable_id():
    source = Source(
        source_id="react-error-418",
        url="https://react.dev/errors/418",
        source_type="official_error_doc",
        stacks=["react", "nextjs"],
        expected_failure_hints=["hydration mismatch"],
        refresh_policy="monthly",
    )

    assert source.source_id == "react-error-418"


def test_evidence_candidate_schema_is_narrow():
    candidate = EvidenceCandidate(
        failure_label="hydration mismatch",
        symptom_quotes=["Hydration failed"],
        cause_quotes=["Date.now() in render"],
        avoidance_quotes=["Do not disable SSR"],
        validation_quotes=["Check browser console"],
        section_refs=["react-error-418#root-1"],
        confidence="medium",
    )

    assert candidate.confidence == "medium"


def test_export_schemas(tmp_path):
    export_schemas(tmp_path)

    exported = sorted(path.name for path in tmp_path.iterdir())
    assert exported == [
        "debug-recipe.schema.json",
        "evidence-candidates.schema.json",
        "review.schema.json",
        "source.schema.json",
    ]

    recipe_schema = json.loads((tmp_path / "debug-recipe.schema.json").read_text())
    assert recipe_schema["title"] == "Recipe"
```

- [ ] **Step 2: Run the model tests to verify they fail**

Run:

```bash
uv run pytest tests/test_models_schema.py -q
```

Expected: fail with `ModuleNotFoundError` or missing model imports.

- [ ] **Step 3: Implement domain models**

Create `src/recipe_importer/models.py`:

```python
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator


class RecipeStatus(StrEnum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    STALE = "stale"
    DEPRECATED = "deprecated"


class ReviewDecision(StrEnum):
    ACCEPT = "accept"
    REJECT = "reject"
    NARROW_SCOPE = "narrow_scope"
    MERGE_EXISTING = "merge_existing"
    NEEDS_MORE_EVIDENCE = "needs_more_evidence"
    MARK_STALE = "mark_stale"
    DEPRECATE = "deprecate"
    KEEP_SEPARATE = "keep_separate"
    REJECT_DUPLICATE = "reject_duplicate"


class EvidenceRef(BaseModel):
    source_id: str
    url: HttpUrl
    final_url: HttpUrl
    source_type: str
    captured_at: str
    section_anchor: str
    span_id: str
    short_excerpt: str = Field(min_length=1, max_length=600)
    quote_hash: str


class Source(BaseModel):
    source_id: str
    url: HttpUrl
    source_type: str
    stacks: list[str]
    expected_failure_hints: list[str] = Field(default_factory=list)
    refresh_policy: str = "manual"

    @field_validator("source_id")
    @classmethod
    def source_id_must_be_slug(cls, value: str) -> str:
        if not value or any(ch.isspace() for ch in value):
            raise ValueError("source_id must be a non-empty slug")
        return value


class SourceList(BaseModel):
    sources: list[Source]


class EvidenceCandidate(BaseModel):
    failure_label: str
    symptom_quotes: list[str] = Field(default_factory=list)
    cause_quotes: list[str] = Field(default_factory=list)
    avoidance_quotes: list[str] = Field(default_factory=list)
    validation_quotes: list[str] = Field(default_factory=list)
    section_refs: list[str] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"] = "low"


class EvidenceCandidates(BaseModel):
    candidates: list[EvidenceCandidate]


class ReviewRecord(BaseModel):
    candidate_id: str
    decision: ReviewDecision
    reviewed_at: str
    reviewer: str = "human"
    notes: str = ""


class Maintenance(BaseModel):
    state: RecipeStatus = RecipeStatus.PROPOSED
    stale_reason: list[str] = Field(default_factory=list)
    stale_detected_at: str | None = None


class Recipe(BaseModel):
    id: str
    kind: Literal["debug-recipe"] = "debug-recipe"
    status: RecipeStatus
    stack: list[str]
    failure_class: str
    symptoms: list[str]
    fingerprints: list[str]
    first_checks: list[str]
    do_not: list[str]
    evidence_needed: list[str]
    minimal_fix_scope: list[str]
    validation_ladder: list[str]
    regression_guard: list[str]
    evidence_refs: list[EvidenceRef]
    review: list[ReviewRecord] = Field(default_factory=list)
    maintenance: Maintenance = Field(default_factory=Maintenance)

    @field_validator("evidence_refs")
    @classmethod
    def must_have_evidence_refs(cls, value: list[EvidenceRef]) -> list[EvidenceRef]:
        if not value:
            raise ValueError("recipe core fields require at least one evidence_ref")
        return value
```

- [ ] **Step 4: Implement schema export**

Create `src/recipe_importer/schema.py`:

```python
import json
from pathlib import Path

from recipe_importer.models import EvidenceCandidates, Recipe, ReviewRecord, SourceList


SCHEMA_TARGETS = {
    "debug-recipe.schema.json": Recipe,
    "source.schema.json": SourceList,
    "review.schema.json": ReviewRecord,
    "evidence-candidates.schema.json": EvidenceCandidates,
}


def export_schemas(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for filename, model in SCHEMA_TARGETS.items():
        target = output_dir / filename
        target.write_text(
            json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(target)
    return written
```

- [ ] **Step 5: Add schema CLI command**

Modify `src/recipe_importer/cli.py`:

```python
from pathlib import Path

import typer

from recipe_importer import __version__
from recipe_importer.schema import export_schemas

app = typer.Typer(no_args_is_help=True)
schema_app = typer.Typer(no_args_is_help=True)
app.add_typer(schema_app, name="schema")


@app.command()
def version() -> None:
    """Print the recipe importer version."""
    typer.echo(f"recipe-importer {__version__}")


@schema_app.command("export")
def schema_export(output_dir: Path = Path("schemas")) -> None:
    """Export JSON Schemas for external adapters and review tooling."""
    for path in export_schemas(output_dir):
        typer.echo(str(path))
```

- [ ] **Step 6: Run tests and export schemas**

Run:

```bash
uv run pytest tests/test_models_schema.py -q
uv run recipe-importer schema export schemas
```

Expected:

```text
5 passed
schemas/debug-recipe.schema.json
schemas/source.schema.json
schemas/review.schema.json
schemas/evidence-candidates.schema.json
```

- [ ] **Step 7: Commit**

```bash
git add src/recipe_importer/models.py src/recipe_importer/schema.py src/recipe_importer/cli.py tests/test_models_schema.py schemas/
git commit -m "feat(schema): 定义 recipe 核心模型"
```

## Task 3: Repository Paths And File Storage

**Files:**
- Create: `src/recipe_importer/paths.py`
- Create: `src/recipe_importer/storage.py`
- Create: `tests/conftest.py`
- Create: `tests/test_storage.py`

- [ ] **Step 1: Write failing storage tests**

Create `tests/conftest.py`:

```python
from pathlib import Path

import pytest


@pytest.fixture
def kb_root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    return root
```

Create `tests/test_storage.py`:

```python
from recipe_importer.paths import KbPaths
from recipe_importer.storage import read_json, read_yaml, write_json, write_text, write_yaml


def test_kb_paths_create_expected_directories(kb_root):
    paths = KbPaths(kb_root)
    created = paths.ensure()

    assert paths.sources_dir in created
    assert paths.proposed_dir.exists()
    assert paths.accepted_dir.exists()
    assert paths.feedback_dir.exists()


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
```

- [ ] **Step 2: Run storage tests to verify they fail**

Run:

```bash
uv run pytest tests/test_storage.py -q
```

Expected: fail with missing `recipe_importer.paths`.

- [ ] **Step 3: Implement path layout**

Create `src/recipe_importer/paths.py`:

```python
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

    def ensure(self) -> "KbPaths":
        for directory in self.directories():
            directory.mkdir(parents=True, exist_ok=True)
        return self

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
```

- [ ] **Step 4: Implement storage helpers**

Create `src/recipe_importer/storage.py`:

```python
import json
from pathlib import Path
from typing import Any

import yaml


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_yaml(path: Path, data: Any) -> None:
    write_text(path, yaml.safe_dump(data, sort_keys=False, allow_unicode=True))


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))
```

- [ ] **Step 5: Run storage tests**

Run:

```bash
uv run pytest tests/test_storage.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 6: Commit**

```bash
git add src/recipe_importer/paths.py src/recipe_importer/storage.py tests/conftest.py tests/test_storage.py
git commit -m "feat(storage): 增加文件型知识库路径"
```

## Task 4: Source List Parsing And Explicit Fetch

**Files:**
- Create: `src/recipe_importer/sources.py`
- Create: `src/recipe_importer/fetch.py`
- Create: `tests/test_sources_fetch.py`
- Modify: `src/recipe_importer/cli.py`
- Create: `recipe-kb/sources/source-list.yml`

- [ ] **Step 1: Write failing source/fetch tests**

Create `tests/test_sources_fetch.py`:

```python
import httpx

from recipe_importer.fetch import fetch_sources
from recipe_importer.paths import KbPaths
from recipe_importer.sources import load_source_list
from recipe_importer.storage import read_json, write_yaml


def test_load_source_list(kb_root):
    path = kb_root / "recipe-kb" / "sources" / "source-list.yml"
    write_yaml(
        path,
        {
            "sources": [
                {
                    "source_id": "react-error-418",
                    "url": "https://react.dev/errors/418",
                    "source_type": "official_error_doc",
                    "stacks": ["react", "nextjs"],
                    "expected_failure_hints": ["hydration mismatch"],
                    "refresh_policy": "monthly",
                }
            ]
        },
    )

    source_list = load_source_list(path)

    assert source_list.sources[0].source_id == "react-error-418"
    assert source_list.sources[0].stacks == ["react", "nextjs"]


def test_fetch_sources_writes_metadata_and_readable_seed(kb_root):
    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://react.dev/errors/418"
        return httpx.Response(
            200,
            headers={"content-type": "text/html"},
            text="<html><body><h1>Hydration failed</h1><p>server rendered HTML did not match</p></body></html>",
        )

    source_path = kb_root / "recipe-kb" / "sources" / "source-list.yml"
    write_yaml(
        source_path,
        {
            "sources": [
                {
                    "source_id": "react-error-418",
                    "url": "https://react.dev/errors/418",
                    "source_type": "official_error_doc",
                    "stacks": ["react"],
                    "expected_failure_hints": ["hydration mismatch"],
                    "refresh_policy": "monthly",
                }
            ]
        },
    )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    paths = KbPaths(kb_root).ensure()
    written = fetch_sources(source_path, paths, client=client, captured_at="2026-05-20T00:00:00Z")

    assert len(written) == 1
    metadata = read_json(paths.snapshots_dir / "react-error-418" / "response.json")
    html = (paths.snapshots_dir / "react-error-418" / "raw.html").read_text(encoding="utf-8")

    assert metadata["source_id"] == "react-error-418"
    assert metadata["retrieved_status"] == 200
    assert metadata["captured_at"] == "2026-05-20T00:00:00Z"
    assert "Hydration failed" in html
```

- [ ] **Step 2: Run source/fetch tests to verify they fail**

Run:

```bash
uv run pytest tests/test_sources_fetch.py -q
```

Expected: fail with missing `recipe_importer.sources`.

- [ ] **Step 3: Implement source list parsing**

Create `src/recipe_importer/sources.py`:

```python
from pathlib import Path

from recipe_importer.models import SourceList
from recipe_importer.storage import read_yaml


def load_source_list(path: Path) -> SourceList:
    return SourceList.model_validate(read_yaml(path))
```

- [ ] **Step 4: Implement explicit fetch**

Create `src/recipe_importer/fetch.py`:

```python
import hashlib
from datetime import UTC, datetime
from pathlib import Path

import httpx

from recipe_importer.paths import KbPaths
from recipe_importer.sources import load_source_list
from recipe_importer.storage import write_json, write_text


def sha256_text(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()


def fetch_sources(
    source_list_path: Path,
    paths: KbPaths,
    *,
    client: httpx.Client | None = None,
    captured_at: str | None = None,
) -> list[Path]:
    source_list = load_source_list(source_list_path)
    owns_client = client is None
    http = client or httpx.Client(follow_redirects=True, timeout=30.0)
    captured = captured_at or datetime.now(UTC).isoformat().replace("+00:00", "Z")
    written: list[Path] = []
    try:
        for source in source_list.sources:
            response = http.get(str(source.url))
            response.raise_for_status()
            snapshot_dir = paths.snapshots_dir / source.source_id
            raw_path = snapshot_dir / "raw.html"
            metadata_path = snapshot_dir / "response.json"
            write_text(raw_path, response.text)
            write_json(
                metadata_path,
                {
                    "source_id": source.source_id,
                    "url": str(source.url),
                    "final_url": str(response.url),
                    "source_type": source.source_type,
                    "captured_at": captured,
                    "retrieved_status": response.status_code,
                    "content_type": response.headers.get("content-type", ""),
                    "content_hash": sha256_text(response.text),
                },
            )
            written.append(snapshot_dir)
    finally:
        if owns_client:
            http.close()
    return written
```

- [ ] **Step 5: Add source seed and fetch CLI**

Create `recipe-kb/sources/source-list.yml`:

```yaml
sources:
  - source_id: react-error-418
    url: https://react.dev/errors/418
    source_type: official_error_doc
    stacks:
      - react
      - nextjs
    expected_failure_hints:
      - hydration mismatch
      - server rendered HTML did not match the client
    refresh_policy: monthly
```

Modify `src/recipe_importer/cli.py`:

```python
from pathlib import Path

import typer

from recipe_importer import __version__
from recipe_importer.fetch import fetch_sources
from recipe_importer.paths import KbPaths
from recipe_importer.schema import export_schemas

app = typer.Typer(no_args_is_help=True)
schema_app = typer.Typer(no_args_is_help=True)
app.add_typer(schema_app, name="schema")


@app.command()
def version() -> None:
    """Print the recipe importer version."""
    typer.echo(f"recipe-importer {__version__}")


@app.command()
def fetch(source_list: Path = Path("recipe-kb/sources/source-list.yml")) -> None:
    """Fetch configured sources and persist snapshot metadata."""
    paths = KbPaths(Path.cwd()).ensure()
    for path in fetch_sources(source_list, paths):
        typer.echo(str(path))


@schema_app.command("export")
def schema_export(output_dir: Path = Path("schemas")) -> None:
    """Export JSON Schemas for external adapters and review tooling."""
    for path in export_schemas(output_dir):
        typer.echo(str(path))
```

- [ ] **Step 6: Run source/fetch tests**

Run:

```bash
uv run pytest tests/test_sources_fetch.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 7: Commit**

```bash
git add src/recipe_importer/sources.py src/recipe_importer/fetch.py src/recipe_importer/cli.py tests/test_sources_fetch.py recipe-kb/sources/source-list.yml
git commit -m "feat(fetch): 增加 source 列表与显式采集"
```

## Task 5: HTML Sections And Evidence Refs

**Files:**
- Create: `src/recipe_importer/extract.py`
- Create: `tests/fixtures/react_error_418.html`
- Create: `tests/test_extract.py`
- Modify: `src/recipe_importer/cli.py`

- [ ] **Step 1: Add the React fixture**

Create `tests/fixtures/react_error_418.html`:

```html
<!doctype html>
<html>
  <body>
    <main>
      <h1>Hydration failed because the server rendered HTML didn't match the client</h1>
      <p>This can happen if a SSR-ed Client Component used a server/client branch.</p>
      <ul>
        <li>A server/client branch such as typeof window !== 'undefined'.</li>
        <li>Variable input such as Date.now() or Math.random().</li>
        <li>Date formatting in a user's locale which doesn't match the server.</li>
        <li>Invalid HTML tag nesting.</li>
      </ul>
      <h2>How to fix</h2>
      <p>Use an effect for client-only differences or pass a stable snapshot.</p>
    </main>
  </body>
</html>
```

- [ ] **Step 2: Write failing extraction tests**

Create `tests/test_extract.py`:

```python
from pathlib import Path

from recipe_importer.extract import extract_snapshot
from recipe_importer.paths import KbPaths
from recipe_importer.storage import read_json, write_json, write_text


def test_extract_snapshot_writes_sections_and_evidence(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    fixture = Path("tests/fixtures/react_error_418.html").read_text(encoding="utf-8")
    write_text(snapshot_dir / "raw.html", fixture)
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-20T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
        },
    )

    result = extract_snapshot(snapshot_dir)

    sections = read_json(snapshot_dir / "sections.json")
    readable = (snapshot_dir / "readable.md").read_text(encoding="utf-8")

    assert result.source_id == "react-error-418"
    assert sections[0]["span_id"] == "react-error-418-1"
    assert "Hydration failed" in readable
    assert sections[0]["quote_hash"].startswith("sha256:")
```

- [ ] **Step 3: Run extraction tests to verify they fail**

Run:

```bash
uv run pytest tests/test_extract.py -q
```

Expected: fail with missing `recipe_importer.extract`.

- [ ] **Step 4: Implement extraction**

Create `src/recipe_importer/extract.py`:

```python
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

from recipe_importer.storage import read_json, write_json, write_text


@dataclass(frozen=True)
class ExtractionResult:
    source_id: str
    section_count: int


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def quote_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(normalize_space(text).encode("utf-8")).hexdigest()


def extract_snapshot(snapshot_dir: Path) -> ExtractionResult:
    metadata = read_json(snapshot_dir / "response.json")
    source_id = metadata["source_id"]
    html = (snapshot_dir / "raw.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html5lib")
    main = soup.find("main") or soup.body or soup
    texts: list[str] = []
    for element in main.find_all(["h1", "h2", "h3", "p", "li"]):
        text = normalize_space(element.get_text(" "))
        if text:
            texts.append(text)

    sections = []
    for index, text in enumerate(texts, start=1):
        span_id = f"{source_id}-{index}"
        excerpt = text[:600]
        sections.append(
            {
                "source_id": source_id,
                "url": metadata["url"],
                "final_url": metadata["final_url"],
                "source_type": metadata["source_type"],
                "captured_at": metadata["captured_at"],
                "section_anchor": "root",
                "span_id": span_id,
                "short_excerpt": excerpt,
                "quote_hash": quote_hash(text),
                "text": text,
            }
        )

    write_json(snapshot_dir / "sections.json", sections)
    readable = "\n\n".join(f"- [{item['span_id']}] {item['text']}" for item in sections) + "\n"
    write_text(snapshot_dir / "readable.md", readable)
    return ExtractionResult(source_id=source_id, section_count=len(sections))
```

- [ ] **Step 5: Add extract CLI command**

Modify `src/recipe_importer/cli.py` to import and expose `extract_snapshot`:

```python
from recipe_importer.extract import extract_snapshot
```

Add command:

```python
@app.command()
def extract(snapshot_dir: Path) -> None:
    """Extract readable sections from one local snapshot directory."""
    result = extract_snapshot(snapshot_dir)
    typer.echo(f"{result.source_id}: {result.section_count} sections")
```

- [ ] **Step 6: Run extraction tests**

Run:

```bash
uv run pytest tests/test_extract.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 7: Commit**

```bash
git add src/recipe_importer/extract.py src/recipe_importer/cli.py tests/fixtures/react_error_418.html tests/test_extract.py
git commit -m "feat(extract): 提取文档 section evidence"
```

## Task 6: Evidence Candidates, Normalization, Render, Check

**Files:**
- Create: `src/recipe_importer/llm.py`
- Create: `src/recipe_importer/normalize.py`
- Create: `src/recipe_importer/render.py`
- Create: `tests/test_normalize_render.py`
- Modify: `src/recipe_importer/cli.py`

- [ ] **Step 1: Write failing normalize/render tests**

Create `tests/test_normalize_render.py`:

```python
from pathlib import Path

import pytest

from recipe_importer.extract import extract_snapshot
from recipe_importer.llm import deterministic_candidates
from recipe_importer.models import RecipeStatus
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.render import check_render_equivalence, render_recipe_file
from recipe_importer.storage import write_json, write_text


@pytest.fixture
def extracted_react_snapshot(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    html = Path("tests/fixtures/react_error_418.html").read_text(encoding="utf-8")
    write_text(snapshot_dir / "raw.html", html)
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-20T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
        },
    )
    extract_snapshot(snapshot_dir)
    return snapshot_dir


def test_deterministic_candidates_find_hydration(extracted_react_snapshot):
    candidates = deterministic_candidates(extracted_react_snapshot)

    assert candidates.candidates[0].failure_label == "hydration mismatch"
    assert candidates.candidates[0].confidence == "high"


def test_normalize_recipe_from_candidates(extracted_react_snapshot):
    candidates = deterministic_candidates(extracted_react_snapshot)
    recipe = normalize_recipe(
        candidates.candidates[0],
        extracted_react_snapshot,
        stack=["react", "nextjs"],
    )

    assert recipe.id == "react-hydration-mismatch"
    assert recipe.status is RecipeStatus.PROPOSED
    assert "Hydration failed" in recipe.symptoms[0]
    assert recipe.evidence_refs[0].source_id == "react-error-418"


def test_render_recipe_file_round_trip(extracted_react_snapshot, kb_root):
    paths = KbPaths(kb_root).ensure()
    recipe = normalize_recipe(
        deterministic_candidates(extracted_react_snapshot).candidates[0],
        extracted_react_snapshot,
        stack=["react", "nextjs"],
    )
    target = paths.proposed_dir / "react-hydration-mismatch.md"

    render_recipe_file(recipe, target)

    assert check_render_equivalence(target)
    text = target.read_text(encoding="utf-8")
    assert "## First Checks" in text
    assert "Do not disable SSR as the first fix" in text
```

- [ ] **Step 2: Run normalize/render tests to verify they fail**

Run:

```bash
uv run pytest tests/test_normalize_render.py -q
```

Expected: fail with missing `recipe_importer.llm`.

- [ ] **Step 3: Implement deterministic candidates**

Create `src/recipe_importer/llm.py`:

```python
from pathlib import Path

from recipe_importer.models import EvidenceCandidate, EvidenceCandidates
from recipe_importer.storage import read_json


def deterministic_candidates(snapshot_dir: Path) -> EvidenceCandidates:
    sections = read_json(snapshot_dir / "sections.json")
    joined = "\n".join(item["text"] for item in sections)
    if "Hydration failed" not in joined:
        return EvidenceCandidates(candidates=[])
    section_refs = [item["span_id"] for item in sections if "Hydration" in item["text"] or "Date.now" in item["text"]]
    return EvidenceCandidates(
        candidates=[
            EvidenceCandidate(
                failure_label="hydration mismatch",
                symptom_quotes=["Hydration failed because the server rendered HTML didn't match the client"],
                cause_quotes=[
                    "server/client branch",
                    "Date.now() or Math.random()",
                    "Date formatting in a user's locale",
                    "Invalid HTML tag nesting",
                ],
                avoidance_quotes=["Do not disable SSR as the first fix"],
                validation_quotes=["Reproduce the page and inspect browser console hydration warning"],
                section_refs=section_refs,
                confidence="high",
            )
        ]
    )
```

- [ ] **Step 4: Implement normalization**

Create `src/recipe_importer/normalize.py`:

```python
from pathlib import Path

from recipe_importer.models import EvidenceCandidate, EvidenceRef, Recipe, RecipeStatus
from recipe_importer.storage import read_json


def _evidence_refs(snapshot_dir: Path, span_ids: list[str]) -> list[EvidenceRef]:
    sections = read_json(snapshot_dir / "sections.json")
    wanted = set(span_ids)
    selected = [item for item in sections if item["span_id"] in wanted]
    if not selected:
        selected = sections[:1]
    return [
        EvidenceRef(
            source_id=item["source_id"],
            url=item["url"],
            final_url=item["final_url"],
            source_type=item["source_type"],
            captured_at=item["captured_at"],
            section_anchor=item["section_anchor"],
            span_id=item["span_id"],
            short_excerpt=item["short_excerpt"],
            quote_hash=item["quote_hash"],
        )
        for item in selected
    ]


def normalize_recipe(candidate: EvidenceCandidate, snapshot_dir: Path, *, stack: list[str]) -> Recipe:
    return Recipe(
        id="react-hydration-mismatch",
        status=RecipeStatus.PROPOSED,
        stack=stack,
        failure_class="render/hydration",
        symptoms=candidate.symptom_quotes or ["Hydration failed"],
        fingerprints=[
            "Hydration failed",
            "server rendered HTML didn't match the client",
            "server rendered HTML did not match the client",
        ],
        first_checks=[
            "Check server/client branches such as typeof window in render output",
            "Check Date.now(), Math.random(), and locale formatting in render output",
            "Check invalid HTML nesting in the affected component",
        ],
        do_not=[
            "Do not disable SSR as the first fix",
            "Do not rewrite the component tree before locating the mismatched markup",
        ],
        evidence_needed=[
            "Identify the component producing different server and client markup",
            "Capture the browser console hydration warning",
        ],
        minimal_fix_scope=[
            "The component producing mismatched markup",
            "The server-to-client data snapshot used by that component",
        ],
        validation_ladder=[
            "Reproduce the page in development",
            "Check browser console for the hydration warning",
            "Run the related smoke test if one exists",
        ],
        regression_guard=[
            "Add or update a smoke test for the affected page or component",
        ],
        evidence_refs=_evidence_refs(snapshot_dir, candidate.section_refs),
    )
```

- [ ] **Step 5: Implement render and equivalence check**

Create `src/recipe_importer/render.py`:

```python
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
            "## Reviewer Notes\n",
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
```

- [ ] **Step 6: Add extract/import/check commands**

Modify `src/recipe_importer/cli.py` to expose:

```python
from recipe_importer.llm import deterministic_candidates
from recipe_importer.normalize import normalize_recipe
from recipe_importer.render import check_render_equivalence, render_recipe_file
```

Add commands:

```python
@app.command()
def import_source(snapshot_dir: Path, stack: list[str] = typer.Option(["react", "nextjs"])) -> None:
    """Create proposed recipes from one extracted snapshot."""
    paths = KbPaths(Path.cwd()).ensure()
    candidates = deterministic_candidates(snapshot_dir)
    for candidate in candidates.candidates:
        recipe = normalize_recipe(candidate, snapshot_dir, stack=stack)
        target = paths.proposed_dir / f"{recipe.id}.md"
        render_recipe_file(recipe, target)
        typer.echo(str(target))


@app.command()
def check(recipe: Path) -> None:
    """Check that generated Markdown matches canonical YAML frontmatter."""
    if not check_render_equivalence(recipe):
        raise typer.BadParameter(f"{recipe} is not render-equivalent")
    typer.echo(f"{recipe}: ok")
```

If Typer rejects the command name `import-source`, keep the Python function name `import_source`; Typer exposes it as `import-source`.

- [ ] **Step 7: Run normalize/render tests**

Run:

```bash
uv run pytest tests/test_normalize_render.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 8: Commit**

```bash
git add src/recipe_importer/llm.py src/recipe_importer/normalize.py src/recipe_importer/render.py src/recipe_importer/cli.py tests/test_normalize_render.py
git commit -m "feat(recipe): 生成 canonical proposed recipe"
```

## Task 7: Manifest Hash And Auto Revision

**Files:**
- Create: `src/recipe_importer/manifest.py`
- Create: `tests/test_manifest.py`
- Create: `prompts/debug_recipe_evidence.md`
- Modify: `src/recipe_importer/cli.py`

- [ ] **Step 1: Write failing manifest tests**

Create `tests/test_manifest.py`:

```python
from recipe_importer.manifest import Manifest, check_manifest, refresh_manifest


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

    assert second.prompts["debug_recipe_evidence"].rev == first.prompts["debug_recipe_evidence"].rev + 1


def test_check_manifest_detects_current_hash(kb_root):
    prompt = kb_root / "prompts" / "debug_recipe_evidence.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("Extract evidence candidates.\n", encoding="utf-8")
    refresh_manifest(kb_root)

    assert check_manifest(kb_root)
```

- [ ] **Step 2: Run manifest tests to verify they fail**

Run:

```bash
uv run pytest tests/test_manifest.py -q
```

Expected: fail with missing `recipe_importer.manifest`.

- [ ] **Step 3: Implement manifest**

Create `src/recipe_importer/manifest.py`:

```python
import hashlib
from pathlib import Path

from pydantic import BaseModel

from recipe_importer.storage import read_yaml, write_yaml


class ManifestItem(BaseModel):
    rev: int
    path: str | None = None
    files: list[str] | None = None
    hash: str


class Manifest(BaseModel):
    prompts: dict[str, ManifestItem] = {}
    schemas: dict[str, ManifestItem] = {}
    extractors: dict[str, ManifestItem] = {}


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
    rev = previous.rev if previous and previous.hash == prompt_hash else (previous.rev + 1 if previous else 1)
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
    item = manifest.prompts["debug_recipe_evidence"]
    return item.hash == _hash_file(root / item.path)
```

- [ ] **Step 4: Add prompt file and manifest CLI**

Create `prompts/debug_recipe_evidence.md`:

```markdown
# Debug Recipe Evidence Candidate Extraction

Extract only source-grounded evidence candidates from official troubleshooting
or error documentation. Return narrow JSON containing failure labels, source
quotes, section references, and confidence. Do not create accepted recipes.
```

Modify `src/recipe_importer/cli.py`:

```python
from recipe_importer.manifest import check_manifest, refresh_manifest
```

Add Typer group and commands:

```python
manifest_app = typer.Typer(no_args_is_help=True)
app.add_typer(manifest_app, name="manifest")


@manifest_app.command("refresh")
def manifest_refresh() -> None:
    manifest = refresh_manifest(Path.cwd())
    typer.echo(f"debug_recipe_evidence rev {manifest.prompts['debug_recipe_evidence'].rev}")


@manifest_app.command("check")
def manifest_check() -> None:
    if not check_manifest(Path.cwd()):
        raise typer.Exit(code=1)
    typer.echo("manifest ok")
```

- [ ] **Step 5: Run manifest tests**

Run:

```bash
uv run pytest tests/test_manifest.py -q
uv run recipe-importer manifest refresh
uv run recipe-importer manifest check
```

Expected:

```text
3 passed
debug_recipe_evidence rev 1
manifest ok
```

- [ ] **Step 6: Commit**

```bash
git add src/recipe_importer/manifest.py src/recipe_importer/cli.py prompts/debug_recipe_evidence.md tests/test_manifest.py recipe-kb/manifest.yml
git commit -m "feat(manifest): 记录抽取资产 hash 与 revision"
```

## Task 8: Inbox-First Review Session

**Files:**
- Create: `src/recipe_importer/review.py`
- Create: `tests/test_review.py`
- Modify: `src/recipe_importer/cli.py`

- [ ] **Step 1: Write failing review tests**

Create `tests/test_review.py`:

```python
from recipe_importer.models import ReviewDecision
from recipe_importer.paths import KbPaths
from recipe_importer.review import current_candidate, decide_current, next_candidate, start_review
from recipe_importer.storage import read_json, write_text


def test_review_session_current_next_and_decide(kb_root):
    paths = KbPaths(kb_root).ensure()
    write_text(paths.proposed_dir / "a.md", "---\nid: a\n---\n")
    write_text(paths.proposed_dir / "b.md", "---\nid: b\n---\n")

    session = start_review(paths)
    assert current_candidate(paths, session).name == "a.md"

    session = next_candidate(paths, session)
    assert current_candidate(paths, session).name == "b.md"

    decide_current(paths, session, ReviewDecision.NEEDS_MORE_EVIDENCE, notes="source quote too broad")
    record = read_json(paths.review_dir / "decisions.json")[0]

    assert record["candidate_id"] == "b"
    assert record["decision"] == "needs_more_evidence"
```

- [ ] **Step 2: Run review tests to verify they fail**

Run:

```bash
uv run pytest tests/test_review.py -q
```

Expected: fail with missing `recipe_importer.review`.

- [ ] **Step 3: Implement review session**

Create `src/recipe_importer/review.py`:

```python
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from recipe_importer.models import ReviewDecision
from recipe_importer.paths import KbPaths
from recipe_importer.storage import read_json, write_json


@dataclass(frozen=True)
class ReviewSession:
    cursor: int
    candidates: list[str]


def _session_path(paths: KbPaths) -> Path:
    return paths.review_dir / "session.json"


def _decisions_path(paths: KbPaths) -> Path:
    return paths.review_dir / "decisions.json"


def _candidate_files(paths: KbPaths) -> list[Path]:
    return sorted(paths.proposed_dir.glob("*.md"))


def _load_session(paths: KbPaths) -> ReviewSession:
    data = read_json(_session_path(paths))
    return ReviewSession(cursor=data["cursor"], candidates=data["candidates"])


def _save_session(paths: KbPaths, session: ReviewSession) -> ReviewSession:
    write_json(_session_path(paths), {"cursor": session.cursor, "candidates": session.candidates})
    return session


def start_review(paths: KbPaths) -> ReviewSession:
    candidates = [path.name for path in _candidate_files(paths)]
    return _save_session(paths, ReviewSession(cursor=0, candidates=candidates))


def current_candidate(paths: KbPaths, session: ReviewSession | None = None) -> Path:
    session = session or _load_session(paths)
    if not session.candidates:
        raise ValueError("review queue is empty")
    return paths.proposed_dir / session.candidates[session.cursor]


def next_candidate(paths: KbPaths, session: ReviewSession) -> ReviewSession:
    if not session.candidates:
        return session
    cursor = min(session.cursor + 1, len(session.candidates) - 1)
    return _save_session(paths, ReviewSession(cursor=cursor, candidates=session.candidates))


def previous_candidate(paths: KbPaths, session: ReviewSession) -> ReviewSession:
    cursor = max(session.cursor - 1, 0)
    return _save_session(paths, ReviewSession(cursor=cursor, candidates=session.candidates))


def decide_current(paths: KbPaths, session: ReviewSession, decision: ReviewDecision, notes: str = "") -> None:
    current = current_candidate(paths, session)
    candidate_id = current.stem
    decisions = read_json(_decisions_path(paths)) if _decisions_path(paths).exists() else []
    decisions.append(
        {
            "candidate_id": candidate_id,
            "decision": decision.value,
            "reviewed_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "reviewer": "human",
            "notes": notes,
        }
    )
    write_json(_decisions_path(paths), decisions)
```

- [ ] **Step 4: Add review CLI**

Modify `src/recipe_importer/cli.py`:

```python
from recipe_importer.models import ReviewDecision
from recipe_importer.review import current_candidate, decide_current, next_candidate, previous_candidate, start_review
```

Add:

```python
review_app = typer.Typer(no_args_is_help=True)
app.add_typer(review_app, name="review")


@review_app.callback(invoke_without_command=True)
def review_start(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        paths = KbPaths(Path.cwd()).ensure()
        session = start_review(paths)
        typer.echo(str(current_candidate(paths, session)))


@review_app.command("current")
def review_current() -> None:
    paths = KbPaths(Path.cwd()).ensure()
    typer.echo(str(current_candidate(paths)))


@review_app.command("accept")
def review_accept(notes: str = "") -> None:
    paths = KbPaths(Path.cwd()).ensure()
    session = start_review(paths)
    decide_current(paths, session, ReviewDecision.ACCEPT, notes)
    typer.echo("accepted")
```

After this step, add `next`, `prev`, `reject`, and `needs-more-evidence` using the same `decide_current` pattern. Use `needs_more_evidence` as the internal enum and expose `needs-more-evidence` as the CLI command name.

- [ ] **Step 5: Run review tests**

Run:

```bash
uv run pytest tests/test_review.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 6: Commit**

```bash
git add src/recipe_importer/review.py src/recipe_importer/cli.py tests/test_review.py
git commit -m "feat(review): 增加 inbox 审阅状态流"
```

## Task 9: Publish, Dedupe, Index, Search, Get

**Files:**
- Create: `src/recipe_importer/dedupe.py`
- Create: `src/recipe_importer/publish.py`
- Create: `src/recipe_importer/index.py`
- Create: `src/recipe_importer/search.py`
- Create: `tests/test_publish_index_search.py`
- Modify: `src/recipe_importer/cli.py`

- [ ] **Step 1: Write failing publish/search tests**

Create `tests/test_publish_index_search.py`:

```python
from pathlib import Path

from recipe_importer.extract import extract_snapshot
from recipe_importer.index import rebuild_index
from recipe_importer.llm import deterministic_candidates
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.publish import publish_recipe
from recipe_importer.render import render_recipe_file
from recipe_importer.search import get_recipe, search_recipes
from recipe_importer.storage import write_json, write_text


def proposed_recipe(paths):
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    html = Path("tests/fixtures/react_error_418.html").read_text(encoding="utf-8")
    write_text(snapshot_dir / "raw.html", html)
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-20T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
        },
    )
    extract_snapshot(snapshot_dir)
    recipe = normalize_recipe(
        deterministic_candidates(snapshot_dir).candidates[0],
        snapshot_dir,
        stack=["react", "nextjs"],
    )
    target = paths.proposed_dir / f"{recipe.id}.md"
    render_recipe_file(recipe, target)
    return target


def test_publish_rebuild_search_and_get(kb_root):
    paths = KbPaths(kb_root).ensure()
    proposed = proposed_recipe(paths)

    accepted = publish_recipe(proposed, paths)
    index_path = rebuild_index(paths)
    results = search_recipes(paths, "Hydration failed")
    full = get_recipe(paths, "react-hydration-mismatch")

    assert accepted == paths.accepted_dir / "react-hydration-mismatch.md"
    assert index_path == paths.index_path
    assert results[0]["id"] == "react-hydration-mismatch"
    assert "Do not disable SSR" in "\n".join(results[0]["do_not"])
    assert full.id == "react-hydration-mismatch"
```

- [ ] **Step 2: Run publish/search tests to verify they fail**

Run:

```bash
uv run pytest tests/test_publish_index_search.py -q
```

Expected: fail with missing `recipe_importer.index`.

- [ ] **Step 3: Implement publish**

Create `src/recipe_importer/publish.py`:

```python
from pathlib import Path

from recipe_importer.models import RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file, render_recipe_file


def publish_recipe(proposed_path: Path, paths: KbPaths) -> Path:
    recipe = parse_recipe_file(proposed_path)
    recipe.status = RecipeStatus.ACCEPTED
    recipe.maintenance.state = RecipeStatus.ACCEPTED
    target = paths.accepted_dir / proposed_path.name
    render_recipe_file(recipe, target)
    return target
```

- [ ] **Step 4: Implement index and search**

Create `src/recipe_importer/index.py`:

```python
from recipe_importer.models import RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file
from recipe_importer.storage import write_json


def rebuild_index(paths: KbPaths):
    records = []
    for directory in [paths.accepted_dir, paths.stale_dir]:
        for path in sorted(directory.glob("*.md")):
            recipe = parse_recipe_file(path)
            records.append(
                {
                    "id": recipe.id,
                    "path": str(path.relative_to(paths.root)),
                    "status": recipe.status.value,
                    "stack": recipe.stack,
                    "failure_class": recipe.failure_class,
                    "symptoms": recipe.symptoms,
                    "fingerprints": recipe.fingerprints,
                    "first_checks": recipe.first_checks,
                    "do_not": recipe.do_not,
                    "validation_ladder": recipe.validation_ladder,
                    "stale": recipe.status is RecipeStatus.STALE,
                }
            )
    write_json(paths.index_path, {"recipes": records})
    return paths.index_path
```

Create `src/recipe_importer/search.py`:

```python
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file
from recipe_importer.storage import read_json


def _score(record: dict, query: str) -> int:
    q = query.lower()
    fields = record["fingerprints"] + record["symptoms"] + [record["failure_class"]]
    return sum(1 for value in fields if q in value.lower() or value.lower() in q)


def search_recipes(paths: KbPaths, query: str, *, top: int = 3, fresh_only: bool = False) -> list[dict]:
    data = read_json(paths.index_path)
    records = [record for record in data["recipes"] if not (fresh_only and record["stale"])]
    ranked = sorted(records, key=lambda record: _score(record, query), reverse=True)
    return [record for record in ranked if _score(record, query) > 0][:top]


def get_recipe(paths: KbPaths, recipe_id: str):
    data = read_json(paths.index_path)
    for record in data["recipes"]:
        if record["id"] == recipe_id:
            return parse_recipe_file(paths.root / record["path"])
    raise KeyError(recipe_id)
```

- [ ] **Step 5: Implement dedupe hints**

Create `src/recipe_importer/dedupe.py`:

```python
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
```

- [ ] **Step 6: Add publish/index/search/get CLI**

Modify `src/recipe_importer/cli.py`:

```python
from recipe_importer.index import rebuild_index
from recipe_importer.publish import publish_recipe
from recipe_importer.search import get_recipe, search_recipes
```

Add:

```python
index_app = typer.Typer(no_args_is_help=True)
app.add_typer(index_app, name="index")


@app.command()
def publish(recipe: Path) -> None:
    paths = KbPaths(Path.cwd()).ensure()
    typer.echo(str(publish_recipe(recipe, paths)))


@index_app.command("rebuild")
def index_rebuild() -> None:
    paths = KbPaths(Path.cwd()).ensure()
    typer.echo(str(rebuild_index(paths)))


@app.command()
def search(query: str, fresh_only: bool = False) -> None:
    paths = KbPaths(Path.cwd()).ensure()
    for record in search_recipes(paths, query, fresh_only=fresh_only):
        warning = " [stale]" if record["stale"] else ""
        typer.echo(f"{record['id']}{warning}")
        for check in record["first_checks"]:
            typer.echo(f"  check: {check}")
        for item in record["do_not"]:
            typer.echo(f"  do-not: {item}")


@app.command("get")
def recipe_get(recipe_id: str) -> None:
    paths = KbPaths(Path.cwd()).ensure()
    typer.echo(get_recipe(paths, recipe_id).model_dump_json(indent=2))
```

- [ ] **Step 7: Run publish/search tests**

Run:

```bash
uv run pytest tests/test_publish_index_search.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 8: Commit**

```bash
git add src/recipe_importer/dedupe.py src/recipe_importer/publish.py src/recipe_importer/index.py src/recipe_importer/search.py src/recipe_importer/cli.py tests/test_publish_index_search.py
git commit -m "feat(search): 发布并检索 accepted recipe"
```

## Task 10: Refresh And Stale Marking

**Files:**
- Create: `src/recipe_importer/refresh.py`
- Create: `tests/test_refresh.py`
- Modify: `src/recipe_importer/cli.py`

- [ ] **Step 1: Write failing refresh test**

Create `tests/test_refresh.py`:

```python
from pathlib import Path

from recipe_importer.extract import extract_snapshot
from recipe_importer.index import rebuild_index
from recipe_importer.llm import deterministic_candidates
from recipe_importer.normalize import normalize_recipe
from recipe_importer.paths import KbPaths
from recipe_importer.publish import publish_recipe
from recipe_importer.refresh import refresh_stale_status
from recipe_importer.render import render_recipe_file
from recipe_importer.storage import write_json, write_text


def test_refresh_marks_recipe_stale_when_quote_hash_changes(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    html = Path("tests/fixtures/react_error_418.html").read_text(encoding="utf-8")
    write_text(snapshot_dir / "raw.html", html)
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-20T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
        },
    )
    extract_snapshot(snapshot_dir)
    recipe = normalize_recipe(deterministic_candidates(snapshot_dir).candidates[0], snapshot_dir, stack=["react"])
    proposed = paths.proposed_dir / "react-hydration-mismatch.md"
    render_recipe_file(recipe, proposed)
    publish_recipe(proposed, paths)

    sections = snapshot_dir / "sections.json"
    data = sections.read_text(encoding="utf-8").replace("sha256:", "sha256:changed-")
    sections.write_text(data, encoding="utf-8")

    stale_paths = refresh_stale_status(paths)
    rebuild_index(paths)

    assert stale_paths == [paths.stale_dir / "react-hydration-mismatch.md"]
    assert (paths.stale_dir / "react-hydration-mismatch.md").exists()
```

- [ ] **Step 2: Run refresh test to verify it fails**

Run:

```bash
uv run pytest tests/test_refresh.py -q
```

Expected: fail with missing `recipe_importer.refresh`.

- [ ] **Step 3: Implement refresh stale detection**

Create `src/recipe_importer/refresh.py`:

```python
from pathlib import Path

from recipe_importer.models import RecipeStatus
from recipe_importer.paths import KbPaths
from recipe_importer.render import parse_recipe_file, render_recipe_file
from recipe_importer.storage import read_json


def _current_quote_hashes(paths: KbPaths, source_id: str) -> set[str]:
    sections_path = paths.snapshots_dir / source_id / "sections.json"
    if not sections_path.exists():
        return set()
    return {item["quote_hash"] for item in read_json(sections_path)}


def refresh_stale_status(paths: KbPaths) -> list[Path]:
    stale_paths: list[Path] = []
    for recipe_path in sorted(paths.accepted_dir.glob("*.md")):
        recipe = parse_recipe_file(recipe_path)
        stale_reasons: list[str] = []
        for ref in recipe.evidence_refs:
            if ref.quote_hash not in _current_quote_hashes(paths, ref.source_id):
                stale_reasons.append("source_quote_hash_changed")
        if stale_reasons:
            recipe.status = RecipeStatus.STALE
            recipe.maintenance.state = RecipeStatus.STALE
            recipe.maintenance.stale_reason = sorted(set(stale_reasons))
            target = paths.stale_dir / recipe_path.name
            render_recipe_file(recipe, target)
            recipe_path.unlink()
            stale_paths.append(target)
    return stale_paths
```

- [ ] **Step 4: Add refresh CLI**

Modify `src/recipe_importer/cli.py`:

```python
from recipe_importer.refresh import refresh_stale_status
```

Add:

```python
@app.command()
def refresh() -> None:
    """Mark accepted recipes stale when local refreshed evidence no longer matches."""
    paths = KbPaths(Path.cwd()).ensure()
    for path in refresh_stale_status(paths):
        typer.echo(f"stale: {path}")
```

- [ ] **Step 5: Run refresh test**

Run:

```bash
uv run pytest tests/test_refresh.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 6: Commit**

```bash
git add src/recipe_importer/refresh.py src/recipe_importer/cli.py tests/test_refresh.py
git commit -m "feat(refresh): 标记 source evidence 变更的 recipe"
```

## Task 11: End-To-End React Error 418 Vertical Slice

**Files:**
- Create: `tests/test_vertical_slice.py`
- Create: `recipe-kb/feedback/.gitkeep`
- Modify: `README.md`
- Modify: `src/recipe_importer/cli.py`

- [ ] **Step 1: Write failing end-to-end test**

Create `tests/test_vertical_slice.py`:

```python
from pathlib import Path

from typer.testing import CliRunner

from recipe_importer.cli import app
from recipe_importer.paths import KbPaths
from recipe_importer.storage import write_json, write_text, write_yaml


def test_vertical_slice_without_network(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    monkeypatch.chdir(repo)
    paths = KbPaths(repo).ensure()
    (repo / "prompts").mkdir()
    write_text(repo / "prompts" / "debug_recipe_evidence.md", "Extract evidence candidates.\n")
    write_yaml(
        paths.sources_dir / "source-list.yml",
        {
            "sources": [
                {
                    "source_id": "react-error-418",
                    "url": "https://react.dev/errors/418",
                    "source_type": "official_error_doc",
                    "stacks": ["react", "nextjs"],
                    "expected_failure_hints": ["hydration mismatch"],
                    "refresh_policy": "monthly",
                }
            ]
        },
    )
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    html = Path(__file__).parent.joinpath("fixtures/react_error_418.html").read_text(encoding="utf-8")
    write_text(snapshot_dir / "raw.html", html)
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-20T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
        },
    )
    runner = CliRunner()

    assert runner.invoke(app, ["extract", str(snapshot_dir)]).exit_code == 0
    assert runner.invoke(app, ["import-source", str(snapshot_dir)]).exit_code == 0
    recipe_path = paths.proposed_dir / "react-hydration-mismatch.md"
    assert runner.invoke(app, ["check", str(recipe_path)]).exit_code == 0
    assert runner.invoke(app, ["publish", str(recipe_path)]).exit_code == 0
    assert runner.invoke(app, ["index", "rebuild"]).exit_code == 0
    search_result = runner.invoke(app, ["search", "Hydration failed"])

    assert search_result.exit_code == 0
    assert "react-hydration-mismatch" in search_result.stdout
    assert "Do not disable SSR" in search_result.stdout
```

- [ ] **Step 2: Run vertical slice test to verify it fails if any command is incomplete**

Run:

```bash
uv run pytest tests/test_vertical_slice.py -q
```

Expected: fail only on missing CLI wiring. If it fails inside core logic, fix the specific task that owns that module before continuing.

- [ ] **Step 3: Complete CLI wiring**

Update `src/recipe_importer/cli.py` so all commands used by the vertical slice exist:

```text
extract
import-source
check
publish
index rebuild
search
get
manifest refresh
manifest check
review current/next/prev/accept/reject/needs-more-evidence
refresh
schema export
version
```

Ensure command names use hyphens for multiword CLI commands. Internal Python function names should stay snake_case.

- [ ] **Step 4: Add feedback placeholder and README usage**

Create `recipe-kb/feedback/.gitkeep` as an empty file.

Update `README.md`:

~~~markdown
## MVP Flow

```bash
uv run recipe-importer fetch recipe-kb/sources/source-list.yml
uv run recipe-importer extract recipe-kb/snapshots/react-error-418
uv run recipe-importer import-source recipe-kb/snapshots/react-error-418
uv run recipe-importer check recipe-kb/proposed/react-hydration-mismatch.md
uv run recipe-importer publish recipe-kb/proposed/react-hydration-mismatch.md
uv run recipe-importer index rebuild
uv run recipe-importer search "Hydration failed"
```

Default tests use local fixtures. Network access happens only during explicit
`fetch`, `import`, or `refresh` operations.
~~~

When inserting the fenced block into `README.md`, use proper Markdown nesting so the outer file renders correctly.

- [ ] **Step 5: Run the full test suite**

Run:

```bash
uv run pytest -q
```

Expected:

```text
all tests pass
```

- [ ] **Step 6: Run CLI verification**

Run:

```bash
uv run recipe-importer version
uv run recipe-importer schema export schemas
uv run recipe-importer manifest refresh
uv run recipe-importer manifest check
```

Expected:

```text
recipe-importer 0.1.0
schemas/debug-recipe.schema.json
schemas/source.schema.json
schemas/review.schema.json
schemas/evidence-candidates.schema.json
debug_recipe_evidence rev 1
manifest ok
```

- [ ] **Step 7: Commit**

```bash
git add tests/test_vertical_slice.py recipe-kb/feedback/.gitkeep README.md src/recipe_importer/cli.py schemas/ recipe-kb/manifest.yml
git commit -m "feat(vertical-slice): 跑通 React hydration recipe 闭环"
```

## Task 12: Final Verification And Plan Closure

**Files:**
- Modify: `docs/superpowers/plans/2026-05-20-debug-recipe-importer-mvp.md`

- [ ] **Step 1: Run default verification**

Run:

```bash
uv run pytest -q
uv run recipe-importer schema export schemas
uv run recipe-importer manifest check
uv run recipe-importer index rebuild
uv run recipe-importer search "Hydration failed"
git diff --check
```

Expected:

```text
pytest exits 0
schema export exits 0
manifest check exits 0
index rebuild exits 0
search prints react-hydration-mismatch
git diff --check exits 0
```

- [ ] **Step 2: Verify design coverage**

Check these design requirements against the implemented files:

```text
CLI-first core exists in src/recipe_importer/cli.py
File-based KB exists under recipe-kb/
Pydantic canonical models exist in models.py
JSON Schemas export under schemas/
Generated Markdown equivalence is enforced by check
Fetch is explicit and default tests do not use network
Evidence refs include section/span and quote hash
LLM extraction is narrow evidence_candidates only
Review is inbox-first
Accepted publish requires render/check path
Index is derived and rebuildable
Search returns top 3 context-safe summaries
Refresh marks stale instead of deleting recipes
```

- [ ] **Step 3: Commit plan checkbox updates if implementation updated this plan**

If this plan file was edited to mark completed checkboxes:

```bash
git add docs/superpowers/plans/2026-05-20-debug-recipe-importer-mvp.md
git commit -m "docs(plan): 更新 importer MVP 执行进度"
```

## Self-Review

Spec coverage:

- The plan covers CLI scaffold, schema, file storage, fetch, extract, evidence refs, deterministic evidence candidates, normalization, YAML canonical rendering, manifest hash/rev, inbox review, publish, index, search/get, refresh/stale, and the React error 418 vertical slice.
- The plan intentionally leaves real LLM providers, embeddings, SQLite, browser rendering, and full feedback commands outside MVP, matching the accepted design.

Placeholder scan:

- This plan contains no placeholder markers or intentionally blank implementation step.
- The only optional path is the known Typer command naming behavior, and the plan gives the exact fallback command name.

Type consistency:

- `Recipe`, `EvidenceRef`, `EvidenceCandidate`, `EvidenceCandidates`, `RecipeStatus`, and `ReviewDecision` are introduced in Task 2 and reused consistently.
- `KbPaths` is introduced in Task 3 and reused by all later modules.
- `render_recipe_file`, `parse_recipe_file`, and `check_render_equivalence` are introduced in Task 6 and reused in publish/search/refresh.

Execution handoff:

Plan complete and saved to `docs/superpowers/plans/2026-05-20-debug-recipe-importer-mvp.md`. Two execution options:

1. Subagent-Driven (recommended) - dispatch a fresh implementation agent per task, review between tasks, fast iteration.
2. Inline Execution - execute tasks in this session with checkpoints after each task.

Choose one before implementation starts.
