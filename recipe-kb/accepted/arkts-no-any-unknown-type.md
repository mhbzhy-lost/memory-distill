---
id: arkts-no-any-unknown-type
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/arkts-syntax
symptoms:
- 'ArkTS compiler error: arkts-no-any-unknown (10605008) — any and unknown types are
  not supported'
fingerprints:
- arkts-no-any-unknown
- arkts-no-any
- '10605008'
- any type not supported
- unknown type not supported
- 显式指定具体类型
first_checks:
- Check whether the variable or parameter is typed as any or unknown
- Check whether the function return type is any or unknown and replace with the actual
  return type
- Check whether an external library API returns any and the result needs to be typed
  with a class or interface
do_not:
- Do not replace any with Object if you need specific field access; define a class
  or interface
- Do not use ESObject as a drop-in replacement for any in .ets files without checking
  API version restrictions
evidence_needed:
- Capture the compiler error showing arkts-no-any-unknown with error code 10605008
- Identify the type declaration site where any or unknown is used
minimal_fix_scope:
- The variable, parameter, or return type annotation using any/unknown
- The class or interface definition that replaces the unknown type
validation_ladder:
- Replace any or unknown with a concrete type and verify no 10605008 error
- Verify the code still compiles and the runtime behavior is unchanged
- Run the module build or type-check step
regression_guard:
- Add a type-check step that flags any or unknown in .ets files
evidence_refs:
- source_id: arkts-migration-guide
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  source_type: official_error_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: arkts-migration-guide-13
  short_excerpt: '### 使用具体的类型而非`any`或`unknown` **规则：**`arkts-no-any-unknown` **级别：错误**
    **错误码：10605008** ArkTS不支持`any`和`unknown`类型。显式指定具体类型。 **TypeScript** ```typescript
    let value1: any value1 = true; value1 = 42; let value2: unknown value2 = true;
    value2 = 42; ``` **ArkTS** ```typescript let value_b: boolean = true; // 或者 let
    value_b = true let value_n: number = 42; // 或者 let value_n = 42 let value_o1:
    Object = true; let value_o2: Object = 42; ```'
  quote_hash: sha256:fd5ee840bcb695b521beb3f3e0bed8b1234018534b0fb380275bf253e800d6cf
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-no-any-unknown-type

## Failure Class
harmonyos/arkts-syntax

## Symptoms
- ArkTS compiler error: arkts-no-any-unknown (10605008) — any and unknown types are not supported

## Fingerprints
- arkts-no-any-unknown
- arkts-no-any
- 10605008
- any type not supported
- unknown type not supported
- 显式指定具体类型

## First Checks
- Check whether the variable or parameter is typed as any or unknown
- Check whether the function return type is any or unknown and replace with the actual return type
- Check whether an external library API returns any and the result needs to be typed with a class or interface

## Do Not Patch Yet
- Do not replace any with Object if you need specific field access; define a class or interface
- Do not use ESObject as a drop-in replacement for any in .ets files without checking API version restrictions

## Evidence Needed
- Capture the compiler error showing arkts-no-any-unknown with error code 10605008
- Identify the type declaration site where any or unknown is used

## Minimal Fix Scope
- The variable, parameter, or return type annotation using any/unknown
- The class or interface definition that replaces the unknown type

## Validation Ladder
- Replace any or unknown with a concrete type and verify no 10605008 error
- Verify the code still compiles and the runtime behavior is unchanged
- Run the module build or type-check step

## Regression Guard
- Add a type-check step that flags any or unknown in .ets files

## Reviewer Notes
