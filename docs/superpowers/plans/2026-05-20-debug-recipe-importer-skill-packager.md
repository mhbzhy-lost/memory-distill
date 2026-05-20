# Debug Recipe Importer Skill Packager Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a one-command packager that generates a Codex skill for agent use of the debug recipe importer.

**Architecture:** The packager is a Python script that deterministically creates a `debug-recipe-importer` skill directory. The skill contains concise agent instructions, UI metadata, a wrapper script, and a bundled copy of the importer code plus static KB assets.

**Tech Stack:** Python 3.12, pytest, uv, Codex skill folder layout.

---

## DAG And Parallelization

```text
Task 1: RED tests for generated skill package
  -> Task 2: packager script and templates
      -> Task 3: verification and commit
```

No task is worth parallelizing because the tests and script touch the same feature boundary.

## Task 1: RED Tests

**Files:**
- Create: `tests/test_build_agent_skill.py`

- [x] **Step 1: Add failing tests**

Create tests that execute `scripts/build_agent_skill.py` into a temporary output directory and assert:

- `SKILL.md`, `agents/openai.yaml`, and `scripts/recipe-importer` are generated.
- `assets/recipe-importer` contains `src/`, `bin/`, `schemas/`, `prompts/`, `recipe-kb/`, `pyproject.toml`, and `uv.lock`.
- `recipe-kb/snapshots/**/raw.html` is not packaged.
- The wrapper can run `version` and `search "Hydration failed"` against the bundled KB.
- Existing output is refused unless `--force` is passed.

- [x] **Step 2: Run RED**

Run:

```bash
uv run pytest tests/test_build_agent_skill.py -q
```

Expected: fail because `scripts/build_agent_skill.py` does not exist yet.

## Task 2: Packager Script

**Files:**
- Create: `scripts/build_agent_skill.py`

- [x] **Step 1: Implement deterministic generation**

The script should:

- Accept `--output <dir>` and optional `--force`.
- Refuse to overwrite existing output without `--force`.
- Write `SKILL.md` and `agents/openai.yaml`.
- Write executable `scripts/recipe-importer`.
- Copy importer executable code and static assets into `assets/recipe-importer`.
- Exclude caches, virtualenvs, bytecode, and raw HTML snapshots.

- [x] **Step 2: Run targeted tests**

Run:

```bash
uv run pytest tests/test_build_agent_skill.py -q
```

Expected: all tests pass.

## Task 3: Verification And Closure

**Files:**
- Modify: `docs/superpowers/plans/2026-05-20-debug-recipe-importer-skill-packager.md`

- [x] **Step 1: Run full verification**

Run:

```bash
uv run pytest -q
git diff --check
```

Expected: all tests pass and whitespace check exits 0.

- [x] **Step 2: Mark plan complete and commit**

Commit the packager, tests, and plan updates.
