---
id: langgraph-graph-recursion-limit
kind: debug-recipe
status: accepted
stack:
- langchain
failure_class: langgraph/graph-execution
symptoms:
- LangGraph StateGraph raises GraphRecursionError because it reached the maximum number
  of steps before hitting a stop condition
fingerprints:
- GRAPH_RECURSION_LIMIT
- GraphRecursionError
- reached the maximum number of steps
- recursion_limit
- infinite loop
first_checks:
- Check whether the graph has an unintended cycle (infinite loop) by reviewing edges
  between nodes
- Check whether the default recursion_limit is too low for complex graphs that legitimately
  need many iterations
- Check whether the graph has a proper stop condition or terminal node
do_not:
- Do not blindly increase recursion_limit without first verifying there is no infinite
  loop
- Do not remove cycles by adding arbitrary stop nodes without understanding the intended
  graph behavior
evidence_needed:
- Capture the graph invocation config and the recursion_limit value
- Identify which nodes form the cycle or exceed the step limit
minimal_fix_scope:
- The graph edge definitions and conditional routing logic
- The config recursion_limit parameter passed to graph.invoke()
validation_ladder:
- Reproduce the GraphRecursionError in development with the failing graph invocation
- Inspect graph edges to confirm whether the cycle is intentional or a bug
- Run the graph unit test covering the affected execution path
regression_guard:
- Add a graph test that asserts the graph terminates within expected steps or raises
  GraphRecursionError when expected
evidence_refs:
- source_id: langgraph-graph-recursion-limit
  url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-graph-recursion-limit-1
  short_excerpt: GRAPH_RECURSION_LIMIT
  quote_hash: sha256:d2e251e08b5e97248f8fc4298b647470265be5239fc7836f7f1dcad286ea759f
- source_id: langgraph-graph-recursion-limit
  url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-graph-recursion-limit-2
  short_excerpt: Your LangGraph [`StateGraph`](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph)
    reached the maximum number of steps before hitting a stop condition.
  quote_hash: sha256:12e753a3c408ac878486a7a2835476a51b3fab9e342dc52be5f138b100778a83
- source_id: langgraph-graph-recursion-limit
  url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-graph-recursion-limit-3
  short_excerpt: 'This is often due to an infinite loop caused by code like the example
    below:'
  quote_hash: sha256:092c0db0c7706bf016850402fd67d9dcff1be6a7e852e792b0f6e7ac0dced9b0
- source_id: langgraph-graph-recursion-limit
  url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-graph-recursion-limit-4
  short_excerpt: 'class State(TypedDict): some_key: str builder = StateGraph(State)
    builder.add_node("a", ...) builder.add_node("b", ...) builder.add_edge("a", "b")
    builder.add_edge("b", "a") ... graph = builder.compile()'
  quote_hash: sha256:93f9739f4c50c9e3f924cbeac9479a1fb659950b2405c56f0fe1b82834d8310c
- source_id: langgraph-graph-recursion-limit
  url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-graph-recursion-limit-7
  short_excerpt: If you are not expecting your graph to go through many iterations,
    you likely have a cycle. Check your logic for infinite loops.
  quote_hash: sha256:7fec5bbdaac02e606245632f249aa3f1169f31006c500cb8ee2527bb5e6439cb
- source_id: langgraph-graph-recursion-limit
  url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-graph-recursion-limit-8
  short_excerpt: 'If you have a complex graph, you can pass in a higher `recursion_limit`
    value into your `config` object when invoking your graph like this:'
  quote_hash: sha256:df6177b3e317bc22e13de0ebe49c0e8f1cdd0a69f5687963be7bfd1dac605d25
- source_id: langgraph-graph-recursion-limit
  url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-graph-recursion-limit-9
  short_excerpt: 'graph.invoke({...}, {"recursion_limit": 100})'
  quote_hash: sha256:cf570260ded8a56b42ddd868457bad976989b873a7624b977a28cbc2aa2e7c53
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# langgraph-graph-recursion-limit

## Failure Class
langgraph/graph-execution

## Symptoms
- LangGraph StateGraph raises GraphRecursionError because it reached the maximum number of steps before hitting a stop condition

## Fingerprints
- GRAPH_RECURSION_LIMIT
- GraphRecursionError
- reached the maximum number of steps
- recursion_limit
- infinite loop

## First Checks
- Check whether the graph has an unintended cycle (infinite loop) by reviewing edges between nodes
- Check whether the default recursion_limit is too low for complex graphs that legitimately need many iterations
- Check whether the graph has a proper stop condition or terminal node

## Do Not Patch Yet
- Do not blindly increase recursion_limit without first verifying there is no infinite loop
- Do not remove cycles by adding arbitrary stop nodes without understanding the intended graph behavior

## Evidence Needed
- Capture the graph invocation config and the recursion_limit value
- Identify which nodes form the cycle or exceed the step limit

## Minimal Fix Scope
- The graph edge definitions and conditional routing logic
- The config recursion_limit parameter passed to graph.invoke()

## Validation Ladder
- Reproduce the GraphRecursionError in development with the failing graph invocation
- Inspect graph edges to confirm whether the cycle is intentional or a bug
- Run the graph unit test covering the affected execution path

## Regression Guard
- Add a graph test that asserts the graph terminates within expected steps or raises GraphRecursionError when expected

## Reviewer Notes
