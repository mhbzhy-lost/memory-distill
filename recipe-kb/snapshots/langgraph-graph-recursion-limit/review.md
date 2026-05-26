# 快照人审：langgraph-graph-recursion-limit

## 快照质量检查
- 来源 URL: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
- 最终 URL: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md
- 来源类型: official_error_doc
- 采集时间: 2026-05-26T09:17:32.948993Z
- HTTP 状态: 200
- 内容哈希: sha256:02f73014c841ae4bf95330ac250d6947a7846b4ad118fcf66e76a68a18e4d631
- 技术栈: langchain
- 抽取段落数: 9

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 9
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 4/5 条 expected_failure_hints

## 预期线索命中
- `GraphRecursionError`
  - [langgraph-graph-recursion-limit-1] GRAPH_RECURSION_LIMIT
  - [langgraph-graph-recursion-limit-8] If you have a complex graph, you can pass in a higher `recursion_limit` value into your `config` object when invoking your graph like this:
  - [langgraph-graph-recursion-limit-9] graph.invoke({...}, {"recursion_limit": 100})
- `GRAPH_RECURSION_LIMIT`
  - [langgraph-graph-recursion-limit-1] GRAPH_RECURSION_LIMIT
- `reached the maximum number of steps`
  - [langgraph-graph-recursion-limit-2] Your LangGraph [`StateGraph`](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) reached the maximum number of steps before hitting a stop condition.
- `StateGraph infinite loop`：未找到直接段落命中
- `recursion_limit`
  - [langgraph-graph-recursion-limit-1] GRAPH_RECURSION_LIMIT
  - [langgraph-graph-recursion-limit-8] If you have a complex graph, you can pass in a higher `recursion_limit` value into your `config` object when invoking your graph like this:
  - [langgraph-graph-recursion-limit-9] graph.invoke({...}, {"recursion_limit": 100})

## 段落样例
- [langgraph-graph-recursion-limit-1] GRAPH_RECURSION_LIMIT
- [langgraph-graph-recursion-limit-2] Your LangGraph [`StateGraph`](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) reached the maximum number of steps before hitting a stop condition.
- [langgraph-graph-recursion-limit-3] This is often due to an infinite loop caused by code like the example below:
- [langgraph-graph-recursion-limit-4] class State(TypedDict): some_key: str builder = StateGraph(State) builder.add_node("a", ...) builder.add_node("b", ...) builder.add_edge("a", "b") builder.add_edge("b", "a") ... graph = builder.compile()
- [langgraph-graph-recursion-limit-5] However, complex graphs may hit the default limit naturally.
- [langgraph-graph-recursion-limit-6] Troubleshooting
- [langgraph-graph-recursion-limit-7] If you are not expecting your graph to go through many iterations, you likely have a cycle. Check your logic for infinite loops.
- [langgraph-graph-recursion-limit-8] If you have a complex graph, you can pass in a higher `recursion_limit` value into your `config` object when invoking your graph like this:

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
