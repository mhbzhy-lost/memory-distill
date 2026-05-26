# 快照人审：swift-sendable-closure-captures

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
- 最终 URL: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
- 来源类型: compiler_diagnostic
- 采集时间: 2026-05-26T13:49:14.876449Z
- HTTP 状态: 200
- 内容哈希: sha256:a286669a76a353b5d09aed60cc13cb75578b7e6da1bd412151dd1c482251cbf3
- 技术栈: swift, ios
- 抽取段落数: 20

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 20
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 4/4 条 expected_failure_hints

## 预期线索命中
- `reference to captured var in concurrently-executing code`
  - [swift-sendable-closure-captures-7] | callConcurrently { | print(result) | `- error: reference to captured var 'result' in concurrently-executing code | } | }
- `capture with non-Sendable type in a @Sendable closure`
  - [swift-sendable-closure-captures-5] func callConcurrently( _ closure: @escaping @Sendable () -> Void ) { ... } func capture() { var result = 0 result += 1 callConcurrently { print(result) } }
  - [swift-sendable-closure-captures-6] The compiler diagnoses the capture of result in a @Sendable closure:
  - [swift-sendable-closure-captures-10] If the type of the capture is Sendable and the closure only needs the value of the variable at the point of capture, resolve the error by explicitly capturing the variable by value in the closure's capture list:
- `data race`
  - [swift-sendable-closure-captures-3] @Sendable closures can be called multiple times concurrently, so any captured values must also be safe to access concurrently. To prevent data races, the compiler prevents capturing mutable values in a @Sendable closure.
- `nonisolated(unsafe)`
  - [swift-sendable-closure-captures-19] If you manually ensure data-race safety, such as by using an external synchronization mechanism, you can use nonisolated(unsafe) to opt out of concurrency checking:
  - [swift-sendable-closure-captures-20] class MyModel { func log() { ... } } func capture(model: MyModel) async { nonisolated(unsafe) let model = model callConcurrently { model.log() } }

## 段落样例
- [swift-sendable-closure-captures-1] Captures in a @Sendable closure (SendableClosureCaptures)
- [swift-sendable-closure-captures-2] Overview
- [swift-sendable-closure-captures-3] @Sendable closures can be called multiple times concurrently, so any captured values must also be safe to access concurrently. To prevent data races, the compiler prevents capturing mutable values in a @Sendable closure.
- [swift-sendable-closure-captures-4] For example:
- [swift-sendable-closure-captures-5] func callConcurrently( _ closure: @escaping @Sendable () -> Void ) { ... } func capture() { var result = 0 result += 1 callConcurrently { print(result) } }
- [swift-sendable-closure-captures-6] The compiler diagnoses the capture of result in a @Sendable closure:
- [swift-sendable-closure-captures-7] | callConcurrently { | print(result) | `- error: reference to captured var 'result' in concurrently-executing code | } | }
- [swift-sendable-closure-captures-8] Because the closure is marked @Sendable , the implementation of callConcurrently can call closure multiple times concurrently. For example, multiple child tasks within a task group can call closure concurrently:

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
