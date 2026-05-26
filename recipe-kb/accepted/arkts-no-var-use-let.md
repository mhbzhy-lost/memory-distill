---
id: arkts-no-var-use-let
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/arkts-syntax
symptoms:
- 'ArkTS compiler error: arkts-no-var (10605005) — var keyword is not supported, use
  let instead'
fingerprints:
- arkts-no-var
- '10605005'
- var keyword not supported
- ArkTS 不支持 var
- let 声明变量
first_checks:
- Check whether the variable declaration uses var instead of let or const
- Check whether the variable scope was intentionally block-scoped and convert to let
- Check whether the code is .ets or .ts file (var works in .ts but not .ets)
do_not:
- Do not use @ts-ignore to silence the ArkTS compiler for var usage
- Do not convert to const if the variable is reassigned later; use let
evidence_needed:
- Capture the compiler error message showing arkts-no-var with error code 10605005
- Identify the file and line where var is declared
minimal_fix_scope:
- The var declaration site
- The surrounding scope if the variable needs block-level scoping
validation_ladder:
- Replace var with let and verify the ArkTS compiler no longer reports 10605005
- Verify the variable still behaves correctly in its block scope
- Run the build or compile step for the affected module
regression_guard:
- Add a CI lint or type-check step that flags var usage in .ets files
evidence_refs:
- source_id: arkts-migration-guide
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  source_type: official_error_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: arkts-migration-guide-12
  short_excerpt: '### 使用`let`而非`var` **规则：**`arkts-no-var` **级别：错误** **错误码：10605005**
    `let`关键字可以在块级作用域中声明变量，帮助程序员避免错误。因此，ArkTS不支持`var`，请使用`let`声明变量。 **TypeScript**
    ```typescript function f(shouldInitialize: boolean) { if (shouldInitialize) {
    var x = ''b''; } return x; } console.info(f(true)); // b console.info(f(false));
    // undefined let upperLet = 0; { var scopedVar = 0; let scopedLet = 0; upperLet
    = 5; } scopedVar = 5; // 可见 scopedLet = 5; // 编译时错误 ``` **ArkTS** ```typescript
    function f(shouldInitialize: boolean): string { let x: string = ''a''; if (shouldInitialize)
    { x = ''b''; } return x; } console.info(f(true))'
  quote_hash: sha256:d6dde5b9624ee42c22d3bb1d716805eeee930e6b57cc342c266824c346fff374
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-no-var-use-let

## Failure Class
harmonyos/arkts-syntax

## Symptoms
- ArkTS compiler error: arkts-no-var (10605005) — var keyword is not supported, use let instead

## Fingerprints
- arkts-no-var
- 10605005
- var keyword not supported
- ArkTS 不支持 var
- let 声明变量

## First Checks
- Check whether the variable declaration uses var instead of let or const
- Check whether the variable scope was intentionally block-scoped and convert to let
- Check whether the code is .ets or .ts file (var works in .ts but not .ets)

## Do Not Patch Yet
- Do not use @ts-ignore to silence the ArkTS compiler for var usage
- Do not convert to const if the variable is reassigned later; use let

## Evidence Needed
- Capture the compiler error message showing arkts-no-var with error code 10605005
- Identify the file and line where var is declared

## Minimal Fix Scope
- The var declaration site
- The surrounding scope if the variable needs block-level scoping

## Validation Ladder
- Replace var with let and verify the ArkTS compiler no longer reports 10605005
- Verify the variable still behaves correctly in its block scope
- Run the build or compile step for the affected module

## Regression Guard
- Add a CI lint or type-check step that flags var usage in .ets files

## Reviewer Notes
