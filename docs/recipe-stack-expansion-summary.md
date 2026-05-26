# Recipe Stack Expansion Summary

**Start date**: 2026-05-26
**Completion date**: 2026-05-26

## Summary

- **Recipes added**: 30 new recipes (9 existing → 39 total)
- **Stacks expanded**: from 6 to 15 logical stacks
- **New stacks**: FastAPI, Pydantic, LangChain (4 recipes incl. LangGraph), Expo/React Native (4 recipes), Android (5 recipes incl. Gradle/Kotlin), HarmonyOS/ArkTS (10 recipes)
- **Code improvements**: `list` CLI sub-command, fuzzy fingerprint scoping fix, build recipe pipeline, lifecycle fingerprint tightening, empty search feedback

## Stack Breakdown

| Stack | Recipes Added | Key Topics |
|-------|---------------|------------|
| FastAPI | 4 | HTTPException 自定义处理、响应类选择、中间件 `call_next` 顺序、lifespan vs on_event |
| Pydantic | 3 | ValidationError 类型匹配、自定义错误消息、类前置定义缺失 |
| LangChain + LangGraph | 4 | OutputParserException、图递归限制、并发更新冲突、checkpointer 缺失 |
| Expo | 1 | Redbox 堆栈解析 |
| React Native | 3 | Metro 端口 8081 冲突、LogBox 致命错误、shell 命令无响应 |
| Android / Gradle / Kotlin | 5 | Daemon 连接失败、依赖解析冲突、JAVA_HOME 无效、Kotlin 空指针（Java 互操作）、require 前置条件检查 |
| HarmonyOS / ArkTS | 10 | ArkTS 静态模式语法限制（any/unknown、delete、for-in、逗号表达式、解构、catch 类型、未类型化字面量、var 用法）+ UIAbility 上下文未就绪、生命周期回调错误 |

> 注：`gradle` 和 `kotlin` 共享部分 recipe，CLI `list` 按 stack 标签展示时会重复计数。
> `harmonyos` 和 `arkts` 同理——同一套 ArkTS 语法 recipe 挂在两个 stack 标签下。

## Quality Metrics

- **109 tests pass**（0 失败、0 跳过）
- 所有 39 条 recipe 通过 `uv run recipe-importer check`
- 跨栈搜索返回相关结果：fastapi 验证错误、Metro bundler、ArkTS delete 限制、UIAbility 生命周期均能命中
- 模糊指纹（如 `error`、`failed`）已在 `cb7b968` 中收紧，跨栈误匹配风险降低

## Technical Improvements

### CLI 与工具
- 新增 `recipe-importer list` 子命令：按 stack 聚合展示 recipe 状态与数量
- `search` 支持 `--fresh-only` 过滤 stale recipe

### Build Recipe 管线
- 系统支持两种 recipe kind：`debug-recipe`（调试）和 `build-recipe`（构建约束）
- `generate-build-recipes` 命令可从 accepted debug recipe 批量反转生成候选 build recipe

### Pipeline 稳定性
- Manifest refresh 增强：`source_removed` / `final_url_changed` / `section_anchor_gone` 三类新 stale 条件
- 模糊指纹收紧（bug-fuzzy-fingerprint.md 记录）
- 生成 recipe 移除 EOF 空白行（fix render equivalence）

### 文档与计划
- `docs/research/ios-stack-research.md`、`docs/research/android-harmonyos-stack-research.md` 调研报告
- `docs/recipe-stack-expansion-plan.md` 实施计划
- `docs/recipe-stack-expansion-design.md` 扩栈设计规范

## Pending Actions

以下内容**已生成但未提交**，等待人工审阅后 commit：

- 30 条新 recipe 文件（`recipe-kb/accepted/`）
- 17 个 snapshot 目录（`recipe-kb/snapshots/`）
- `source-list.yml` 的源列表更新
- `recipe-kb/index.json` 重建
- `src/recipe_importer/llm.py`、`render.py` 的扩栈相关调整
- 测试文件调整（`tests/test_normalize_render.py`）

建议拆分 commit：
1. `feat(recipe): add HarmonyOS ArkTS recipes`
2. `feat(recipe): add Android/Gradle/Kotlin recipes`
3. `feat(recipe): add LangChain/LangGraph recipes`
4. `feat(recipe): add Expo/React Native recipes`
5. `feat(recipe): fastapi/pydantic stack`（如未含在 c54f23d）
6. `chore(recipe): rebuild index + update source list`

## Future Recommendations

- **iOS 栈**：调研已完成（`docs/research/ios-stack-research.md`），待选择合适源（Swift 编译错误文档、UIKit/SwiftUI 生命周期），预计可补 6-8 条 recipe
- **空搜索反馈**：当前 `search "nonexistent"` 无输出，建议加一行 "No recipes matched" 提示
- **跨栈 fingerprint 冲突**：ArkTS `onCreate` 与 Android `onCreate` 在关键词上不同（ArkTS 是 UIAbility 生命周期，Android 是 Activity 生命周期），目前 `arkts-uiability-lifecycle-callback-error` 已通过 `UIAbility` 前缀区分，但需要持续监控
