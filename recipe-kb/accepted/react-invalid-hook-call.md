---
id: react-invalid-hook-call
kind: debug-recipe
status: accepted
stack:
- react
failure_class: react/hooks
symptoms:
- 'Invalid hook call: Hooks can only be called inside the body of a function component'
fingerprints:
- Invalid hook call
- Hooks can only be called inside the body of a function component
- mismatching versions of React and React DOM
- more than one copy of React
first_checks:
- Check whether every Hook is called at the top level of a function component or custom
  Hook
- Check that react and react-dom resolve to matching versions
- Check whether the app bundles more than one copy of React
do_not:
- Do not call Hooks inside loops, conditions, nested functions, or event handlers
- Do not silence the warning before locating the invalid call site or duplicate React
  copy
evidence_needed:
- Identify the component or custom Hook where the invalid Hook call originates
- Capture dependency tree evidence for React and React DOM versions
- Check module resolution for duplicate React copies
minimal_fix_scope:
- The invalid Hook call site or custom Hook boundary
- The package dependency or bundler resolution path that duplicates React
validation_ladder:
- Run the affected component path in development and confirm the warning is gone
- Run dependency inspection for react and react-dom
- Run the related component or smoke test
regression_guard:
- Add a component or dependency-resolution test for the invalid Hook call path
evidence_refs:
- source_id: react-invalid-hook-call
  url: https://react.dev/warnings/invalid-hook-call-warning
  final_url: https://react.dev/warnings/invalid-hook-call-warning
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-invalid-hook-call-5
  short_excerpt: You might have mismatching versions of React and React DOM.
  quote_hash: sha256:bda30fd3170081916d5a202e7caa7d59ab2321b4515f899534700d94c7a37fd1
- source_id: react-invalid-hook-call
  url: https://react.dev/warnings/invalid-hook-call-warning
  final_url: https://react.dev/warnings/invalid-hook-call-warning
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-invalid-hook-call-6
  short_excerpt: You might have more than one copy of React in the same app.
  quote_hash: sha256:0c95602418cea64ebf7ae98de95dfbd6f3ceb5384b467462bd328259e892a705
- source_id: react-invalid-hook-call
  url: https://react.dev/warnings/invalid-hook-call-warning
  final_url: https://react.dev/warnings/invalid-hook-call-warning
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-invalid-hook-call-26
  short_excerpt: Mismatching Versions of React and React DOM
  quote_hash: sha256:98f8a04740579ecf3f6df421f1670dc48db9c8f652429bdfe42415a678398d93
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# react-invalid-hook-call

## Failure Class
react/hooks

## Symptoms
- Invalid hook call: Hooks can only be called inside the body of a function component

## Fingerprints
- Invalid hook call
- Hooks can only be called inside the body of a function component
- mismatching versions of React and React DOM
- more than one copy of React

## First Checks
- Check whether every Hook is called at the top level of a function component or custom Hook
- Check that react and react-dom resolve to matching versions
- Check whether the app bundles more than one copy of React

## Do Not Patch Yet
- Do not call Hooks inside loops, conditions, nested functions, or event handlers
- Do not silence the warning before locating the invalid call site or duplicate React copy

## Evidence Needed
- Identify the component or custom Hook where the invalid Hook call originates
- Capture dependency tree evidence for React and React DOM versions
- Check module resolution for duplicate React copies

## Minimal Fix Scope
- The invalid Hook call site or custom Hook boundary
- The package dependency or bundler resolution path that duplicates React

## Validation Ladder
- Run the affected component path in development and confirm the warning is gone
- Run dependency inspection for react and react-dom
- Run the related component or smoke test

## Regression Guard
- Add a component or dependency-resolution test for the invalid Hook call path

## Reviewer Notes
