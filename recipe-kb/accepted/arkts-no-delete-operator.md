---
id: arkts-no-delete-operator
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/arkts-syntax
symptoms:
- 'ArkTS compiler error: arkts-no-delete (10605059) — delete operator is not supported'
fingerprints:
- arkts-no-delete
- '10605059'
- delete operator
- delete 运算符
- 不支持 delete
first_checks:
- Check whether the code uses the delete operator on an object property
- Check whether the intent is to remove a property from an object or delete an array
  element
- Check whether the target is a Map and Map.delete() should be used instead
do_not:
- Do not set the property to undefined or null as equivalent to deletion; ArkTS object
  layout is fixed at compile time
- Do not use Reflect.deleteProperty as an alternative; it is also restricted in ArkTS
  static mode
evidence_needed:
- Capture the compiler error showing arkts-no-delete with error code 10605059
- Identify the property and object that the delete operation targets
minimal_fix_scope:
- The delete expression site
- The data structure used to represent the object or collection
validation_ladder:
- Replace delete with an appropriate alternative (Map.delete(), array splice, or field
  reset) and verify no 10605059 error
- Verify the runtime behavior matches the original intent
- Run the build or compile step for the affected module
regression_guard:
- Add a type-check or lint step that flags delete operator usage in .ets files
evidence_refs:
- source_id: arkts-migration-guide
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  source_type: official_error_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: arkts-migration-guide-37
  short_excerpt: '### 不支持`delete`运算符 **规则：**`arkts-no-delete` **级别：错误** **错误码：10605059**
    在ArkTS中，对象布局于编译时确定，运行时不可更改，因此删除属性的操作无意义。 **TypeScript** ```typescript class Point
    { x?: number = 0.0 y?: number = 0.0 } let p = new Point(); delete p.y; ``` **ArkTS**
    ```typescript // 可以声明一个可空类型并使用null作为缺省值 class Point { x: number | null = 0 y:
    number | null = 0 } let p = new Point(); p.y = null; ```'
  quote_hash: sha256:f62732582af2d6b861a7a715e0325104341b7e38794c63c68ce061a4dc9d34c5
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-no-delete-operator

## Failure Class
harmonyos/arkts-syntax

## Symptoms
- ArkTS compiler error: arkts-no-delete (10605059) — delete operator is not supported

## Fingerprints
- arkts-no-delete
- 10605059
- delete operator
- delete 运算符
- 不支持 delete

## First Checks
- Check whether the code uses the delete operator on an object property
- Check whether the intent is to remove a property from an object or delete an array element
- Check whether the target is a Map and Map.delete() should be used instead

## Do Not Patch Yet
- Do not set the property to undefined or null as equivalent to deletion; ArkTS object layout is fixed at compile time
- Do not use Reflect.deleteProperty as an alternative; it is also restricted in ArkTS static mode

## Evidence Needed
- Capture the compiler error showing arkts-no-delete with error code 10605059
- Identify the property and object that the delete operation targets

## Minimal Fix Scope
- The delete expression site
- The data structure used to represent the object or collection

## Validation Ladder
- Replace delete with an appropriate alternative (Map.delete(), array splice, or field reset) and verify no 10605059 error
- Verify the runtime behavior matches the original intent
- Run the build or compile step for the affected module

## Regression Guard
- Add a type-check or lint step that flags delete operator usage in .ets files

## Reviewer Notes
