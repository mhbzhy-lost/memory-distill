---
name: debug-recipe-lookup
description: Use when encountering framework errors, debug symptoms, hydration warnings, hook misuse, Next.js server errors, TanStack Query cache issues, Vite ESM errors, React effect loops, or state reset bugs. Queries the local debug recipe knowledge base for first-check guidance before patching code. Triggers on error messages, stack traces, and failure fingerprints from React, Next.js, Vite, TanStack Query.
---

# Debug Recipe Lookup

When an error message, stack trace, or failure symptom matches a known framework
pattern, **query the recipe knowledge base before changing code**. The recipes
encode the shortest path to a correct fix, common wrong fixes to avoid, and the
minimum validation needed — all sourced from official framework docs and reviewed
by a human.

## When to Use

- A framework error message appears (React, Next.js, Vite, TanStack Query).
- A bug or test failure points to a framework behavior (hydration, hooks, effects,
  query cache, ESM config).
- A build or dev error mentions a known stack fingerprint.
- A user describes a common framework symptom in natural language.

Do not use this skill for build recipes, conformance recipes, or project scaffold
questions — those are a separate category that this skill does not cover.

## How to Search

Run the search from the memory-distill repo root:

```bash
uv run recipe-importer search "<error text or symptom keyword>"
```

Pass the actual error text, fingerprint phrase, or symptom keyword. Examples:

- `uv run recipe-importer search "Hydration failed"`
- `uv run recipe-importer search "Invalid hook call"`
- `uv run recipe-importer search "Effect keeps re-running"`
- `uv run recipe-importer search "ERR_REQUIRE_ESM"`
- `uv run recipe-importer search "DynamicServerError"`
- `uv run recipe-importer search "invalidateQueries stale data"`

The command returns up to 3 matching recipes. Each recipe shows:

- `id`: recipe identifier (use with `get` for the full recipe).
- `summary`: one-line description of the failure.
- `check`: first-check actions (execute in order, before patching).
- `do-not`: wrong fixes to avoid (treat each as a hard constraint).
- `validate`: validation ladder (execute after the fix, in order).
- `[stale]` marker in the id line: recipe may be outdated.

To exclude stale recipes, add `--fresh-only`:

```bash
uv run recipe-importer search "<query>" --fresh-only
```

## How to Inspect a Full Recipe

When a search hit looks relevant, fetch the full JSON:

```bash
uv run recipe-importer get <recipe-id>
```

The full recipe adds fields the summary omits: `evidence_needed`,
`minimal_fix_scope`, `regression_guard`, `evidence_refs`, and
`maintenance.state`. These are important when deciding whether to follow the
recipe's guidance.

## How to Apply a Recipe

In this order:

1. Run each `first_checks` entry before changing any code. These are diagnostic,
   not fixes.
2. Treat each `do_not` entry as a hard constraint — even if the prohibited action
   looks obvious. Recipes encode common wrong fixes that look right but make
   things worse.
3. Keep changes inside `minimal_fix_scope`. Expanding scope is usually a sign the
   root cause has not been isolated yet.
4. Run each `validation_ladder` step in order after the fix. Skip to the next
   step only when the current one passes.
5. Add the suggested `regression_guard` test if one covering the same path does
   not already exist.

Only deviate from a recipe after first-checks fail and you have exhausted the
recipe's guidance. When deviating, document why the recipe did not apply so the
knowledge base can be updated.

## Handling Stale Recipes

A `[stale]` marker means the source evidence (official framework doc) changed since
the recipe was last reviewed. Treat stale recipes as advisory, not authoritative —
cross-check against the current official docs before relying on a stale recipe's
`first_checks` or `do_not` list.

The `maintenance.stale_reason` field in the full recipe indicates why it was
marked stale: `source_removed`, `final_url_changed`, `section_anchor_gone`, or
`source_quote_hash_changed`. Use that to decide how much to trust the recipe.

## If No Recipe Matches

If the search returns no results, the knowledge base has no reviewed entry for this
symptom. Fall back to your normal debugging workflow: gather full evidence,
reproduce the failure, and investigate the source directly. Do not invent a
recipe or pretend a loosely matches applies.

If this happens to be in a stack the knowledge base should cover (React, Next.js,
Vite, TanStack Query), note the missing coverage as potential feedback to the
recipe importer workflow.

## Working Directory

All `recipe-importer` commands must run from the memory-distill repo root. When
working in another repo, this skill is not available — that is expected, the
recipes here are scoped to this knowledge base.
