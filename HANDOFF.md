# Debug Recipe Importer Handoff

## Context

This project builds a long-lived, semi-automated importer for acquiring, normalizing, reviewing, publishing, and maintaining agent-facing debug recipes.

The importer is not a one-off crawler and not a replacement coding harness. It is a recipe supply-chain tool that works around existing harnesses such as Codex, Claude Code, OpenCode, Cursor, and similar tools.

The first MVP is debug-only. Build recipes and project scaffolds are intentionally deferred.

## Background Sources

These prior discussions are useful background for future agents working on this project:

- [Enhancing agent engineering capability](https://chatgpt.com/share/6a0c034d-45c0-832e-8746-dee736fc4a56): establishes the broader idea of an engineering substrate, recipe/playbook knowledge, decision capture, human review, and promotion from observed knowledge to accepted rules.
- [LLM coding capability and recipe/debug recipe discussion](https://chatgpt.com/share/6a0cf582-1644-832c-8808-4903254cf6de): narrows the focus to build recipe vs debug recipe, public-stack recipe sources, the lack of complete stack-specific debug recipe registries, and the semi-automated importer concept.

## Product Goal

Create a tool that continuously turns high-quality public engineering knowledge into reviewed, structured debug recipes that agents can retrieve during bugfix/debug loops.

The tool should help agents:

- classify a failure before patching
- inspect the right evidence first
- avoid common wrong fixes
- keep fix scope small
- validate the fix with the shortest useful check
- avoid repeating stale or outdated framework knowledge

The long-term value is not "more documentation". The value is a maintained, auditable, version-aware recipe registry for agentic coding.

## Current Core Decision

The importer should be **CLI-first, LLM-inside, MCP/skill-as-adapters**.

Meaning:

- Core importer logic lives in a well-packaged CLI/batch tool.
- The CLI may call an LLM internally for structured extraction.
- LLM output must be schema-validated and source-grounded.
- MCP servers and skills are thin adapters, not the core implementation.
- Agents call the importer or query accepted recipes through MCP/skills, but they do not manually perform the import workflow in conversation.

Rationale:

- Import needs repeatability, audit logs, source hashes, scheduled refresh, and tests.
- A pure skill/MCP implementation would be too tied to one harness and hard to batch or maintain.
- A standalone CLI can run locally, in CI, from cron, or under an agent.
- A thin MCP/skill layer keeps the system portable across harnesses.

## Non-Goals For MVP

- Do not build a full harness.
- Do not build a general web crawler.
- Do not import build/project scaffold recipes yet.
- Do not auto-accept recipes into the registry.
- Do not rely on vector search as the first retrieval mechanism.
- Do not scrape low-quality blogs or broad StackOverflow by default.
- Do not let agents write final accepted recipes without human review.

## MVP Scope

First version imports debug recipes from curated, high-signal sources:

- official error documentation
- official troubleshooting documentation
- official framework common-errors pages
- official testing/debugging guides
- selected framework-maintained templates only when they provide validation patterns

Initial target stacks:

- React / Next.js
- FastAPI / Pydantic / SQLAlchemy
- LangGraph / LangChain
- Expo / React Native
- Scrapy / Playwright

The first useful target is 20-30 high-frequency debug recipes, not broad coverage.

## Recipe Types

### Build Recipe

Deferred for MVP.

Build recipes prevent errors during project creation and feature construction. They answer:

- what stack defaults to use
- which choices not to re-evaluate
- which scaffold to start from
- which boundaries and validation commands apply

Build recipe structure:

```text
Defaults
Do Not
Scaffold
Capabilities
Stack/Profile
Validation
Known failures
```

### Debug Recipe

MVP target.

Debug recipes guide convergence after code already exists and something fails. They answer:

- what failure class this is
- what evidence to inspect first
- what not to patch first
- what minimal fix scope is acceptable
- how to verify the fix
- what regression guard is required

Debug recipe structure:

```text
Failure Class
Symptoms
Fingerprints
First Checks
Do Not Patch Yet
Evidence Needed
Minimal Fix Scope
Validation Ladder
Regression Guard
Sources
Maintenance Metadata
```

### Conformance Recipe

Later bridge between build and debug.

Conformance recipes check whether the current code has drifted away from the original golden path. For example:

- multiple API clients
- service layer bypassed
- duplicate auth/session entry points
- frontend code holding backend business logic
- second state-management library introduced

Conformance recipes are not in the first MVP, but the schema should not block them.

## Candidate Schema

Importer output should start as a proposed candidate.

Example:

```yaml
id: react-hydration-mismatch
kind: debug-recipe
status: proposed
stack:
  - react
  - nextjs
failure_class: render/hydration
symptoms:
  - "Hydration failed"
fingerprints:
  - "server rendered HTML didn't match the client"
first_checks:
  - "Check Date.now(), Math.random(), and locale formatting in render output"
  - "Check typeof window branches and browser-only APIs"
  - "Check invalid HTML nesting"
do_not:
  - "Do not disable SSR as the first fix"
  - "Do not rewrite the whole component tree first"
minimal_fix_scope:
  - "The component producing mismatched markup"
  - "The server-to-client data snapshot"
validate:
  - "Reproduce the page in dev"
  - "Check browser console for hydration warning"
  - "Run the related Playwright smoke test if present"
sources:
  - url: "https://react.dev/errors/418"
    source_type: official_error_doc
    captured_at: "2026-05-20"
    source_hash: "<hash>"
review:
  state: pending
maintenance:
  last_verified: null
  stale_if_source_changed: true
  stale_if_major_version_changed: true
  recrawl: monthly
```

## Source Quality Policy

Preferred MVP sources:

```text
official troubleshooting / error docs
official common-errors docs
official AI agent docs
official starter validation scripts
```

Secondary sources, after MVP:

```text
community skills / rules
AGENTS.md / CLAUDE.md / Cursor rules from reputable repos
high-quality GitHub issues and merged PRs
starter template CI and test patterns
```

Avoid by default:

```text
random blogs
unmerged issue comments without maintainer confirmation
StackOverflow answers without version context
old framework docs for active stacks
```

## Import Pipeline

```text
source URL list
  -> fetch source
  -> create source snapshot and hash
  -> extract readable text/sections
  -> split into candidate failure entries
  -> call LLM for structured extraction
  -> validate JSON schema
  -> normalize stack tags and failure class
  -> deduplicate against existing candidates/accepted recipes
  -> write proposed recipe candidate
  -> human review
  -> publish accepted recipe
  -> refresh and stale detection
```

The importer must preserve evidence at every step:

- source URL
- captured timestamp
- content hash
- extracted text span or section reference
- LLM prompt version
- LLM model/provider
- schema version
- reviewer decision

## CLI Shape

Preferred initial command shape:

```text
bin/recipe-importer fetch <source-list.yml>
bin/recipe-importer extract <snapshot-id>
bin/recipe-importer normalize <candidate-id>
bin/recipe-importer review-queue
bin/recipe-importer publish <candidate-id>
bin/recipe-importer refresh
bin/recipe-importer search <query-or-fingerprint>
```

Possible combined MVP shortcut:

```text
bin/recipe-importer import <source-list.yml>
```

The shortcut should still persist intermediate artifacts.

## Repository Layout Proposal

```text
bin/
  recipe-importer

src/
  recipe_importer/
    cli.py
    fetch.py
    extract.py
    normalize.py
    schema.py
    review.py
    publish.py
    refresh.py
    llm.py

recipe-kb/
  sources/
    source-list.yml
  snapshots/
  proposed/
  accepted/
  rejected/
  stale/
  index.json

schemas/
  debug-recipe.schema.json
  source.schema.json
  review.schema.json

agent-adapters/
  skills/
  mcp/
```

## Human Review Workflow

Human review is required before a recipe becomes accepted.

Allowed review decisions:

```text
accept
reject
narrow_scope
merge_existing
needs_more_evidence
convert_to_generic_debug_skill
convert_to_validation_recipe
mark_stale
deprecate
```

Reviewer should inspect:

- source credibility
- framework version fit
- whether fingerprint is specific enough
- whether first checks are actionable
- whether do_not entries prevent real bad fixes
- whether validation is executable
- whether the candidate duplicates existing accepted recipes
- whether scope is too broad

Agents may generate candidates, but they may not approve candidates.

## Maintenance Model

Recipes expire. Maintenance is a first-class feature.

Each accepted recipe should track:

- source URLs
- source hash
- captured_at
- last_verified
- relevant framework versions
- stale policy
- review history
- usage feedback if available

Stale triggers:

- source content hash changed
- source page removed
- framework major version changed
- validation command no longer works
- accepted recipe repeatedly fails during agent use
- reviewer marks source as superseded

Stale does not mean deletion. It means the recipe needs re-review.

## Agent Retrieval Model

The importer produces the registry. Agents consume accepted recipes through a thin retrieval layer.

Retrieval keys:

- exact error text
- failure fingerprint
- stack tags
- file path hints
- package/version hints
- command/test failure category

First retrieval implementation should be simple:

- normalized keyword/fingerprint matching
- stack tag filter
- failure class filter
- top 1-3 accepted recipes

Do not start with broad semantic retrieval. Add embeddings later only if deterministic matching is insufficient.

## Thin MCP / Skill Adapters

MCP/skills are integration surfaces, not the core importer.

MCP can expose:

```text
recipe_search
recipe_get
recipe_import_source
recipe_status
recipe_mark_feedback
```

Skill can tell an agent:

- when to search for debug recipes
- how to use returned recipes
- when to stop patching and gather evidence
- how to feed failed recipe usage back into the registry

The skill should not contain large stack-specific recipe content. It should route to the registry.

## LLM Use Policy

LLM calls are allowed only in controlled extraction/normalization steps.

Requirements:

- prompt version must be recorded
- model/provider must be recorded
- output must be JSON and schema-validated
- output must cite source spans or section references
- hallucinated fields must fail validation or go to needs_review
- no accepted recipe may be created directly from LLM output

The LLM should not decide final status.

## First MVP Task List

1. Create project skeleton and schemas.
2. Implement source list format.
3. Implement fetch and snapshot hashing for static docs pages.
4. Implement text extraction for HTML pages.
5. Implement debug recipe JSON schema validation.
6. Implement LLM extraction for one source type.
7. Generate proposed recipe files.
8. Implement file-based review queue.
9. Implement publish from proposed to accepted.
10. Implement simple search by fingerprint/tag.
11. Add refresh that detects source hash changes and marks stale.
12. Seed 3-5 React/Next.js debug recipes from official docs.

## Recommended First Vertical Slice

Use React hydration mismatch as the first end-to-end slice.

Why:

- official source exists
- error fingerprint is clear
- first checks are concrete
- bad fixes are common
- validation steps are understandable

Target outcome:

```text
source-list.yml contains React hydration source
importer fetches and snapshots source
extract produces react-hydration-mismatch proposed recipe
review accepts it
publish writes accepted recipe
search "Hydration failed" returns the accepted recipe
refresh marks it stale if source hash changes
```

## Important Design Principle

The system should not optimize for producing many recipes quickly. It should optimize for producing recipes that agents can safely rely on during debugging.

High-value recipe traits:

- narrow scope
- precise fingerprint
- short first-check list
- clear do-not entries
- minimal fix scope
- executable validation
- source-backed
- version-aware
- reviewable by a human

## Open Questions

- Which language/runtime should be used for the CLI: Python is currently the natural default, but Bash entrypoint is required.
- Which LLM provider should be used first for extraction.
- Whether source snapshots should be stored as files only or also indexed in SQLite.
- Whether accepted recipes should be one YAML file or Markdown with YAML frontmatter.
- How much local project-specific adaptation belongs in this importer versus a separate project-local KB.

## Current Recommendation On Open Questions

- Use Python for implementation with a Bash entrypoint.
- Store source snapshots and recipe files on disk first.
- Use YAML frontmatter plus Markdown body for human review.
- Keep an `index.json` for fast deterministic lookup.
- Keep project-local adaptation separate from public-stack debug recipes.
