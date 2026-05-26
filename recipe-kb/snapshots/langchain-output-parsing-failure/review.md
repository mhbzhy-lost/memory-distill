# 快照人审：langchain-output-parsing-failure

## 快照质量检查
- 来源 URL: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
- 最终 URL: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
- 来源类型: official_error_doc
- 采集时间: 2026-05-26T09:17:32.948993Z
- HTTP 状态: 200
- 内容哈希: sha256:8c133f74a38bcc37cc0823a5dc9ec394c4b83aa31a5f1976bb5a50af0bc3bbda
- 技术栈: langchain
- 抽取段落数: 7

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 7
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 5/5 条 expected_failure_hints

## 预期线索命中
- `OUTPUT_PARSING_FAILURE`
  - [langchain-output-parsing-failure-1] OUTPUT_PARSING_FAILURE
- `OutputParserException`
  - [langchain-output-parsing-failure-2] An [output parser](https://reference.langchain.com/python/langchain_core/output_parsers/) was unable to handle model output as expected.
  - [langchain-output-parsing-failure-3] Some prebuilt constructs like legacy LangChain agents and chains may use output parsers internally, so you may see this error even if you're not visibly instantiating and using an output parser.
  - [langchain-output-parsing-failure-5] Consider using tool calling or other structured output techniques if possible without an output parser to reliably output parseable values.
- `output parser was unable to handle model output`
  - [langchain-output-parsing-failure-2] An [output parser](https://reference.langchain.com/python/langchain_core/output_parsers/) was unable to handle model output as expected.
- `formatting instructions`
  - [langchain-output-parsing-failure-6] Add more precise formatting instructions to your prompt.
- `structured output`
  - [langchain-output-parsing-failure-5] Consider using tool calling or other structured output techniques if possible without an output parser to reliably output parseable values.

## 段落样例
- [langchain-output-parsing-failure-1] OUTPUT_PARSING_FAILURE
- [langchain-output-parsing-failure-2] An [output parser](https://reference.langchain.com/python/langchain_core/output_parsers/) was unable to handle model output as expected.
- [langchain-output-parsing-failure-3] Some prebuilt constructs like legacy LangChain agents and chains may use output parsers internally, so you may see this error even if you're not visibly instantiating and using an output parser.
- [langchain-output-parsing-failure-4] Troubleshooting
- [langchain-output-parsing-failure-5] Consider using tool calling or other structured output techniques if possible without an output parser to reliably output parseable values.
- [langchain-output-parsing-failure-6] Add more precise formatting instructions to your prompt.
- [langchain-output-parsing-failure-7] If you are using a smaller or less capable model, try using a more capable one.

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
