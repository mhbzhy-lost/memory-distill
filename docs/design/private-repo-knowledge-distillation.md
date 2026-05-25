# 私有 Repo 知识蒸馏：设计探索

状态：探索阶段，尚未进入实施。记录调研结论和设计方向，供后续捡起时参考。

## 问题定义

当前 debug recipe importer 只有"从外部公开文档提取"的链路，缺少"从私有 repo
长期维护中沉淀调试知识"的链路。

目标是为某个技术栈沉淀可复用的 debug recipe，而非为某个特定项目量身定制——
后者会大幅降低方案的泛用性。

## 核心洞察：本质是同一条管道

从架构角度看，私有 repo 知识蒸馏与公开文档提取的管道形状相同：

```
source → fetch → extract → review → publish → search
```

输出端完全一致（同一个 recipe schema）。review、publish、index、search、refresh
可以直接复用。差异集中在输入端：fetch adapter 和 extract 前的聚合逻辑。

### 公开文档 vs 私有 repo 的输入差异

| 维度 | 公开文档（如 react.dev/errors/418） | 私有 repo |
|------|------|------|
| 知识聚合度 | 已由文档作者预聚合 | 散落在 N 个 commit / PR / comment / bug doc 中 |
| 显性程度 | 明确以文档形式存在 | 往往隐式——埋在 diff 形状或口头讨论中 |
| 证据格式 | URL + section anchor + excerpt | commit SHA + file path + PR link |
| 源权威性 | 来自框架维护者，天然可信 | 需要其他信号：重复频次、code review 结论、作者经验 |
| 过期检测 | 源页面独立于代码变化 | 源和代码在同一 repo，refactor 可同时让 recipe 失效 |

### 管道复用分析

| 模块 | 复用程度 | 说明 |
|------|----------|------|
| recipe schema / models | 完全复用 | 输出格式不变 |
| review workflow | 完全复用 | 人审逻辑不分来源 |
| publish / state machine | 完全复用 | |
| index / search | 完全复用 | |
| refresh / stale detection | 需适配 | 过期信号从"URL 内容变了"变为"引用的代码路径被重构了" |
| fetch | 需新 adapter | 数据源从 HTTP 变为 git log / file read / code platform API |
| extract | 需适配 prompt | 输入从 HTML sections 变为 evidence bundle |
| 聚合层（新） | 不存在，需新建 | 从 N 条离散观察到 1 个 pattern candidate |

## 信息来源评估

### 企业内部 PR 的实际信息量

理论上 PR 包含丰富信号（description、review discussion、关联 issue），但实际
企业内部 PR 的常态是：

- title: 简短描述，如"fix: 修复白屏问题"
- diff: 具体代码改动
- comments: 少量 code style 类 nit 或 "LGTM"
- 关联 bug: 可能有链接，可能没有；即使有，bug 系统里的信息也常常很薄

这种密度下，能从 PR 可靠提取的只有**修复形状（diff）和大致方向（title）**。
Recipe 最有价值的部分（do_not、first_checks、排查路径）通常不在其中。

### 各信号源的 recipe 字段覆盖能力

| Recipe 字段 | commit message | diff | PR comments | bug analysis doc |
|-------------|:-:|:-:|:-:|:-:|
| failure_class | ❌ | ⚠️ 可推断 | ❌ | ✅ |
| symptoms / fingerprints | ⚠️ 偶尔 | ❌ | ❌ | ✅ |
| first_checks | ❌ | ❌ | ⚠️ 偶尔 | ✅ |
| do_not | ❌ | ❌ | ⚠️ 偶尔 | ✅ |
| minimal_fix_scope | ❌ | ✅ | ❌ | ✅ |
| validation_ladder | ❌ | ⚠️ 从 test diff 推断 | ❌ | ✅ |

### 核心矛盾

Recipe 最有价值的信息（"走过什么弯路"、"下次怎么快速定位"）恰恰是**从未被写下
来的部分**。这些知识只存在于修复者脑中或口头讨论中。

这将问题的性质从"提取（extraction）"转变为"捕获（capture）"：

- **提取**：知识已存在于某个文本，需要结构化
- **捕获**：知识只存在于人脑，需要在产生时拦截记录

## 可行路径

### 路径 A：前瞻式捕获（推荐，改变工作流）

在 fix 发生时就生产 recipe 的原料，而非事后从历史中回溯。

前提：使用 AI agent 辅助维护时，可以零额外成本地要求 agent 在修复过程中写出
结构化 bug analysis（现象 → 调用链 → 根因假设 → 验证 → 确认 → 影响范围）。

这些文档的字段天然映射到 recipe schema：

```
bug analysis 现象      → symptoms / fingerprints
bug analysis 调用链    → first_checks 候选
bug analysis 根因假设  → failure_class
bug analysis 验证方式  → validation_ladder
bug analysis 影响范围  → regression_guard
修复过程中的失败尝试  → do_not
```

**流程**：

```
agent 修复 bug → 产出 docs/bugs/bug-*.md
                        ↓
       聚合：N 份同区域 bug analysis → 识别 pattern
                        ↓
         extract：从 evidence bundle → recipe candidate
                        ↓
              现有管道：review → publish → search
```

**优势**：
- 信息密度最高，所有 recipe 字段都有源
- 捕获成本在 AI agent 辅助下几乎为零
- 不依赖历史 PR 质量
- 可以从第一天就开始积累

**局限**：
- 需要团队（或 agent 工作流）遵守结构化 bug analysis 规范
- 只能前瞻积累，无法回溯已经修过但没留记录的 bug

### 路径 B：从 diff 形状做有限推断（补充，不改工作流）

对历史 commit/PR 做模式识别，产出骨架化 candidate：

```
diff 加了 null check         → 推测 failure_class: null_reference
diff 改了 import 路径        → 推测 failure_class: module_resolution
diff 加了 try-catch + retry → 推测 failure_class: transient_network_error
```

**能做到的**：
- 批量发现 hotspot（哪个模块反复出同类问题）
- 给出 failure_class + fix pattern 的骨架
- 提示"这个区域值得人工补写一条 recipe"

**做不到的**：
- 产出完整、可直接使用的 recipe
- 填充 do_not / first_checks / validation_ladder
- 大量字段需标记 `needs_review`，依赖人补完

**定位**：作为路径 A 的补充，用于发现历史上没有 paperwork 的 hotspot，
引导团队回填知识。

## 自动化程度谱系

| 模式 | 人工介入点 | 适合场景 |
|------|-----------|----------|
| 全自动 hotspot → candidate | 只在 review 环节人审 | repo 活跃、PR 质量高、有 conventional commit |
| 半自动：人指定 hotspot | 人说"X 类问题值得总结"，工具聚合 evidence | PR 质量参差，需要人指方向 |
| 手动触发：指定具体 PR 或 bug doc | 人给一组链接，工具做结构化提取 | 起步阶段，验证管道可行性 |

建议从最右侧开始做 vertical slice，逐步向左扩展。

## 去项目化策略

为保持栈级通用性而非项目绑定，需要在 extract 阶段执行"去项目化"：

- 用 failure_class + stack tags + fingerprints 作为锚点
- 剥离项目特有的文件名、变量名、业务术语
- 保留栈级通用的 error message、API 名、框架概念
- 将项目特有的复现条件移入 `context_example` 字段（可选参考，非核心语义）

判断标准：**如果另一个使用相同技术栈的项目遇到同类问题，这条 recipe 是否仍然
有用？** 如果必须了解原项目的业务逻辑才能理解 recipe，则去项目化不充分。

## 业界参考

调研未发现端到端的成熟方案。以下是各环节的参考实践：

| 环节 | 参考 | 做法 |
|------|------|------|
| 观察/聚合 | Sentry fingerprinting | stack trace 做分组签名，分离栈级信号与项目上下文 |
| 跨项目抽象 | Google SRE postmortem | 跨团队聚合 → 趋势分析 → 识别 cross-product 的系统性弱点 |
| 知识分层 | LangChain memory | episodic（事件序列）vs semantic（去上下文的通用事实） |
| 栈级组织 | awesome-cursorrules | 按技术栈交叉点组织 rules，不按项目 |
| 版本化迭代 | Jina meta-prompt | v0→v13 渐进迭代，每版吸收上版教训，default 指向最佳版 |
| 晋升机制 | LangGraph memory | 用户正向标记 → 交互提升为复用范例 |

## 当前结论

1. **最有价值的信息源是 bug analysis 文档**，不是 PR/commit
2. **前瞻式捕获优于回溯式提取**——在 fix 时写好记录，比事后从薄弱的 PR 中挖掘高效得多
3. **现有管道的后半段（review → publish → search）可直接复用**
4. **需要新建的是：聚合层 + 适配 fetch adapter + extract prompt 调整**
5. 当前阶段缺少高价值输入源，优先级后置；待 bug analysis 文档积累到一定量后再启动实施

## 后续启动条件

满足以下任一条件时可考虑启动实施：

- 同一技术栈下积累了 5+ 份结构化 bug analysis 文档
- 发现同一 failure_class 在 3+ 份 bug analysis 中重复出现
- 团队有明确的"从过往经验中提炼规范"的需求
