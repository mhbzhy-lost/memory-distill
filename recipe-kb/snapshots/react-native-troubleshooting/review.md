# 快照人审：react-native-troubleshooting

## 快照质量检查
- 来源 URL: https://reactnative.dev/docs/troubleshooting
- 最终 URL: https://reactnative.dev/docs/troubleshooting
- 来源类型: official_doc
- 采集时间: 2026-05-26T09:49:06.514472Z
- HTTP 状态: 200
- 内容哈希: sha256:7cb4f332f1238a16f040387fdc7ec127017be8769fbd249da9eb57c33c2e3dc6
- 技术栈: react-native
- 抽取段落数: 38

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 38
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 4/5 条 expected_failure_hints

## 预期线索命中
- `port 8081`
  - [react-native-troubleshooting-3] The Metro bundler runs on port 8081. If another process is already using that port, you can either terminate that process, or change the port that the bundler uses.
  - [react-native-troubleshooting-4] Run the following command to find the id for the process that is listening on port 8081:
  - [react-native-troubleshooting-8] On Windows you can find the process using port 8081 using Resource Monitor and stop it using Task Manager.
- `NPM locking error`
  - [react-native-troubleshooting-14] NPM locking error ​
- `ShellCommandUnresponsiveException`
  - [react-native-troubleshooting-29] If you encounter a ShellCommandUnresponsiveException exception such as:
  - [react-native-troubleshooting-30] Execution failed for task ':app:installDebug' . com . android . builder . testing . api . DeviceException : com . android . ddmlib . ShellCommandUnresponsiveException
- `ENOSPC inotify`：未找到直接段落命中
- `gradlew EACCES`
  - [react-native-troubleshooting-37] Error: spawnSync ./gradlew EACCES ​

## 段落样例
- [react-native-troubleshooting-1] These are some common issues you may run into while setting up React Native. If you encounter something that is not listed here, try searching for the issue in GitHub .
- [react-native-troubleshooting-2] Port already in use ​
- [react-native-troubleshooting-3] The Metro bundler runs on port 8081. If another process is already using that port, you can either terminate that process, or change the port that the bundler uses.
- [react-native-troubleshooting-4] Run the following command to find the id for the process that is listening on port 8081:
- [react-native-troubleshooting-5] sudo lsof -i :8081
- [react-native-troubleshooting-6] Then run the following to terminate the process:
- [react-native-troubleshooting-7] kill -9 < PID >
- [react-native-troubleshooting-8] On Windows you can find the process using port 8081 using Resource Monitor and stop it using Task Manager.

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
