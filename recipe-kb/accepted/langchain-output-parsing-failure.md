---
id: langchain-output-parsing-failure
kind: debug-recipe
status: accepted
stack:
- langchain
failure_class: langchain/output-parsing
symptoms:
- LangChain output parser raises OutputParserException because it was unable to handle
  model output
fingerprints:
- OUTPUT_PARSING_FAILURE
- OutputParserException
- output parser was unable to handle
- formatting instructions
- structured output
first_checks:
- Check whether the model output matches the expected format defined in the output
  parser
- Check whether formatting instructions in the prompt are specific enough for the
  model
- Check whether a more capable model would follow the formatting instructions reliably
do_not:
- Do not catch OutputParserException and return a default value without first improving
  the prompt
- Do not rely on output parsers when tool calling or structured_output techniques
  are available
evidence_needed:
- Capture the raw model output that failed to parse
- Capture the output parser's expected format or schema
minimal_fix_scope:
- The prompt formatting instructions
- The output parser class and its parsing logic
validation_ladder:
- Reproduce the parsing failure with the failing model output
- Improve the prompt formatting and verify the model produces parseable output
- Run the chain test covering the output parsing step
regression_guard:
- Add a chain test that asserts the output parser succeeds with representative model
  output
evidence_refs:
- source_id: langchain-output-parsing-failure
  url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  final_url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langchain-output-parsing-failure-1
  short_excerpt: OUTPUT_PARSING_FAILURE
  quote_hash: sha256:712d73a5ad2860ab7779d69a9440bf2cb277489178568ede86c0baab2b85940d
- source_id: langchain-output-parsing-failure
  url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  final_url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langchain-output-parsing-failure-2
  short_excerpt: An [output parser](https://reference.langchain.com/python/langchain_core/output_parsers/)
    was unable to handle model output as expected.
  quote_hash: sha256:0d25b707d66fc360ae1f36d8b4aa325356a2ffe531e56f449a09a239a581f370
- source_id: langchain-output-parsing-failure
  url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  final_url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langchain-output-parsing-failure-3
  short_excerpt: Some prebuilt constructs like legacy LangChain agents and chains
    may use output parsers internally, so you may see this error even if you're not
    visibly instantiating and using an output parser.
  quote_hash: sha256:e6ab519cf3b2e46063ef38d33451979c272e6cab6ba085316029b5de49ce8bf5
- source_id: langchain-output-parsing-failure
  url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  final_url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langchain-output-parsing-failure-5
  short_excerpt: Consider using tool calling or other structured output techniques
    if possible without an output parser to reliably output parseable values.
  quote_hash: sha256:f429993a9ac49cb85bc246548d3a679b6adde4638b9af6176ecebefa1fbb0a64
- source_id: langchain-output-parsing-failure
  url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  final_url: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE.md
  source_type: official_error_doc
  captured_at: '2026-05-26T09:17:32.948993Z'
  section_anchor: root
  span_id: langchain-output-parsing-failure-6
  short_excerpt: Add more precise formatting instructions to your prompt.
  quote_hash: sha256:bc4f441e79dd75038d07a72c7ce9250d9fa40203ee1e6a97fcd087b17f7dc62c
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# langchain-output-parsing-failure

## Failure Class
langchain/output-parsing

## Symptoms
- LangChain output parser raises OutputParserException because it was unable to handle model output

## Fingerprints
- OUTPUT_PARSING_FAILURE
- OutputParserException
- output parser was unable to handle
- formatting instructions
- structured output

## First Checks
- Check whether the model output matches the expected format defined in the output parser
- Check whether formatting instructions in the prompt are specific enough for the model
- Check whether a more capable model would follow the formatting instructions reliably

## Do Not Patch Yet
- Do not catch OutputParserException and return a default value without first improving the prompt
- Do not rely on output parsers when tool calling or structured_output techniques are available

## Evidence Needed
- Capture the raw model output that failed to parse
- Capture the output parser's expected format or schema

## Minimal Fix Scope
- The prompt formatting instructions
- The output parser class and its parsing logic

## Validation Ladder
- Reproduce the parsing failure with the failing model output
- Improve the prompt formatting and verify the model produces parseable output
- Run the chain test covering the output parsing step

## Regression Guard
- Add a chain test that asserts the output parser succeeds with representative model output

## Reviewer Notes
