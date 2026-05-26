---
id: arkts-no-destruct-assignment
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/arkts-syntax
symptoms:
- 'ArkTS compiler error: arkts-no-destruct-assignment (10605069) — destructuring assignment
  is not supported'
fingerprints:
- arkts-no-destruct-assignment
- '10605069'
- destructuring assignment
- 解构赋值
- 不支持解构
first_checks:
- Check whether the code uses array or object destructuring in an assignment (left
  side is a pattern)
- Check whether destructuring is used for swapping variables or extracting nested
  fields
- Check whether the destructuring target is a function return value or an external
  data structure
do_not:
- Do not convert destructuring to indexed access ([a, b] = [x, y]) without ensuring
  the array is typed
- Do not use temporary variable assignment inside an expression to mimic destructuring;
  use separate statements
evidence_needed:
- Capture the compiler error showing arkts-no-destruct-assignment with error code
  10605069
- Identify the destructuring pattern and the source value
minimal_fix_scope:
- The destructuring assignment expression
- The separate assignment statements used as replacement
validation_ladder:
- Replace destructuring with separate variable assignments and verify no 10605069
  error
- Verify the replaced code produces identical values at runtime
- Run the build or compile step for the affected module
regression_guard:
- Add a type-check or lint step that flags destructuring patterns in .ets files
evidence_refs:
- source_id: arkts-migration-guide
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  source_type: official_error_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: arkts-migration-guide-41
  short_excerpt: '### 不支持解构赋值 **规则：**`arkts-no-destruct-assignment` **级别：错误** **错误码：10605069**
    ArkTS不支持解构赋值。可使用其他替代方法，例如，使用临时变量。 **TypeScript** ```typescript let [one, two]
    = [1, 2]; // 此处需要分号 [one, two] = [two, one]; let head, tail [head, ...tail] =
    [1, 2, 3, 4]; ``` **ArkTS** ```typescript let arr: number[] = [1, 2]; let one
    = arr[0]; let two = arr[1]; let tmp = one; one = two; two = tmp; let data: Number[]
    = [1, 2, 3, 4]; let head = data[0]; let tail: Number[] = []; for (let i = 1; i
    < data.length; ++i) { tail.push(data[i]); } ```'
  quote_hash: sha256:9ba9a7388130ff9f8e03910a46583715a3a313f9910b2bfb8498364f29cf5d87
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-no-destruct-assignment

## Failure Class
harmonyos/arkts-syntax

## Symptoms
- ArkTS compiler error: arkts-no-destruct-assignment (10605069) — destructuring assignment is not supported

## Fingerprints
- arkts-no-destruct-assignment
- 10605069
- destructuring assignment
- 解构赋值
- 不支持解构

## First Checks
- Check whether the code uses array or object destructuring in an assignment (left side is a pattern)
- Check whether destructuring is used for swapping variables or extracting nested fields
- Check whether the destructuring target is a function return value or an external data structure

## Do Not Patch Yet
- Do not convert destructuring to indexed access ([a, b] = [x, y]) without ensuring the array is typed
- Do not use temporary variable assignment inside an expression to mimic destructuring; use separate statements

## Evidence Needed
- Capture the compiler error showing arkts-no-destruct-assignment with error code 10605069
- Identify the destructuring pattern and the source value

## Minimal Fix Scope
- The destructuring assignment expression
- The separate assignment statements used as replacement

## Validation Ladder
- Replace destructuring with separate variable assignments and verify no 10605069 error
- Verify the replaced code produces identical values at runtime
- Run the build or compile step for the affected module

## Regression Guard
- Add a type-check or lint step that flags destructuring patterns in .ets files

## Reviewer Notes
