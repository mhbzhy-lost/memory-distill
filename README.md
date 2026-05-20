# Recipe Importer

CLI-first importer for reviewed, source-grounded debug recipes.

The MVP imports official troubleshooting/error documentation into a local
file-based recipe knowledge base. Accepted recipes are reviewed before agent
consumption.

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
`fetch` or source refresh operations.

## Agent Skill Package

Build a self-contained Codex skill for agent use:

```bash
uv run python scripts/build_agent_skill.py --force
dist/skills/debug-recipe-importer/scripts/recipe-importer search "Hydration failed"
```

The generated skill bundles the importer CLI, schemas, prompts, accepted recipes,
and local source-evidence snapshots. It does not package raw HTML snapshots.
