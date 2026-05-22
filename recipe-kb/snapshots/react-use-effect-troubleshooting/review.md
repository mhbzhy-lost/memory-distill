# 快照人审：react-use-effect-troubleshooting

## 快照质量检查
- 来源 URL: https://react.dev/reference/react/useEffect
- 最终 URL: https://react.dev/reference/react/useEffect
- 来源类型: official_doc
- 采集时间: 2026-05-21T09:50:51.121768Z
- HTTP 状态: 200
- 内容哈希: sha256:792a72c2435c730be340b1d22ce4c492555de366b153ab00c23201ad15937243
- 技术栈: react
- 抽取段落数: 190

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 190
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 4/4 条 expected_failure_hints

## 预期线索命中
- `Effect keeps re-running in an infinite cycle`
  - [react-use-effect-troubleshooting-17] Troubleshooting My Effect runs twice when the component mounts My Effect runs after every re-render My Effect keeps re-running in an infinite cycle My cleanup logic runs even though my component didn’t unmount My Effe...
  - [react-use-effect-troubleshooting-20] My Effect keeps re-running in an infinite cycle
- `Effect runs twice when the component mounts`
  - [react-use-effect-troubleshooting-17] Troubleshooting My Effect runs twice when the component mounts My Effect runs after every re-render My Effect keeps re-running in an infinite cycle My cleanup logic runs even though my component didn’t unmount My Effe...
  - [react-use-effect-troubleshooting-18] My Effect runs twice when the component mounts
- `missing cleanup function`
  - [react-use-effect-troubleshooting-27] setup : The function with your Effect’s logic. Your setup function may also optionally return a cleanup function. When your component commits , React will run your setup function. After every commit with changed depen...
  - [react-use-effect-troubleshooting-33] When Strict Mode is on, React will run one extra development-only setup+cleanup cycle before the first real setup. This is a stress-test that ensures that your cleanup logic “mirrors” your setup logic and that it stop...
  - [react-use-effect-troubleshooting-45] A setup function with setup code that connects to that system. It should return a cleanup function with cleanup code that disconnects from that system.
- `dependency changes on every render`
  - [react-use-effect-troubleshooting-142] By itself, creating a function from scratch on every re-render is not a problem. You don’t need to optimize that. However, if you use it as a dependency of your Effect, it will cause your Effect to re-run after every...
  - [react-use-effect-troubleshooting-168] If you’ve specified the dependency array but your Effect still re-runs in a loop, it’s because one of your dependencies is different on every re-render.
  - [react-use-effect-troubleshooting-173] When you find the dependency that is different on every re-render, you can usually fix it in one of these ways:

## 段落样例
- [react-use-effect-troubleshooting-1] useEffect
- [react-use-effect-troubleshooting-2] useEffect is a React Hook that lets you synchronize a component with an external system.
- [react-use-effect-troubleshooting-3] useEffect ( setup , dependencies ? )
- [react-use-effect-troubleshooting-4] Reference useEffect(setup, dependencies?)
- [react-use-effect-troubleshooting-5] useEffect(setup, dependencies?)
- [react-use-effect-troubleshooting-6] Usage Connecting to an external system Wrapping Effects in custom Hooks Controlling a non-React widget Fetching data with Effects Specifying reactive dependencies Updating state based on previous state from an Effect...
- [react-use-effect-troubleshooting-7] Connecting to an external system
- [react-use-effect-troubleshooting-8] Wrapping Effects in custom Hooks

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
