# Accepted Recipe Trailing Blank

## 现象

最终 code-quality reviewer 运行：

```bash
git diff --check 6cd7e32..HEAD
```

失败信息：

```text
recipe-kb/accepted/react-hydration-mismatch.md:102: new blank line at EOF.
```

本地复现同样失败。`tail` 显示 accepted recipe 的 Markdown body 以
`## Reviewer Notes` 后的空行结束。

## 调用链

1. Task12 为当前仓库生成真实 KB seed。
2. `recipe-importer import-source` 调用 `render_recipe_file(recipe, proposed_path)`。
3. `recipe-importer publish` 调用 `publish_recipe()`，通过 `parse_recipe_file()` 读取
   proposed recipe，再调用 `render_recipe_file()` 写入 accepted recipe。
4. `render_recipe_file()` 调用 `render_recipe_text()`。
5. `render_recipe_text()` 拼接 YAML frontmatter 和 `render_body(recipe)`。
6. `render_body()` 的最后一个 section 是 `"## Reviewer Notes\n"`，随后整体再追加
   `"\n"`，因此生成文件末尾有一个空白行。
7. `git diff --check 6cd7e32..HEAD` 对新增文件报告 `new blank line at EOF`。

## 根因假设

1. `render_body()` 的 `Reviewer Notes` section 自带尾随换行，并且函数末尾再次追加
   换行，导致生成的每个 recipe 都以空白行结束。
2. 只是在 accepted recipe 生成过程中额外多写了一行，而 proposed/render 路径本身没有问题。

## 验证方式

- 运行 `git diff --check 6cd7e32..HEAD` 复现 whitespace failure。
- 检查 `src/recipe_importer/render.py` 中 `render_body()` 的最后一个 section。
- 修复后增加单测，直接断言 `render_recipe_text(recipe)` 不以 `"\n\n"` 结尾。
- 修复后重新运行：
  - `uv run pytest tests/test_normalize_render.py tests/test_vertical_slice.py -q`
  - `uv run pytest -q`
  - `git diff --check 6cd7e32..HEAD`
  - `uv run recipe-importer check recipe-kb/accepted/react-hydration-mismatch.md`

## 根因确认

根因是 `render_body()` 对最后一个 `Reviewer Notes` section 追加了多余换行，生成
recipe 文件时保留了 EOF 空白行；accepted seed 只是暴露了这个 renderer 层问题。

## 影响范围

- 所有通过 `render_recipe_file()` 生成的 proposed / accepted / stale recipe 都可能带
  EOF 空白行。
- `check_render_equivalence()` 会把这个空白行视作当前 canonical output 的一部分；
  因此不能只手动删除 committed recipe 末尾空行，必须修 renderer 并重生成 recipe。
- 受影响的验证路径包括 `git diff --check`、Task12 final verification，以及后续任何
  新增 generated recipe 文件。

## 修复方案

- 将 `render_body()` 的最后一个 section 改为不自带尾随换行，让整体渲染结果只以单个
  文件终止换行结束。
- 增加 renderer 单测，覆盖生成文本不以空白行结束。
- 重新生成 / 调整 `recipe-kb/accepted/react-hydration-mismatch.md`，确保仍通过
  render-equivalence check。

## 为什么不会引入新问题

Markdown section 间仍由 `"\n\n"` 分隔，文件仍保留单个 POSIX 终止换行；只移除 EOF
额外空白行。`check_render_equivalence()` 会同步使用新的 renderer 输出，确保现有 seed
和 future generated recipe 的语义一致。
