# 快照人审：swift-actor-isolated-call

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
- 最终 URL: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
- 来源类型: compiler_diagnostic
- 采集时间: 2026-05-26T13:49:14.876449Z
- HTTP 状态: 200
- 内容哈希: sha256:06ccf6de3da653f54783ac7d9cccf99e6e18bfd9c422d51efb025a5ad35f22f7
- 技术栈: swift, ios
- 抽取段落数: 13

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 13
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 2/3 条 expected_failure_hints

## 预期线索命中
- `actor-isolated property can not be referenced from a non-isolated context`：未找到直接段落命中
- `call to main actor-isolated method`
  - [swift-actor-isolated-call-1] Calling an actor-isolated method from a synchronous nonisolated context (ActorIsolatedCall)
  - [swift-actor-isolated-call-4] Calls to actor-isolated methods from outside the actor must be done asynchronously. Otherwise, access to actor state can happen concurrently and lead to data races. These rules also apply to global actors like the mai...
  - [swift-actor-isolated-call-7] Building the above code produces an error about calling a main actor isolated method from outside the actor:
- `actor isolation violation`
  - [swift-actor-isolated-call-9] The runUpdate function doesn't specify any actor isolation, so it is nonisolated by default. nonisolated methods can be called from any concurrency domain. To prevent data races, nonisolated methods cannot access acto...
  - [swift-actor-isolated-call-10] To resolve the error, runUpdate has to make sure the call to model.update() is on the main actor. One way to do that is to add main actor isolation to the runUpdate function:

## 段落样例
- [swift-actor-isolated-call-1] Calling an actor-isolated method from a synchronous nonisolated context (ActorIsolatedCall)
- [swift-actor-isolated-call-2] Overview
- [swift-actor-isolated-call-3] Accessing actor-isolated state from outside the actor can cause data races in your program. Resolve this error by calling actor-isolated functions on the actor.
- [swift-actor-isolated-call-4] Calls to actor-isolated methods from outside the actor must be done asynchronously. Otherwise, access to actor state can happen concurrently and lead to data races. These rules also apply to global actors like the mai...
- [swift-actor-isolated-call-5] For example:
- [swift-actor-isolated-call-6] @MainActor class MyModel { func update() { ... } } func runUpdate(model: MyModel) { model.update() }
- [swift-actor-isolated-call-7] Building the above code produces an error about calling a main actor isolated method from outside the actor:
- [swift-actor-isolated-call-8] | func runUpdate(model: MyModel) { | model.update() | `- error: call to main actor-isolated instance method 'update()' in a synchronous nonisolated context | }

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
