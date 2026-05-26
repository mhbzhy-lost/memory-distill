# Recipe Stack Expansion Design

## Section 1: 总目标与验收标准

**总目标**：扩栈后 recipe 总数达到 **25-35 个**（现 9 + 新增 16-26），覆盖以下 6 个新栈：

| 栈 | 目标 recipe 数 | 验收标准 |
|---|---|---|
| FastAPI / Pydantic | 3-4 | validation 错误 + middleware 错误 + async 生命周期陷阱 |
| LangChain / LangGraph | 3-4 | chain 错误 + retrieval 失败 + agent loop 卡死 |
| Expo / React Native | 3-4 | bundler 错误 + native module 链接失败 + navigation 状态丢失 |
| iOS (Swift/Xcode) | 3-4 | signing/profile 错误 + concurrency race + Swift 类型陷阱 |
| Android (Kotlin/Gradle) | 3-4 | Gradle 构建错误 + ProGuard/R8 keep 失败 + Activity 生命周期陷阱 |
| HarmonyOS (ArkTS) | 3-4 | ArkTS 限制 + Stage 模型生命周期 + Ability 通信失败 |

**验收方式**：
- 每个栈的 `search "<典型错误>"` 至少能命中 1 个 recipe
- 每个 recipe 必须有 accepted 状态 + 1+ evidence_refs（源证据）
- 总 accepted recipes 数 ≥ 25

**非目标**：
- 不引入 Playwright（继续只接入静态 HTML 可抓取的文档）
- 不做 framework major version 跟踪（留作 P2）
- 不做 build recipe（只做 debug recipe）

---

## Section 2: Stack Index 索引

**两个产出：**

1. **CLI 命令 `recipe-importer list`**
   ```bash
   recipe-importer list                  # 所有 stack，按 stack 名分组显示
   recipe-importer list --stack react    # 只看某个 stack
   ```
   输出形如：
   ```
   react (5 recipes, all accepted)
     react-hydration-mismatch     render/hydration
     react-invalid-hook-call      react/hooks
     react-effect-dependency-...  react/effect-lifecycle
     react-state-reset-by-...     react/state-preservation
     react-effect-dependency-...  react/effect-lifecycle
   
   nextjs (3 recipes, 2 stale)
     next-dynamic-server-usage    nextjs/dynamic-rendering
     next-invalid-dynamic-...     nextjs/dynamic-import
     ...
   ```

2. **每次 `index rebuild` 时顺带更新**，不需要单独维护文件——数据已在 `index.json` 里（stack 字段），`list` 只是读取并按 stack 分组。

**验收**：`recipe-importer list` 按栈聚合，显示每个栈的 recipe 数量 + 已接受/过期比例，便于决策是否需要再补。

---

## Section 3: 实施顺序与 pipeline 风险预判

**实施顺序**（推荐）：

| 顺序 | 栈 | 理由 |
|---|---|---|
| 1 | **FastAPI** | Python 栈，文档风格类似现有 React/Next.js（mkdocs 渲染），预期 extract pipeline 无需大改；用来验证 pipeline 跨语言迁移 |
| 2 | **LangChain / LangGraph** | Python + JS 混合文档，可能踩到多语言 snippet 处理；验证 pipeline 对"长文档含多个独立 topic"的拆分 |
| 3 | **Expo / React Native** | 文档风格接近 Next.js，预期顺利，作为 React 生态的延伸 |
| 4 | **iOS** | Apple developer docs，需要验证 HTML 结构是否能被当前 selector 抽取；可能引入新 extraction_profile |
| 5 | **Android** | developer.android.com 是 SPA（部分 JS 渲染）但 Google 也提供纯 HTML 文档页面，需要挑选 URL |
| 6 | **HarmonyOS** | ArkTS 中文文档 + Stage 模型，文档站可能是 Vue/React SSR，需验证 SSR 内容能否被抽取；**最高风险** |

**每栈的 pipeline 风险预判**：

| 栈 | 可能需要的 extraction_profile 调整 | 失败回退 |
|---|---|---|
| FastAPI | 一般无需调整 | — |
| LangChain | Python + JS snippet 边界需要 `content_selectors` 扩展 | 启用 `agentic_fallback=true` |
| Expo/RN | 一般无需调整 | — |
| iOS | Apple doc 用 `.article` 容器，需新增 selector | `agentic_fallback` 接管 |
| Android | 部分页面是 CSR，需要挑 static-friendly URL 或用 `agentic_fallback` | 换候选 URL |
| HarmonyOS | 文档站 URL 结构不稳定，需多次试错 | 若持续失败，暂时只保留 source 记录，不强制 recipe 产出 |

**每栈验收节奏**：
- 每完成一栈，跑一次 `uv run recipe-importer list --stack <stack>` 确认 recipe 已 accepted
- 每栈完成后 git commit 一次，保持 main 分支持续绿
