---
id: arkts-no-for-in-loop
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/arkts-syntax
symptoms:
- 'ArkTS compiler error: arkts-no-for-in (10605080) — for..in loop over object properties
  is not supported'
fingerprints:
- arkts-no-for-in
- '10605080'
- for .. in
- for..in
- 不支持 for..in
first_checks:
- Check whether the code uses a for..in loop to iterate over object keys
- Check whether the intent is to iterate over properties, array indices, or a Map's
  keys
- Check whether the object is typed and all its keys are known at compile time
do_not:
- Do not use Object.keys() as a drop-in replacement without verifying the object type
  is compatible
- Do not convert for..in to for..of on an untyped array; ensure the array is explicitly
  typed
evidence_needed:
- Capture the compiler error showing arkts-no-for-in with error code 10605080
- Identify the object being iterated and the properties accessed inside the loop
minimal_fix_scope:
- The for..in loop and its body
- The data structure iteration (convert to for..of on Object.keys or array iteration)
validation_ladder:
- Replace for..in with for..of on typed keys or array iteration and verify no 10605080
  error
- Verify the iteration produces identical property access sequence
- Run the build or compile step for the affected module
regression_guard:
- Add a type-check or lint step that flags for..in loops in .ets files
evidence_refs:
- source_id: arkts-migration-guide
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  source_type: official_error_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: arkts-migration-guide-45
  short_excerpt: '### 不支持`for .. in` **规则：**`arkts-no-for-in` **级别：错误** **错误码：10605080**
    在ArkTS中，对象布局在编译时确定且运行时不可修改，因此不支持使用`for .. in`迭代对象属性。 **TypeScript** ```typescript
    let a: string[] = [''1.0'', ''2.0'', ''3.0'']; for (let i in a) { console.info(a[i]);
    } ``` **ArkTS** ```typescript let a: string[] = [''1.0'', ''2.0'', ''3.0'']; for
    (let i = 0; i < a.length; ++i) { console.info(a[i]); } ```'
  quote_hash: sha256:da110381a3a9d7f0fe7ae5bccba10b834de168130aa02914a32cdd6aa2c14f3b
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-no-for-in-loop

## Failure Class
harmonyos/arkts-syntax

## Symptoms
- ArkTS compiler error: arkts-no-for-in (10605080) — for..in loop over object properties is not supported

## Fingerprints
- arkts-no-for-in
- 10605080
- for .. in
- for..in
- 不支持 for..in

## First Checks
- Check whether the code uses a for..in loop to iterate over object keys
- Check whether the intent is to iterate over properties, array indices, or a Map's keys
- Check whether the object is typed and all its keys are known at compile time

## Do Not Patch Yet
- Do not use Object.keys() as a drop-in replacement without verifying the object type is compatible
- Do not convert for..in to for..of on an untyped array; ensure the array is explicitly typed

## Evidence Needed
- Capture the compiler error showing arkts-no-for-in with error code 10605080
- Identify the object being iterated and the properties accessed inside the loop

## Minimal Fix Scope
- The for..in loop and its body
- The data structure iteration (convert to for..of on Object.keys or array iteration)

## Validation Ladder
- Replace for..in with for..of on typed keys or array iteration and verify no 10605080 error
- Verify the iteration produces identical property access sequence
- Run the build or compile step for the affected module

## Regression Guard
- Add a type-check or lint step that flags for..in loops in .ets files

## Reviewer Notes
