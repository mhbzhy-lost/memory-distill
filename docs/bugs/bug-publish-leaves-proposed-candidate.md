# Publish Leaves Proposed Candidate

## 现象

执行：

```bash
uv run recipe-importer publish recipe-kb/proposed/react-hydration-mismatch.md
```

后，命令生成了：

```text
recipe-kb/accepted/react-hydration-mismatch.md
```

但源文件仍然留在：

```text
recipe-kb/proposed/react-hydration-mismatch.md
```

这会让 `recipe-importer review` / `review current` 继续把已经发布的 recipe 当作待审候选展示。

## 调用链

1. `recipe-importer import-source` 生成 `proposed/<recipe>.md`。
2. 人审批准后，`recipe-importer publish proposed/<recipe>.md` 调用 `publish_recipe()`。
3. `publish_recipe()` 校验 proposed 路径和 render-equivalence。
4. `publish_recipe()` 将 recipe 状态改为 accepted 并写入 `accepted/<recipe>.md`。
5. 当前实现返回 accepted 路径，但没有删除源 proposed 文件。
6. review queue 由 `review._candidate_files()` 扫描 `proposed/*.md` 得到。
7. 因此已发布 recipe 仍会留在待审队列里。

## 根因假设

1. publish 被实现为“复制并改状态”，而不是“状态迁移”，导致源 proposed 未被消费。
2. review queue 只看 `proposed/` 目录，没有额外排除已 accepted 的同名文件。
3. 缺少 publish 后 review queue 清空的回归测试。

## 验证方式

- 新增测试：publish 一个 proposed recipe 后，断言源 proposed 文件不存在。
- 同时断言 `review current` 对空队列应报告 `review queue is empty`。

## 根因确认

根因是 publish 没有把 proposed 候选迁移出待审队列，导致已发布 recipe 仍被人审流程看见。

## 影响范围

- 所有通过 `publish` 发布的 proposed recipe。
- 人审 CLI 的 `current` / `next` / `prev` 队列语义。
- 自动化流水线中依赖 proposed 目录判断“是否还有待审条目”的步骤。

## 修复方案

- 在 `publish_recipe()` 成功写入 accepted 并清理同名 stale 后，删除源 proposed 文件。
- 增加回归测试覆盖 publish 后 proposed 被消费、review queue 为空。

## 为什么不会引入新问题

删除范围限定为传入的 `proposed_path`，且只在 accepted 写入和 render-equivalence 校验成功后执行。
publish 失败时 proposed 保留，便于重新审查或修复；publish 成功后 proposed 已被 accepted 状态替代。
