# Snapshot Review Navigation Noise

## 现象

执行 React 前端 source 采集后，`recipe-kb/snapshots/next-dynamic-server-error/readable.md`
包含大量导航/侧栏条目，例如：

```text
[next-dynamic-server-error-40] Forms
```

这类条目只有导航标题，没有正文证据，无法支撑 recipe 字段，也不适合作为人审入口。
Next.js 两个页面分别抽出 440+ sections，远超窄错误文档应有的规模。

## 调用链

1. `uv run recipe-importer fetch recipe-kb/sources/source-list.yml` 下载官方文档 HTML。
2. `uv run recipe-importer extract recipe-kb/snapshots/<source_id>` 调用
   `extract_snapshot(snapshot_dir)`。
3. `extract_snapshot()` 用 BeautifulSoup 解析 HTML，然后选择
   `soup.find("main") or soup.body or soup` 作为抽取根。
4. 对抽取根下所有 `h1/h2/h3/p/li` 做无差别文本提取。
5. Next.js 文档页面的 `main` 区域或 body 中包含导航、目录、侧栏、版本菜单等
   非正文元素。
6. 导航项被写入 `sections.json` 和 `readable.md`，导致 snapshot review 面向人类时
   出现大量不可审条目。

## 根因假设

1. 抽取器没有在正文抽取前移除 `nav/aside/header/footer` 和常见导航容器。
2. 抽取器按单个元素展平输出，没有生成适合人审的命中摘要和噪声样本。
3. 工作流缺少 snapshot QA artifact，无法在 import 前提示“此 source 需要过滤或人工复核”。

## 验证方式

- 用 Next.js fixture / 当前 snapshot 验证抽取后不包含孤立导航项 `Forms`。
- 验证抽取后生成 `review.md`，包含：
  - source metadata
  - section count
  - matched expected failure hints 的 evidence 摘要
  - noise/sample section
  - review decision checklist
- 运行：
  - `uv run pytest tests/test_extract.py -q`
  - `uv run pytest -q`
  - 对当前 Next.js snapshot 重新 `extract`，确认 `review.md` 比 `readable.md` 更适合人审。

## 根因确认

根因是 extractor 只做粗粒度 HTML 文本展平，没有过滤文档站点导航，也没有生成
面向人类的 snapshot QA artifact；`readable.md` 被误用为人审入口时暴露了导航噪声。

修复尝试中补充发现：仅按 class/id 中是否包含 `sidebar` 删除节点会误删
React 文档的正文布局容器（例如 `grid-cols-sidebar-content`），导致正文 `article`
一并丢失。过滤规则必须区分“导航容器”与“包含正文 landmark 的布局容器”。

真实 TanStack 快照进一步暴露：Tailwind class 中的 `var(--navbar-height)` 只是布局变量，
不是导航容器标记；用裸 `nav`/`navbar` 子串匹配会误删整个页面布局。无 `main`/`article`
的文档页还需要识别 `.prose` / markdown 内容容器作为正文根。

TanStack review 还显示 expected hints 与正文常常是语义等价但非逐字相同，例如
`query data is stale by default` 对应正文 `by default consider cached data as stale`。
人审摘要不能只依赖 substring，否则会把有效证据标成未命中。

## 影响范围

- Next.js 文档页面、TanStack/Vite 等包含大型导航或 sidebar 的文档站点。
- 后续 `import-source` 若直接读取噪声 sections，可能误生成过宽或错误的 recipe。
- 人审工作流会被大量无效条目淹没，无法判断 source 是否适合 recipe 生成。

## 修复方案

- 在 extractor 中移除导航/侧栏/页头/页脚/脚本样式等非正文节点。
- 对 class/id 命中的导航候选做保护：如果该节点包含 `main` 或 `article`，只删除其内部
  明确的 `nav/aside/header/footer` 等子节点，不整体删除布局容器。
- 不使用裸 `nav`/`navbar` 子串作为删除依据，避免误伤 `--navbar-height` 这类布局变量；
  对无 `main`/`article` 的页面优先选择 `.prose` / markdown 内容容器。
- `review.md` 的 expected hints 匹配先做精确 substring，再用保守关键词重合兜底，
  只用于人审摘要展示，不改变 evidence hash 或 recipe canonical 模型。
- 引入 `review.md` 作为 snapshot QA 人审入口，而不是让人直接审完整 `readable.md`。
- `review.md` 展示 source 信息、section 数、expected hints 命中上下文、噪声样本和
  approve / needs-filter / reject-source 决策提示。
- 保留 `readable.md` 作为 agent 深挖用的完整可读文本。

## 为什么不会引入新问题

过滤只删除非正文容器和明显重复/过短导航噪声，不改变 canonical recipe 渲染逻辑。
`sections.json` 仍保留可引用的 `span_id` 和 `quote_hash`；新增 `review.md` 是辅助
人审 artifact，不参与 recipe 语义模型。

## 修复后验证

- `uv run pytest tests/test_extract.py -q`：4 passed
- `uv run pytest -q`：66 passed
- `git diff --check`：通过
- 真实 snapshot 重新 extract 后：
  - `next-dynamic-server-error` 从 440+ sections 降到 16 sections，未再命中
    `[next-dynamic-server-error-40] Forms` 这类导航项。
  - `tanstack-query-important-defaults` 生成 30 sections，`review.md` 能把
    `query data is stale by default` 关联到正文证据。
  - 9 个 snapshot 均生成 `review.md`。

## 外源复审状态

暂未执行。原因：本仓外源复审要求 `BASE..HEAD` 严格对应本次修复 commit；当前用户明确
要求“产物还没 review，不要提交”，因此没有可用于该约束的本次修复 commit。
