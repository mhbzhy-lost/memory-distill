---
id: langgraph-missing-checkpointer
kind: debug-recipe
status: accepted
stack:
- langchain
failure_class: langgraph/persistence
symptoms:
- LangGraph StateGraph raises an error because no checkpointer is configured for persistence-required
  features
fingerprints:
- MISSING_CHECKPOINTER
- checkpointer
- compile() without checkpointer
- InMemorySaver
- human-in-the-loop
first_checks:
- Check whether compile() was called with checkpointer= parameter
- Check whether human-in-the-loop, memory, or time-travel features require persistence
- Check whether @entrypoint decorator received a checkpointer argument
do_not:
- Do not use InMemorySaver in production; use PostgresSaver or another persistent
  checkpointer
- Do not skip checkpointer configuration if your graph uses interrupts, resume, or
  thread_id
evidence_needed:
- Identify whether the graph uses features that require persistence (human-in-the-loop,
  memory, time-travel)
- Capture the compile() call site to verify checkpointer parameter
minimal_fix_scope:
- The StateGraph.compile() call or @entrypoint decorator
- The checkpointer initialization (InMemorySaver, PostgresSaver, etc.)
validation_ladder:
- Instantiate the graph with a checkpointer and verify compile() succeeds
- Invoke the graph with a thread_id and confirm state is persisted
- Run the graph test covering the persistence-requiring feature
regression_guard:
- Add a graph test that asserts checkpointer is configured and state persists across
  invocations
evidence_refs:
- source_id: langgraph-missing-checkpointer
  url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-missing-checkpointer-1
  short_excerpt: MISSING_CHECKPOINTER
  quote_hash: sha256:73b4a9d0d4d28640e6eac373d7270cfd7ed877f7636830b9a77ae73cd4a5d2cb
- source_id: langgraph-missing-checkpointer
  url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-missing-checkpointer-2
  short_excerpt: You are attempting to use built-in LangGraph persistence without
    providing a checkpointer.
  quote_hash: sha256:ebcd9e9ffe7b8bc17eff2f1cfe5b6f4e844d3a2dccb09023dff3f7e05458b7f4
- source_id: langgraph-missing-checkpointer
  url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-missing-checkpointer-3
  short_excerpt: This happens when a `checkpointer` is missing in the `compile()`
    method of [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph)
    or [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint).
  quote_hash: sha256:f30f433d343cf6219081a8f53ed4ae08a4ddf686e23f5667187a126861ec9a91
- source_id: langgraph-missing-checkpointer
  url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-missing-checkpointer-6
  short_excerpt: Initialize and pass a checkpointer to the `compile()` method of [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph)
    or [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint).
  quote_hash: sha256:b1480e20bdfac6133c435516229be3f029b4392164fec04ef4792c8a74507b7d
- source_id: langgraph-missing-checkpointer
  url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-missing-checkpointer-7
  short_excerpt: 'from langgraph.checkpoint.memory import InMemorySaver checkpointer
    = InMemorySaver() # Graph API graph = StateGraph(...).compile(checkpointer=checkpointer)
    # Functional API @entrypoint(checkpointer=checkpointer) def workflow(messages:
    list[str]) -> str: ...'
  quote_hash: sha256:0747f2db8a732a281fa9e172fcb83678e528f7e5cbb3feabf1dd1d10a9343fc9
- source_id: langgraph-missing-checkpointer
  url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-missing-checkpointer-8
  short_excerpt: Use the LangGraph API so you don't need to implement or configure
    checkpointers manually. The API handles all persistence infrastructure for you.
  quote_hash: sha256:bab71f4db1d739b1e4f901e19d40900d01574fffe7e1a51f783e6f5a14afeac8
- source_id: langgraph-missing-checkpointer
  url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  final_url: https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langgraph-missing-checkpointer-10
  short_excerpt: Read more about [persistence](/oss/python/langgraph/persistence).
  quote_hash: sha256:26c5e936b954db1e13241b18557fa10c0ff9d8faa52da71f30afdf52969fb8c8
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# langgraph-missing-checkpointer

## Failure Class
langgraph/persistence

## Symptoms
- LangGraph StateGraph raises an error because no checkpointer is configured for persistence-required features

## Fingerprints
- MISSING_CHECKPOINTER
- checkpointer
- compile() without checkpointer
- InMemorySaver
- human-in-the-loop

## First Checks
- Check whether compile() was called with checkpointer= parameter
- Check whether human-in-the-loop, memory, or time-travel features require persistence
- Check whether @entrypoint decorator received a checkpointer argument

## Do Not Patch Yet
- Do not use InMemorySaver in production; use PostgresSaver or another persistent checkpointer
- Do not skip checkpointer configuration if your graph uses interrupts, resume, or thread_id

## Evidence Needed
- Identify whether the graph uses features that require persistence (human-in-the-loop, memory, time-travel)
- Capture the compile() call site to verify checkpointer parameter

## Minimal Fix Scope
- The StateGraph.compile() call or @entrypoint decorator
- The checkpointer initialization (InMemorySaver, PostgresSaver, etc.)

## Validation Ladder
- Instantiate the graph with a checkpointer and verify compile() succeeds
- Invoke the graph with a thread_id and confirm state is persisted
- Run the graph test covering the persistence-requiring feature

## Regression Guard
- Add a graph test that asserts checkpointer is configured and state persists across invocations

## Reviewer Notes
