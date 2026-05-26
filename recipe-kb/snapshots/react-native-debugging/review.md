# 快照人审：react-native-debugging

## 快照质量检查
- 来源 URL: https://reactnative.dev/docs/debugging
- 最终 URL: https://reactnative.dev/docs/debugging
- 来源类型: official_doc
- 采集时间: 2026-05-26T09:49:06.514472Z
- HTTP 状态: 200
- 内容哈希: sha256:39ed7cb1f1038ca09637786e97ed5894f08c2b655c1358dddf7aba43ab9d64bc
- 技术栈: react-native
- 抽取段落数: 32

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 32
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 5/5 条 expected_failure_hints

## 预期线索命中
- `Dev Menu`
  - [react-native-debugging-1] Debugging features, such as the Dev Menu, LogBox, and React Native DevTools are disabled in release (production) builds.
  - [react-native-debugging-2] React Native provides an in-app developer menu providing access to debugging features. You can access the Dev Menu by shaking your device or via keyboard shortcuts:
  - [react-native-debugging-9] Select "Open DevTools" in the Dev Menu.
- `React Native DevTools`
  - [react-native-debugging-1] Debugging features, such as the Dev Menu, LogBox, and React Native DevTools are disabled in release (production) builds.
  - [react-native-debugging-7] React Native DevTools is our built-in debugger for React Native. It allows you to inspect and understand how your JavaScript code is running, similar to a web browser.
  - [react-native-debugging-12] Learn more in our React Native DevTools guide .
- `LogBox`
  - [react-native-debugging-1] Debugging features, such as the Dev Menu, LogBox, and React Native DevTools are disabled in release (production) builds.
  - [react-native-debugging-13] LogBox ​
  - [react-native-debugging-14] LogBox is an in-app tool that displays when warnings or errors are logged by your app.
- `Performance Monitor`
  - [react-native-debugging-30] Performance Monitor ​
  - [react-native-debugging-32] The Performance Monitor runs in-app and is a guide. We recommend investigating the native tooling under Android Studio and Xcode for accurate performance measurements.
- `JavaScript debugger`
  - [react-native-debugging-7] React Native DevTools is our built-in debugger for React Native. It allows you to inspect and understand how your JavaScript code is running, similar to a web browser.
  - [react-native-debugging-11] On first launch, DevTools will open to a welcome panel, along with an open console drawer where you can view logs and interact with the JavaScript runtime. From the top of the window, you can navigate to other panels,...
  - [react-native-debugging-16] When an unrecoverable error occurs, such as a JavaScript syntax error, LogBox will open with the location of the error. In this state, LogBox is not dismissable since your code cannot be executed. LogBox will automati...

## 段落样例
- [react-native-debugging-1] Debugging features, such as the Dev Menu, LogBox, and React Native DevTools are disabled in release (production) builds.
- [react-native-debugging-2] React Native provides an in-app developer menu providing access to debugging features. You can access the Dev Menu by shaking your device or via keyboard shortcuts:
- [react-native-debugging-3] iOS Simulator: Ctrl + Cmd ⌘ + Z (or Device > Shake)
- [react-native-debugging-4] Android emulators: Cmd ⌘ + M (macOS) or Ctrl + M (Windows and Linux)
- [react-native-debugging-5] Alternative (Android): adb shell input keyevent 82 .
- [react-native-debugging-6] Opening DevTools ​
- [react-native-debugging-7] React Native DevTools is our built-in debugger for React Native. It allows you to inspect and understand how your JavaScript code is running, similar to a web browser.
- [react-native-debugging-8] To open DevTools, either:

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
