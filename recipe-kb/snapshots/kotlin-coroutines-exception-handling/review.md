# 快照人审：kotlin-coroutines-exception-handling

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
- 最终 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
- 来源类型: library_doc
- 采集时间: 2026-05-26T10:27:19.494775Z
- HTTP 状态: 200
- 内容哈希: sha256:7939820cde28c22f3ae29fd39f8c38bfb685aa1e7a5ce2bf9aecbf3dcffeee1d
- 技术栈: kotlin, android
- 抽取段落数: 0

## QA 闸门
- 状态: 需要 agentic fallback
- sections_non_empty: 失败；抽取段落数: 0
- section_count_within_bounds: 失败；期望范围: 1-500
- expected_hints_matched: 失败；命中 0/5 条 expected_failure_hints
- fallback: 启动 agentic loop
- fallback 输入: raw.html, response.json, sections.json, review.md
- fallback 要求: 读取 raw.html、response.json、sections.json、review.md，产出最小 extraction_profile 或 extractor patch，并补回归测试。

## 预期线索命中
- `CoroutineExceptionHandler got uncaught exception`：未找到直接段落命中
- `CancellationException ignored by coroutine machinery`：未找到直接段落命中
- `exception aggregation suppressed exceptions`：未找到直接段落命中
- `SupervisorJob cancellation propagation`：未找到直接段落命中
- `supervisorScope vs coroutineScope exception handling`：未找到直接段落命中

## 段落样例
- 未抽取到段落。

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
