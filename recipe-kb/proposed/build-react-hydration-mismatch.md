---
id: build-react-hydration-mismatch
kind: build-recipe
status: proposed
stack:
- react
- nextjs
trigger:
  file_pattern: ''
  code_signals: []
  description: 代码可能触发 render/hydration 类故障（Hydration failed because the server rendered
    HTML didn't match the client）
correct_pattern: []
decision_context: []
constraints:
- Do not disable SSR as the first fix
- Do not rewrite the component tree before locating the mismatched markup
do_not:
- Do not disable SSR as the first fix
- Do not rewrite the component tree before locating the mismatched markup
defaults: []
validation:
- Reproduce the page in development
- Check browser console for the hydration warning
- Run the related smoke test if one exists
related_debug_recipes:
- react-hydration-mismatch
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
  state: proposed
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# build-react-hydration-mismatch

## Trigger
**代码可能触发 render/hydration 类故障（Hydration failed because the server rendered HTML didn't match the client）**

## Correct Pattern


## Constraints
- Do not disable SSR as the first fix
- Do not rewrite the component tree before locating the mismatched markup

## Do Not
- Do not disable SSR as the first fix
- Do not rewrite the component tree before locating the mismatched markup

## Validation
- Reproduce the page in development
- Check browser console for the hydration warning
- Run the related smoke test if one exists

## Related Debug Recipes
- react-hydration-mismatch

## Reviewer Notes
