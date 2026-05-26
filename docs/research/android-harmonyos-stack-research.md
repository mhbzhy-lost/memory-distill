# Android/Kotlin & HarmonyOS/ArkTS Stack Research

> 任务：Task 7 (Research Static Alternatives for Android and HarmonyOS)
> 研究者：opencode qwen3.7-max
> 日期：2026-05-26
> 测试方法：`webfetch` tool（无 headless 浏览器）

## 摘要

对 Android/Kotlin 和 HarmonyOS/ArkTS 两个栈进行静态可达源全面测试。

**Android/Kotlin 结论**：通过 GitHub raw URL（kotlinx.coroutines / kotlinx.serialization 文档）、
`kotlinlang.org` 静态 HTML 和 `docs.gradle.org` 排障指南，可以获得丰富的 Kotlin 错误处理、
协程异常、序列化错误和 Gradle 构建排障内容。**developer.android.com 仍不可用（超时）**。

**HarmonyOS/ArkTS 结论**：通过 OpenHarmony GitHub docs 仓的 raw Markdown，可以获得 ArkTS 编译器
错误代码（40+ 条含错误码和迁移 recipe）、ArkTS 语言规范和常见问题解答。内容以英文 Markdown 为主，
部分 URL 路径已变更需注意。

| 来源类别 | 可达性 | 内容质量 | 行动建议 |
| -------- | ------ | -------- | -------- |
| **Android/Kotlin** | | | |
| GitHub raw: Kotlin/kotlinx.coroutines/docs/topics/*.md | ✅ 完全可用 | 极高（协程异常全流程） | 主力源 |
| GitHub raw: Kotlin/kotlinx.serialization/docs/*.md | ✅ 完全可用 | 极高（序列化错误码 + 示例） | 主力源 |
| kotlinlang.org/docs/*.html | ✅ 静态 HTML | 高（异常层次 / null safety） | 补充源 |
| docs.gradle.org/current/userguide/troubleshooting.html | ✅ 静态 HTML | 高（Gradle 排障全指南） | 主力源 |
| android-developers.googleblog.com | ⚠️ 静态 HTML | 中（偏新闻公告） | 低优先 |
| developer.android.com | ❌ 超时 | — | 跳过 |
| github.com/android/samples | ❌ 404（路径不存在） | — | 跳过 |
| **HarmonyOS/ArkTS** | | | |
| GitHub raw: openharmony/docs/.../typescript-to-arkts-migration-guide.md | ✅ 完全可用 | 极高（40+ 编译错误码 + recipe） | 核心源 |
| GitHub raw: openharmony/docs/.../introduction-to-arkts.md | ✅ 完全可用 | 极高（完整 ArkTS 语言教程） | 核心源 |
| GitHub raw: openharmony/docs/.../common_problem_of_application.md | ✅ 完全可用 | 中（签名/包 FAQ） | 补充源 |
| GitHub raw: openharmony/docs/.../arkts-get-started.md | ✅ 完全可用 | 高（ArkTS 入门指南） | 补充源 |
| GitHub tree: openharmony/docs/.../quick-start | ✅ GitHub 渲染 | 高（目录入口） | 发现源 |
| developer.huawei.com | ❌ 超时/SPA | — | 跳过 |

---

## Android/Kotlin 主力源

### 1. kotlinx.coroutines 异常处理文档

**URL 模式**：`https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/<slug>.md`

Note: kotlinx.coroutines 的文档在 2024-2025 年迁移到 `docs/topics/` 子目录。旧路径
（`docs/exception-handling.md`）返回重定向说明。

#### exception-handling.md — 协程异常处理全指南

- URL: `https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md`
- 内容: 异常传播规则（launch vs async）、`CoroutineExceptionHandler`、取消与异常关系、
  异常聚合（suppressed exceptions）、`SupervisorJob` / `supervisorScope`
- Quality: 极高，含 6 段完整 Kotlin 可运行代码、异常堆栈输出示例、Supervision 策略对比
- source_type: `library_doc`
- expected_failure_hints:
  - `CoroutineExceptionHandler got` uncaught exception
  - `IndexOutOfBoundsException` in launch
  - `CancellationException` ignored by coroutine machinery
  - exception aggregation (first exception wins + suppressed)
  - `SupervisorJob` cancellation propagation
  - `supervisorScope` vs `coroutineScope`

#### flow.md — Asynchronous Flow 全指南（含异常章节）

- URL: `https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md`
- 内容: Flow 构建器、操作符、异常处理（try/catch、`catch` 操作符、exception transparency）、
  `onCompletion`、`flowOn` context 错误（emit from wrong context）
- Quality: 极高，含 34 段完整 Kotlin 代码、Flow 异常输出示例、context preservation 违规错误
- Note: 内容超长（14000+ 字符），parser 需分段或限制 max_sections
- source_type: `library_doc`
- expected_failure_hints:
  - `Flow invariant is violated` (emit from wrong context)
  - `Please refer to 'flow' documentation or use 'flowOn' instead`
  - `IllegalStateException: Flow was collected in ... but emission happened in ...`
  - Flow exception transparency violation
  - `catch` operator only catches upstream exceptions

### 2. kotlinx.serialization 文档

**URL 模式**：`https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/<slug>.md`

#### basic-serialization.md — 序列化基础与常见错误

- URL: `https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md`
- 内容: `@Serializable` 注解要求、JSON encoding/decoding、`MissingFieldException`、
  `JsonDecodingException`、`SerializationException`、可空属性、泛型类、
  `@Transient` / `@Required` / `@SerialName` / `@EncodeDefault`
- Quality: 极高，含 16 段 Kotlin 代码、异常堆栈输出示例、错误修复建议
- source_type: `library_doc`
- expected_failure_hints:
  - `Serializer for class '...' is not found`
  - `Please ensure that class is marked as '@Serializable'`
  - `MissingFieldException: Field '...' is required ... but it was missing`
  - `JsonDecodingException: Unexpected JSON token`
  - `Encountered an unknown key '...'`
  - `Expected string literal but 'null' literal was found`
  - `coerceInputValues` / `ignoreUnknownKeys` 配置建议

### 3. Kotlin 语言异常处理文档

**URL 模式**：`https://kotlinlang.org/docs/<slug>.html`

#### exceptions.html — Kotlin 异常处理全指南

- URL: `https://kotlinlang.org/docs/exceptions.html`
- 内容: throw / try-catch-finally、`require()` / `check()` / `error()` 预置函数、
  自定义异常（sealed class 层次）、`Nothing` 类型、异常层次（RuntimeException 子类）、
  stack trace 解读、Java/Swift 异常互操作
- Access: ✅ 静态 HTML，完整代码示例，2026-05-26
- Quality: 高，覆盖 Kotlin 异常全貌
- source_type: `language_doc`
- expected_failure_hints:
  - `ArithmeticException` (division by zero)
  - `IndexOutOfBoundsException`
  - `NoSuchElementException`
  - `NumberFormatException`
  - `NullPointerException` (!! operator, Java interop)
  - `require()` throws `IllegalArgumentException`
  - `check()` throws `IllegalStateException`
  - `NotImplementedError` (TODO())

### 4. Gradle 排障指南

**URL 模式**：`https://docs.gradle.org/current/userguide/<slug>.html`

#### troubleshooting.html — Gradle 构建排障全指南

- URL: `https://docs.gradle.org/current/userguide/troubleshooting.html`
- 内容: 安装问题（command not found / JAVA_HOME / permission denied）、
  依赖解析调试（dependency tree / Build Scan）、构建性能排查、
  构建逻辑调试（debugger attach、logging、UP-TO-DATE 原因）、
  IDE 集成（IntelliJ / Eclipse 刷新）、Daemon 连接问题（NAT masquerade）
- Access: ✅ 静态 HTML，完整命令行示例和日志输出，2026-05-26
- Quality: 高，覆盖 Gradle 构建全流程常见错误
- source_type: `build_tool_doc`
- expected_failure_hints:
  - `Command not found: gradle`
  - `JAVA_HOME is set to an invalid directory`
  - `Permission denied` (wrapper not executable)
  - `A new daemon was started but could not be connected to`
  - `Task executed when it should have been UP-TO-DATE`
  - IntelliJ / Eclipse Gradle sync failure
  - dependency resolution conflict

### 5. Android Developers Blog（补充源）

**URL 模式**：`https://android-developers.googleblog.com/<year>/<month>/<slug>.html`

- Access: ✅ 基于 Blogger 的服务端渲染 HTML，webfetch 可提取
- Quality: 中，偏新闻/公告，非排障文档
- source_type: `official_blog_post`
- Note: 文章内容多为新 API/工具介绍，非错误调试类。部分文章 URL 已失效（路径变更）。
  仅在有针对性的 debug-related 文章时作为补充源。

---

## Android 不可用源测试记录

| URL | 状态 | 原因 |
| --- | ---- | ---- |
| `developer.android.com/studio/debug` | ❌ 超时 | SPA，webfetch 无法渲染 |
| `developer.android.com/studio/publish/troubleshoot` | ❌ 超时 | SPA |
| `developer.android.com/studio/build/optimize-your-build` | ❌ 超时 | SPA |
| `kotlinlang.org/docs/compiler-errors.html` | ❌ 404 | URL 不存在 |
| `kotlinlang.org/docs/diagnostics.html` | ❌ 404 | URL 不存在 |
| `github.com/android/samples` | ❌ 404 | 仓库不存在 |
| `github.com/nicklama/kotlin-error-codes` | ❌ 404 | 仓库不存在 |
| `android-developers.googleblog.com/2023/11/compose-performance.html` | ❌ 404 | URL 路径变更 |

---

## HarmonyOS/ArkTS 主力源

### 1. TypeScript to ArkTS 迁移指南（核心源）

**URL**: `https://raw.githubusercontent.com/openharmony/docs/master/en/application-dev/quick-start/typescript-to-arkts-migration-guide.md`

- 内容: ArkTS 对 TypeScript 的 40+ 项限制，含**错误码**（10605001-10605091+）、severity 级别
  （Error/Warning）、TypeScript 与 ArkTS 对比代码、编译器规则名
- Quality: **极高**——这是最有价值的 recipe 源。每个 recipe 含：
  - 错误码（如 `Error code: 10605005`）
  - 规则名（如 `arkts-no-var`）
  - 编译错误描述
  - TypeScript 原始代码 vs ArkTS 迁移代码
- source_type: `compiler_doc`
- 覆盖的常见 ArkTS 编译错误:
  - `arkts-no-var` (10605005): Use let instead of var
  - `arkts-no-any-unknown` (10605008): Use explicit types
  - `arkts-no-symbol` (10605002): Symbol() not supported
  - `arkts-no-call-signatures` (10605014): Use class instead
  - `arkts-no-structural-typing` (10605030): No structural typing
  - `arkts-no-destruct-decls` (10605074): No destructuring declarations
  - `arkts-no-destruct-params` (10605091): No destructuring parameters
  - `arkts-no-inferred-generic-params` (10605034): Generic inference limited
  - `arkts-as-casts` (10605053): Only `as T` syntax for casting
  - `arkts-no-delete` (10605059): delete operator not supported
  - `arkts-no-for-in` (10605080): for..in not supported
  - `arkts-limited-throw` (10605087): throw only Error subclass
  - `arkts-no-untyped-obj-literals` (10605038): Object literals need type
  - `arkts-no-jsx` (10605054): JSX not supported
  - ... 40+ 条总计
- expected_failure_hints:
  - `arkts-` 规则名前缀
  - `Error code: 10605` 系列错误码
  - `Compile-time error in ArkTS`
  - `compile-time error` 关键词

### 2. Introduction to ArkTS（核心源）

**URL**: `https://raw.githubusercontent.com/openharmony/docs/master/en/application-dev/quick-start/introduction-to-arkts.md`

- 内容: ArkTS 语言完整教程——声明、类型（number/string/boolean/void/Object/Array/Enum/Union）、
  运算符、语句（if/switch/for/while/throw-try）、函数（声明/参数/返回/重载/闭包）、
  类（字段/方法/继承/构造函数/可见性/Object Literal/Abstract）、接口、泛型、
  空安全（Non-Null Assertion / Null-Coalescing / Optional Chaining）、模块
- Quality: **极高**，覆盖 ArkTS 全部核心语法，含大量代码示例和编译错误说明
- Note: 内容超长（17000+ 字符），parser 需限制 max_sections
- source_type: `language_doc`
- expected_failure_hints:
  - `Compile-time error: cannot access to a nullable value`
  - `name can be undefined`
  - `Return type "string" hides the fact that name can be undefined`
  - `Compilation failed` (nullable access without `?.`)
  - Abstract class instantiation error
  - Interface method not implemented

### 3. Getting Started with ArkTS（补充源）

**URL**: `https://raw.githubusercontent.com/openharmony/docs/master/en/application-dev/quick-start/arkts-get-started.md`

- 内容: ArkTS 快速入门，静态类型强制、禁止运行时对象布局变更、受限运算符语义、
  不支持 structural typing、与 TS/JS 生态兼容性、ArkCompiler Runtime
- Quality: 高，适合作为 recipe 的 "why ArkTS restricts X" 背景引用
- source_type: `language_doc`
- expected_failure_hints:
  - static typing enforcement
  - forbidden object layout at runtime
  - structural typing not supported

### 4. FAQs About Application Packages（补充源）

**URL**: `https://raw.githubusercontent.com/openharmony/docs/master/en/application-dev/quick-start/common_problem_of_application.md`

- 内容: 应用包签名 FAQ（获取 fingerprint / appIdentifier / appId）、
  bundleManager API 使用、bm 命令行工具、hapsigner 工具
- Quality: 中，偏签名/打包配置
- source_type: `faq_doc`
- expected_failure_hints:
  - `getBundleInfoForSelf failed`
  - `bundleManager.BundleFlag` 错误使用
  - signing / certificate / fingerprint issue
  - appIdentifier mismatch (automatic vs manual signing)

---

## HarmonyOS 不可用源测试记录

| URL | 状态 | 原因 |
| --- | ---- | ---- |
| `developer.huawei.com/consumer/en/doc/...` | ❌ 超时/SPA | 华为官方站为 SPA |
| `openharmony/docs/.../reference/faq/faq-ability.md` | ❌ 404 | 文件不存在（路径变更） |
| `openharmony/docs/.../ui/arkts-layout-development-bindsheet.md` | ❌ 404 | 文件不存在 |

---

## 推荐 Source List 条目

### Android/Kotlin（高优先级）

```yaml
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  stacks:
    - kotlin
    - android
  expected_failure_hints:
    - CoroutineExceptionHandler got uncaught exception
    - CancellationException ignored by coroutine machinery
    - exception aggregation suppressed exceptions
    - SupervisorJob cancellation propagation
    - supervisorScope vs coroutineScope exception handling
  refresh_policy: monthly

- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  stacks:
    - kotlin
    - android
  extraction_profile:
    max_sections: 40
  expected_failure_hints:
    - Flow invariant is violated
    - Flow was collected in ... but emission happened in ...
    - Please refer to 'flow' documentation or use 'flowOn' instead
    - Flow exception transparency violation
    - catch operator only catches upstream exceptions
  refresh_policy: monthly

- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  stacks:
    - kotlin
    - android
  expected_failure_hints:
    - Serializer for class ... is not found
    - Please ensure that class is marked as '@Serializable'
    - MissingFieldException
    - JsonDecodingException Unexpected JSON token
    - Encountered an unknown key
    - Expected string literal but 'null' literal was found
    - coerceInputValues
    - ignoreUnknownKeys
  refresh_policy: monthly

- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  stacks:
    - kotlin
    - android
  expected_failure_hints:
    - ArithmeticException division by zero
    - IndexOutOfBoundsException
    - NoSuchElementException
    - NumberFormatException
    - NullPointerException
    - require throws IllegalArgumentException
    - check throws IllegalStateException
    - NotImplementedError TODO()
  refresh_policy: monthly

- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  stacks:
    - android
    - kotlin
    - gradle
  expected_failure_hints:
    - Command not found gradle
    - JAVA_HOME is set to an invalid directory
    - Permission denied wrapper not executable
    - A new daemon was started but could not be connected to
    - Task executed when it should have been UP-TO-DATE
    - dependency resolution conflict
    - IntelliJ Gradle sync failure
  refresh_policy: monthly
```

### HarmonyOS/ArkTS（高优先级）

```yaml
- source_id: arkts-typescript-migration-guide
  url: https://raw.githubusercontent.com/openharmony/docs/master/en/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  source_type: compiler_doc
  stacks:
    - arkts
    - harmonyos
  extraction_profile:
    max_sections: 50
  expected_failure_hints:
    - arkts-no-var
    - arkts-no-any-unknown
    - arkts-no-structural-typing
    - arkts-no-destruct-decls
    - arkts-no-destruct-params
    - arkts-as-casts
    - arkts-no-delete
    - arkts-no-for-in
    - arkts-limited-throw
    - arkts-no-untyped-obj-literals
    - arkts-no-jsx
    - Error code 10605
    - Compile-time error in ArkTS
  refresh_policy: monthly

- source_id: arkts-language-introduction
  url: https://raw.githubusercontent.com/openharmony/docs/master/en/application-dev/quick-start/introduction-to-arkts.md
  source_type: language_doc
  stacks:
    - arkts
    - harmonyos
  extraction_profile:
    max_sections: 50
  expected_failure_hints:
    - Compile-time error cannot access nullable value
    - name can be undefined
    - Return type hides that value can be undefined
    - Compilation failed nullable access
    - Abstract class instantiation error
    - Interface method not implemented
    - null safety strictNullChecks
  refresh_policy: monthly

- source_id: arkts-common-problems-packages
  url: https://raw.githubusercontent.com/openharmony/docs/master/en/application-dev/quick-start/common_problem_of_application.md
  source_type: faq_doc
  stacks:
    - arkts
    - harmonyos
  expected_failure_hints:
    - getBundleInfoForSelf failed
    - bundleManager.BundleFlag
    - signing certificate fingerprint
    - appIdentifier mismatch
    - automatic vs manual signing
  refresh_policy: monthly

- source_id: arkts-getting-started
  url: https://raw.githubusercontent.com/openharmony/docs/master/en/application-dev/quick-start/arkts-get-started.md
  source_type: language_doc
  stacks:
    - arkts
    - harmonyos
  expected_failure_hints:
    - static typing enforcement
    - forbidden object layout at runtime
    - operator semantics restricted
    - structural typing not supported
  refresh_policy: monthly
```

---

## Recipe 候选

### Android/Kotlin 候选

| Recipe ID | 源 | 失败场景 |
| --------- | --- | -------- |
| `kotlin-coroutine-exception-handler-uncaught` | exception-handling.md | 未设置 CoroutineExceptionHandler 导致 uncaught 异常 |
| `kotlin-coroutine-supervisor-job-isolation` | exception-handling.md | 子协程异常取消父协程（需要 SupervisorJob） |
| `kotlin-flow-emit-wrong-context` | flow.md | Flow 在错误 context 中 emit（需要 flowOn） |
| `kotlin-flow-catch-upstream-only` | flow.md | catch 操作符只捕获上游异常 |
| `kotlin-serializable-annotation-missing` | basic-serialization.md | 未标记 @Serializable 导致 Serializer not found |
| `kotlin-serialization-missing-field` | basic-serialization.md | JSON 缺少必需字段（MissingFieldException） |
| `kotlin-null-pointer-java-interop` | exceptions.html | Kotlin 与 Java 互操作时的 NullPointerException |
| `android-gradle-daemon-connection-failed` | troubleshooting.html | Gradle daemon 连接失败（NAT masquerade） |
| `android-gradle-java-home-invalid` | troubleshooting.html | JAVA_HOME 指向无效目录 |
| `android-gradle-dependency-resolution-conflict` | troubleshooting.html | 依赖版本冲突解析失败 |

### HarmonyOS/ArkTS 候选

| Recipe ID | 源 | 失败场景 |
| --------- | --- | -------- |
| `arkts-no-var-use-let` | migration-guide | ArkTS 禁止 `var`（Error 10605005） |
| `arkts-no-any-explicit-type` | migration-guide | ArkTS 禁止 `any`/`unknown`（Error 10605008） |
| `arkts-no-structural-typing` | migration-guide | 两个无关类即使 API 相同也不能互赋值（Error 10605030） |
| `arkts-no-destruct-decls` | migration-guide | ArkTS 不支持解构声明（Error 10605074） |
| `arkts-no-for-in-loop` | migration-guide | ArkTS 不支持 `for...in`（Error 10605080） |
| `arkts-throw-only-error-subclass` | migration-guide | throw 只接受 Error 子类（Error 10605087） |
| `arkts-nullable-access-without-optional-chaining` | introduction-to-arkts | 访问可空属性但未用 `?.` |
| `arkts-field-uninitialized-runtime-error` | introduction-to-arkts | 字段未初始化导致运行时异常 |
| `arkts-abstract-class-instantiation` | introduction-to-arkts | 实例化抽象类编译错误 |
| `arkts-signing-app-identifier-mismatch` | common_problem_of_application | 签名 appIdentifier 不匹配跨设备调试失败 |

---

## 特殊处理注意事项

### kotlinx.coroutines 文档路径迁移

- 旧路径（`docs/exception-handling.md`）返回重定向文本，非实际内容
- 正确路径为 `docs/topics/exception-handling.md`
- **建议**：pipeline 对 `Kotlin/kotlinx.coroutines` 仓库 URL 做路径映射（`docs/` → `docs/topics/`）
- 或使用 GitHub directory listing 验证文件实际位置

### raw.githubusercontent.com parser 适配

- **优势**：返回纯文本 Markdown，100% 可 parse
- **content_selectors**：raw MD 不适用——parser 应直接使用 Markdown 解析器
- **source_type**：复用 `library_doc`、`language_doc`、`compiler_doc`、`build_tool_doc`
- **extraction_profile**：`typescript-to-arkts-migration-guide.md` 和 `flow.md` 超长，
  需要设置 `max_sections: 40-50`

### kotlinlang.org HTML 解析

- `kotlinlang.org/docs/*.html` 返回服务端渲染 HTML，webfetch markdown 提取正常
- 但代码块中混有 HTML `<` 实体（如 `<` in examples），parser 需处理 HTML 实体解码
- URL 格式统一为 `https://kotlinlang.org/docs/<slug>.html`

### OpenHarmony docs 路径不稳定

- 部分文件（`faq-ability.md`、`arkts-layout-development-bindsheet.md`）返回 404
- 说明 OpenHarmony docs 仓目录结构在持续调整
- **建议**：使用 `quick-start/` 子目录下的文件（已验证稳定），
  不依赖 `reference/faq/` 或 `ui/` 等子目录
- tree 页（`github.com/openharmony/docs/tree/master/en/application-dev/quick-start`）
  可作为源发现入口，但每个具体文件需逐 URL 验证

---

## 决策

### Android/Kotlin: 推荐进行实施 ✅

Android/Kotlin 栈有以下高质量可用源：

1. **3 个 GitHub raw kotlinx.* docs**（协程异常、Flow、序列化）——核心，100% 可达
2. **kotlinlang.org 异常文档**（语言级）——补充，静态 HTML 可达
3. **docs.gradle.org 排障**（构建工具级）——主力，静态 HTML 可达

**建议**：
- 直接加入 5 个源到 source-list.yml
- 先导入 3-4 个高优先级 recipe 验证端到端流程
- 后续可追加 kotlinx.coroutines 的其他 docs/topics/*.md（如 channels.md、shared-mutable-state.md）

### HarmonyOS/ArkTS: 推荐进行实施 ✅

HarmonyOS/ArkTS 栈有以下高质量可用源：

1. **TypeScript to ArkTS Migration Guide**（核心，40+ 编译错误码 + recipe）——这是最有价值的源
2. **Introduction to ArkTS**（核心，完整语言教程）
3. **Application Packages FAQ**（补充，签名配置）
4. **Getting Started with ArkTS**（补充，入门指南）

**建议**：
- 直接加入 4 个源到 source-list.yml
- 重点利用 `typescript-to-arkts-migration-guide.md` 的 40+ 条编译规则
- 实现 `source_type: compiler_doc` 对 ArkTS 错误码的解析逻辑
- 中文文档（`zh-cn/application-dev/...`）可作为后续补充源（需逐 URL 验证）

**不建议标记为 "deferred"**——两个栈的可用源已充分覆盖常见错误场景：
- Android: 协程异常、序列化错误、Gradle 构建问题、Kotlin 空安全
- HarmonyOS: ArkTS 编译错误码、类型系统限制、签名配置、空安全

---

## 测试日志（URL → status）

> Legend: ✅ 可达内容完整 | ⚠️ 可达但内容被重定向 / 不完整 | ❌ 超时 / 404 / JS 空壳

### Android / Kotlin
- `android-developers.googleblog.com/` ✅（Blogger 静态 HTML）
- `github.com/android/samples` ❌ 404（路径不存在）
- `kotlinlang.org/docs/home.html` ✅（静态 HTML）
- `kotlinlang.org/docs/exceptions.html` ✅（静态 HTML，丰富内容）
- `docs.gradle.org/current/userguide/troubleshooting.html` ✅（完整排障指南）
- `developer.android.com/studio/debug` ❌ 超时
- `developer.android.com/studio/publish/troubleshoot` ❌ 超时
- `raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md` ✅
- `raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md` ✅
- `raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md` ✅
- `raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/exception-handling.md` ⚠️（重定向到 topics/）
- `android-developers.googleblog.com/2023/11/compose-performance.html` ❌ 404

### HarmonyOS / ArkTS
- `github.com/openharmony/docs/tree/master/en/application-dev/quick-start` ✅
- `raw.githubusercontent.com/openharmony/docs/master/.../typescript-to-arkts-migration-guide.md` ✅（极丰富）
- `raw.githubusercontent.com/openharmony/docs/master/.../introduction-to-arkts.md` ✅（极丰富）
- `raw.githubusercontent.com/openharmony/docs/master/.../common_problem_of_application.md` ✅
- `raw.githubusercontent.com/openharmony/docs/master/.../arkts-get-started.md` ✅
- `raw.githubusercontent.com/openharmony/docs/master/.../reference/faq/faq-ability.md` ❌ 404
- `raw.githubusercontent.com/openharmony/docs/master/.../ui/arkts-layout-development-bindsheet.md` ❌ 404
- `developer.huawei.com` ❌ 超时/SPA
