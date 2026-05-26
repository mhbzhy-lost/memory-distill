- [langgraph-graph-recursion-limit-1] GRAPH_RECURSION_LIMIT

- [langgraph-graph-recursion-limit-2] Your LangGraph [`StateGraph`](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) reached the maximum number of steps before hitting a stop condition.

- [langgraph-graph-recursion-limit-3] This is often due to an infinite loop caused by code like the example below:

- [langgraph-graph-recursion-limit-4] class State(TypedDict): some_key: str builder = StateGraph(State) builder.add_node("a", ...) builder.add_node("b", ...) builder.add_edge("a", "b") builder.add_edge("b", "a") ... graph = builder.compile()

- [langgraph-graph-recursion-limit-5] However, complex graphs may hit the default limit naturally.

- [langgraph-graph-recursion-limit-6] Troubleshooting

- [langgraph-graph-recursion-limit-7] If you are not expecting your graph to go through many iterations, you likely have a cycle. Check your logic for infinite loops.

- [langgraph-graph-recursion-limit-8] If you have a complex graph, you can pass in a higher `recursion_limit` value into your `config` object when invoking your graph like this:

- [langgraph-graph-recursion-limit-9] graph.invoke({...}, {"recursion_limit": 100})
