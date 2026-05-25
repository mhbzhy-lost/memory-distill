# Build Recipe：统一产出管道设计

状态：设计草案，待评审后进入实施规划。

## 动机

Debug recipe 解决的是"出了问题怎么修"。但更高效的做法是让 agent 在构建阶段就
不犯错——避免一次错误比修复一次错误便宜得多。

Agent 场景下尤其如此：一次可预防的错误会触发完整 bugfix 流程（分析文档 → TDD →
review → 异源复审），代价远超一次及时的构建约束提醒。

## 核心设计原则：一次提取，两种产物

源文档本身同时包含两种知识：

```
react.dev/errors/418 这一页里同时写了：
  - "这个错误是什么、为什么发生"    → debug recipe
  - "正确的做法是..."              → build recipe
```

没有理由分两条管道处理同一份源。统一流程一次 extract 产出一对 candidate。

## 统一管道形态

```
source-list.yml
  → fetch → snapshot
  → extract (统一 prompt，产出双视角 evidence)
  → normalize + split
      ├── debug recipe candidate
      └── build recipe candidate
  → review (各自独立审阅，共享 evidence context)
  → publish
  → index / search
```

### 与现有管道的关系

| 环节 | 变化 |
|------|------|
| source-list / fetch / snapshot | 不变。新增 guide/tutorial 类页面作为源。 |
| extract prompt | 扩展。同一 prompt 同时提取 debug 和 build 两个视角的 evidence。 |
| evidence_candidates schema | 扩展。新增 build 视角字段。 |
| normalize | 扩展。从统一 evidence 拆分为两种 recipe candidate。 |
| build-recipe schema | 新增。 |
| review / publish / status machine | 复用。两种 recipe 各自走独立状态机。 |
| index / search | 扩展。支持 `kind: build-recipe` 的索引和检索。 |
| render / check | 扩展。支持 build recipe 的 Markdown 渲染。 |

## Build Recipe 定位

### 与 debug recipe 的关系

| | Debug Recipe | Build Recipe |
|-|---|---|
| 回答什么 | 出了问题怎么修 | 怎么写才不出问题 |
| 消费时机 | agent 遇到 error message 时 | agent 准备写代码时 |
| 核心价值 | 缩短排查路径、避免错误方向 | 避免触发已知 failure mode、选择正确模式 |
| 触发信号 | error message / fingerprint | file pattern / import / code pattern |

### Build recipe 的知识结构

一条 build recipe 需要回答：

- **何时适用**（trigger）：什么场景下 agent 应该收到这条指导
- **正确模式**（correct_pattern）：应该怎么写
- **约束/禁止**（constraints / do_not）：不能怎么写
- **决策上下文**（decision_context）：多种正确做法之间的权衡
- **默认值**（defaults）：没有特殊需求时选什么
- **验证**（validation）：怎么确认写对了
- **违反后果**（related_debug_recipes）：如果忽略这条 recipe 会触发什么问题

### Build recipe 的两层知识来源

| 层 | 内容 | 来源 | 自动化程度 |
|----|------|------|-----------|
| 约束层 | "不能做什么" | 反转已有 debug recipe 的 do_not + root cause | 高（可批量推导） |
| 指导层 | "应该怎么做" | 官方 guide / best practice / tutorial 文档 | 中（需要新的 extract） |

反转 debug recipe 只能得到约束层。完整的 build recipe 必须从正向知识源补充
指导层（正确模式、决策上下文、defaults）。

统一管道确保这两层在同一次 extract 中完成，避免不一致。

## Build Recipe Schema 草案

```yaml
id: nextjs-server-component-no-hooks
kind: build-recipe
status: proposed
stack:
  - react
  - nextjs

# 被动触发条件（机器可匹配）
trigger:
  file_pattern: "app/**/*.{ts,tsx}"
  code_signals:
    - import: ["useState", "useEffect", "useReducer", "useContext"]
    - absent: ["'use client'", "\"use client\""]
  description: "在 Next.js App Router 的 Server Component 中使用了 React hooks"

# 正确模式（指导层）
correct_pattern:
  - "需要 client interactivity 的组件必须在文件顶部声明 'use client'"
  - "Server Component 只能使用 async/await、server actions、fetch 等服务端 API"
  - "如果只需要在客户端初始化一次，考虑用 dynamic import with ssr: false"

# 决策上下文（何时选哪种方案）
decision_context:
  - condition: "组件需要 useState / useEffect 等 hooks"
    recommendation: "标记为 Client Component ('use client')"
  - condition: "组件只需要一次性数据获取"
    recommendation: "保持 Server Component，使用 async function + fetch"
  - condition: "组件需要浏览器 API 但不需要 hydration"
    recommendation: "使用 next/dynamic with { ssr: false }"

# 约束/禁止（约束层，可从 debug recipe 反向推导）
constraints:
  - "Server Component 不能使用 React hooks (useState, useEffect, etc.)"
  - "Server Component 不能使用 browser-only API (window, document, localStorage)"
  - "Server Component 不能使用 event handlers (onClick, onChange, etc.)"
do_not:
  - "不要在未标记 'use client' 的 app/ 组件中使用 React hooks"
  - "不要把整个页面标记为 'use client' 只为了用一个小交互"

# 默认值
defaults:
  - "app/ 下的组件默认是 Server Component"
  - "只在需要 client interactivity 的最小子树标记 'use client'"

# 验证
validation:
  - "next build 成功，无 hook-in-server-component error"
  - "next dev 无相关 warning"

# 关联 debug recipe
related_debug_recipes:
  - react-invalid-hook-call

# 共享结构
evidence_refs: [...]
review: [...]
maintenance:
  state: proposed
  stale_reason: []
  stale_detected_at: null
```

## Evidence Candidates Schema 扩展

现有 schema 只有 debug 视角的字段。扩展后同时承载两种视角：

```json
{
  "candidates": [
    {
      "failure_label": "hooks in server component",
      "section_refs": ["nextjs-server-components#when-to-use-client"],
      "confidence": "high",

      "symptom_quotes": ["..."],
      "cause_quotes": ["..."],
      "avoidance_quotes": ["..."],
      "validation_quotes": ["..."],

      "correct_pattern_quotes": ["..."],
      "decision_context_quotes": ["..."],
      "default_quotes": ["..."],
      "trigger_signals": ["import useState without 'use client'"]
    }
  ]
}
```

新增字段：

| 字段 | 用途 | 映射目标 |
|------|------|----------|
| `correct_pattern_quotes` | 源文档中描述正确做法的摘录 | build recipe 的 correct_pattern |
| `decision_context_quotes` | 源文档中描述方案选择/权衡的摘录 | build recipe 的 decision_context |
| `default_quotes` | 源文档中描述推荐默认值的摘录 | build recipe 的 defaults |
| `trigger_signals` | 从源文档推断的触发条件描述 | build recipe 的 trigger |

所有新增字段均为 optional。纯 error page 可能只产出 debug 视角字段；
纯 guide page 可能主要产出 build 视角字段。不强求每次都两侧齐全。

## 触发机制：Plan 注入 + 被动精准

Build recipe 需要两层触发协作：

### Plan 阶段注入（宽，设方向）

Agent 进入 writing-plans 时，按任务涉及的 stack tags 检索相关 build recipes，
作为计划约束注入：

```
任务："给 Next.js 项目加一个需要用户交互的表单页"
  → 检索 stack: [react, nextjs] + 相关 trigger description
  → 注入："以下 build recipes 是本次任务的约束边界..."
```

### 被动精准触发（窄，兜底）

上下文变长后 agent 可能遗忘 plan 中的约束。被动触发在 agent 写代码时实时检查：

```
Agent 调用 Write/Edit tool 写入 app/form/page.tsx
  → 检查文件内容是否匹配任何 build recipe 的 trigger
  → 命中 trigger: import useState + absent 'use client'
  → 向 agent 推送精准警告 + recipe 摘要
```

实现路径：通过 PostToolUse hook 或 skill 适配层完成匹配和注入。

### 两层协作模型

```
┌───────────────────────────────────────────────────┐
│  Plan 阶段                                         │
│  "本任务涉及 Server/Client Component 边界，        │
│   以下约束必须遵守：..."                           │
└───────────────────────┬───────────────────────────┘
                        │  agent 实现中...
                        │  上下文增长，约束被稀释...
                        ▼
┌───────────────────────────────────────────────────┐
│  被动触发                                          │
│  "你刚写入的 app/form/page.tsx 命中了              │
│   build-recipe nextjs-server-component-no-hooks：  │
│   检测到 import useState 但缺少 'use client'"      │
└───────────────────────────────────────────────────┘
```

Plan 注入防止走错大方向；被动触发防止细节上犯已知错误。

## 不强求 1:1 配对

并非每条 debug recipe 都有对应的 build recipe，反之亦然：

| 源类型 | 典型产出 |
|--------|----------|
| Error page (react.dev/errors/418) | debug recipe 为主 + 可能附带 build 约束 |
| Guide/learn page (react.dev/learn/...) | build recipe 为主 + 可能发现隐含 failure mode |
| Troubleshooting page | 两者兼有 |
| Getting started / tutorial | 几乎纯 build recipe |
| Migration guide | build recipe（新版正确模式）+ debug recipe（迁移常见错误） |

流程不强制"必须出一对"。extract 后按实际内容决定产出哪种或两种都产出。
关联字段 `related_debug_recipes` / `related_build_recipes` 建立跨引用。

## Source List 扩展

现有 source-list.yml 以 error page 为主。build recipe 需要增加 guide 类源：

```yaml
sources:
  # 现有：error page → 主要产出 debug recipe
  - source_id: react-error-418
    url: https://react.dev/errors/418
    source_type: official_error_doc
    stacks: [react, nextjs]
    expected_failure_hints: [hydration mismatch]
    refresh_policy: monthly

  # 新增：guide page → 主要产出 build recipe
  - source_id: nextjs-rendering-server-components
    url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
    source_type: official_guide
    stacks: [react, nextjs]
    expected_build_hints:
      - server component vs client component boundary
      - when to use 'use client'
      - data fetching in server components
    refresh_policy: monthly

  # 新增：tutorial/getting-started → 纯 build recipe
  - source_id: nextjs-app-router-getting-started
    url: https://nextjs.org/docs/getting-started/installation
    source_type: official_tutorial
    stacks: [react, nextjs]
    expected_build_hints:
      - project structure defaults
      - recommended file conventions
    refresh_policy: quarterly
```

新增 `source_type` 值：`official_guide`、`official_tutorial`、`official_migration`。

新增字段 `expected_build_hints`：与现有 `expected_failure_hints` 对称，
描述预期从该源提取的构建指导方向。

## 粒度选择：Decision-Point 级

Build recipe 的粒度选择 decision-point 级（小粒度），而非 scaffold 级（大粒度）。

理由：

- Agent 不需要你教它"怎么用 Next.js"（它的训练数据已经覆盖）
- Agent 需要的是"到了这个岔路口该选哪边、哪边是陷阱"
- 小粒度 recipe 的 trigger 可以做到精准匹配，大粒度做不到
- 小粒度更容易维护——框架升级时只需更新受影响的几条 recipe
- 小粒度天然适合被动触发——一条 recipe 对应一个具体决策点

每条 build recipe 应聚焦于**一个决策点**：

```
✅ "Server Component 中不能使用 hooks，需要时标记 'use client'"
✅ "TanStack Query 的 staleTime 默认为 0，列表页建议设为 60s"
✅ "Next.js dynamic route 需要 generateStaticParams 否则 build 时不预渲染"

❌ "如何用 Next.js + TanStack Query + Tailwind 搭建一个完整的数据管理页面"
```

## 与现有 Debug Recipe 的一致性保证

统一管道的关键好处是**语义一致性**：

1. **Evidence 共享**：debug recipe 的 do_not 和 build recipe 的 constraints
   引用同一份 evidence_ref，不会说法不一
2. **维护联动**：源文档变化 → 一次 refresh 同时标记相关的 debug + build recipe
   为 stale
3. **Review 效率**：reviewer 看同一份 evidence 上下文审两条 recipe

关联字段设计：

```yaml
# debug recipe 中
related_build_recipes:
  - nextjs-server-component-no-hooks

# build recipe 中
related_debug_recipes:
  - react-invalid-hook-call
```

## 实施路径建议

### Phase 1：Schema + 反转生成（低成本验证）

1. 定义 build-recipe schema
2. 从现有 9 条 accepted debug recipes 批量反转生成 build recipe 约束层草稿
3. 人工审阅 + 补全指导层
4. 验证 search / index 能正确处理 `kind: build-recipe`

**产出**：若干条仅有约束层的 build recipe，验证管道可行性。

### Phase 2：Extract prompt 扩展（统一产出）

1. 扩展 evidence_candidates schema（新增 build 视角字段）
2. 扩展 extract prompt（同时提取双视角）
3. 实现 normalize 拆分逻辑
4. 新增 guide/tutorial 类源到 source-list.yml
5. 跑通一条 vertical slice：从 Next.js Server Components guide 同时产出 debug + build recipe

### Phase 3：触发机制（agent 消费端）

1. 实现 plan 阶段 build recipe 检索注入
2. 实现 PostToolUse hook 的 trigger 匹配
3. 定义 trigger pattern 的匹配语法和优先级

### Vertical Slice 建议

第一条 build recipe 建议选：**Next.js Server Component / Client Component 边界**

理由：
- 已有 `react-invalid-hook-call` debug recipe 作为反向输入
- 官方文档清晰，guide page 质量高
- trigger 条件明确（import hooks + absent 'use client'）
- 是 agent 在 Next.js 项目中最常犯的错误之一
- 既有约束层（不能做什么）也有指导层（应该怎么做）

## 开放问题

1. **trigger pattern 的表达能力**：file glob + import 检测够不够？是否需要
   简单 AST 匹配？初期是否只做 file pattern + 关键词？
2. **被动触发的性能**：每次 Write/Edit 都做匹配是否有性能问题？
   是否需要预编译 trigger index？
3. **粒度控制**：如何防止 build recipe 过度细碎导致 agent 收到太多提醒？
   是否需要 priority / severity 分层？
4. **与 harness 的集成方式**：PostToolUse hook 是否是最佳注入点？
   还是应该在 skill 层做（不同 harness 适配）？
5. **build recipe 的验证自动化**：debug recipe 的 validation 是
   "error 消失了"，build recipe 的 validation 是"代码正确"——后者更难
   自动判定，是否需要不同的 validation 模型？
