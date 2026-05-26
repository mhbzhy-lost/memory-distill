# 快照人审：kotlin-flow-exception-handling

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
- 最终 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
- 来源类型: library_doc
- 采集时间: 2026-05-26T13:49:14.876449Z
- HTTP 状态: 200
- 内容哈希: sha256:e8ab1752ce8b21f72436022ea7c630f5819b0355d26d396dde4e7d0310e02bda
- 技术栈: kotlin, android
- 抽取段落数: 248

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 248
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 5/5 条 expected_failure_hints

## 预期线索命中
- `Flow invariant is violated`
  - [kotlin-flow-exception-handling-97] Exception in thread "main" java.lang.IllegalStateException: Flow invariant is violated: Flow was collected in [CoroutineId(1), "coroutine#1":BlockingCoroutine{Active}@5511c7f8, BlockingEventLoop@2eac3323], but emissio...
- `Flow was collected in ... but emission happened in ...`
  - [kotlin-flow-exception-handling-97] Exception in thread "main" java.lang.IllegalStateException: Flow invariant is violated: Flow was collected in [CoroutineId(1), "coroutine#1":BlockingCoroutine{Active}@5511c7f8, BlockingEventLoop@2eac3323], but emissio...
- `Please refer to 'flow' documentation or use 'flowOn' instead`
  - [kotlin-flow-exception-handling-97] Exception in thread "main" java.lang.IllegalStateException: Flow invariant is violated: Flow was collected in [CoroutineId(1), "coroutine#1":BlockingCoroutine{Active}@5511c7f8, BlockingEventLoop@2eac3323], but emissio...
- `Flow exception transparency violation`
  - [kotlin-flow-exception-handling-178] Flows must be transparent to exceptions and it is a violation of the exception transparency to emit values in the flow { ... } builder from inside of a try/catch block. This guarantees that a collector throwing an exc...
- `catch operator only catches upstream exceptions`
  - [kotlin-flow-exception-handling-187] The catch intermediate operator, honoring exception transparency, catches only upstream exceptions (that is an exception from all the operators above catch , but not below it). If the block in collect { ... } (placed...
  - [kotlin-flow-exception-handling-213] Another difference with catch operator is that onCompletion sees all exceptions and receives a null exception only on successful completion of the upstream flow (without cancellation or failure).

## 段落样例
- [kotlin-flow-exception-handling-1] https://github.com/Kotlin/kotlinx.coroutines/edit/master/docs/topics/
- [kotlin-flow-exception-handling-2] A suspending function asynchronously returns a single value, but how can we return multiple asynchronously computed values? This is where Kotlin Flows come in.
- [kotlin-flow-exception-handling-3] Representing multiple values
- [kotlin-flow-exception-handling-4] Multiple values can be represented in Kotlin using collections . For example, we can have a simple function that returns a List of three numbers and then print them all using forEach :
- [kotlin-flow-exception-handling-5] fun simple(): List<Int> = listOf(1, 2, 3) fun main() { simple().forEach { value -> println(value) } }
- [kotlin-flow-exception-handling-6] {kotlin-runnable="true" kotlin-min-compiler-version="1.3"}
- [kotlin-flow-exception-handling-7] You can get the full code here .
- [kotlin-flow-exception-handling-8] {style="note"}

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
