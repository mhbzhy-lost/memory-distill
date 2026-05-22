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
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-error-418-5
  short_excerpt: 'Hydration failed because the server rendered %s didn''t match the
    client. As a result this tree will be regenerated on the client. This can happen
    if a SSR-ed Client Component used: - A server/client branch `if (typeof window
    !== ''undefined'')`. - Variable input such as `Date.now()` or `Math.random()`
    which changes each time it''s called. - Date formatting in a user''s locale which
    doesn''t match the server. - External changing data without sending a snapshot
    of it along with the HTML. - Invalid HTML tag nesting. It can also happen if the
    client has a browser extension installed which messes with t'
  quote_hash: sha256:e76e20313a2da174553088217329e4a665891c75252578b0b6b8d8c45f5a147c
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
