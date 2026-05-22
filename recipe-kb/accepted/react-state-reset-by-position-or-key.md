---
id: react-state-reset-by-position-or-key
kind: debug-recipe
status: accepted
stack:
- react
failure_class: react/state-preservation
symptoms:
- Component state is reset unexpectedly or preserved when it should reset
fingerprints:
- state is reset unexpectedly
- state is isolated between components
- key forces subtree reset
- nested component definitions reset state
first_checks:
- Check whether the component is rendered at a different position in the tree
- Check whether a key change is intentionally or accidentally forcing a reset
- Check whether a component function is nested inside another component
do_not:
- Do not move state upward before confirming whether identity or key is the cause
- Do not define component functions inside render when state must be preserved
evidence_needed:
- Compare the component tree position before and after the reset
- Capture key values for the affected subtree
- Identify whether a nested component definition is recreated each render
minimal_fix_scope:
- The affected component identity, position, or key
- The parent render branch that changes subtree identity
validation_ladder:
- Reproduce the state reset with a minimal interaction
- Verify the component keeps or resets state according to the chosen identity
- Run the focused component test for the affected branch
regression_guard:
- Add a component interaction test for the preserve/reset behavior
evidence_refs:
- source_id: react-preserving-resetting-state
  url: https://react.dev/learn/preserving-and-resetting-state
  final_url: https://react.dev/learn/preserving-and-resetting-state
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-preserving-resetting-state-2
  short_excerpt: State is isolated between components. React keeps track of which
    state belongs to which component based on their place in the UI tree. You can
    control when to preserve state and when to reset it between re-renders.
  quote_hash: sha256:bbec4489c57e58509766eb736977c9eba22002fcc9a666dcb5c3720828bbd0d5
- source_id: react-preserving-resetting-state
  url: https://react.dev/learn/preserving-and-resetting-state
  final_url: https://react.dev/learn/preserving-and-resetting-state
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-preserving-resetting-state-78
  short_excerpt: 'Switching between Taylor and Sarah does not preserve the state.
    This is because you gave them different key s:'
  quote_hash: sha256:161809ccc2cc2cf8ab41c0214cf5f8933ad9c43477e807c7b0f224f9b98be0f8
- source_id: react-preserving-resetting-state
  url: https://react.dev/learn/preserving-and-resetting-state
  final_url: https://react.dev/learn/preserving-and-resetting-state
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-preserving-resetting-state-103
  short_excerpt: You can force a subtree to reset its state by giving it a different
    key.
  quote_hash: sha256:8a5e455e305fdbf6710089d0869bc39443575362efc46ee2f0eef48916f29846
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# react-state-reset-by-position-or-key

## Failure Class
react/state-preservation

## Symptoms
- Component state is reset unexpectedly or preserved when it should reset

## Fingerprints
- state is reset unexpectedly
- state is isolated between components
- key forces subtree reset
- nested component definitions reset state

## First Checks
- Check whether the component is rendered at a different position in the tree
- Check whether a key change is intentionally or accidentally forcing a reset
- Check whether a component function is nested inside another component

## Do Not Patch Yet
- Do not move state upward before confirming whether identity or key is the cause
- Do not define component functions inside render when state must be preserved

## Evidence Needed
- Compare the component tree position before and after the reset
- Capture key values for the affected subtree
- Identify whether a nested component definition is recreated each render

## Minimal Fix Scope
- The affected component identity, position, or key
- The parent render branch that changes subtree identity

## Validation Ladder
- Reproduce the state reset with a minimal interaction
- Verify the component keeps or resets state according to the chosen identity
- Run the focused component test for the affected branch

## Regression Guard
- Add a component interaction test for the preserve/reset behavior

## Reviewer Notes
