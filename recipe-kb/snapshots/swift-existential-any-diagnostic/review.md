# 快照人审：swift-existential-any-diagnostic

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
- 最终 URL: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
- 来源类型: compiler_diagnostic
- 采集时间: 2026-05-26T13:49:14.876449Z
- HTTP 状态: 200
- 内容哈希: sha256:69d0360842059387e92ca5d1c1cec7a0040ab1a9e67d7084aaaf1ed50c661bbe
- 技术栈: swift, ios
- 抽取段落数: 14

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 14
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 2/3 条 expected_failure_hints

## 预期线索命中
- `'any' existential type syntax missing`
  - [swift-existential-any-diagnostic-2] any existential type syntax.
  - [swift-existential-any-diagnostic-4] any was introduced in Swift 5.6 to explicitly mark "existential types", i.e., abstract boxed types that conform to a set of constraints. For source compatibility, these are not diagnosed by default except for existent...
- `protocol used as a type requires any`：未找到直接段落命中
- `ExistentialAny upcoming feature`
  - [swift-existential-any-diagnostic-6] When enabled via -enable-upcoming-feature ExistentialAny , the upcoming language feature ExistentialAny will diagnose all existential types without any :
  - [swift-existential-any-diagnostic-10] -enable-upcoming-feature ExistentialAny:migrate

## 段落样例
- [swift-existential-any-diagnostic-1] Existential any (ExistentialAny)
- [swift-existential-any-diagnostic-2] any existential type syntax.
- [swift-existential-any-diagnostic-3] Overview
- [swift-existential-any-diagnostic-4] any was introduced in Swift 5.6 to explicitly mark "existential types", i.e., abstract boxed types that conform to a set of constraints. For source compatibility, these are not diagnosed by default except for existent...
- [swift-existential-any-diagnostic-5] protocol Foo { associatedtype Bar func foo(_: Bar) } protocol Baz {} func pass(foo: Foo) {} // `any Foo` is required instead of `Foo` func pass(baz: Baz) {} // no warning or error by default for source compatibility
- [swift-existential-any-diagnostic-6] When enabled via -enable-upcoming-feature ExistentialAny , the upcoming language feature ExistentialAny will diagnose all existential types without any :
- [swift-existential-any-diagnostic-7] func pass(baz: Baz) {} // `any Baz` required instead of `Baz`
- [swift-existential-any-diagnostic-8] This will become the default in a future language mode.

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
