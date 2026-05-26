# 快照人审：langgraph-invalid-concurrent-update

## 快照质量检查
- 来源 URL: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
- 最终 URL: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE.md
- 来源类型: official_error_doc
- 采集时间: 2026-05-26T09:17:32.948993Z
- HTTP 状态: 200
- 内容哈希: sha256:5fbaa5cc4e1e0f67bfb7b3e75dcd4dce127ed3dac1126ec295f8e8b241651d9c
- 技术栈: langchain
- 抽取段落数: 15

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 15
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 5/5 条 expected_failure_hints

## 预期线索命中
- `InvalidUpdateError`
  - [langgraph-invalid-concurrent-update-1] INVALID_CONCURRENT_GRAPH_UPDATE
- `INVALID_CONCURRENT_GRAPH_UPDATE`
  - [langgraph-invalid-concurrent-update-1] INVALID_CONCURRENT_GRAPH_UPDATE
- `concurrent updates to state`
  - [langgraph-invalid-concurrent-update-2] A LangGraph [`StateGraph`](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) received concurrent updates to its state from multiple nodes to a state property that doesn't
- `fanout parallel nodes same key`
  - [langgraph-invalid-concurrent-update-8] However, if multiple nodes in e.g. a fanout within a single step return values for `"some_key"`, the graph will throw this error because
  - [langgraph-invalid-concurrent-update-12] This will allow you to define logic that handles the same key returned from multiple nodes executed in parallel.
- `reducer Annotated operator.add`
  - [langgraph-invalid-concurrent-update-11] import operator from typing import Annotated class State(TypedDict): # The operator.add reducer fn makes this append-only # [!code highlight] some_key: Annotated[list, operator.add] # [!code highlight]

## 段落样例
- [langgraph-invalid-concurrent-update-1] INVALID_CONCURRENT_GRAPH_UPDATE
- [langgraph-invalid-concurrent-update-2] A LangGraph [`StateGraph`](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) received concurrent updates to its state from multiple nodes to a state property that doesn't
- [langgraph-invalid-concurrent-update-3] support it.
- [langgraph-invalid-concurrent-update-4] One way this can occur is if you are using a [fanout](/oss/python/langgraph/use-graph-api#map-reduce-and-the-send-api)
- [langgraph-invalid-concurrent-update-5] or other parallel execution in your graph and you have defined a graph like this:
- [langgraph-invalid-concurrent-update-6] class State(TypedDict): some_key: str # [!code highlight] def node(state: State): return {"some_key": "some_string_value"} def other_node(state: State): return {"some_key": "some_string_value"} builder = StateGraph(St...
- [langgraph-invalid-concurrent-update-7] If a node in the above graph returns `{ "some_key": "some_string_value" }`, this will overwrite the state value for `"some_key"` with `"some_string_value"`.
- [langgraph-invalid-concurrent-update-8] However, if multiple nodes in e.g. a fanout within a single step return values for `"some_key"`, the graph will throw this error because

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
