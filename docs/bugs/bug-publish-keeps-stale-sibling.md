# Publish Keeps Stale Sibling

## 现象

当前工作流中，`react-hydration-mismatch` 的旧 accepted recipe 在 refresh 后已被移动到：

```text
recipe-kb/stale/react-hydration-mismatch.md
```

修复 `react-error-418` 抽取后，重新执行：

```bash
uv run recipe-importer import-source recipe-kb/snapshots/react-error-418
```

会生成：

```text
recipe-kb/proposed/react-hydration-mismatch.md
```

如果继续执行 publish，现有 `publish_recipe()` 只会把 proposed 写入
`recipe-kb/accepted/react-hydration-mismatch.md`，不会删除同名 stale 文件。
随后 `index rebuild` 会同时索引 accepted 与 stale 两条同 ID recipe。

## 调用链

1. `recipe-importer refresh` 检测 accepted recipe 的 evidence quote hash 已变化。
2. `refresh_stale_status()` 把旧 recipe 写入 `stale/`，并删除 accepted 版本。
3. `recipe-importer import-source` 基于刷新后的 snapshot 生成同 ID proposed recipe。
4. `recipe-importer publish` 调用 `publish_recipe(proposed_path, paths)`。
5. `publish_recipe()` 校验 proposed 路径与 render-equivalence。
6. `publish_recipe()` 将 recipe 状态改为 accepted，并写入 `accepted/<name>.md`。
7. 当前实现没有检查或清理 `stale/<name>.md`。
8. `rebuild_index()` 遍历 `accepted/` 和 `stale/`，因此同 ID 会出现两条记录。

## 根因假设

1. publish 流程只处理 proposed -> accepted，没有定义“同 ID stale 被新证据替代”的状态迁移。
2. index 构建器没有去重或冲突检测，因此会暴露 accepted/stale 同 ID 重复。
3. refresh 与 publish 的组合路径缺少回归测试，导致该状态组合未被覆盖。

## 验证方式

- 新增测试：先构造同名 `stale/react-hydration-mismatch.md`，再 publish
  `proposed/react-hydration-mismatch.md`。
- 断言 publish 后：
  - `accepted/react-hydration-mismatch.md` 存在；
  - `stale/react-hydration-mismatch.md` 不存在；
  - `index rebuild` 后同 ID 只出现一条 accepted 记录。

## 根因确认

根因是 publish 缺少“新 accepted 替代同名 stale”的状态迁移逻辑，导致 refresh 后重新采集的 recipe
无法闭环回到唯一 accepted 状态。

## 影响范围

- 所有 refresh 后进入 stale、随后又重新 import/publish 的同 ID recipe。
- `search --fresh-only` 之外的普通 search 结果可能出现同 ID 双记录。
- `get_recipe()` 会返回索引中第一个同 ID，结果依赖目录遍历顺序，不适合长期保留重复状态。

## 修复方案

- 在 `publish_recipe()` 写入 accepted 后，删除同名 stale sibling。
- 删除 stale sibling 时使用 `missing_ok=True`，避免并发 publish 或人工清理导致
  `exists()` 与 `unlink()` 之间发生竞态。
- 新增覆盖 refresh 后 re-publish 的单测，确保 index 中同 ID 只保留 accepted 记录。

## 为什么不会引入新问题

删除范围只限定为 `paths.stale_dir / proposed_path.name` 这个同名 sibling，不会影响其他 stale recipe。
当用户发布一个同 ID 新版本时，旧 stale 已被新 accepted 替代，继续保留同名 stale 只会制造索引歧义。
