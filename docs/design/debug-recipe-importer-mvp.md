# Debug Recipe Importer MVP 设计草案

## 背景

本项目要建设一个面向 agentic coding 的 debug recipe supply-chain 工具。
它不是新的 coding harness，也不是通用网页爬虫，而是把高质量公开工程知识
转成可审阅、可追踪、可维护、可检索的调试 recipe。

MVP 只覆盖 debug recipe，不覆盖 build recipe、project scaffold 或
conformance recipe。后两类可以在后续版本中接入，但不进入第一条闭环。

## 目标

第一版要跑通一条最小但完整的供应链：

```text
source-list.yml
  -> fetch source
  -> snapshot metadata + evidence refs
  -> extract readable sections
  -> generate proposed recipe
  -> human review
  -> publish accepted recipe
  -> search by fingerprint/tag
  -> refresh detects stale source
```

首个 vertical slice 使用 React hydration mismatch，优先采集
React error 418 这类窄来源页面，避免第一条 recipe 过宽。

## 非目标

- 不做完整 coding harness。
- 不做通用网页爬虫。
- 不导入 build/project scaffold recipe。
- 不让 LLM 直接生成 accepted recipe。
- 不使用 embedding 作为 MVP 检索路径。
- 不自动合并相似 recipe。
- 不要求默认测试访问公网实时内容。

## 核心原则

### CLI-first

核心能力放在 Python CLI 中。MCP 和 skill 只作为后续 adapter，
不承载 importer 的核心状态机。

### 文件优先

MVP 不使用 SQLite。事实源是文件：

```text
recipe-kb/
  sources/
  snapshots/
  proposed/
  accepted/
  rejected/
  stale/
  index.json
```

其中 `index.json` 是派生产物，由命令重建，不允许作为人工编辑事实源。

### 单一语义事实源

每条 recipe 使用一个 `.md` 文件，frontmatter 中的 canonical YAML 是唯一语义源。
Markdown body 是由工具根据 YAML 渲染出的审阅视图。

人可以阅读 Markdown，但不能通过手改 body 改变 recipe 语义。
允许人工书写的非语义内容应单独放入 reviewer notes 区域，且不进入 search/index/publish
的语义模型。

配套命令：

```text
recipe-importer render <recipe>
recipe-importer check <recipe>
recipe-importer compile <recipe>
```

`check` 必须重新渲染 body 并做 normalized diff，防止 YAML 与 Markdown 漂移。

## 推荐项目结构

```text
bin/
  recipe-importer
src/
  recipe_importer/
    cli.py
    sources.py
    fetch.py
    extract.py
    schema.py
    normalize.py
    render.py
    review.py
    publish.py
    search.py
    refresh.py
    llm.py
    manifest.py
recipe-kb/
  sources/source-list.yml
  snapshots/
  proposed/
  accepted/
  rejected/
  stale/
  feedback/
  index.json
schemas/
  debug-recipe.schema.json
  source.schema.json
  review.schema.json
  evidence-candidates.schema.json
prompts/
  debug_recipe_evidence.md
agent-adapters/
  skills/
  mcp/
tests/
```

## 技术选型

- Python 项目管理：`uv` + `pyproject.toml`
- CLI 框架：Typer
- 内部模型：Pydantic
- 外部契约：JSON Schema
- HTML 解析：BeautifulSoup + lxml/html5lib
- 测试：pytest，结合 fixtures 与 parametrization

MVP 不引入 Playwright 渲染。第一批来源限定为静态文档页。

## Source List

`source-list.yml` 不只写 URL，还应写导入意图，降低抽取阶段对模型猜测的依赖。

示例字段：

```yaml
sources:
  - source_id: react-error-418
    url: https://react.dev/errors/418
    source_type: official_error_doc
    stacks:
      - react
      - nextjs
    expected_failure_hints:
      - hydration mismatch
      - server rendered HTML did not match the client
    refresh_policy: monthly
```

每个 source 必须有稳定 `source_id`。不能只用 URL 作为 ID，因为 redirect、
文档迁移、多个 anchor 共用页面都会让 URL 变得脆弱。

## Source Snapshot 与 Evidence

事实源只在首次采集或显式 `refresh` 时联网下载。
默认测试、`check`、`render`、`publish`、`search`、`index` 不联网。

允许联网的命令：

```text
recipe-importer fetch
recipe-importer import
recipe-importer refresh
```

其他命令如果缺少本地 snapshot，应报错提示用户先 fetch，而不是自动联网。

### 保存边界

默认不把完整 raw HTML 提交进知识库。MVP 保存：

```text
metadata
readable sections
evidence excerpts
hashes
source links
```

raw HTML 可选放本地 cache，用于调试或高价值来源，但不作为默认提交内容。
这样可以避免仓库膨胀、版权边界复杂和 review diff 噪声。

### Evidence Ref 粒度

核心字段不能只引用整页，必须引用到 source section/span。

每个 evidence ref 至少包含：

```yaml
source_id:
url:
final_url:
source_type:
captured_at:
section_anchor:
span_id:
short_excerpt:
quote_hash:
```

`short_excerpt` 只保存短摘录，辅助人审；`quote_hash` 用于 refresh 和 stale detection。

## Recipe 数据模型

Recipe ID 默认由 `stack + failure_class/failure_label` slug 生成，
review 时允许改名。ID 必须稳定且可读。

核心字段：

```yaml
id:
kind: debug-recipe
status:
stack:
failure_class:
symptoms:
fingerprints:
first_checks:
do_not:
evidence_needed:
minimal_fix_scope:
validation_ladder:
regression_guard:
sources:
review:
maintenance:
```

核心字段必须关联 `evidence_ref`。无法找到证据的字段应标记 `needs_review`，
不能伪装成已被 source 证明。

## LLM 抽取策略

第一条 vertical slice 不强制接真实 LLM。可以先用 deterministic/mock extractor
跑通状态机、schema、review、publish、search。

接入 LLM 时，LLM 只输出窄 schema 的 `evidence_candidates`，不直接写最终 recipe。

示例：

```json
{
  "candidates": [
    {
      "failure_label": "hydration mismatch",
      "symptom_quotes": ["..."],
      "cause_quotes": ["..."],
      "avoidance_quotes": ["..."],
      "validation_quotes": ["..."],
      "section_refs": ["react-error-418#section-1"],
      "confidence": "medium"
    }
  ]
}
```

本地代码负责：

```text
normalize tags
生成 recipe_id
填充 canonical YAML
渲染 Markdown
校验 evidence refs
标记 needs_review
```

这样把复杂度放在代码里，避免模型一次性生成大结构导致字段漂移或幻觉。

## Manifest 与版本记录

Prompt、schema、extractor 的版本不靠人工维护。使用 manifest 管理 `id + rev + hash`。

```yaml
prompts:
  debug_recipe_evidence:
    rev: 3
    path: prompts/debug_recipe_evidence.md
    hash: sha256:...
schemas:
  evidence_candidates:
    rev: 2
    path: schemas/evidence-candidates.schema.json
    hash: sha256:...
extractors:
  normalize_debug_recipe:
    rev: 5
    files:
      - src/recipe_importer/normalize.py
      - src/recipe_importer/render.py
      - schemas/debug-recipe.schema.json
    hash: sha256:...
```

规则：

```text
hash 相同 -> rev 不变
hash 不同 -> manifest refresh 更新 hash，并自动 rev + 1
```

命令：

```text
recipe-importer manifest check
recipe-importer manifest refresh
```

`manifest check` 用于 CI，只检查不修改。`manifest refresh` 用于开发者本地更新。

Extraction metadata 引用 manifest 当前值：

```yaml
extraction:
  prompt:
    id:
    rev:
    hash:
  schema:
    id:
    rev:
    hash:
  extractor:
    id:
    rev:
    hash:
  provider:
  model:
  temperature:
  input_snapshot_id:
  output_hash:
  extracted_at:
```

## Review Workflow

人审入口采用 inbox-first CLI，而不是 id-first。

基础体验：

```text
recipe-importer review
recipe-importer review current
recipe-importer review next
recipe-importer review prev
recipe-importer review accept
recipe-importer review reject
recipe-importer review skip
recipe-importer review edit
recipe-importer review list
```

默认命令作用于当前 review session 的当前条目。ID-based 操作保留为高级/脚本接口。

Review session 可以存储在：

```text
recipe-kb/review/session.json
```

每条审阅包应展示：

```text
candidate summary
generated Markdown recipe
source evidence refs / excerpts / links
schema validation result
dedupe result
search fingerprints preview
review checklist
```

Review decision 不只是 approve/deny，至少支持：

```text
accept
reject
narrow_scope
merge_existing
needs_more_evidence
mark_stale
deprecate
```

## Publish 与状态模型

主状态集合：

```text
proposed
accepted
rejected
stale
deprecated
```

Review decision 作为事件记录，不把每种 decision 都扩展成主状态。

`accepted` recipe 不允许直接编辑。修改必须走：

```text
accepted -> proposed_revision -> review -> publish
```

这样可以防止绕过 evidence、schema、review 和 index 更新。

`publish` 前必须运行：

```text
schema validation
render equivalence check
source evidence check
dedupe check
search/index preview
```

## Stale 语义

`stale` 不等于失效。它只表示：

```text
这条已接受 recipe 的外部依据可能变了，需要复审。
```

触发条件：

```text
source evidence 的 excerpt/hash 变了
source URL 404 或 redirect 到新页面
官方文档 section anchor 消失
框架 major version 升级
reviewer 手动标记 source superseded
agent 使用反馈显示多次不适用
```

`refresh` 只标记 stale，不自动删除、不自动改写、不自动从搜索结果中移除。

搜索默认仍返回 stale recipe，但必须展示 warning。支持 `--fresh-only` 排除 stale。

## Search 与 Agent 消费

MVP 不引入 embedding，只做 deterministic search：

```text
fingerprint exact/substring
stack tag filter
failure_class filter
source/status filter
```

默认返回 top 3，避免 top 1 误锁单一路径，也避免长列表污染 agent 上下文。

Search 默认输出：

```text
summary
first_checks
do_not
validation_ladder
status warning
```

完整 recipe 通过 `recipe get` 查看。

未来可以预留：

```text
recipe-importer index --with-embeddings
recipe-importer search --semantic "..."
```

但不进入 MVP。

## Dedupe

Dedupe 自动发现相似，不自动合并。

自动提示规则：

```text
same recipe_id -> hard conflict
same primary fingerprint + overlapping stack -> possible duplicate
same source_id + same section/span -> possible duplicate
same failure_class + high symptom overlap -> possible duplicate
```

审阅包中展示 potential duplicates、重叠字段和差异点。
Reviewer 决定：

```text
merge_existing
narrow_scope
keep_separate
reject_duplicate
```

原因是 debug recipe 的 scope 差异需要人判断。自动合并容易把相似但不同的失败类合成过宽 recipe。

## Feedback

MVP 只预留 feedback 文件结构，不实现完整 feedback 命令。

建议目录：

```text
recipe-kb/feedback/
```

后续可以记录：

```text
recipe used
matched fingerprint
agent outcome
validation result
reason not applicable
```

这些反馈可作为 stale、revision 或 deprecation 的输入。

## CLI MVP

MVP 命令覆盖第一条闭环即可：

```text
recipe-importer fetch
recipe-importer extract
recipe-importer import
recipe-importer review
recipe-importer publish
recipe-importer search
recipe-importer get
recipe-importer refresh
recipe-importer check
recipe-importer index rebuild
recipe-importer manifest check
recipe-importer manifest refresh
```

保留 combined shortcut：

```text
recipe-importer import <source-list.yml>
```

但 shortcut 必须持久化每个中间产物，不允许牺牲审计链。

## 测试策略

默认测试和常规验证只使用本地数据。

```text
pytest
```

不访问公网。

联网只发生在：

```text
首次 fetch
显式 import
显式 refresh
显式 network integration test
```

这样可以区分代码回归和外部页面变化。

测试重点：

```text
source-list parsing
snapshot metadata
readable section extraction
evidence ref generation
recipe schema validation
YAML -> Markdown render equivalence
manifest hash/rev behavior
review session cursor behavior
publish state transition
index rebuild
deterministic search
refresh stale detection with fixtures
```

## 已确认决策

1. MVP 只做 debug recipe importer。
2. Recipe 采用 YAML canonical + generated Markdown + check gate。
3. 第一条 vertical slice 允许先不用真实 LLM。
4. 第一版不上 SQLite。
5. Human review 采用 inbox-first CLI。
6. Source evidence 不允许只存裸链接。
7. MVP 不引入 embedding。
8. LLM 输出窄 schema evidence candidates。
9. 核心字段必须关联 evidence ref 或标记 needs_review。
10. Manifest 管理 id + rev + hash，rev 自动递增。
11. Accepted recipe 不允许直接编辑。
12. Stale 不等于失效，默认搜索返回但带 warning。
13. Index 是派生产物。
14. 默认测试不联网，事实源只在首次采集或显式 refresh 时联网。
15. Source、recipe、evidence ref、状态模型均采用稳定 ID 与受控状态机。
16. 使用 uv、Typer、Pydantic、JSON Schema、BeautifulSoup/lxml/html5lib。
17. Source-list 包含 URL 与导入意图。
18. 默认不提交完整 raw HTML。
19. Evidence excerpt 使用短摘录 + hash + section/span。
20. Dedupe 只提示，不自动合并。
21. Search 默认 top 3，默认返回可注入 agent 上下文的摘要。
22. 创建 git repo 并提交设计草案。

## 后续待确认

- 第一版是否需要生成正式 implementation plan。
- 第一条 React source 的具体 URL 与 seed recipe 期望内容。
- Review session 文件格式细节。
- Recipe frontmatter 的完整字段 schema。
- Evidence section/span 的具体抽取算法。
- `recipe get` 与 `search` 的输出格式。
- `feedback/` 的最小文件格式。
