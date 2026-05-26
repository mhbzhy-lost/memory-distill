# 快照人审：expo-errors-and-warnings

## 快照质量检查
- 来源 URL: https://docs.expo.dev/debugging/errors-and-warnings/
- 最终 URL: https://docs.expo.dev/debugging/errors-and-warnings/
- 来源类型: official_doc
- 采集时间: 2026-05-26T09:52:36.774688Z
- HTTP 状态: 200
- 内容哈希: sha256:1a64441c0947d0727576d06949f8f99076c18493b202e0c418223bcd9dc2325a
- 技术栈: expo, react-native
- 抽取段落数: 15

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 15
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 5/5 条 expected_failure_hints

## 预期线索命中
- `Redbox`
  - [expo-errors-and-warnings-4] Learn about Redbox errors and stack traces in your Expo project.
  - [expo-errors-and-warnings-6] When developing an application using Expo, you'll encounter a Redbox error or Yellowbox warning. These logging experiences are provided by LogBox in React Native .
  - [expo-errors-and-warnings-7] Redbox error and Yellowbox warning
- `Yellowbox`
  - [expo-errors-and-warnings-6] When developing an application using Expo, you'll encounter a Redbox error or Yellowbox warning. These logging experiences are provided by LogBox in React Native .
  - [expo-errors-and-warnings-7] Redbox error and Yellowbox warning
  - [expo-errors-and-warnings-8] A Redbox error is displayed when a fatal error prevents your app from running. A Yellowbox warning is displayed to inform you that there is a possible issue and you should probably resolve it before shipping your app.
- `stack trace`
  - [expo-errors-and-warnings-4] Learn about Redbox errors and stack traces in your Expo project.
  - [expo-errors-and-warnings-11] Stack traces
  - [expo-errors-and-warnings-12] When you encounter an error during development, you'll see the error message and a stack trace , which is a report of the recent calls your application made when it crashed. This stack trace is shown both in your term...
- `console.warn`
  - [expo-errors-and-warnings-9] You can also create warnings and errors on your own with console.warn("Warning message") and console.error("Error message") . Another way to trigger the redbox is to throw an error and not catch it: throw Error("Error...
- `console.error`
  - [expo-errors-and-warnings-9] You can also create warnings and errors on your own with console.warn("Warning message") and console.error("Error message") . Another way to trigger the redbox is to throw an error and not catch it: throw Error("Error...

## 段落样例
- [expo-errors-and-warnings-1] Errors and warnings
- [expo-errors-and-warnings-2] Edit page
- [expo-errors-and-warnings-3] Copy page
- [expo-errors-and-warnings-4] Learn about Redbox errors and stack traces in your Expo project.
- [expo-errors-and-warnings-5] For the complete documentation index, see llms.txt . Use this file to discover all available pages.
- [expo-errors-and-warnings-6] When developing an application using Expo, you'll encounter a Redbox error or Yellowbox warning. These logging experiences are provided by LogBox in React Native .
- [expo-errors-and-warnings-7] Redbox error and Yellowbox warning
- [expo-errors-and-warnings-8] A Redbox error is displayed when a fatal error prevents your app from running. A Yellowbox warning is displayed to inform you that there is a possible issue and you should probably resolve it before shipping your app.

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
