---
id: build-vite-esm-only-config-require
kind: build-recipe
status: proposed
stack:
- react
- vite
trigger:
  file_pattern: ''
  code_signals: []
  description: 代码可能触发 vite/config-module-format 类故障（Vite fails because an ESM-only
    package was loaded by require）
correct_pattern: []
decision_context: []
constraints:
- Do not pin an old dependency version before confirming the config module format
- Do not rely on experimental require support as the primary fix
do_not:
- Do not pin an old dependency version before confirming the config module format
- Do not rely on experimental require support as the primary fix
defaults: []
validation:
- Run the Vite command that originally failed
- Confirm the config loads under ESM
- Run the project build or dev-server smoke
related_debug_recipes:
- vite-esm-only-config-require
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
  state: proposed
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# build-vite-esm-only-config-require

## Trigger
**代码可能触发 vite/config-module-format 类故障（Vite fails because an ESM-only package was loaded by require）**

## Correct Pattern


## Constraints
- Do not pin an old dependency version before confirming the config module format
- Do not rely on experimental require support as the primary fix

## Do Not
- Do not pin an old dependency version before confirming the config module format
- Do not rely on experimental require support as the primary fix

## Validation
- Run the Vite command that originally failed
- Confirm the config loads under ESM
- Run the project build or dev-server smoke

## Related Debug Recipes
- vite-esm-only-config-require

## Reviewer Notes
