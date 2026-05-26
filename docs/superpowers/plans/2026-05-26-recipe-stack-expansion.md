# Recipe Stack Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the recipe knowledge base from 9 recipes across 6 frameworks to 25-35 recipes across 12 frameworks by adding FastAPI, LangChain, Expo, iOS, Android, and HarmonyOS stacks.

**Architecture:** This is primarily a content curation task. For each new stack, research official error/troubleshooting documentation URLs, add them to `source-list.yml`, run the existing fetch-extract-import pipeline, review generated recipes, and publish accepted ones. The `list` command provides stack-level aggregation for decision-making.

**Tech Stack:** Python (uv), FastAPI static docs (MkDocs), Pydantic static docs, LangChain MDX docs, Expo Docusaurus docs. iOS/Android/HarmonyOS docs are SPAs and require manual research for static alternatives.

---

## File Structure

| File | Responsibility | Changes |
|------|----------------|---------|
| `src/recipe_importer/cli.py` | CLI commands | Add `list` subcommand |
| `src/recipe_importer/index.py` | Index management | Add stack aggregation function |
| `recipe-kb/sources/source-list.yml` | Source configuration | Add 15-25 new sources |
| `recipe-kb/index.json` | Search index | Auto-generated on `index rebuild` |
| `recipe-kb/accepted/*.md` | Published recipes | 16-26 new files |

---

## Task 1: Research and Validate Documentation URLs

**Goal:** Create a curated list of accessible, high-quality error/troubleshooting documentation URLs for each target stack.

**Files:**
- Create: `docs/research/stack-url-research.md`

### Steps

- [ ] **Step 1: Research FastAPI/Pydantic URLs**

Create `docs/research/stack-url-research.md` with the following structure:

```markdown
# Stack URL Research

## FastAPI (target: 3-4 recipes)

### High-priority sources (static HTML confirmed)
1. https://fastapi.tiangolo.com/tutorial/handling-errors/
   - Covers: HTTPException, custom error handlers, request validation errors
   - Access: ✅ Static MkDocs, tested 2026-05-26
2. https://docs.pydantic.dev/latest/errors/validation_errors/
   - Covers: ValidationError structure, error types, debugging
   - Access: ✅ Static HTML, tested 2026-05-26
3. https://docs.pydantic.dev/latest/errors/errors/
   - Covers: Error handling patterns, custom validators
   - Access: ✅ Static HTML, tested 2026-05-26

### Additional candidates to test
- https://fastapi.tiangolo.com/tutorial/middleware/
- https://fastapi.tiangolo.com/advanced/custom-response/
- [Add more as discovered]

## LangChain/LangGraph (target: 3-4 recipes)

### High-priority sources (MDX docs)
- https://docs.langchain.com/llms-full.txt (comprehensive docs dump)
- https://python.langchain.com/docs/how_to/debugging/
- [Research specific error pages]

### Access concerns
- LangChain docs are MDX/React-based
- May need to test extraction quality
- Fallback: use GitHub raw markdown files

## Expo/React Native (target: 3-4 recipes)

### Candidates to research
- https://docs.expo.dev/troubleshooting/ (section pages)
- https://reactnative.dev/docs/troubleshooting
- https://docs.expo.dev/build-reference/troubleshooting/

### Access concerns
- Expo docs are Docusaurus-based
- Need to find specific error pages (not 404s)

## iOS/Swift (target: 3-4 recipes)

### Challenge: Apple developer docs are SPAs
- developer.apple.com uses heavy JavaScript rendering
- WebFetch timeout on test URLs

### Potential solutions
1. GitHub raw docs: https://github.com/apple/swift/tree/main/docs
2. Swift forums troubleshooting guides
3. Third-party iOS troubleshooting blogs (high-quality, maintained)

### Research needed
- [ ] Find static HTML or Markdown alternatives
- [ ] Check if Swift compiler error docs are in repo
- [ ] Look for community troubleshooting guides

## Android/Kotlin (target: 3-4 recipes)

### Challenge: Android developer docs are SPAs
- developer.android.com times out (likely SPA)
- Similar issue to iOS

### Potential solutions
1. GitHub raw docs: Android build tools repos
2. Kotlin official compiler error messages
3. Community Android troubleshooting guides

### Research needed
- [ ] Find static HTML alternatives
- [ ] Check Kotlin compiler docs accessibility
- [ ] Research third-party resources

## HarmonyOS/ArkTS (target: 3-4 recipes)

### Challenge: Limited public documentation
- HarmonyOS docs may be SPA-based
- ArkTS-specific troubleshooting sparse

### Potential solutions
1. OpenHarmony GitHub repos documentation
2. HarmonyOS developer forum guides
3. Community ArkTS troubleshooting

### Research needed
- [ ] Check OpenHarmony docs format
- [ ] Research ArkTS compiler error documentation
- [ ] Find maintained community resources

## Summary of accessibility

| Stack | Doc format | Accessibility | Action needed |
|-------|-----------|---------------|---------------|
| FastAPI | Static HTML | ✅ Easy | Add directly |
| Pydantic | Static HTML | ✅ Easy | Add directly |
| LangChain | MDX | ⚠️ Medium | Test extraction |
| Expo/RN | Docusaurus | ⚠️ Medium | Find specific pages |
| iOS | SPA | ❌ Hard | Research static alternatives |
| Android | SPA | ❌ Hard | Research static alternatives |
| HarmonyOS | Unknown | ❌ Hard | Research OpenHarmony docs |
```

- [ ] **Step 2: Test LangChain and Expo URL accessibility**

Run webfetch on candidate URLs for LangChain and Expo:

```bash
# Test LangChain
uv run python -c "
import httpx
urls = [
    'https://python.langchain.com/docs/how_to/debugging/',
    'https://python.langchain.com/docs/troubleshooting/errors/',
]
for url in urls:
    try:
        r = httpx.get(url, timeout=10, follow_redirects=True)
        print(f'{url}: {r.status_code}')
    except Exception as e:
        print(f'{url}: ERROR {e}')
"

# Test Expo
# [Add URLs as found]
```

- [ ] **Step 3: Research static alternatives for iOS/Android/HarmonyOS**

For each hard-tier stack, research at least 2-3 static alternatives:

**iOS:**
- Search for `site:github.com/apple/swift "error" OR "troubleshooting"`
- Check Swift compiler error message documentation
- Look for raywenderlich.com or similar tutorial troubleshooting guides

**Android:**
- Search for `site:github.com/nicokosi/gradle-samples "error"`
- Check Kotlin compiler error documentation
- Look for Android developer blog troubleshooting guides

**HarmonyOS:**
- Check OpenHarmony GitHub: `https://github.com/openharmony/docs`
- Search for ArkTS compiler error documentation
- Research community resources

- [ ] **Step 4: Update research document with findings**

Update `docs/research/stack-url-research.md` with:
- Tested URLs with access status (✅/❌/⚠️)
- Final selected URLs for each stack
- Notes on extraction quality (if tested)
- Fallback strategies for SPA-based stacks

- [ ] **Step 5: Commit research document**

```bash
git add docs/research/stack-url-research.md
git commit -m "docs(research): add stack URL research for recipe expansion

Research documentation accessibility for 6 target stacks:
- FastAPI/Pydantic: static HTML, fully accessible
- LangChain: MDX, needs extraction testing
- Expo/RN: Docusaurus, specific pages needed
- iOS/Android/HarmonyOS: SPAs, need static alternatives

Document selected URLs and fallback strategies."
```

---

## Task 2: Implement `list` Command

**Goal:** Add a CLI `list` subcommand that displays recipes grouped by stack with counts and status.

**Files:**
- Modify: `src/recipe_importer/cli.py`
- Modify: `src/recipe_importer/index.py`

### Steps

- [ ] **Step 1: Write failing test for list command**

Add to `tests/test_cli.py`:

```python
def test_list_command_shows_stacks(monkeypatch, capsys):
    """list command shows recipes grouped by stack."""
    from recipe_importer import cli

    with monkeypatch.context() as m:
        m.chdir(TEST_KB_DIR.parent)  # project root
        
        result = runner.invoke(cli.app, ['list'])
        assert result.exit_code == 0
        assert 'stack: react' in result.stdout.lower()
        assert 'react-hydration-mismatch' in result.stdout


def test_list_command_filters_by_stack(monkeypatch, capsys):
    """list --stack <name> shows only that stack."""
    from recipe_importer import cli

    with monkeypatch.context() as m:
        m.chdir(TEST_KB_DIR.parent)
        
        result = runner.invoke(cli.app, ['list', '--stack', 'react'])
        assert result.exit_code == 0
        assert 'react-hydration-mismatch' in result.stdout
        
        result = runner.invoke(cli.app, ['list', '--stack', 'nonexistent'])
        assert result.exit_code == 0
        assert 'no recipes found' in result.stdout.lower()
```

Run test:
```bash
uv run pytest tests/test_cli.py::test_list_command_shows_stacks -xvs
```

Expected: FAIL with error about missing `list` command.

- [ ] **Step 2: Implement stack aggregation in index.py**

Add to `src/recipe_importer/index.py`:

```python
def list_stacks(kb_paths: KbPaths, stack_filter: Optional[str] = None) -> dict[str, list[dict]]:
    """Group recipes by stack, optionally filtering by stack name.
    
    Returns:
        dict mapping stack names to lists of recipe summaries:
        {
            "react": [
                {"id": "react-hydration-mismatch", "status": "accepted", "stale": false},
                ...
            ],
            ...
        }
    """
    index = _read_index(kb_paths)
    stacked = defaultdict(list)
    
    for recipe in index.get("recipes", []):
        for stack in recipe.get("stack", []):
            stacked[stack].append({
                "id": recipe["id"],
                "status": recipe["status"],
                "stale": recipe["status"] == "stale",
            })
    
    # Sort recipes within each stack by ID
    for stack in stacked:
        stacked[stack].sort(key=lambda r: r["id"])
    
    # Apply filter if specified
    if stack_filter:
        stack_filter_lower = stack_filter.lower()
        stacked = {
            k: v for k, v in stacked.items()
            if k.lower() == stack_filter_lower
        }
    
    return dict(stacked)
```

Update imports in `index.py`:
```python
from collections import defaultdict
from typing import Optional
```

- [ ] **Step 3: Add list command to cli.py**

Add to `src/recipe_importer/cli.py`:

```python
@app.command()
def list(
    stack: Optional[str] = typer.Option(None, "--stack", "-s", help="Filter by stack name"),
):
    """List recipes grouped by stack."""
    from recipe_importer.index import list_stacks
    
    kb_paths = KbPaths()
    stacked = list_stacks(kb_paths, stack_filter=stack)
    
    if not stacked:
        if stack:
            typer.echo(f"No recipes found for stack: {stack}")
        else:
            typer.echo("No recipes found. Run 'recipe-importer index rebuild' first.")
        return
    
    for stack_name in sorted(stacked.keys()):
        recipes = stacked[stack_name]
        accepted = sum(1 for r in recipes if r["status"] == "accepted")
        stale = sum(1 for r in recipes if r["stale"])
        
        typer.echo(f"\nStack: {stack_name} ({len(recipes)} recipes, {accepted} accepted, {stale} stale)")
        typer.echo("-" * 60)
        for recipe in recipes:
            status_indicator = "✓" if recipe["status"] == "accepted" and not recipe["stale"] else "⚠"
            typer.echo(f"  {status_indicator} {recipe['id']}")
    
    typer.echo()
```

Update imports in `cli.py`:
```python
from typing import Optional
```

- [ ] **Step 4: Run tests and verify**

```bash
uv run pytest tests/test_cli.py::test_list_command_shows_stacks -xvs
uv run pytest tests/test_cli.py::test_list_command_filters_by_stack -xvs
```

Expected: PASS

- [ ] **Step 5: Manual smoke test**

```bash
uv run recipe-importer list
uv run recipe-importer list --stack react
uv run recipe-importer list --stack nonexistent
```

Expected output format:
```
Stack: react (5 recipes, 4 accepted, 1 stale)
------------------------------------------------------------
  ✓ react-effect-dependency-rerun-loop
  ✓ react-hydration-mismatch
  ⚠ react-invalid-hook-call
  ✓ react-state-reset-by-position-or-key
  ✓ react-use-effect-troubleshooting

Stack: nextjs (2 recipes, 2 accepted, 0 stale)
------------------------------------------------------------
  ✓ next-dynamic-server-error
  ✓ next-dynamic-server-suspense
```

- [ ] **Step 6: Commit list command implementation**

```bash
git add src/recipe_importer/cli.py src/recipe_importer/index.py tests/test_cli.py
git commit -m "feat(cli): add list command for stack-level recipe overview

Implement 'recipe-importer list' to display recipes grouped by stack,
showing counts of accepted and stale recipes. Use --stack to filter.

Example usage:
  recipe-importer list
  recipe-importer list --stack react

Provides quick overview for decision-making on recipe expansion and
maintenance priorities."
```

---

## Task 3: Add FastAPI Stack Sources

**Goal:** Add 3-4 FastAPI/Pydantic sources to `source-list.yml`, run fetch-extract-import pipeline, and publish recipes.

**Files:**
- Modify: `recipe-kb/sources/source-list.yml`
- Create: `recipe-kb/accepted/fastapi-*.md` (3-4 files)
- Create: `recipe-kb/accepted/pydantic-*.md` (1-2 files)

### Steps

- [ ] **Step 1: Add FastAPI sources to source-list.yml**

Edit `recipe-kb/sources/source-list.yml` and append:

```yaml
# === FastAPI Stack Expansion ===
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_error_doc
  stacks:
    - fastapi
  expected_failure_hints:
    - HTTPException
    - RequestValidationError
    - custom exception handler
    - 422 Unprocessable Entity
  refresh_policy: monthly

- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  source_type: official_error_doc
  stacks:
    - pydantic
    - fastapi
  expected_failure_hints:
    - ValidationError
    - validation error
    - field required
    - type error
    - value error
  refresh_policy: monthly

- source_id: pydantic-error-handling
  url: https://docs.pydantic.dev/latest/errors/errors/
  source_type: official_error_doc
  stacks:
    - pydantic
    - fastapi
  expected_failure_hints:
    - error handling
    - custom validation error
    - ValidationError attributes
    - error context
  refresh_policy: monthly

- source_id: fastapi-middleware
  url: https://fastapi.tiangolo.com/tutorial/middleware/
  source_type: official_doc
  stacks:
    - fastapi
  expected_failure_hints:
    - middleware error
    - CORS error
    - CORS middleware
    - middleware exception
  refresh_policy: monthly
```

- [ ] **Step 2: Fetch new sources**

```bash
uv run recipe-importer fetch recipe-kb/sources/source-list.yml
```

Expected: Downloads 4 new HTML files to `recipe-kb/snapshots/fastapi-*` and `recipe-kb/snapshots/pydantic-*`.

- [ ] **Step 3: Extract sections for each source**

```bash
for snapshot in fastapi-handling-errors pydantic-validation-errors pydantic-error-handling fastapi-middleware; do
  echo "=== Extracting $snapshot ==="
  uv run recipe-importer extract recipe-kb/snapshots/$snapshot
  echo
done
```

Expected: Each extraction creates `sections.json` and `qa.json` in the snapshot directory.

- [ ] **Step 4: Import recipes**

```bash
for snapshot in fastapi-handling-errors pydantic-validation-errors pydantic-error-handling fastapi-middleware; do
  echo "=== Importing from $snapshot ==="
  uv run recipe-importer import-source recipe-kb/snapshots/$snapshot
  echo
done
```

Expected: Each import creates proposed recipe files in `recipe-kb/proposed/`.

- [ ] **Step 5: Review and accept recipes**

```bash
# List proposed recipes
ls recipe-kb/proposed/fastapi-* recipe-kb/proposed/pydantic-*

# For each proposed recipe, review and accept
for recipe in recipe-kb/proposed/fastapi-* recipe-kb/proposed/pydantic-*; do
  echo "=== Reviewing $recipe ==="
  
  # Show the recipe
  cat "$recipe"
  
  # Accept if quality is good
  read -p "Accept? (y/n): " accept
  if [ "$accept" = "y" ]; then
    uv run recipe-importer publish "$recipe"
  fi
done
```

Expected: Published recipes move to `recipe-kb/accepted/`.

- [ ] **Step 6: Rebuild index and verify**

```bash
uv run recipe-importer index rebuild
uv run recipe-importer list --stack fastapi
uv run recipe-importer list --stack pydantic
```

Expected: Shows 3-5 recipes for fastapi stack, 2-3 for pydantic.

- [ ] **Step 7: Test search functionality**

```bash
uv run recipe-importer search "validation error"
uv run recipe-importer search "HTTPException"
uv run recipe-importer search "middleware CORS"
```

Expected: Returns relevant FastAPI/Pydantic recipes.

- [ ] **Step 8: Commit FastAPI stack recipes**

```bash
git add recipe-kb/sources/source-list.yml
git add recipe-kb/snapshots/fastapi-* recipe-kb/snapshots/pydantic-*
git add recipe-kb/accepted/fastapi-* recipe-kb/accepted/pydantic-*
git add recipe-kb/index.json

git commit -m "feat(recipes): add FastAPI/Pydantic stack recipes

Add 3-5 debug recipes for FastAPI and Pydantic frameworks:
- HTTPException and custom error handlers
- ValidationError handling and debugging
- Middleware and CORS troubleshooting

Sources validated as static HTML (MkDocs), fully accessible.
Total recipes: $(ls recipe-kb/accepted/*.md | wc -l)"
```

---

## Task 4: Add LangChain Stack Sources

**Goal:** Add 3-4 LangChain/LangGraph sources and publish recipes.

**Files:**
- Modify: `recipe-kb/sources/source-list.yml`
- Create: `recipe-kb/accepted/langchain-*.md` (3-4 files)

### Steps

- [ ] **Step 1: Research and validate LangChain URLs**

Based on Task 1 research, select 3-4 accessible LangChain URLs. Example candidates:

```yaml
- source_id: langchain-debugging
  url: https://python.langchain.com/docs/how_to/debugging/
  source_type: official_doc
  stacks:
    - langchain
  expected_failure_hints:
    - debug agent
    - trace execution
    - langsmith
    - callback
  refresh_policy: monthly

- source_id: langchain-agents-troubleshooting
  url: https://python.langchain.com/docs/troubleshooting/errors/
  source_type: official_error_doc
  stacks:
    - langchain
  expected_failure_hints:
    - agent error
    - tool error
    - chain error
    - output parsing error
  refresh_policy: monthly
```

**Note:** Test these URLs with webfetch first. If MDX extraction fails, try:
- GitHub raw markdown: `https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/docs/...`
- Alternative: `https://docs.langchain.com/llms.txt` overview page

- [ ] **Step 2: Add LangChain sources and run pipeline**

```bash
# Add sources to source-list.yml (from Step 1)

uv run recipe-importer fetch recipe-kb/sources/source-list.yml

for snapshot in langchain-debugging langchain-agents-troubleshooting [add more]; do
  uv run recipe-importer extract recipe-kb/snapshots/$snapshot
  uv run recipe-importer import-source recipe-kb/snapshots/$snapshot
done
```

- [ ] **Step 3: Review, accept, and rebuild index**

```bash
for recipe in recipe-kb/proposed/langchain-*; do
  cat "$recipe"
  # Review and accept if good
  uv run recipe-importer publish "$recipe"
done

uv run recipe-importer index rebuild
uv run recipe-importer list --stack langchain
```

- [ ] **Step 4: Commit LangChain recipes**

```bash
git add recipe-kb/sources/source-list.yml
git add recipe-kb/snapshots/langchain-*
git add recipe-kb/accepted/langchain-*
git add recipe-kb/index.json

git commit -m "feat(recipes): add LangChain/LangGraph stack recipes

Add 3-4 debug recipes for LangChain agent development:
- Agent debugging and tracing
- Tool and chain error handling
- Output parsing troubleshooting

Sources: LangChain MDX documentation (tested extraction quality)."
```

---

## Task 5: Add Expo/React Native Stack Sources

**Goal:** Add 3-4 Expo/React Native sources and publish recipes.

**Files:**
- Modify: `recipe-kb/sources/source-list.yml`
- Create: `recipe-kb/accepted/expo-*.md` or `react-native-*.md` (3-4 files)

### Steps

- [ ] **Step 1: Research Expo/RN documentation URLs**

Test these URLs with webfetch:
- `https://docs.expo.dev/troubleshooting/` section pages
- `https://reactnative.dev/docs/troubleshooting`
- `https://docs.expo.dev/build-reference/troubleshooting/`

Select 3-4 accessible URLs. If Docusaurus extraction fails, try:
- GitHub: `https://github.com/expo/expo/tree/main/docs/pages`
- Alternative: React Native GitHub wiki

- [ ] **Step 2: Add sources and run pipeline**

```bash
# Add to source-list.yml
# Example:
- source_id: expo-build-troubleshooting
  url: https://docs.expo.dev/build-reference/troubleshooting/
  source_type: official_error_doc
  stacks:
    - expo
    - react-native
  expected_failure_hints:
    - build error
    - eas build
    - prebuild error
    - native module
  refresh_policy: monthly

uv run recipe-importer fetch recipe-kb/sources/source-list.yml

for snapshot in expo-build-troubleshooting [add more]; do
  uv run recipe-importer extract recipe-kb/snapshots/$snapshot
  uv run recipe-importer import-source recipe-kb/snapshots/$snapshot
done
```

- [ ] **Step 3: Review, accept, commit**

```bash
for recipe in recipe-kb/proposed/expo-* recipe-kb/proposed/react-native-*; do
  cat "$recipe"
  uv run recipe-importer publish "$recipe"
done

uv run recipe-importer index rebuild

git add -A
git commit -m "feat(recipes): add Expo/React Native stack recipes

Add 3-4 debug recipes for mobile app development:
- EAS build troubleshooting
- Native module linking errors
- Prebuild and configuration issues

Sources: Expo Docusaurus documentation (tested extraction)."
```

---

## Task 6: Research Static Alternatives for iOS Stack

**Goal:** Find 3-4 static-HTML alternatives for iOS/Swift documentation (since Apple developer docs are SPAs).

**Files:**
- Modify: `docs/research/stack-url-research.md`

### Steps

- [ ] **Step 1: Research Swift compiler error documentation**

Search for:
```
site:github.com/apple/swift "error" OR "Diagnostic"
```

Check these potential sources:
- Swift compiler diagnostic messages in GitHub repo
- Swift forums troubleshooting guides
- Third-party iOS troubleshooting sites (e.g., raywenderlich.com, hackingwithswift.com)

Test each with webfetch.

- [ ] **Step 2: Research Xcode build error alternatives**

Look for:
- Xcode build error documentation in Markdown format
- Common Xcode errors and solutions in static HTML
- Community-maintained troubleshooting guides

- [ ] **Step 3: Document findings**

Update `docs/research/stack-url-research.md`:

```markdown
## iOS/Swift Static Alternatives Found

### Source 1: [URL]
- Format: [GitHub markdown / static HTML]
- Coverage: [what errors/problems covered]
- Quality: [high/medium/low]
- Access: ✅/⚠️/❌

### Source 2: [URL]
- ...

### Recommendation
[Which sources to use for recipe expansion]
```

- [ ] **Step 4: If 3+ valid sources found, add to source-list.yml**

If successful, add sources and run pipeline (similar to Task 3/4/5).

If insufficient static sources found, document this as a deferred stack:

```markdown
## Deferred: iOS/Swift

**Reason:** Apple developer documentation is SPA-based, no accessible static alternatives found.

**Future work:**
- Wait for Playwright support in recipe-importer pipeline
- Alternatively: manually download Apple docs pages and place in `recipe-kb/manual/`
- Or: partner with community maintainers for static guides
```

- [ ] **Step 5: Commit research findings**

```bash
git add docs/research/stack-url-research.md
git commit -m "docs(research): document iOS static alternatives

[Summarize findings: found X sources / deferred due to SPA limitation]"
```

---

## Task 7: Research Static Alternatives for Android and HarmonyOS

**Goal:** Find static-HTML alternatives for Android and HarmonyOS documentation.

**Files:**
- Modify: `docs/research/stack-url-research.md`

### Steps

- [ ] **Step 1: Research Android static alternatives**

Similar to Task 6, search for:
- Gradle build error documentation in GitHub repos
- Kotlin compiler error messages
- Android troubleshooting blogs with static HTML

- [ ] **Step 2: Research HarmonyOS/ArkTS alternatives**

Check:
- OpenHarmony GitHub documentation: `https://github.com/openharmony/docs`
- ArkTS compiler error documentation
- Community HarmonyOS development guides

- [ ] **Step 3: Document and decide**

Update research document. For each stack:
- If 3+ valid static sources: plan to add in Task 8/9
- If insufficient: mark as deferred

- [ ] **Step 4: Commit findings**

```bash
git add docs/research/stack-url-research.md
git commit -m "docs(research): document Android/HarmonyOS alternatives

[Summarize findings for both stacks]"
```

---

## Task 8: Add Android Stack (if static sources found in Task 7)

**Goal:** Add 3-4 Android sources and publish recipes.

**Condition:** Only proceed if Task 7 found 3+ accessible static sources.

**Files:**
- Modify: `recipe-kb/sources/source-list.yml`
- Create: `recipe-kb/accepted/android-*.md` (3-4 files)

### Steps

- [ ] **Step 1: Add Android sources to source-list.yml**

Use the URLs researched in Task 7. Example:

```yaml
- source_id: android-gradle-sync-errors
  url: [URL from Task 7 research]
  source_type: official_error_doc
  stacks:
    - android
    - gradle
  expected_failure_hints:
    - gradle sync error
    - dependency resolution
    - build script error
  refresh_policy: monthly
```

- [ ] **Step 2: Run fetch-extract-import pipeline**

```bash
uv run recipe-importer fetch recipe-kb/sources/source-list.yml

for snapshot in android-gradle-sync-errors [add more]; do
  uv run recipe-importer extract recipe-kb/snapshots/$snapshot
  uv run recipe-importer import-source recipe-kb/snapshots/$snapshot
done
```

- [ ] **Step 3: Review, accept, rebuild index, commit**

Same pattern as previous stack tasks.

---

## Task 9: Add HarmonyOS Stack (if static sources found in Task 7)

**Goal:** Add 3-4 HarmonyOS/ArkTS sources and publish recipes.

**Condition:** Only proceed if Task 7 found 3+ accessible static sources.

**Files:**
- Modify: `recipe-kb/sources/source-list.yml`
- Create: `recipe-kb/accepted/harmonyos-*.md` or `arkts-*.md` (3-4 files)

### Steps

- [ ] **Step 1: Add HarmonyOS sources to source-list.yml**

Use URLs from Task 7 research.

- [ ] **Step 2: Run pipeline**

Same pattern as previous stack tasks.

- [ ] **Step 3: Review, accept, rebuild index, commit**

---

## Task 10: Final Verification and Documentation

**Goal:** Verify all recipes are accessible, create summary report, and plan future work.

**Files:**
- Create: `docs/research/recipe-expansion-summary.md`

### Steps

- [ ] **Step 1: Run refresh command to verify all recipes**

```bash
uv run recipe-importer refresh
uv run recipe-importer list
```

Expected: All stacks listed, recipes in accepted/stale state.

- [ ] **Step 2: Calculate recipes per stack**

```bash
uv run recipe-importer list | grep "Stack:" | sed 's/Stack: //' | sort
```

Expected output:
```
android (3 recipes, 3 accepted, 0 stale)
expo (4 recipes, 4 accepted, 0 stale)
fastapi (4 recipes, 4 accepted, 0 stale)
harmonyos (3 recipes, 3 accepted, 0 stale)
langchain (3 recipes, 3 accepted, 0 stale)
pydantic (2 recipes, 2 accepted, 0 stale)
react (5 recipes, 4 accepted, 1 stale)
```

- [ ] **Step 3: Create summary report**

Create `docs/research/recipe-expansion-summary.md`:

```markdown
# Recipe Expansion Summary Report

**Date:** 2026-05-26
**Initial recipe count:** 9 recipes (6 frameworks)
**Final recipe count:** [X] recipes ([Y] frameworks)

## Stacks successfully added

### FastAPI (static HTML, MkDocs)
- Recipes added: [count]
- Sources: [count] official documentation pages
- Accessibility: ✅ Fully accessible static HTML
- Quality: High

### Pydantic (static HTML)
- Recipes added: [count]
- Sources: [count] official error/troubleshooting pages
- Accessibility: ✅ Fully accessible
- Quality: High

### LangChain (MDX docs)
- Recipes added: [count]
- Sources: [count] pages
- Accessibility: ⚠️ MDX extraction required manual URL selection
- Quality: Medium-High

### Expo/React Native (Docusaurus)
- Recipes added: [count]
- Sources: [count] pages
- Accessibility: ⚠️ Docusaurus extraction required specific URLs
- Quality: Medium

## Stacks requiring SPA support (deferred)

### iOS/Swift
- **Status:** Deferred
- **Reason:** Apple developer documentation is SPA-based
- **Alternative sources found:** [X] (insufficient for comprehensive coverage)
- **Future work:** Wait for Playwright support

### Android (partial success)
- **Recipes added:** [count] (from static alternatives)
- **Official docs status:** SPA-based, inaccessible
- **Note:** Used community guides and GitHub documentation instead

### HarmonyOS/ArkTS
- **Recipes added:** [count]
- **Sources:** OpenHarmony GitHub docs
- **Quality:** [High/Medium/Low]

## Recommendations

### Immediate
1. [e.g., Add more FastAPI recipes for middleware patterns]
2. [e.g., Expand LangChain recipes for memory management]

### Short-term (next quarter)
1. Implement Playwright-based extraction for SPA documentation
2. Add automated quality scoring for recipes
3. Expand Expo recipes for native module troubleshooting

### Long-term
1. Partner with framework maintainers for recipe quality feedback
2. Community contributions for underrepresented stacks
3. Internationalization (recipes in multiple languages)

## Lessons learned

1. **Static HTML is critical:** Stacks with MkDocs/Docusaurus/GitHub markdown were easy to process. SPA-based docs (Apple, Google) required workarounds.

2. **URL research upfront saves time:** Spending 2-3 hours on URL research prevented failed pipeline runs later.

3. **Community guides fill gaps:** When official docs were inaccessible, high-quality community tutorials provided useful troubleshooting content.

4. **Manual review matters:** Generated recipes required human review to ensure first_checks were actionable and do_not patterns were relevant.
```

- [ ] **Step 4: Commit summary report**

```bash
git add docs/research/recipe-expansion-summary.md
git commit -m "docs(research): add recipe expansion summary report

Document results of 6-stack expansion effort:
- Successfully added: FastAPI, Pydantic, LangChain, Expo/RN
- Partially added: Android (static alternatives)
- Deferred: iOS/Swift (SPA limitation)

Final recipe count: [X] recipes across [Y] frameworks

Include recommendations for future expansion and lessons learned
about documentation accessibility."
```

---

## Appendix: Quality Checklist for Recipe Review

Use this checklist when reviewing proposed recipes (Task 3, 4, 5, 8, 9):

### First Checks
- [ ] Are the first_checks specific and actionable? (e.g., "Check X in file Y" not "Check for errors")
- [ ] Do first_checks follow logical debugging order?
- [ ] Are checks framed as questions to answer, not solutions to apply?

### Do Not Patterns
- [ ] Are do_not entries common mistakes (not obvious ones)?
- [ ] Do do_not entries explain why the pattern is harmful?
- [ ] Are do_not entries specific to the error being addressed?

### Fingerprint
- [ ] Is the fingerprint specific enough to match this error uniquely?
- [ ] Does fingerprint include actual error message text?
- [ ] Would a developer searching for this error find this recipe?

### Validation Ladder
- [ ] Are validation steps executable? (not vague)
- [ ] Do validation steps increase in effort?
- [ ] Is the first validation step quick (< 1 minute)?

### Evidence
- [ ] Are evidence_refs pointing to specific sections of source docs?
- [ ] Is quote text accurate (copied from source, not paraphrased)?
- [ ] Are evidence sources authoritative (official docs, not random blogs)?

### Quality
- [ ] No code comments in recipe YAML (recipe-importer convention)
- [ ] Recipe ID follows naming convention: `{stack}-{problem-type}`
- [ ] Summary is clear and includes stack name
