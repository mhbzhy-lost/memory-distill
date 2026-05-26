# parse_recipe_file splits on dashes inside YAML content

## 现象

`recipe-importer publish` 对新生成的 `gradle-daemon-connection-failed.md` 报错：

```
ScannerError: while scanning a quoted scalar
found unexpected end of stream
```

错误位置：`render.py:99` `yaml.safe_load(frontmatter)` 收到的 frontmatter 被截断在
`short_excerpt: '` 处。

## 调用链

`publish` → `publish_recipe` → `check_render_equivalence` → `parse_recipe_file` →
`text.split("---", 2)` → `yaml.safe_load(frontmatter)`

## 根因假设

1. **`split("---", 2)` 误命中内容中的 `---`**
   - Gradle 版本输出 banner 为 60+ 个连续 `-`，出现在 `short_excerpt` 字段内
   - `split("---", 2)` 在前两段 `---`（file 开头 + evidence 内 `---`）处切割，导致
     后续 YAML 结构被截断
2. **`split("---", 2)` 只找第一、第二个 `---`，不考虑行首位置**

## 验证方式

```python
text = "---\nid: x\nshort_excerpt: '---abc'\n---\n\nbody"
_, fm, _ = text.split("---", 2)
yaml.safe_load(fm)  # truncation expected
```

## 根因确认

`parse_recipe_file` 使用 `text.split("---", 2)` 做 frontmatter 提取。当 YAML
内容（如 `short_excerpt` 字段）含有 `---` 子串时，split 点落在内容内而非 frontmatter
结束标记处，frontmatter 被截断。

## 影响范围

- 任何 recipe 的 `short_excerpt`、`symptoms`、`fingerprints` 等字段如果包含
  `---` 作为子串（日志输出、代码片段、版本号 banner 等），`publish`、`check`、
  `normalize`、`search` 都会失败。

## 修复方案

### 根因修复

将 `parse_recipe_file` 中的 `text.split("---", 2)` 替换为基于行边界的查找：
用 `text.find("\n---\n", start)` 定位 frontmatter 的结束 `---`（必须以换行符围
绕），而非任意子串匹配。这消除了内容中含 `---` 子串时的误命中。

回退策略：若 `text.find("\n---\n", start)` 未找到（极少数格式变体），回退到
原始 `split("---", 2)`，确保向前兼容。

### 安全性

- 行分隔符 `\n---\n` 匹配只对标准 frontmatter 边界命中，YAML 内容中的
  `---` 子串（如日志 banner `----...`）不会被匹配，因为它们不会恰好前后
  各有一个换行符形成行边界。
- 原始 `split` 回退保证了对无换行变体（例如文件末尾 `---` 后无换行）的兼容，
  避免引入新故障模式。

### 回归测试

`tests/test_normalize_render.py::test_parse_recipe_file_with_dashes_in_excerpt`
覆盖此根因路径：验证 `short_excerpt` 字段中含 `---` 子串时，`parse_recipe_file`
能正确恢复完整 frontmatter。
