---
id: arkts-no-comma-outside-loops
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/arkts-syntax
symptoms:
- 'ArkTS compiler error: arkts-no-comma-outside-loops (10605071) — comma operator
  only allowed in for loop header'
fingerprints:
- arkts-no-comma-outside-loops
- '10605071'
- comma operator
- 逗号运算符
- 逗号运算符仅适用于 for 循环
first_checks:
- Check whether the comma operator is used as an expression (value1, value2) not as
  a separator in declarations or function arguments
- Check whether the comma is inside a for loop header (allowed) vs. in a general expression
  (not allowed)
- Check whether the intended semantics is sequential expression evaluation or just
  a multi-value return
do_not:
- Do not use the comma operator to chain side effects in arbitrary expressions; use
  separate statements
- Do not confuse the comma expression operator with the comma used in variable declarations
  or function call arguments
evidence_needed:
- Capture the compiler error showing arkts-no-comma-outside-loops with error code
  10605071
- Identify the comma expression site and its intended semantics
minimal_fix_scope:
- The comma expression site
- The surrounding statement or block where the sequential logic is split into separate
  statements
validation_ladder:
- Split the comma expression into separate statements or move to a for loop header;
  verify no 10605071 error
- Verify the sequential semantics is preserved after the refactor
- Run the build or compile step for the affected module
regression_guard:
- Add a type-check or lint step that flags comma expression usage outside for loops
  in .ets files
evidence_refs:
- source_id: arkts-migration-guide
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  source_type: official_error_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: arkts-migration-guide-42
  short_excerpt: '### 逗号运算符`,`仅用在`for`循环语句中 **规则：**`arkts-no-comma-outside-loops`
    **级别：错误** **错误码：10605071** 在ArkTS中，逗号运算符仅适用于`for`循环语句，用于明确执行顺序。 >**注意：** 这与声明变量和函数参数传递时使用的逗号分隔符不同。
    **TypeScript** ```typescript for (let i = 0, j = 0; i < 10; ++i, j += 2) { //
    ... } let x = 0; x = (++x, x++); // 1 ``` **ArkTS** ```typescript for (let i =
    0, j = 0; i < 10; ++i, j += 2) { // ... } // 通过语句表示执行顺序，而非逗号运算符 let x = 0; ++x;
    x = x++; ```'
  quote_hash: sha256:d12ab29b4b788a135310db67bf45cc29b4f4d569f0c8e3ef9abbe0bceaa86d92
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-no-comma-outside-loops

## Failure Class
harmonyos/arkts-syntax

## Symptoms
- ArkTS compiler error: arkts-no-comma-outside-loops (10605071) — comma operator only allowed in for loop header

## Fingerprints
- arkts-no-comma-outside-loops
- 10605071
- comma operator
- 逗号运算符
- 逗号运算符仅适用于 for 循环

## First Checks
- Check whether the comma operator is used as an expression (value1, value2) not as a separator in declarations or function arguments
- Check whether the comma is inside a for loop header (allowed) vs. in a general expression (not allowed)
- Check whether the intended semantics is sequential expression evaluation or just a multi-value return

## Do Not Patch Yet
- Do not use the comma operator to chain side effects in arbitrary expressions; use separate statements
- Do not confuse the comma expression operator with the comma used in variable declarations or function call arguments

## Evidence Needed
- Capture the compiler error showing arkts-no-comma-outside-loops with error code 10605071
- Identify the comma expression site and its intended semantics

## Minimal Fix Scope
- The comma expression site
- The surrounding statement or block where the sequential logic is split into separate statements

## Validation Ladder
- Split the comma expression into separate statements or move to a for loop header; verify no 10605071 error
- Verify the sequential semantics is preserved after the refactor
- Run the build or compile step for the affected module

## Regression Guard
- Add a type-check or lint step that flags comma expression usage outside for loops in .ets files

## Reviewer Notes
