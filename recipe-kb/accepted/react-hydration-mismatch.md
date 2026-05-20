---
id: react-hydration-mismatch
kind: debug-recipe
status: accepted
stack:
- react
- nextjs
failure_class: render/hydration
symptoms:
- Hydration failed because the server rendered HTML didn't match the client
fingerprints:
- Hydration failed
- server rendered HTML didn't match the client
- server rendered HTML did not match the client
first_checks:
- Check server/client branches such as typeof window in render output
- Check Date.now(), Math.random(), and locale formatting in render output
- Check invalid HTML nesting in the affected component
do_not:
- Do not disable SSR as the first fix
- Do not rewrite the component tree before locating the mismatched markup
evidence_needed:
- Identify the component producing different server and client markup
- Capture the browser console hydration warning
minimal_fix_scope:
- The component producing mismatched markup
- The server-to-client data snapshot used by that component
validation_ladder:
- Reproduce the page in development
- Check browser console for the hydration warning
- Run the related smoke test if one exists
regression_guard:
- Add or update a smoke test for the affected page or component
evidence_refs:
- source_id: react-error-418
  url: https://react.dev/errors/418
  final_url: https://react.dev/errors/418
  source_type: official_error_doc
  captured_at: '2026-05-20T00:00:00Z'
  section_anchor: root
  span_id: react-error-418-1
  short_excerpt: Hydration failed because the server rendered HTML didn't match the
    client
  quote_hash: sha256:a7b3c9e34a8081fb36e39f44e34fd2cf68c8285ccba68d4c6031041f183d84dc
- source_id: react-error-418
  url: https://react.dev/errors/418
  final_url: https://react.dev/errors/418
  source_type: official_error_doc
  captured_at: '2026-05-20T00:00:00Z'
  section_anchor: root
  span_id: react-error-418-4
  short_excerpt: Variable input such as Date.now() or Math.random().
  quote_hash: sha256:80b353a51f90d0c7b41b9b2416bf54adaf087c6a8b5a74855eb7b4114d4eeefb
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# react-hydration-mismatch

## Failure Class
render/hydration

## Symptoms
- Hydration failed because the server rendered HTML didn't match the client

## Fingerprints
- Hydration failed
- server rendered HTML didn't match the client
- server rendered HTML did not match the client

## First Checks
- Check server/client branches such as typeof window in render output
- Check Date.now(), Math.random(), and locale formatting in render output
- Check invalid HTML nesting in the affected component

## Do Not Patch Yet
- Do not disable SSR as the first fix
- Do not rewrite the component tree before locating the mismatched markup

## Evidence Needed
- Identify the component producing different server and client markup
- Capture the browser console hydration warning

## Minimal Fix Scope
- The component producing mismatched markup
- The server-to-client data snapshot used by that component

## Validation Ladder
- Reproduce the page in development
- Check browser console for the hydration warning
- Run the related smoke test if one exists

## Regression Guard
- Add or update a smoke test for the affected page or component

## Reviewer Notes
