# 快照人审：kotlin-coroutines-exception-handling

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
- 最终 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
- 来源类型: library_doc
- 采集时间: 2026-05-26T13:49:14.876449Z
- HTTP 状态: 200
- 内容哈希: sha256:7939820cde28c22f3ae29fd39f8c38bfb685aa1e7a5ce2bf9aecbf3dcffeee1d
- 技术栈: kotlin, android
- 抽取段落数: 52

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 52
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 5/5 条 expected_failure_hints

## 预期线索命中
- `CoroutineExceptionHandler got uncaught exception`
  - [kotlin-coroutines-exception-handling-4] Coroutine builders come in two flavors: propagating exceptions automatically ( launch ) or exposing them to users ( async and produce ). When these builders are used to create a root coroutine, that is not a child of...
  - [kotlin-coroutines-exception-handling-8] import kotlinx.coroutines.* //sampleStart @OptIn(DelicateCoroutinesApi::class) fun main() = runBlocking { val job = GlobalScope.launch { // root coroutine with launch println("Throwing exception from launch") throw In...
  - [kotlin-coroutines-exception-handling-13] CoroutineExceptionHandler
- `CancellationException ignored by coroutine machinery`
  - [kotlin-coroutines-exception-handling-2] This section covers exception handling and cancellation on exceptions. We already know that a cancelled coroutine throws CancellationException in suspension points and that it is ignored by the coroutines' machinery....
  - [kotlin-coroutines-exception-handling-22] Cancellation is closely related to exceptions. Coroutines internally use CancellationException for cancellation, these exceptions are ignored by all handlers, so they should be used only as the source of additional de...
  - [kotlin-coroutines-exception-handling-25] If a coroutine encounters an exception other than CancellationException , it cancels its parent with that exception. This behaviour cannot be overridden and is used to provide stable coroutines hierarchies for structu...
- `exception aggregation suppressed exceptions`
  - [kotlin-coroutines-exception-handling-31] When multiple children of a coroutine fail with an exception, the general rule is "the first exception wins", so the first exception gets handled. All additional exceptions that happen after the first one are attached...
- `SupervisorJob cancellation propagation`
  - [kotlin-coroutines-exception-handling-43] The SupervisorJob can be used for these purposes. It is similar to a regular Job with the only exception that cancellation is propagated only downwards. This can easily be demonstrated using the following example:
  - [kotlin-coroutines-exception-handling-44] import kotlinx.coroutines.* fun main() = runBlocking { //sampleStart val supervisor = SupervisorJob() with(CoroutineScope(coroutineContext + supervisor)) { // launch the first child -- its exception is ignored for thi...
- `supervisorScope vs coroutineScope exception handling`
  - [kotlin-coroutines-exception-handling-2] This section covers exception handling and cancellation on exceptions. We already know that a cancelled coroutine throws CancellationException in suspension points and that it is ignored by the coroutines' machinery....
  - [kotlin-coroutines-exception-handling-8] import kotlinx.coroutines.* //sampleStart @OptIn(DelicateCoroutinesApi::class) fun main() = runBlocking { val job = GlobalScope.launch { // root coroutine with launch println("Throwing exception from launch") throw In...
  - [kotlin-coroutines-exception-handling-14] It is possible to customize the default behavior of printing uncaught exceptions to the console. CoroutineExceptionHandler context element on a root coroutine can be used as a generic catch block for this root corouti...

## 段落样例
- [kotlin-coroutines-exception-handling-1] https://github.com/Kotlin/kotlinx.coroutines/edit/master/docs/topics/
- [kotlin-coroutines-exception-handling-2] This section covers exception handling and cancellation on exceptions. We already know that a cancelled coroutine throws CancellationException in suspension points and that it is ignored by the coroutines' machinery....
- [kotlin-coroutines-exception-handling-3] Exception propagation
- [kotlin-coroutines-exception-handling-4] Coroutine builders come in two flavors: propagating exceptions automatically ( launch ) or exposing them to users ( async and produce ). When these builders are used to create a root coroutine, that is not a child of...
- [kotlin-coroutines-exception-handling-5] It can be demonstrated by a simple example that creates root coroutines using the GlobalScope :
- [kotlin-coroutines-exception-handling-6] GlobalScope is a delicate API that can backfire in non-trivial ways. Creating a root coroutine for the whole application is one of the rare legitimate uses for GlobalScope , so you must explicitly opt-in into using Gl...
- [kotlin-coroutines-exception-handling-7] {style="note"}
- [kotlin-coroutines-exception-handling-8] import kotlinx.coroutines.* //sampleStart @OptIn(DelicateCoroutinesApi::class) fun main() = runBlocking { val job = GlobalScope.launch { // root coroutine with launch println("Throwing exception from launch") throw In...

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
