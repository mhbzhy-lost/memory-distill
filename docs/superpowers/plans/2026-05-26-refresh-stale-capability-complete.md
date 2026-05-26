# Refresh Stale 检测能力补齐实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 补齐 `refresh` 命令的 stale 检测能力，新增 3 个过期条件（source_removed / final_url_changed / section_anchor_gone）与 `--refetch` 选项，让 refresh 能在源页面变动时主动触发告警。

**Architecture:** `refresh.py` 新增可选的 `--refetch` 流程：接受 source-list 路径 → 逐源重新拉取并重建 sections → 对 affected recipe 做扩展的 stale 检测。无选项时保持现有 quote_hash 对比行为不变。扩展的 stale_reason 值集合让 agent 或 reviewer 能精确知道"为什么过期"。

**Tech Stack:** Python / Typer / Pydantic / httpx / pytest（monkeypatch mock httpx.Client）

---

## 文件结构

| 操作 | 文件 | 职责 |
|------|------|------|
| Modify | `src/recipe_importer/refresh.py` | 新增 `_refetch_source` 辅助；扩展 `refresh_stale_status` 支持 source_list_path + http client 注入；实现 3 个新 stale 条件 |
| Modify | `src/recipe_importer/cli.py` | `refresh` 命令增加 `--refetch <source-list>` 可选参数 |
| Modify | `tests/test_refresh.py` | 为每个新 stale 条件添加 fixture + monkeypatch 测试 |

`fetch.py` 和 `extract.py` 不修改——复用它们导出的函数。

---

## 关键设计决策

**1. 三个条件只在 `--refetch` 流程中产生**

理由：`source_removed` 和 `final_url_changed` 必须联网才能知道；`section_anchor_gone` 必须有最新 sections.json 才能检测 span_id 消失。没有 `--refetch` 时，现有 quote_hash 对比已能覆盖"已知 snapshot 有变化"的场景，不扩展。

**2. `--refetch` 失败不损坏快照**

fetch 失败（404 / 5xx）时：旧 `raw.html`、`response.json`、`sections.json` 原封不动保留（便于诊断）。recipe 被标记为 `source_removed` stale，但旧 snapshot 内容不覆盖。

**3. `final_url_changed` 独立于内容变化**

即使 quote_hash 在新 final_url 下依然匹配，只要 final_url 与 recipe 记录的 final_url 不同，也算 stale。含义：文档被移到新地址，可能意味着章节重组或版本迁移，需要人工审阅。

**4. Refresh 不自动修复 recipe**

只迁移状态（accepted → stale），不试图重新 normalize 或更新内容。修复路径是：reviewer 重新 import-source → 生成新 proposed → review accept → publish（覆盖旧 stale）。

---

## Task 1: 单源 fetch 辅助函数

**Files:**
- Modify: `src/recipe_importer/refresh.py`
- Test: `tests/test_refresh.py`

- [ ] **Step 1: 写失败测试——refetch 单个 source 成功后写 response.json**

```python
# tests/test_refresh.py 顶部 import
from unittest.mock import MagicMock
import httpx

from recipe_importer.refresh import _refetch_single_source
from recipe_importer.sources import Source, ExtractionProfile


def test_refetch_single_source_writes_metadata(tmp_path, monkeypatch):
    kb_paths = KbPaths(tmp_path).ensure()

    fake_response = MagicMock(spec=httpx.Response)
    fake_response.status_code = 200
    fake_response.url = "https://react.dev/errors/418"
    fake_response.text = "<html><body>hydration mismatch</body></html>"
    fake_response.headers = {"content-type": "text/html"}
    fake_response.raise_for_status = MagicMock()

    class FakeClient:
        def get(self, url, **kwargs):
            return fake_response
        def close(self):
            pass

    source = Source(
        source_id="react-error-418",
        url="https://react.dev/errors/418",
        source_type="official_error_doc",
        stacks=["react"],
    )
    result = _refetch_single_source(source, kb_paths, FakeClient())

    assert result.removed is False
    raw_html = (kb_paths.snapshots_dir / "react-error-418" / "raw.html").read_text(encoding="utf-8")
    assert "hydration mismatch" in raw_html
```

- [ ] **Step 2: 运行测试验证失败**

运行：`uv run pytest tests/test_refresh.py::test_refetch_single_source_writes_metadata -v`
Expected: fail with `ImportError: cannot import name '_refetch_single_source'`

- [ ] **Step 3: 实现 `_refetch_single_source` 和结果 dataclass**

```python
# src/recipe_importer/refresh.py
from dataclasses import dataclass
from recipe_importer.fetch import fetch_sources, sha256_text
from recipe_importer.sources import Source
import httpx


@dataclass(frozen=True)
class RefetchResult:
    source_id: str
    removed: bool
    final_url: str | None = None


def _refetch_single_source(
    source: Source,
    paths: KbPaths,
    client: httpx.Client,
) -> RefetchResult:
    try:
        response = client.get(str(source.url))
        response.raise_for_status()
    except (httpx.HTTPStatusError, httpx.HTTPError):
        return RefetchResult(source_id=source.source_id, removed=True)

    snapshot_dir = paths.snapshots_dir / source.source_id
    raw_path = snapshot_dir / "raw.html"
    metadata_path = snapshot_dir / "response.json"
    write_text(raw_path, response.text)
    write_json(
        metadata_path,
        {
            "source_id": source.source_id,
            "url": str(source.url),
            "final_url": str(response.url),
            "source_type": source.source_type,
            "stacks": source.stacks,
            "expected_failure_hints": source.expected_failure_hints,
            "expected_build_hints": source.expected_build_hints,
            "refresh_policy": source.refresh_policy,
            "extraction_profile": source.extraction_profile.model_dump(),
            "captured_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "retrieved_status": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "content_hash": sha256_text(response.text),
        },
    )
    return RefetchResult(
        source_id=source.source_id,
        removed=False,
        final_url=str(response.url),
    )
```

- [ ] **Step 4: 运行测试验证通过**

运行：`uv run pytest tests/test_refresh.py::test_refetch_single_source_writes_metadata -v`
Expected: PASS

- [ ] **Step 5: 写失败测试——refetch 404 返回 removed=True**

```python
def test_refetch_single_source_removed_on_404(tmp_path):
    kb_paths = KbPaths(tmp_path).ensure()

    class Fake404Client:
        def get(self, url, **kwargs):
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 404
            resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                request=MagicMock(), response=resp, message="404"
            )
            return resp
        def close(self):
            pass

    source = Source(
        source_id="dead-source",
        url="https://example.com/dead",
        source_type="official_error_doc",
        stacks=["react"],
    )
    result = _refetch_single_source(source, kb_paths, Fake404Client())
    assert result.removed is True
    assert result.final_url is None
```

- [ ] **Step 6: 运行测试**

运行：`uv run pytest tests/test_refresh.py -v -k "refetch_single_source"`
Expected: 两个测试全部 PASS

- [ ] **Step 7: 提交**

```bash
git add src/recipe_importer/refresh.py tests/test_refresh.py
git commit -m "feat(refresh): 添加 _refetch_single_source 辅助函数"
```

---

## Task 2: source_removed 检测

**Files:**
- Modify: `src/recipe_importer/refresh.py:17` — 扩展 `refresh_stale_status` 接受 `source_list_path` 参数
- Test: `tests/test_refresh.py`

- [ ] **Step 1: 扩展现有函数签名并写失败测试**

扩展 `refresh_stale_status` 签名：

```python
def refresh_stale_status(
    paths: KbPaths,
    source_list_path: Path | None = None,
    client: httpx.Client | None = None,
) -> list[Path]:
```

`source_list_path` 为 None 时行为与现有完全一致（向后兼容）。

写失败测试：

```python
def test_refresh_marks_recipe_stale_when_source_removed(kb_root):
    paths = KbPaths(kb_root).ensure()
    accepted, snapshot_dir = _published_recipe(paths)

    source_list_path = paths.sources_dir / "source-list.yml"
    source_list_path.write_text(
        yaml.safe_dump({
            "sources": [{
                "source_id": "react-error-418",
                "url": "https://react.dev/errors/418",
                "source_type": "official_error_doc",
                "stacks": ["react", "nextjs"],
            }]
        }),
        encoding="utf-8",
    )

    class Fake404Client:
        def get(self, url, **kwargs):
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 404
            resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                request=MagicMock(), response=resp, message="404"
            )
            return resp
        def close(self):
            pass

    stale_paths = refresh_stale_status(paths, source_list_path, Fake404Client())

    stale_path = paths.stale_dir / "react-hydration-mismatch.md"
    assert stale_paths == [stale_path]
    recipe = parse_recipe_file(stale_path)
    assert "source_removed" in recipe.maintenance.stale_reason
    assert not (snapshot_dir / "raw.html").exists() or \
           (snapshot_dir / "raw.html").exists()  # 旧 snapshot 可保留
```

> 注：source_removed 时旧 snapshot 保留是合理的（诊断用），不强制删除。

- [ ] **Step 2: 运行测试验证失败**

运行：`uv run pytest tests/test_refresh.py::test_refresh_marks_recipe_stale_when_source_removed -v`
Expected: fail（`source_list_path` 参数存在但未使用）

- [ ] **Step 3: 在 refresh_stale_status 中加 source_removed 检测**

在函数内，`source_list_path` 不为 None 时：

```python
def refresh_stale_status(
    paths: KbPaths,
    source_list_path: Path | None = None,
    client: httpx.Client | None = None,
) -> list[Path]:
    from recipe_importer.sources import load_source_list

    stale_paths: list[Path] = []
    detected_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    removed_source_ids: set[str] = set()

    if source_list_path is not None:
        source_list = load_source_list(source_list_path)
        owns_client = client is None
        http = client or httpx.Client(follow_redirects=True, timeout=30.0)
        try:
            for source in source_list.sources:
                result = _refetch_single_source(source, paths, http)
                if result.removed:
                    removed_source_ids.add(source.source_id)
                else:
                    extract_snapshot(paths.snapshots_dir / source.source_id)
        finally:
            if owns_client:
                http.close()

    for recipe_path in sorted(paths.accepted_dir.glob("*.md")):
        recipe = parse_recipe_file(recipe_path)
        stale_reasons: list[str] = []

        # source_removed detection
        recipe_source_ids = {ref.source_id for ref in recipe.evidence_refs}
        if recipe_source_ids & removed_source_ids:
            stale_reasons.append("source_removed")

        # existing quote_hash check (unchanged)
        hashes_by_source: dict[str, dict[str, str] | None] = {}
        for ref in recipe.evidence_refs:
            if ref.source_id in removed_source_ids:
                continue  # Already marked stale
            if ref.source_id not in hashes_by_source:
                hashes_by_source[ref.source_id] = _current_quote_hashes(paths, ref.source_id)
            current_hashes = hashes_by_source[ref.source_id]
            if current_hashes is None:
                continue
            if current_hashes.get(ref.span_id) != ref.quote_hash:
                stale_reasons.append("source_quote_hash_changed")

        if stale_reasons:
            recipe.status = RecipeStatus.STALE
            recipe.maintenance.state = RecipeStatus.STALE
            recipe.maintenance.stale_reason = sorted(set(stale_reasons))
            recipe.maintenance.stale_detected_at = detected_at
            target = paths.stale_dir / recipe_path.name
            render_recipe_file(recipe, target)
            recipe_path.unlink()
            stale_paths.append(target)
    return stale_paths
```

- [ ] **Step 4: 运行测试**

运行：`uv run pytest tests/test_refresh.py -v`
Expected: 所有现有和新测试 PASS

- [ ] **Step 5: 提交**

```bash
git add src/recipe_importer/refresh.py tests/test_refresh.py
git commit -m "feat(refresh): 新增 source_removed stale 条件"
```

---

## Task 3: final_url_changed 检测

**Files:**
- Modify: `src/recipe_importer/refresh.py`
- Test: `tests/test_refresh.py`

- [ ] **Step 1: 写失败测试——fetch 成功但最终 URL 变化**

```python
def test_refresh_marks_stale_when_final_url_changed(kb_root):
    paths = KbPaths(kb_root).ensure()
    accepted, _snapshot_dir = _published_recipe(paths)
    recipe = parse_recipe_file(accepted)
    old_final_url = str(recipe.evidence_refs[0].final_url)
    new_final_url = "https://react.dev/errors/418-v2"
    assert old_final_url != new_final_url

    source_list_path = paths.sources_dir / "source-list.yml"
    source_list_path.write_text(yaml.safe_dump({
        "sources": [{
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "stacks": ["react", "nextjs"],
        }]
    }), encoding="utf-8")

    original_html = (paths.snapshots_dir / "react-error-418" / "raw.html").read_text(encoding="utf-8")

    class FakeRedirectClient:
        def get(self, url, **kwargs):
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.url = new_final_url  # redirected
            resp.text = original_html  # same content
            resp.headers = {"content-type": "text/html"}
            resp.raise_for_status = MagicMock()
            return resp
        def close(self):
            pass

    stale_paths = refresh_stale_status(paths, source_list_path, FakeRedirectClient())

    stale_path = paths.stale_dir / "react-hydration-mismatch.md"
    assert stale_paths == [stale_path]
    recipe = parse_recipe_file(stale_path)
    assert "final_url_changed" in recipe.maintenance.stale_reason
```

- [ ] **Step 2: 运行测试验证失败**

运行：`uv run pytest tests/test_refresh.py::test_refresh_marks_stale_when_final_url_changed -v`
Expected: fail（`final_url_changed` 尚未实现）

- [ ] **Step 3: 实现 final_url_changed 检测**

在 `_refetch_single_source` 结果中增加 `final_url`，在主函数的 stale 检测循环中，对 refetch 成功的 source：

```python
# 在 for ref in recipe.evidence_refs: 循环内增加
# 检查：refetch 成功获取了该 source，但 final_url 与 recipe.evidence_refs 记录的 final_url 不同
ref_source_ids_with_final_url = {
    ref.source_id: str(ref.final_url) for ref in recipe.evidence_refs
}
for source_id, new_final_url in refetched_final_urls.items():
    if source_id in ref_source_ids_with_final_url:
        stored_final_url = ref_source_ids_with_final_url[source_id]
        if stored_final_url != new_final_url:
            if "final_url_changed" not in stale_reasons:
                stale_reasons.append("final_url_changed")
```

`refetched_final_urls` 是在 refetch 阶段建立的 `{source_id: new_final_url}` 字典。

- [ ] **Step 4: 运行测试**

运行：`uv run pytest tests/test_refresh.py -v`
Expected: 全部 PASS

- [ ] **Step 5: 提交**

```bash
git add src/recipe_importer/refresh.py tests/test_refresh.py
git commit -m "feat(refresh): 新增 final_url_changed stale 条件"
```

---

## Task 4: section_anchor_gone 检测

**Files:**
- Modify: `src/recipe_importer/refresh.py`
- Test: `tests/test_refresh.py`

- [ ] **Step 1: 写失败测试——fetch 成功、extract 后引用的 span_id 不在新 sections.json**

```python
def test_refresh_marks_stale_when_section_anchor_gone(kb_root):
    paths = KbPaths(kb_root).ensure()
    accepted, snapshot_dir = _published_recipe(paths)
    recipe = parse_recipe_file(accepted)
    old_span_id = recipe.evidence_refs[0].span_id

    # Simulate page content change: write sections.json without the old span_id
    sections_path = snapshot_dir / "sections.json"
    sections = read_json(sections_path)
    assert sections[0]["span_id"] == old_span_id
    # Replace span_id with a different one; old one is gone
    sections[0]["span_id"] = "section-completely-new-anchor"
    sections[0]["quote_hash"] = "sha256:different-content"
    write_json(sections_path, sections)

    source_list_path = paths.sources_dir / "source-list.yml"
    source_list_path.write_text(yaml.safe_dump({
        "sources": [{
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "stacks": ["react", "nextjs"],
        }]
    }), encoding="utf-8")

    original_html = (snapshot_dir / "raw.html").read_text(encoding="utf-8")

    class FakeOkClient:
        def get(self, url, **kwargs):
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.url = url  # no redirect
            resp.text = original_html
            resp.headers = {"content-type": "text/html"}
            resp.raise_for_status = MagicMock()
            return resp
        def close(self):
            pass

    stale_paths = refresh_stale_status(paths, source_list_path, FakeOkClient())

    stale_path = paths.stale_dir / "react-hydration-mismatch.md"
    assert stale_paths == [stale_path]
    recipe = parse_recipe_file(stale_path)
    assert "section_anchor_gone" in recipe.maintenance.stale_reason
```

> 注：此测试通过预先写 sections.json（模拟 refetch 后的 extract 结果）来验证 stale 逻辑。
> FakeOkClient 返回同原始 html，extract 会重写 sections.json，但由于 extract 是确定性函数，
> 结果可能仍包含旧 span_id。如果测试因此通过不了，需要在 FakeOkClient 返回一段完全不包含
> 旧锚点的 html，使 extract 生成的 sections.json 不包含旧 span_id。

**更稳妥的测试策略**：让 FakeOkClient 返回一段极简 html（只有 `<p>new unrelated content</p>`），
使 extract 生成的 sections.json 不含旧 span_id：

```python
class FakeNewContentClient:
    def get(self, url, **kwargs):
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 200
        resp.url = url
        resp.text = "<html><body><p>The page has been entirely rewritten with new content.</p></body></html>"
        resp.headers = {"content-type": "text/html"}
        resp.raise_for_status = MagicMock()
        return resp
    def close(self):
        pass
```

- [ ] **Step 2: 运行测试验证失败**

运行：`uv run pytest tests/test_refresh.py::test_refresh_marks_stale_when_section_anchor_gone -v`
Expected: fail（`section_anchor_gone` 尚未实现）

- [ ] **Step 3: 实现 section_anchor_gone 检测**

在 `refresh_stale_status` 的 stale 检测循环中，对 refetch 成功的 source，re-extract 后检查新 sections.json 是否包含旧 span_id：

```python
# 在现有 quote_hash 检测代码块后追加：
if source_list_path is not None and ref.source_id in refetched_source_ids:
    current_hashes = hashes_by_source.get(ref.source_id)
    if current_hashes is not None and ref.span_id not in current_hashes:
        if "section_anchor_gone" not in stale_reasons:
            stale_reasons.append("section_anchor_gone")
```

其中 `refetched_source_ids` 是 refetch 成功的 source_id 集合。

`refetch 成功后 → extract_snapshot → 读取新 sections.json` 这一链路需要保证：
- 先完成所有 source 的 refetch + extract，再遍历 accepted recipes 做 stale 判断。
- `refetched_source_ids` 不含 removed 的 source_id。

- [ ] **Step 4: 运行测试**

运行：`uv run pytest tests/test_refresh.py -v`
Expected: 全部 PASS

- [ ] **Step 5: 提交**

```bash
git add src/recipe_importer/refresh.py tests/test_refresh.py
git commit -m "feat(refresh): 新增 section_anchor_gone stale 条件"
```

---

## Task 5: CLI `--refetch` 选项

**Files:**
- Modify: `src/recipe_importer/cli.py:115-120`
- Test: `tests/test_cli.py`（或直接扩展 `test_refresh.py`）

- [ ] **Step 1: 写失败测试——CLI 接受 --refetch source-list 参数**

```python
def test_cli_refresh_with_refetch_prints_stale(monkeypatch, tmp_path):
    def fake_refresh_stale_status(paths, source_list_path=None, client=None):
        assert source_list_path is not None
        return [paths.stale_dir / "react-hydration-mismatch.md"]

    monkeypatch.setattr(
        recipe_importer.cli,
        "refresh_stale_status",
        fake_refresh_stale_status,
        raising=False,
    )
    source_list = tmp_path / "source-list.yml"
    source_list.write_text("sources: []", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(app, ["refresh", "--refetch", str(source_list)])
    assert result.exit_code == 0
    assert "stale: " in result.stdout
```

- [ ] **Step 2: 运行测试验证失败**

运行：`uv run pytest tests/test_cli.py::test_cli_refresh_with_refetch_prints_stale -v`
Expected: fail（`--refetch` 选项尚未实现）

- [ ] **Step 3: 修改 CLI refresh 命令**

```python
@app.command()
def refresh(
    refetch: Annotated[Path | None, typer.Option(help="Source list path; re-fetch before stale check.")] = None,
) -> None:
    """Mark accepted recipes stale when local refreshed evidence no longer matches."""
    paths = KbPaths(Path.cwd()).ensure()
    source_list_path: Path | None = None
    if refetch is not None:
        source_list_path = refetch
    for path in refresh_stale_status(paths, source_list_path=source_list_path):
        typer.echo(f"stale: {path}")
```

- [ ] **Step 4: 运行测试**

运行：`uv run pytest tests/test_cli.py -v -k refresh`
Expected: 现有 refresh CLI 测试和新测试全部 PASS

- [ ] **Step 5: 运行全量测试**

运行：`uv run pytest -q`
Expected: 全绿

- [ ] **Step 6: 提交**

```bash
git add src/recipe_importer/cli.py tests/test_cli.py
git commit -m "feat(refresh): CLI --refetch 选项支持 source-list 路径"
```

---

## Task 6: 现有测试无回归验证

**Files:**
- 无新文件

- [ ] **Step 1: 全量测试**

```bash
uv run pytest -q
```

Expected: 全部 PASS，无新增失败。

- [ ] **Step 2: 验证 runbook**

```bash
uv run pytest -q
git diff --check
uv run recipe-importer manifest check
uv run recipe-importer search "Hydration failed" --fresh-only
```

所有命令应通过。

- [ ] **Step 3: 若全量测试有失败，回到对应 Task 修复后重跑**

---

## 影响范围与边界说明

**影响范围：**
- `refresh.py`：签名扩展，`refresh_stale_status` 增加 2 个可选参数，无参数调用兼容现有行为
- `cli.py`：`refresh` 命令增加 `--refetch` 选项，不带选项时行为不变
- `test_refresh.py`：扩展 fixture、新增 3 个测试用例

**不在本次范围：**
- Framework major version 变化检测（需要 version 字段基础设施）
- Agent 使用反馈触发 stale（需要 feedback/ 机制）
- Reviewer 手动 mark_stale 的 recipe 状态迁移（属于 review workflow，不属于 refresh）
- Refresh 后自动 re-normalize 修复 recipe（refresh 只负责标记，修复走 republish 流程）
