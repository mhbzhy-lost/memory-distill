---
title: Debug Recipe Importer Workflow
kind: runbook
status: active
applies_to:
  - src/recipe_importer
  - recipe-kb
  - scripts/build_agent_skill.py
last_verified: 2026-05-22
source: docs/bugs/bug-react-error-next-data-message-missing.md
---

# Debug recipe importer 的稳定工作流

维护 importer 时，要把 source snapshot、QA gate、recipe 发布和 skill 打包看作同一条
可验证流水线。

## 适用场景

- 新增或刷新 `recipe-kb/sources/source-list.yml` 中的来源。
- 修改 `src/recipe_importer/extract.py`、`publish.py`、`fetch.py`、CLI 或 review 流程。
- 发布 recipe 或重新打包 `debug-recipe-importer` skill。

## 项目事实 / 约定

- 事实源只在第一次采集或显式 refresh 时联网；测试和后续导入使用本地 snapshot。
- `raw.html` 是本地证据输入，但不提交到 git；`response.json`、`sections.json`、
  `qa.json`、`review.md`、`readable.md` 是可提交的 snapshot 产物。
- 人审入口是中文 `review.md`。源证据摘录、代码标识、命令和外部专有名词保持原文。
- extractor 必须先走确定性抽取；`qa.json` 失败时才进入 agentic fallback。
- React / Next 等站点可能把关键正文放在 `pre/code` 或 `#__NEXT_DATA__` 里，
  不要只依赖普通 `p/li/h*` 可见文本。
- `publish` 是状态迁移：成功后 accepted 成为唯一正式产物，同名 stale 和源 proposed
  都必须被清理。
- 打包交付使用 `python3 scripts/build_agent_skill.py --force`，生成目录在 `dist/`
  下，`dist/` 不提交。

## 修改时注意

- 修改 extractor 时，同步覆盖：
  - 抽取段落；
  - `qa.json` 状态；
  - 中文 `review.md`；
  - `import-source` 空候选诊断。
- `extraction_profile.content_selectors` 来自配置或 fallback 产物，不能假设 selector
  永远合法；无效 selector 应回退默认正文抽取，而不是让 snapshot 崩溃。
- 修改 publish/review 队列时，确认 `accepted/`、`stale/`、`proposed/` 三个状态目录
  不会留下同 ID 歧义。
- 修改 skill 打包器时，测试必须验证 skill 文档、wrapper、CLI 代码、snapshot 产物和
  raw.html 排除规则。
- 发现 bug 时先写 `docs/bugs/bug-<summary>.md`，文档完成后直接按 TDD 修复，不再等待
  额外人工审批。

## 验证方式

常用验证命令：

```bash
uv run pytest -q
git diff --check
uv run recipe-importer manifest check
uv run recipe-importer check recipe-kb/accepted/react-hydration-mismatch.md
uv run recipe-importer search "Hydration failed" --fresh-only
python3 scripts/build_agent_skill.py --force
```

发布后检查：

```bash
find recipe-kb -maxdepth 2 -type f -name 'react-hydration-mismatch.md' -print
uv run recipe-importer review current
```

`review current` 在无待审候选时应输出 `review queue is empty` 并返回非零。

## 相关资料

- `docs/bugs/bug-react-error-next-data-message-missing.md`
- `docs/bugs/bug-publish-keeps-stale-sibling.md`
- `docs/bugs/bug-publish-leaves-proposed-candidate.md`
