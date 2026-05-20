# bug-extract-section-count-expectation

## 现象

运行 `uv run pytest tests/test_extract.py tests/test_cli.py -q` 时，
`tests/test_extract.py::test_extract_snapshot_writes_sections_and_evidence`
失败。

错误信息：

```text
AssertionError: assert 8 == 7
where 8 = ExtractionResult(source_id='react-error-418', section_count=8).section_count
```

## 调用链

1. 测试读取 `tests/fixtures/react_error_418.html`。
2. 测试把 fixture 写入临时 snapshot 的 `raw.html`，并写入 `response.json`。
3. 测试调用 `extract_snapshot(snapshot_dir)`。
4. `extract_snapshot` 使用 BeautifulSoup 解析 HTML，选择 `main` 节点。
5. `extract_snapshot` 遍历 `h1`、`h2`、`h3`、`p`、`li` 元素并生成 section。
6. 当前 fixture 中可提取元素为 `h1` 1 个、`p` 2 个、`li` 4 个、`h2` 1 个，总数 8。
7. 测试断言 `result.section_count == 7`，与实际 fixture 结构不一致。

## 根因假设

1. 测试断言写错，把 fixture 中的 `h2` 或第二个 `p` 漏算了。
2. `extract_snapshot` 不应该把 `h2` 当作 section 提取。
3. `extract_snapshot` 不应该把修复说明段落当作 section 提取。

## 验证方式

通过失败输出确认 `section_count` 实际为 8；对照 fixture 结构逐项计数：
`h1`、第一个 `p`、4 个 `li`、`h2`、第二个 `p`，共 8 个可提取文本节点。

## 根因确认

根因是主会话新增测试断言错误：Task 5 设计明确要求提取 `h1`、`h2`、`h3`、`p`、`li`，
当前 fixture 在该规则下应产生 8 个 section，而不是 7 个。

## 影响范围

- `tests/test_extract.py` 中对 `section_count` 的精确数量断言。
- `tests/test_cli.py` 中 mock 的 CLI 输出数量仅验证 CLI 打印，不依赖真实 fixture。
- Task 6 的 deterministic candidate 测试会读取 `sections.json`，应接受 fixture 的真实
  section 列表，不应假设错误数量。

## 修复方案

将 `tests/test_extract.py` 中 `result.section_count == 7` 修正为 `8`。该修复针对根因，
即测试期望与 fixture/提取规则不一致；不改变提取逻辑，因此不会改变后续 Task 6
依赖的 `sections.json` 行为。

## 修复后验证

- 原失败用例：`uv run pytest tests/test_extract.py tests/test_cli.py -q`
- 影响范围验证：`uv run pytest tests/test_extract.py tests/test_cli.py -q`
- 全量验证：`uv run pytest -q`

实际结果：

- `uv run pytest tests/test_extract.py tests/test_cli.py -q`：6 passed
- `uv run pytest -q`：19 passed
- `git diff --check`：通过，无输出

## 异源复审豁免

本次修复 diff 为单行测试断言修正，不改生产逻辑；外部复审按小修复豁免。
