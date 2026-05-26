# 快照人审：kotlin-serialization-basic-errors

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
- 最终 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
- 来源类型: library_doc
- 采集时间: 2026-05-26T10:27:19.494775Z
- HTTP 状态: 200
- 内容哈希: sha256:6b22e35bb77a8c27c5bc5ee567b12bb4e0ac977f2f8dc4247ee3d0b9ca7bad04
- 技术栈: kotlin, android
- 抽取段落数: 0

## QA 闸门
- 状态: 需要 agentic fallback
- sections_non_empty: 失败；抽取段落数: 0
- section_count_within_bounds: 失败；期望范围: 1-500
- expected_hints_matched: 失败；命中 0/6 条 expected_failure_hints
- fallback: 启动 agentic loop
- fallback 输入: raw.html, response.json, sections.json, review.md
- fallback 要求: 读取 raw.html、response.json、sections.json、review.md，产出最小 extraction_profile 或 extractor patch，并补回归测试。

## 预期线索命中
- `Serializer for class ... is not found`：未找到直接段落命中
- `Please ensure that class is marked as '@Serializable'`：未找到直接段落命中
- `MissingFieldException`：未找到直接段落命中
- `JsonDecodingException Unexpected JSON token`：未找到直接段落命中
- `Encountered an unknown key`：未找到直接段落命中
- `Expected string literal but 'null' literal was found`：未找到直接段落命中

## 段落样例
- 未抽取到段落。

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
