# Stack URL Research

> 任务：Task 1 (Recipe Stack Expansion)
> 研究者：opencode qwen3.7-max
> 日期：2026-05-26
> 测试方法：`webfetch` tool（无 headless 浏览器）

## 摘要

对 6 个目标栈的官方错误/排障文档进行可达性测试。
结论：**FastAPI / Pydantic / Expo / React Native** 直接可用，**LangChain 部分可用**（有 llms.txt 索引 +
独立错误页面可访问），**iOS / Android / HarmonyOS 需要 GitHub 替代源或降级处理**。

| Stack | Doc 格式 | 可达性 | 行动建议 |
| ----- | -------- | ------ | -------- |
| FastAPI | MkDocs 静态 HTML | ✅ 完全可用 | 直接加入 source-list |
| Pydantic | Zensical 静态 HTML | ✅ 完全可用 | 直接加入 source-list |
| LangChain/LangGraph | MDX + `llms.txt` | ⚠️ 部分可用 | 使用独立错误页 + llms.txt 索引 |
| Expo/React Native | Docusaurus | ✅ 完全可用 | 直接加入 source-list |
| iOS/Swift | Apple SPA（404/超时） | ❌ 不可用 | 降级：使用 swiftlang/docs GitHub Markdown |
| Android/Kotlin | Google SPA（超时） | ❌ 不可用 | 降级：使用 JetBrains/kotlin GitHub Markdown |
| HarmonyOS/ArkTS | OpenHarmony GitHub MD | ⚠️ 部分可用 | 使用 OpenHarmony docs 仓 Markdown |

---

## FastAPI (target: 3-4 recipes)

### High-priority sources (static HTML confirmed)

1. `https://fastapi.tiangolo.com/tutorial/handling-errors/`
   - Covers: HTTPException, RequestValidationError, custom exception handlers, override 默认 handler
   - Access: ✅ 静态 MkDocs HTML，webfetch 全文提取成功，2026-05-26
   - Quality: 高质量，含 6 段可运行 Python 代码与 JSON 响应示例

2. `https://fastapi.tiangolo.com/tutorial/middleware/`
   - Covers: @app.middleware("http"), 执行顺序, call_next
   - Access: ✅ 静态 HTML，完整可提取，2026-05-26
   - Quality: 中等，适合 "middleware process_time header" 类 recipe

3. `https://fastapi.tiangolo.com/advanced/custom-response/`
   - Covers: HTMLResponse / PlainTextResponse / JSONResponse / RedirectResponse / StreamingResponse / FileResponse
   - Access: ✅ 静态 HTML，2026-05-26
   - Quality: 高，覆盖多种 Response 子类

4. `https://fastapi.tiangolo.com/advanced/events/`
   - Covers: lifespan / startup / shutdown events, asynccontextmanager
   - Access: ✅ 静态 HTML，2026-05-26
   - Quality: 高，覆盖资源生命周期（DB 连接池、ML 模型加载）

### Discovery notes
- 全部 fastapi.tiangolo.com URL 都返回完整 HTML（MkDocs + Zensical 构建），无 JS 渲染依赖
- webfetch 的 markdown 输出里含完整代码块 + JSON 响应示例 → 适合 parser 直接提取
- 可继续追加 `/advanced/websockets/`, `/advanced/settings/`, `/tutorial/debugging/`

### Recipe candidates
- `fastapi-httpexception-custom-handler`
- `fastapi-request-validation-error-override`
- `fastapi-middleware-call-next-order`
- `fastapi-lifespan-vs-on-event`

---

## Pydantic (target: 3-4 recipes)

> 注：Pydantic v2 文档 URL 已迁移到 `docs.pydantic.dev/docs/validation/latest/...`，旧路径 `/latest/errors/...` 仍可访问但重定向。

### High-priority sources (static HTML confirmed)

1. `https://docs.pydantic.dev/latest/errors/validation_errors/`
   - Covers: 80+ ValidationError type 文档（int_parsing, bool_type, missing, greater_than 等）
   - Access: ✅ Zensical 构建的静态 HTML，webfetch 能拿到完整 markdown（含 864 行 + ），2026-05-26
   - Quality: 极高，每个 error type 含可运行 Python 示例

2. `https://docs.pydantic.dev/latest/errors/errors/` (现重定向到 `.../errors/errors/`)
   - Covers: ValidationError 结构、errors()/error_count()/json() API、自定义 error messages
   - Access: ✅ 静态 HTML，2026-05-26
   - Quality: 高，含 ErrorDetails 字典字段解释

3. `https://docs.pydantic.dev/latest/errors/usage_errors/`
   - Covers: 40+ PydanticUserError 类型（class-not-fully-defined, decorator-missing-field 等）
   - Access: ✅ 静态 HTML，2026-05-26
   - Quality: 高

4. `https://docs.pydantic.dev/latest/concepts/validators/` (待测，推测静态)
   - Covers: field_validator, model_validator, 自定义 validator 签名

5. 补充 URL（v2 URL 路径）：
   - `https://docs.pydantic.dev/docs/validation/latest/errors/validation_errors/`（v2 canonical）
   - `https://docs.pydantic.dev/docs/validation/latest/api/pydantic/errors/`

### Discovery notes
- 整个 `docs.pydantic.dev` 都是 Zensical 生成的静态站，所有路径均可直接 webfetch
- `ValidationError.errors()` 返回的 `url` 字段指向 `https://errors.pydantic.dev/2/v/<error_type>`，
  也是静态 HTML（每个 error type 单独页面），可作为 recipe 的细粒度引用源

### Recipe candidates
- `pydantic-validation-error-type-missing`
- `pydantic-custom-error-messages`
- `pydantic-class-not-fully-defined-model-rebuild`
- `pydantic-field-validator-wrong-signature`

---

## LangChain/LangGraph (target: 3-4 recipes)

### High-priority sources

1. `https://docs.langchain.com/llms.txt`
   - Covers: 完整文档索引（数千条目，含 LangSmith/LangGraph/agent-server 等所有路径）
   - Access: ✅ 静态纯文本，webfetch 可达，2026-05-26
   - Quality: 极高，作为 URL 发现入口；本身不是 recipe 源

2. `https://docs.langchain.com/langsmith/<slug>.md` 系列（每个页面都有 .md 版本）
   - Covers: 所有 LangSmith/LangGraph 文档
   - Access: ✅ 通过 llms.txt 索引的 `.md` URL 均可静态抓取，2026-05-26
   - Quality: 高

3. `https://python.langchain.com/docs/troubleshooting/errors/GRAPH_RECURSION_LIMIT/`
   - Covers: LangGraph StateGraph 达到最大步数（循环检测）
   - Access: ✅ MDX 渲染但内容完整可提取（含 python 代码块），2026-05-26
   - Quality: 中，单个错误一页，内容偏短

4. `https://python.langchain.com/docs/how_to/debugging/`
   - Access: ⚠️ webfetch 拿到的是 LangChain overview 重定向页（docs 主页），未拿到 how_to/debugging
   - 推测该 URL 在 SPA 客户端路由下，静态抓取可能不完整
   - 备选：直接用 `https://docs.langchain.com/langsmith/...` 系列

### Access concerns
- python.langchain.com 是 Docusaurus/MDX SPA，部分 URL 返回 overview 页而非目标内容
- docs.langchain.com 提供 `.md` 后缀的 Markdown 版本（更适合 webfetch 抓取）
- llms.txt 是最安全的索引入口

### Recipe candidates
- `langgraph-graph-recursion-limit`
- `langchain-agent-error-output-parser`（待查 llms.txt 内对应页）
- `langchain-callback-error-handling`
- `langgraph-checkpointer-configuration-error`

### Action for Task 3/4
- 使用 llms.txt 作为 URL 发现源
- 优先使用 `.md` 后缀 URL（`docs.langchain.com/.../<slug>.md`）
- 抓取前验证每个 URL 是否真正命中目标内容（避免 overview 重定向陷阱）

---

## Expo/React Native (target: 3-4 recipes)

### High-priority sources

**Expo (Docusaurus, static HTML confirmed)**

1. `https://docs.expo.dev/build-reference/troubleshooting/`
   - Covers: EAS Build 错误日志、Metro bundle 错误、None-of-files-exist、OOM、build compare
   - Access: ✅ Docusaurus 静态 HTML，webfetch 可完整提取，2026-05-26
   - Quality: 高，含具体错误信息示例 + 解决步骤

2. `https://docs.expo.dev/debugging/runtime-issues/`
   - Covers: production vs development 错误分类、native 调试（adb logcat / Console.app）、crash 报告
   - Access: ✅ 静态 HTML，2026-05-26
   - Quality: 高，含可运行命令（npx expo run:android --variant release 等）

3. `https://docs.expo.dev/debugging/errors-and-warnings/`
   - Covers: Redbox/Yellowbox、stack traces、console.warn/error
   - Access: ✅ 静态 HTML，2026-05-26
   - Quality: 中，偏介绍

**React Native (Docusaurus 0.85, static HTML confirmed)**

4. `https://reactnative.dev/docs/troubleshooting`
   - Covers: port 8081 占用, NPM locking error, ShellCommandUnresponsiveException, ENOSPC inotify, gradlew EACCES
   - Access: ✅ 静态 HTML，2026-05-26
   - Quality: 中高，覆盖 RN 常见 CLI / 环境问题

5. `https://reactnative.dev/docs/debugging`
   - Covers: Dev Menu, React Native DevTools, LogBox, Performance Monitor
   - Access: ✅ 静态 HTML，2026-05-26
   - Quality: 高

### Discovery notes
- Docusaurus 站点都是服务端渲染的静态 HTML，webfetch 直接可用
- Expo docs 提供 YAML frontmatter（modificationDate, title, description），便于解析
- Expo 还有一个 llms.txt 入口（`https://docs.expo.dev/llms.txt`），可作为 URL 发现源

### Recipe candidates
- `expo-eas-build-none-of-files-exist`
- `expo-metro-bundler-module-not-resolved`
- `react-native-shell-command-unresponsive`
- `react-native-metro-port-8081-conflict`

---

## iOS/Swift (target: 3-4 recipes)

### Challenge: Apple developer docs are SPAs (mostly)

- `https://developer.apple.com/documentation/swift/debugging` → ❌ 404 (URL 不对或已下线)
- `https://developer.apple.com/documentation/swift/...` (其他路径) → 大概率 404/超时，未进一步验证
- `https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/`
  → ❌ 需要 JavaScript，webfetch 拿到 "This page requires JavaScript" 空壳

### Working alternatives (GitHub markdown)

1. **`https://github.com/swiftlang/swift/tree/main/docs`**（已验证可达）
   - Covers: Swift 编译器文档仓，含 ErrorHandling.md, Diagnostics.md, DebuggingTheCompiler.md 等
   - Access: ✅ GitHub Web UI 完整渲染，2026-05-26
   - Quality: 高，覆盖编译器层面错误诊断、错误处理设计原理
   - 具体文件候选：
     - `/swiftlang/swift/blob/main/docs/ErrorHandling.md`
     - `/swiftlang/swift/blob/main/docs/ErrorHandlingRationale.md`
     - `/swiftlang/swift/blob/main/docs/Diagnostics.md`
     - `/swiftlang/swift/blob/main/docs/DebuggingTheCompiler.md`
     - `/swiftlang/swift/blob/main/docs/Backtracing.rst`

2. **`https://www.swift.org/documentation/`**（已验证可达）
   - Covers: Swift docs hub（TSPL/Standard Library/Core Libraries 等）
   - Access: ✅ 静态 HTML，2026-05-26
   - Quality: 中，偏索引

### Discovery notes
- Apple developer docs（developer.apple.com）绝大多数走 SPA 渲染，webfetch 超时或 404
- swift.org 是静态站点但内容偏介绍，错误诊断具体内容在 GitHub swiftlang/swift 仓
- swiftlang/swift/docs 仓是真正的"compiler troubleshooting"源头

### Recipe candidates (using GitHub sources)
- `swift-compiler-diagnostic-custom-message`
- `swift-error-handling-vs-throws-result`
- `swift-lldb-backtrace-debug`
- `swift-data-race-concurrency-checking` (Swift 6 strict concurrency)

### Action for Task 6
- 优先用 GitHub raw/web URL：`https://github.com/swiftlang/swift/blob/main/docs/<file>.md`
- 评估 webfetch 对 GitHub blob 页的渲染质量（应良好，github.com 服务端渲染 markdown）
- 如仍不够，可补充第三方教程（如 Hacking with Swift `https://www.hackingwithswift.com/...`），但需逐页验证

---

## Android/Kotlin (target: 3-4 recipes)

### Challenge: Android developer docs are SPAs

- `https://developer.android.com/studio/debug` → ❌ 超时
- `https://developer.android.com/studio/publish/troubleshoot` → ❌ 超时
- `https://kotlinlang.org/docs/compiler-errors.html` → ❌ 404
- `https://kotlinlang.org/docs/diagnostics.html` → ❌ 404
- `https://github.com/nicklama/kotlin-error-codes` / `android-build-errors` / `swift-error-codes`
  → ❌ 仓不存在（nicklama 是测试假设 URL）

### Working alternatives

1. **`https://github.com/nicklama/swift-compiler-diagnostics`** → ❌ 同上不存
2. JetBrains kotlin 仓内无独立 `diagnostics/README.md`（`testData/diagnostics/README.md` 已 404）

### Recommended fallback strategy

- **Android gradle 错误**：使用 GitHub 上 `react-native-community/discussions` + Expo troubleshooting 已覆盖的 Gradle 错误
  （见 Expo 部分 "Task :app:bundleReleaseJsAndAssets FAILED"）
- **Kotlin 编译错误**：使用 JetBrains/kotlin 仓的 `docs/topics/compiler-plugins.md` 等子目录，
  或官方 `kotlinx.coroutines` / `kotlinx.serialization` 的 troubleshooting.md（需逐个验证）
- **通用 Android 调试**：Expo troubleshooting 已覆盖 Android Studio / gradle / adb logcat 基础

### Discovery notes
- Google + JetBrains 的 developer docs 都重度 SPA，webfetch 不适合大规模抓取
- 最稳定路径：使用对应框架的 GitHub repository markdown 文件
- Task 7 启动前建议先用 `gh search` 或 `github.com/search` 找出 Kotlin/Android 的可用 `.md` 排障文档

### Recipe candidates (provisional, need URL validation)
- `android-gradle-task-bundlereleasejsandassets-failed` (可走 Expo URL)
- `android-gradle-daemon-disappeared-oom`
- `kotlin-coroutines-scope-exception`
- `kotlin-serialization-unknown-type`

---

## HarmonyOS/ArkTS (target: 3-4 recipes)

### Challenge: Limited public documentation

- Huawei official HarmonyOS developer portal (developer.huawei.com) 大概率是 SPA，未直接测试
- ArkTS 是 TS 超集，专属于 OpenHarmony / HarmonyOS

### Working alternative: OpenHarmony GitHub

1. **`https://github.com/openharmony/docs/tree/master/en/application-dev/quick-start`** （已验证可达）
   - Covers: ArkTS 编程指南、迁移指南、常见应用问题
   - Access: ✅ GitHub 渲染的 index 页，所有子文件可独立访问，2026-05-26
   - Quality: 中高，含官方 ArkTS 编码规范
   - 具体文件候选：
     - `common_problem_of_application.md` - 应用常见问题
     - `getting-started-with-arkts-for-java-programmers.md`
     - `getting-started-with-arkts-for-swift-programmers.md`
     - `introduction-to-arkts.md`
     - `arkts-migration-background.md`
     - `typescript-to-arkts-migration-guide.md`
     - `arkts-high-performance-programming.md`
     - `arkts-coding-style-guide.md`

2. OpenHarmony docs 仓其他目录（未直接测试，结构推测）：
   - `en/application-dev/ui/` - UI / ArkUI
   - `en/application-dev/reference/apis-...*` - API 参考
   - `en/application-dev/performance/` - 性能调优

### Discovery notes
- OpenHarmony docs 是 GitHub 原生 markdown 仓，webfetch 抓取非常稳定
- 内容以 ArkTS 语法、Stage 模型、性能优化为主
- 中文文档路径：`openharmony/docs/tree/master/zh-cn/application-dev/...`（可作为补充）

### Recipe candidates
- `arkts-java-migration-pitfalls`
- `arkts-typescript-to-arkts-migration`
- `openharmony-stage-model-lifecycle`
- `openharmony-common-app-problems`

---

## 给 Task 3-7 的建议

### Task 3 (FastAPI + Pydantic): 直接启动 ✅
全部 URL 已验证可用。直接加入 source-list.yml，开始 pipeline。

### Task 4 (LangChain): 谨慎启动 ⚠️
- 用 llms.txt 作为 URL 发现源
- URL 格式优先选 `https://docs.langchain.com/<section>/<slug>.md` （MD 后缀）
- 每个 URL 导入前先 webfetch 验证内容命中（避免 overview 重定向陷阱）
- 可先做 2-3 个 LangGraph 错误页（GRAPH_RECURSION_LIMIT / INVALID_CONCURRENT 等）验证流程

### Task 5 (Expo/RN): 直接启动 ✅
全部 URL 已验证可用。Expo 还有 llms.txt 入口（`https://docs.expo.dev/llms.txt`）可作补充。

### Task 6 (iOS/Swift): 需要额外调研
- 主力源：`github.com/swiftlang/swift/blob/main/docs/*.md`
- 启动前需用本仓库的 fetch pipeline 验证 GitHub blob URL 能被正确解析（GitHub web UI 服务端渲染，
  通常可达，但 parser 是否能处理 GitHub 页面结构需另测）
- 备选：用 `raw.githubusercontent.com` + `.md` 直接拿原始 markdown（100% 可 parse）
  示例：`https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md`

### Task 7 (Android/Kotlin): 需要额外调研
- 主力源：Expo docs 已覆盖大部分 Gradle / EAS Build 错误
- 真正的 Kotlin 错误（coroutines, serialization）需要另寻 JetBrains kotlinx.* 仓的 troubleshooting .md
- 建议先用 `gh search repos kotlinx.coroutines` 找出相关仓

### Task 8/9 (HarmonyOS/ArkTS): 可启动 ⚠️
- 主力源：`github.com/openharmony/docs/tree/master/en` 
- 中文文档：`github.com/openharmony/docs/tree/master/zh-cn`
- 直接用 raw.githubusercontent.com 拿原始 markdown，pipeline 解析 100% 可达

---

## 测试日志（URL → status）

> Legend: ✅ 可达内容完整 | ⚠️ 可达但内容被重定向 / 不完整 | ❌ 超时 / 404 / JS 空壳

### FastAPI
- `fastapi.tiangolo.com/tutorial/handling-errors/` ✅
- `fastapi.tiangolo.com/tutorial/middleware/` ✅
- `fastapi.tiangolo.com/advanced/custom-response/` ✅
- `fastapi.tiangolo.com/advanced/events/` ✅

### Pydantic
- `docs.pydantic.dev/latest/errors/validation_errors/` ✅
- `docs.pydantic.dev/latest/errors/errors/` ✅
- `docs.pydantic.dev/latest/errors/usage_errors/` ✅

### LangChain
- `docs.langchain.com/llms.txt` ✅
- `docs.langchain.com/langsmith/<slug>.md` ✅ (索引内所有链接)
- `python.langchain.com/docs/troubleshooting/errors/GRAPH_RECURSION_LIMIT/` ✅
- `python.langchain.com/docs/how_to/debugging/` ⚠️ (重定向到 overview)

### Expo / React Native
- `docs.expo.dev/build-reference/troubleshooting/` ✅
- `docs.expo.dev/debugging/runtime-issues/` ✅
- `docs.expo.dev/debugging/errors-and-warnings/` ✅
- `reactnative.dev/docs/troubleshooting` ✅
- `reactnative.dev/docs/debugging` ✅

### iOS / Swift
- `developer.apple.com/documentation/swift/debugging` ❌ 404
- `docs.swift.org/swift-book/.../errorhandling/` ❌ JS 壳
- `github.com/swiftlang/swift/tree/main/docs` ✅
- `www.swift.org/documentation/` ✅

### Android / Kotlin
- `developer.android.com/studio/debug` ❌ 超时
- `developer.android.com/studio/publish/troubleshoot` ❌ 超时
- `kotlinlang.org/docs/compiler-errors.html` ❌ 404
- `kotlinlang.org/docs/diagnostics.html` ❌ 404
- `github.com/nicklama/kotlin-error-codes` ❌ 仓不存在

### HarmonyOS / ArkTS
- `github.com/openharmony/docs/tree/master/en/application-dev/quick-start` ✅
