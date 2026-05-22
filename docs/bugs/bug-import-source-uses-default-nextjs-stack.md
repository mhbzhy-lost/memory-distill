# Import Source Uses Default Nextjs Stack

## 现象

`recipe-importer import-source <snapshot>` 默认使用 `stack=["react", "nextjs"]`。
当 snapshot 来自 React-only、Vite 或 TanStack Query source 时，如果调用方不显式传
`--stack`，最终 recipe 会被错误标记为 Next.js recipe。

## 调用链

1. `recipe-importer fetch` 将 source 的 `stacks` 写入 snapshot 的 `response.json`。
2. `recipe-importer import-source <snapshot>` 进入 CLI `import_source()`。
3. 当前 `stack` 参数默认值是 `["react", "nextjs"]`。
4. `import_source()` 调用 `normalize_recipe(candidate, snapshot_dir, stack=stack)`。
5. 对 `react-invalid-hook-call`、`vite-troubleshooting`、`tanstack-query-*` 等 source，
   未显式传 `--stack` 时 recipe stack 与 source metadata 不一致。

## 根因假设

1. 早期 vertical slice 只支持 hydration/Next.js，因此默认 stack 被写死。
2. `import-source` 没有优先读取 snapshot 的 `response.json.stacks`。
3. 缺少非 Next.js source 的 CLI 回归测试。

## 验证方式

- 新增 CLI 测试：`response.json` 中写入 `stacks: ["react", "vite"]`，调用
  `import-source` 不传 `--stack`。
- 断言传给 `normalize_recipe()` 的 stack 来自 snapshot metadata。
- 保留显式 `--stack` 覆盖能力。

## 根因确认

根因是 `import-source` 把 hydration vertical slice 的默认栈当作所有 source 的默认值，
没有使用 source snapshot 中已采集的 stack metadata。

后续外源复审还指出：如果 `response.json` 存在但内容损坏，或虽然是合法 JSON 但顶层
不是对象，当前读取 stack 的逻辑也可能直接崩溃，无法走到保守 fallback。

## 影响范围

- 所有非 Next.js source 生成的 recipe。
- `recipe-kb/index.json` 的 stack 检索结果。
- 打包后的 `debug-recipe-importer` skill 搜索与 agent 选用 recipe 的准确性。

## 修复方案

- 将 CLI `stack` 默认值改为 `None`。
- 未显式传 `--stack` 时读取 `snapshot/response.json` 的 `stacks` 字段。
- 若 metadata 缺失 stacks，再回退到 `["react", "nextjs"]` 以保持旧 fixture 可用。
- 若 `response.json` 缺失、损坏或结构不是对象，同样回退到 `["react", "nextjs"]`，避免旧
  snapshot 或部分写入的 metadata 让导入流程崩溃。
- fallback 时记录 warning，避免批量处理时静默污染 stack。

## 为什么不会引入新问题

source list 已要求每个 source 有 `stacks`，fetch 也会把 metadata 写进 snapshot。
显式 `--stack` 仍然优先，旧调用方如果传参不会受影响；缺失 metadata 的旧测试 fixture
仍有保守 fallback。
