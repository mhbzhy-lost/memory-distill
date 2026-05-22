# React Error Next Data Message Missing

## 现象

执行已批准 source 的后续流程时：

```bash
uv run recipe-importer import-source recipe-kb/snapshots/react-error-418
```

命令退出码为 0，但没有输出 proposed recipe，也没有生成
`recipe-kb/proposed/react-hydration-mismatch.md`。

进一步检查：

```bash
uv run python -c "from pathlib import Path; from recipe_importer.llm import deterministic_candidates; c=deterministic_candidates(Path('recipe-kb/snapshots/react-error-418')); print(c.model_dump_json(indent=2))"
```

输出为：

```json
{
  "candidates": []
}
```

当前 `recipe-kb/snapshots/react-error-418/readable.md` 只包含 minified error 页面导语，
没有包含 hydration mismatch 的完整错误正文。

## 调用链

1. `recipe-importer fetch recipe-kb/sources/source-list.yml` 抓取 `https://react.dev/errors/418`。
2. `recipe-importer extract recipe-kb/snapshots/react-error-418` 调用
   `extract_snapshot(snapshot_dir)`。
3. `extract_snapshot()` 解析 HTML，过滤导航噪声后选择正文 DOM。
4. 抽取器只从 `h1/h2/h3/p/li` 读取可见 DOM 文本。
5. React error 页面把完整错误正文同时放在：
   - 一个 `<code>` 可见节点中；
   - `#__NEXT_DATA__` JSON 的 `props.pageProps.errorMessage` 字段中。
6. 当前抽取器没有读取 `code/pre`，也没有解析 `#__NEXT_DATA__`。
7. `sections.json` 缺少 `Hydration failed...` 正文。
8. `deterministic_candidates()` 根据 sections 拼接文本查找 `"Hydration failed"`。
9. 因为 sections 中没有该文本，返回空 candidates，后续 `import-source` 无产物。

## 根因假设

1. 抽取器的正文标签集合过窄，漏掉 React error 页面中的 `<code>` 错误正文。
2. React/Next 文档站点把关键正文放在 `#__NEXT_DATA__` JSON 中，当前抽取器没有针对该确定性来源做结构化补充。
3. `import-source` 对空 candidates 静默成功，导致流水线看起来执行成功但没有产物。

## 验证方式

- 用包含 `#__NEXT_DATA__` 的 fixture 验证 `extract_snapshot()` 会生成包含
  `Hydration failed...` 的 section。
- 验证 `deterministic_candidates()` 对该 snapshot 返回一个 hydration candidate。
- 验证 `recipe-importer import-source recipe-kb/snapshots/react-error-418` 生成
  `recipe-kb/proposed/react-hydration-mismatch.md`。
- 验证 `review.md` 的 `expected_failure_hints` 能命中 hydration 证据。

## 根因确认

根因是 extractor 没有抽取 React error 页面承载完整错误正文的确定性节点
（`code/pre` 或 `#__NEXT_DATA__.props.pageProps.errorMessage`），导致候选生成器拿不到
hydration fingerprint。

## 影响范围

- React `react.dev/errors/<code>` 这类 minified error 页面。
- 其他把核心正文放在 `pre/code`、hydrated JSON 或脚本数据中的文档站点。
- 任何依赖 `expected_failure_hints` 或 deterministic candidate 的后续导入流程；
  它们可能静默无产物。

## 修复方案

- 引入轻量 `extraction_profile`：source 可以声明正文选择器、结构化文本路径、
  section 数量阈值和是否允许 agentic fallback。
- 在 extractor 中补充确定性正文来源：
  - 抽取正文根下的 block `pre/code` 文本，跳过普通行内 code；
  - 针对 `#__NEXT_DATA__` 解析 JSON，默认提取 `props.pageProps.errorMessage`；
  - 支持 `extraction_profile.structured_text_paths` 声明其他 JSON 路径。
- 增加 snapshot QA gate：
  - `sections_non_empty`
  - `section_count_within_bounds`
  - `expected_hints_matched`
- QA gate 失败时，在中文 `review.md` 和结构化 `qa.json` 中标记
  `needs_agentic_fallback`，并提示 agent 读取 `raw.html`、`response.json`、
  `sections.json`、`review.md` 后产出 profile 或 extractor patch。
- 为 `import-source` 空 candidates 增加可诊断提示，避免后续流水线静默无产物。

## 为什么不会引入新问题

补充来源只增加同一 snapshot 内的确定性文本，不改变 recipe schema 和 canonical renderer。
`quote_hash` 仍基于规范化文本计算；如果页面更新，refresh/stale 仍能检测到证据变化。
QA gate 不负责模型判断，只负责把失败显式暴露；真正的 agentic loop 只在 gate 失败后
介入，避免每次抽取都依赖不可复现的模型判断。
