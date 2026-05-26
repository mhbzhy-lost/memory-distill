# 快照人审：gradle-build-troubleshooting

## 快照质量检查
- 来源 URL: https://docs.gradle.org/current/userguide/troubleshooting.html
- 最终 URL: https://docs.gradle.org/current/userguide/troubleshooting.html
- 来源类型: build_tool_doc
- 采集时间: 2026-05-26T10:27:19.494775Z
- HTTP 状态: 200
- 内容哈希: sha256:7a0f5a82df53b091cfb83042457b8ace9cf9c71a6e83f50ce248232ad6d51c98
- 技术栈: android, kotlin, gradle
- 抽取段落数: 62

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 62
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 6/7 条 expected_failure_hints

## 预期线索命中
- `Command not found gradle`
  - [gradle-build-troubleshooting-10] Command not found: gradle
  - [gradle-build-troubleshooting-11] If you get "command not found: gradle", you must ensure that Gradle is correctly added to your PATH .
  - [gradle-build-troubleshooting-51] If you’re using Buildship for the Eclipse IDE, you can re-synchronize your Gradle build by opening the "Gradle Tasks" view and clicking the "Refresh" icon, or by executing the Gradle > Refresh Gradle Project command f...
- `JAVA_HOME is set to an invalid directory`
  - [gradle-build-troubleshooting-12] JAVA_HOME is set to an invalid directory
  - [gradle-build-troubleshooting-14] ERROR: JAVA_HOME is set to an invalid directory
- `Permission denied wrapper not executable`
  - [gradle-build-troubleshooting-20] If you get "permission denied", that means that Gradle likely exists in the correct place, but it is not executable. You can fix this using chmod +x path/to/executable on *nix-based systems.
- `A new daemon was started but could not be connected to`
  - [gradle-build-troubleshooting-55] Starting a Gradle Daemon, 1 stopped Daemon could not be reused, use --status for details FAILURE: Build failed with an exception. * What went wrong: A new daemon was started but could not be connected to: pid=DaemonIn...
- `Task executed when it should have been UP-TO-DATE`
  - [gradle-build-troubleshooting-43] Task executed when it should have been UP-TO-DATE
- `dependency resolution conflict`
  - [gradle-build-troubleshooting-24] Debugging dependency resolution
  - [gradle-build-troubleshooting-25] You can see a dependency tree and see which resolved dependency versions differed from what was requested by clicking the Dependencies view and using the search functionality, specifying the resolution reason.
- `IntelliJ Gradle sync failure`：未找到直接段落命中

## 段落样例
- [gradle-build-troubleshooting-1] Troubleshooting builds
- [gradle-build-troubleshooting-2] The following is a collection of common issues and suggestions for addressing them. You can get other tips and search the Gradle forums and StackOverflow #gradle answers.
- [gradle-build-troubleshooting-3] Troubleshooting the installation
- [gradle-build-troubleshooting-4] If you followed the installation instructions , and aren’t able to execute your Gradle build, here are some tips that may help.
- [gradle-build-troubleshooting-5] If you installed Gradle outside of just invoking the Gradle Wrapper , you can check your Gradle installation by running gradle --version in a terminal.
- [gradle-build-troubleshooting-6] You should see something like this:
- [gradle-build-troubleshooting-7] $ ./gradlew --version
- [gradle-build-troubleshooting-8] ------------------------------------------------------------ Gradle {gradleVersion} ------------------------------------------------------------ Build time: 2025-05-13 06:56:13 UTC Revision: 3c890746756262d3778e12eaa5...

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
