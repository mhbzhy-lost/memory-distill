- [langgraph-invalid-concurrent-update-1] INVALID_CONCURRENT_GRAPH_UPDATE

- [langgraph-invalid-concurrent-update-2] A LangGraph [`StateGraph`](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) received concurrent updates to its state from multiple nodes to a state property that doesn't

- [langgraph-invalid-concurrent-update-3] support it.

- [langgraph-invalid-concurrent-update-4] One way this can occur is if you are using a [fanout](/oss/python/langgraph/use-graph-api#map-reduce-and-the-send-api)

- [langgraph-invalid-concurrent-update-5] or other parallel execution in your graph and you have defined a graph like this:

- [langgraph-invalid-concurrent-update-6] class State(TypedDict): some_key: str # [!code highlight] def node(state: State): return {"some_key": "some_string_value"} def other_node(state: State): return {"some_key": "some_string_value"} builder = StateGraph(State) builder.add_node(node) builder.add_node(other_node) builder.add_edge(START, "node") builder.add_edge(START, "other_node") graph = builder.compile()

- [langgraph-invalid-concurrent-update-7] If a node in the above graph returns `{ "some_key": "some_string_value" }`, this will overwrite the state value for `"some_key"` with `"some_string_value"`.

- [langgraph-invalid-concurrent-update-8] However, if multiple nodes in e.g. a fanout within a single step return values for `"some_key"`, the graph will throw this error because

- [langgraph-invalid-concurrent-update-9] there is uncertainty around how to update the internal state.

- [langgraph-invalid-concurrent-update-10] To get around this, you can define a reducer that combines multiple values:

- [langgraph-invalid-concurrent-update-11] import operator from typing import Annotated class State(TypedDict): # The operator.add reducer fn makes this append-only # [!code highlight] some_key: Annotated[list, operator.add] # [!code highlight]

- [langgraph-invalid-concurrent-update-12] This will allow you to define logic that handles the same key returned from multiple nodes executed in parallel.

- [langgraph-invalid-concurrent-update-13] Troubleshooting

- [langgraph-invalid-concurrent-update-14] The following may help resolve this error:

- [langgraph-invalid-concurrent-update-15] If your graph executes nodes in parallel, make sure you have defined relevant state keys with a reducer.
