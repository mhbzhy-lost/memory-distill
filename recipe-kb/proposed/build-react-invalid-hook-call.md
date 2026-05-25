---
id: build-react-invalid-hook-call
kind: build-recipe
status: proposed
stack:
- react
trigger:
  file_pattern: ''
  code_signals: []
  description: '代码可能触发 react/hooks 类故障（Invalid hook call: Hooks can only be called
    inside the body of a function compon）'
correct_pattern: []
decision_context: []
constraints:
- Do not call Hooks inside loops, conditions, nested functions, or event handlers
- Do not silence the warning before locating the invalid call site or duplicate React
  copy
do_not:
- Do not call Hooks inside loops, conditions, nested functions, or event handlers
- Do not silence the warning before locating the invalid call site or duplicate React
  copy
defaults: []
validation:
- Run the affected component path in development and confirm the warning is gone
- Run dependency inspection for react and react-dom
- Run the related component or smoke test
related_debug_recipes:
- react-invalid-hook-call
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
  state: proposed
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# build-react-invalid-hook-call

## Trigger
**代码可能触发 react/hooks 类故障（Invalid hook call: Hooks can only be called inside the body of a function compon）**

## Correct Pattern


## Constraints
- Do not call Hooks inside loops, conditions, nested functions, or event handlers
- Do not silence the warning before locating the invalid call site or duplicate React copy

## Do Not
- Do not call Hooks inside loops, conditions, nested functions, or event handlers
- Do not silence the warning before locating the invalid call site or duplicate React copy

## Validation
- Run the affected component path in development and confirm the warning is gone
- Run dependency inspection for react and react-dom
- Run the related component or smoke test

## Related Debug Recipes
- react-invalid-hook-call

## Reviewer Notes
