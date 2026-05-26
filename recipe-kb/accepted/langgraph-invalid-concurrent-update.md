---
id: langgraph-invalid-concurrent-update
kind: debug-recipe
status: accepted
stack:
- langchain
failure_class: langgraph/state-management
symptoms:
- LangGraph StateGraph raises InvalidUpdateError because multiple parallel nodes updated
  the same state key without a reducer
fingerprints:
- INVALID_CONCURRENT_GRAPH_UPDATE
- InvalidUpdateError
- concurrent updates
- reducer
- Annotated
- operator.add
first_checks:
- Check whether the state key being updated by multiple parallel nodes has a reducer
  function
- Check whether the state schema uses Annotated[list, operator.add] or similar reducer
  for list/accumulator keys
- Check whether the graph uses fanout or parallel execution that could trigger concurrent
  writes
do_not:
- Do not remove parallelism from the graph just to avoid concurrent update errors
- Do not use a reducer that silently overwrites values unless that is the intended
  behavior
evidence_needed:
- Identify which state keys are updated by multiple parallel nodes
- Capture the state schema definition and the reducer functions used
minimal_fix_scope:
- The state schema TypedDict or Pydantic model definition
- The reducer function annotations on state keys (e.g., Annotated[list, operator.add])
validation_ladder:
- Reproduce the InvalidUpdateError with a graph invocation that triggers parallel
  writes
- Add the appropriate reducer and verify the graph executes without error
- Run the graph test covering the parallel node execution path
regression_guard:
- Add a graph test that asserts parallel node execution succeeds and state is correctly
  merged
evidence_refs:
- source_id: langgraph-invalid-concurrent-update
  url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-invalid-concurrent-update-1
  short_excerpt: INVALID_CONCURRENT_GRAPH_UPDATE
  quote_hash: sha256:76e1ba9cb006926a8a89b446382adfd2fcd56745956468023f13c974e571b953
- source_id: langgraph-invalid-concurrent-update
  url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-invalid-concurrent-update-2
  short_excerpt: A LangGraph [`StateGraph`](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph)
    received concurrent updates to its state from multiple nodes to a state property
    that doesn't
  quote_hash: sha256:bd9e11e577c33790193221fdb236fb77d2c5dcfd47d29bc426c1eaccf84622a3
- source_id: langgraph-invalid-concurrent-update
  url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-invalid-concurrent-update-4
  short_excerpt: One way this can occur is if you are using a [fanout](/oss/python/langgraph/use-graph-api#map-reduce-and-the-send-api)
  quote_hash: sha256:98e5ba129227bd37136582d2eb10de5aed36f88305262fd87220ae0f2b51cfbb
- source_id: langgraph-invalid-concurrent-update
  url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-invalid-concurrent-update-5
  short_excerpt: 'or other parallel execution in your graph and you have defined a
    graph like this:'
  quote_hash: sha256:b9f66ed97e5029baf36bfb2d73be5a77060e3ccace4e9b740ba60a922f1b9237
- source_id: langgraph-invalid-concurrent-update
  url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-invalid-concurrent-update-8
  short_excerpt: However, if multiple nodes in e.g. a fanout within a single step
    return values for `"some_key"`, the graph will throw this error because
  quote_hash: sha256:f173617c32ccf5691af0678d2b832f67bf39d011c417924b59ba9040da613662
- source_id: langgraph-invalid-concurrent-update
  url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-invalid-concurrent-update-10
  short_excerpt: 'To get around this, you can define a reducer that combines multiple
    values:'
  quote_hash: sha256:78707fcbf7fc49a1043a3d299f70f5747201a8ac2fad1319e27d0d683fc6269f
- source_id: langgraph-invalid-concurrent-update
  url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-invalid-concurrent-update-11
  short_excerpt: 'import operator from typing import Annotated class State(TypedDict):
    # The operator.add reducer fn makes this append-only # [!code highlight] some_key:
    Annotated[list, operator.add] # [!code highlight]'
  quote_hash: sha256:86d0efc59b3a251e445c0d0706242928bdb59beb855d0d85780fdc3f7c5914d3
- source_id: langgraph-invalid-concurrent-update
  url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-invalid-concurrent-update-12
  short_excerpt: This will allow you to define logic that handles the same key returned
    from multiple nodes executed in parallel.
  quote_hash: sha256:93b5001f3c34e880c3fbe9a14fb97e70c337505b9ee13c8e7b34e25bceb684e9
- source_id: langgraph-invalid-concurrent-update
  url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-invalid-concurrent-update-15
  short_excerpt: If your graph executes nodes in parallel, make sure you have defined
    relevant state keys with a reducer.
  quote_hash: sha256:6d2c6c8c5c9bf99c0cd5d6a382cb65aa0131b628a485eaf5ef2bc71d731c01f5
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# langgraph-invalid-concurrent-update

## Failure Class
langgraph/state-management

## Symptoms
- LangGraph StateGraph raises InvalidUpdateError because multiple parallel nodes updated the same state key without a reducer

## Fingerprints
- INVALID_CONCURRENT_GRAPH_UPDATE
- InvalidUpdateError
- concurrent updates
- reducer
- Annotated
- operator.add

## First Checks
- Check whether the state key being updated by multiple parallel nodes has a reducer function
- Check whether the state schema uses Annotated[list, operator.add] or similar reducer for list/accumulator keys
- Check whether the graph uses fanout or parallel execution that could trigger concurrent writes

## Do Not Patch Yet
- Do not remove parallelism from the graph just to avoid concurrent update errors
- Do not use a reducer that silently overwrites values unless that is the intended behavior

## Evidence Needed
- Identify which state keys are updated by multiple parallel nodes
- Capture the state schema definition and the reducer functions used

## Minimal Fix Scope
- The state schema TypedDict or Pydantic model definition
- The reducer function annotations on state keys (e.g., Annotated[list, operator.add])

## Validation Ladder
- Reproduce the InvalidUpdateError with a graph invocation that triggers parallel writes
- Add the appropriate reducer and verify the graph executes without error
- Run the graph test covering the parallel node execution path

## Regression Guard
- Add a graph test that asserts parallel node execution succeeds and state is correctly merged

## Reviewer Notes
