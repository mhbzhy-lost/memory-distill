# Skill Packager Stale Recipe Expectation

## 现象

执行采集后运行：

```bash
uv run pytest -q
```

失败用例：

```text
tests/test_build_agent_skill.py::test_build_agent_skill_packages_cli_code_and_static_assets
```

错误信息：

```text
assert (bundle / "recipe-kb/accepted/react-hydration-mismatch.md").exists()
```

实际情况是 `recipe-importer refresh` 根据新采集的 `react-error-418` evidence
将 `react-hydration-mismatch` 从 `accepted/` 移动到了 `stale/`。

## 调用链

1. `uv run recipe-importer fetch recipe-kb/sources/source-list.yml` 重新抓取
   `react-error-418` 和新增 React 前端 sources。
2. `uv run recipe-importer extract ...` 重新生成每个 snapshot 的 `sections.json`
   和 `readable.md`。
3. `uv run recipe-importer refresh` 对 accepted recipe 的 `evidence_refs.quote_hash`
   与当前本地 `sections.json` 做对比。
4. 新的 React #418 线上页面抽取结果不再包含旧 recipe 使用的 hydration quote hash。
5. `refresh_stale_status()` 将 `recipe-kb/accepted/react-hydration-mismatch.md`
   移动到 `recipe-kb/stale/react-hydration-mismatch.md`。
6. `tests/test_build_agent_skill.py` 的 packager 断言仍硬编码要求 bundled KB 中存在
   `recipe-kb/accepted/react-hydration-mismatch.md`，因此失败。

## 根因假设

1. 测试把 seed recipe 的状态固定为 accepted，但 packager 的真实契约应该是打包
   KB 中现有的 accepted/stale recipe，而不是强制某个 recipe 必须在 accepted。
2. 采集后 stale 状态是正确业务结果，但 packager 测试没有覆盖 stale recipe 作为
   合法打包产物的路径。
3. 若 packager 实现遗漏 `recipe-kb/stale/`，即使测试修正路径也会暴露真实打包缺口。

## 验证方式

- 检查 `recipe-kb/stale/react-hydration-mismatch.md` 存在且
  `recipe-kb/accepted/react-hydration-mismatch.md` 不存在。
- 运行 `uv run recipe-importer search "Hydration failed"`，确认结果带 `[stale]`。
- 修改测试后运行：
  - `uv run pytest tests/test_build_agent_skill.py -q`
  - `uv run pytest -q`
  - `uv run python scripts/build_agent_skill.py --force`
  - `dist/skills/debug-recipe-importer/scripts/recipe-importer search "Hydration failed"`

## 根因确认

根因是 packager 测试把 recipe 状态路径写死为 `accepted/`，没有跟随采集 refresh 后的
KB 状态迁移；当前业务状态下 recipe 位于 `stale/` 是预期结果。

## 影响范围

- `tests/test_build_agent_skill.py` 中所有依赖固定 recipe 路径的断言。
- `scripts/build_agent_skill.py` 对 `recipe-kb/` 的打包契约：必须包含 accepted/stale
  等 KB 状态目录，而不是只面向 accepted。
- 生成后的 skill wrapper 搜索结果会显示 `[stale]`，下游 agent 需要把该 recipe
  当作需要 refresh/复核的知识，而不是 fresh accepted recipe。

## 修复方案

- 将 packager 测试从固定断言 `recipe-kb/accepted/react-hydration-mismatch.md`
  改为断言当前实际 KB 中的 recipe 状态文件被打包；在本次采集后应为
  `recipe-kb/stale/react-hydration-mismatch.md`。
- 保留 wrapper 搜索断言，但接受输出中的 `[stale]` 标记。
- 如果测试暴露 packager 未包含 `stale/`，则修 packager 的 KB 复制范围。

## 为什么不会引入新问题

此修复只让测试契约与 KB 状态机一致，不改变 recipe 状态迁移逻辑。`recipe-kb/`
仍整体作为静态资产打包，agent 可以检索 stale recipe，但 stale 标记会在搜索输出中
明确暴露，避免把过期 evidence 当作 fresh accepted evidence 使用。
