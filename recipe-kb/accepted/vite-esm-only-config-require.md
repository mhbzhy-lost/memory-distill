---
id: vite-esm-only-config-require
kind: debug-recipe
status: accepted
stack:
- react
- vite
failure_class: vite/config-module-format
symptoms:
- Vite fails because an ESM-only package was loaded by require
fingerprints:
- This package is ESM only
- ERR_REQUIRE_ESM
- tried to load by require
- vite config ESM
first_checks:
- Check whether vite.config.* or a plugin config is loaded as CommonJS
- Check whether the failing dependency is ESM-only
- Check whether the config file extension should be .mjs or .mts
do_not:
- Do not pin an old dependency version before confirming the config module format
- Do not rely on experimental require support as the primary fix
evidence_needed:
- Capture the ERR_REQUIRE_ESM stack and the dependency path
- Identify the Vite config filename and package type
- Confirm how the dependency is imported from config
minimal_fix_scope:
- The Vite config module format or import statement
- The plugin/dependency entry loaded from config
validation_ladder:
- Run the Vite command that originally failed
- Confirm the config loads under ESM
- Run the project build or dev-server smoke
regression_guard:
- Add a config-load smoke test or CI build check
evidence_refs:
- source_id: vite-troubleshooting
  url: https://vite.dev/guide/troubleshooting.html
  final_url: https://vite.dev/guide/troubleshooting.html
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: vite-troubleshooting-11
  short_excerpt: This package is ESM only ​
  quote_hash: sha256:b76968f58cbe7416410326b93f9e4b1b019aabe5e742a34b2329b75470f0419b
- source_id: vite-troubleshooting
  url: https://vite.dev/guide/troubleshooting.html
  final_url: https://vite.dev/guide/troubleshooting.html
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: vite-troubleshooting-13
  short_excerpt: Failed to resolve "foo". This package is ESM only but it was tried
    to load by require .
  quote_hash: sha256:4cc486e25ba24557a3523c7f9df4f40273d02256189648fad8428fdc586a32df
- source_id: vite-troubleshooting
  url: https://vite.dev/guide/troubleshooting.html
  final_url: https://vite.dev/guide/troubleshooting.html
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: vite-troubleshooting-14
  short_excerpt: 'Error [ERR_REQUIRE_ESM]: require() of ES Module /path/to/dependency.js
    from /path/to/vite.config.js not supported. Instead change the require of index.js
    in /path/to/vite.config.js to a dynamic import() which is available in all CommonJS
    modules.'
  quote_hash: sha256:4976d09a854db189bbc07dd580ed387ce0ca8e79bb25e3740e2ef3483bc06306
- source_id: vite-troubleshooting
  url: https://vite.dev/guide/troubleshooting.html
  final_url: https://vite.dev/guide/troubleshooting.html
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: vite-troubleshooting-17
  short_excerpt: 'While it may work using --experimental-require-module , or Node.js
    >22, or in other runtimes, we still recommend converting your config to ESM by
    either:'
  quote_hash: sha256:49cae24b9e02862710e7680510c322f15b191972e75d599993dd6121a50d90e5
- source_id: vite-troubleshooting
  url: https://vite.dev/guide/troubleshooting.html
  final_url: https://vite.dev/guide/troubleshooting.html
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: vite-troubleshooting-20
  short_excerpt: renaming vite.config.js / vite.config.ts to vite.config.mjs / vite.config.mts
  quote_hash: sha256:99d7fb1970f3086e36d6287361f55057593c879c7949b183db26752fb9d6f0e1
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# vite-esm-only-config-require

## Failure Class
vite/config-module-format

## Symptoms
- Vite fails because an ESM-only package was loaded by require

## Fingerprints
- This package is ESM only
- ERR_REQUIRE_ESM
- tried to load by require
- vite config ESM

## First Checks
- Check whether vite.config.* or a plugin config is loaded as CommonJS
- Check whether the failing dependency is ESM-only
- Check whether the config file extension should be .mjs or .mts

## Do Not Patch Yet
- Do not pin an old dependency version before confirming the config module format
- Do not rely on experimental require support as the primary fix

## Evidence Needed
- Capture the ERR_REQUIRE_ESM stack and the dependency path
- Identify the Vite config filename and package type
- Confirm how the dependency is imported from config

## Minimal Fix Scope
- The Vite config module format or import statement
- The plugin/dependency entry loaded from config

## Validation Ladder
- Run the Vite command that originally failed
- Confirm the config loads under ESM
- Run the project build or dev-server smoke

## Regression Guard
- Add a config-load smoke test or CI build check

## Reviewer Notes
