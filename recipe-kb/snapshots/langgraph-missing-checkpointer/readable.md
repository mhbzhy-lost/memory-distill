- [langgraph-missing-checkpointer-1] MISSING_CHECKPOINTER

- [langgraph-missing-checkpointer-2] You are attempting to use built-in LangGraph persistence without providing a checkpointer.

- [langgraph-missing-checkpointer-3] This happens when a `checkpointer` is missing in the `compile()` method of [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) or [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint).

- [langgraph-missing-checkpointer-4] Troubleshooting

- [langgraph-missing-checkpointer-5] The following may help resolve this error:

- [langgraph-missing-checkpointer-6] Initialize and pass a checkpointer to the `compile()` method of [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) or [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint).

- [langgraph-missing-checkpointer-7] from langgraph.checkpoint.memory import InMemorySaver checkpointer = InMemorySaver() # Graph API graph = StateGraph(...).compile(checkpointer=checkpointer) # Functional API @entrypoint(checkpointer=checkpointer) def workflow(messages: list[str]) -> str: ...

- [langgraph-missing-checkpointer-8] Use the LangGraph API so you don't need to implement or configure checkpointers manually. The API handles all persistence infrastructure for you.

- [langgraph-missing-checkpointer-9] Related

- [langgraph-missing-checkpointer-10] Read more about [persistence](/oss/python/langgraph/persistence).
