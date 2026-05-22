# 快照人审：react-invalid-hook-call

## 快照质量检查
- 来源 URL: https://react.dev/warnings/invalid-hook-call-warning
- 最终 URL: https://react.dev/warnings/invalid-hook-call-warning
- 来源类型: official_error_doc
- 采集时间: 2026-05-21T09:50:51.121768Z
- HTTP 状态: 200
- 内容哈希: sha256:b7afbb06f1a96c40bc0a40aa31761ccd6c59714f51dac3f5699d8eabed3ae966
- 技术栈: react
- 抽取段落数: 40

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 40
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 4/4 条 expected_failure_hints

## 预期线索命中
- `invalid hook call`
  - [react-invalid-hook-call-12] ✅ Call them at the top level in the body of a custom Hook .
- `Hooks can only be called inside the body of a function component`
  - [react-invalid-hook-call-10] Don’t call Hooks inside loops, conditions, or nested functions. Instead, always use Hooks at the top level of your React function, before any early returns. You can only call Hooks while React is rendering a function...
  - [react-invalid-hook-call-25] Custom Hooks may call other Hooks (that’s their whole purpose). This works because custom Hooks are also supposed to only be called while a function component is rendering.
- `mismatching versions of React and React DOM`
  - [react-invalid-hook-call-5] You might have mismatching versions of React and React DOM.
  - [react-invalid-hook-call-26] Mismatching Versions of React and React DOM
- `more than one copy of React`
  - [react-invalid-hook-call-6] You might have more than one copy of React in the same app.

## 段落样例
- [react-invalid-hook-call-1] Rules of Hooks
- [react-invalid-hook-call-2] You are probably here because you got the following error message:
- [react-invalid-hook-call-3] There are three common reasons you might be seeing it:
- [react-invalid-hook-call-4] You might be breaking the Rules of Hooks .
- [react-invalid-hook-call-5] You might have mismatching versions of React and React DOM.
- [react-invalid-hook-call-6] You might have more than one copy of React in the same app.
- [react-invalid-hook-call-7] Let’s look at each of these cases.
- [react-invalid-hook-call-8] Breaking Rules of Hooks

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
