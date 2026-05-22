# Invalid Extraction Selector Crashes

## 现象

当 source 的 `extraction_profile.content_selectors` 中包含无效 CSS selector 时，
`recipe-importer extract <snapshot>` 会在 `soup.select_one(selector)` 处抛出
`SelectorSyntaxError`，整个 snapshot 抽取中断。

## 调用链

1. `recipe-importer fetch` 将 source 的 `extraction_profile` 写入 snapshot 的
   `response.json`。
2. `recipe-importer extract <snapshot>` 调用 `extract_snapshot(snapshot_dir)`。
3. `extract_snapshot()` 调用 `configured_content_root(soup, metadata)`。
4. `configured_content_root()` 遍历 `content_selectors` 并执行 `soup.select_one(selector)`。
5. 对无效 CSS selector，BeautifulSoup / Soup Sieve 抛出 `SelectorSyntaxError`。
6. 当前实现未捕获该异常，导致无法回退到默认 `content_root()`，也不会生成 `qa.json`
   或中文 `review.md`。

## 根因假设

1. `content_selectors` 是 source/profile 配置，当前实现把它当作可信 CSS selector。
2. extractor 没有把 selector 失败纳入 QA/fallback 机制。
3. 缺少无效 selector 的回归测试。

## 验证方式

- 构造包含 `extraction_profile.content_selectors: ["main["]` 的 snapshot。
- 执行 `extract_snapshot()`，断言不会抛异常，并会回退到默认正文根抽取段落。
- 验证生成 `sections.json` 和 `qa.json`。

## 根因确认

根因是 extractor 没有隔离 source/profile 配置错误，导致一个无效 CSS selector 可以绕过
QA gate，直接让抽取流程崩溃。

## 影响范围

- 所有手写或 agentic fallback 生成的 `extraction_profile.content_selectors`。
- 批量采集时的单个 source 配置错误会阻断该 snapshot 的抽取。
- 人审无法看到 `review.md` 中的失败上下文。

## 修复方案

- 捕获 `SelectorSyntaxError`，忽略该 selector 并继续尝试后续 selector。
- 所有 selector 都失败时，回退到默认 `content_root()`。
- 同时将 `script_json_payloads()` 传给 `json.loads()` 的值显式转成 `str`，降低 BS4
  类型差异导致的兼容风险。

## 为什么不会引入新问题

无效 selector 本来无法选择任何正文；忽略它并回退到默认抽取比崩溃更接近现有 fallback
语义。有效 selector 的路径不变，仍然优先命中用户配置。
