---
id: arkts-no-untyped-obj-literals
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/arkts-syntax
symptoms:
- 'ArkTS compiler error: arkts-no-untyped-obj-literals (10605038) — object literals
  require explicit type annotation'
fingerprints:
- arkts-no-untyped-obj-literals
- '10605038'
- object literal type
- 需要显式标注对象字面量的类型
- 编译时错误
first_checks:
- Check whether an object literal is assigned to a variable without a type annotation
- Check whether an object literal is passed as a function argument without an explicit
  type interface
- Check whether the context type (variable annotation or parameter type) is sufficient
  to infer the literal type
do_not:
- Do not rely solely on contextual inference; add explicit type annotation when the
  context is ambiguous
- Do not convert object literals to class instances without checking whether an interface
  or class is more appropriate
evidence_needed:
- Capture the compiler error showing arkts-no-untyped-obj-literals with error code
  10605038
- Identify the variable or parameter expecting the object literal
minimal_fix_scope:
- The object literal expression and its surrounding type context
- The interface or class definition used to annotate the literal type
validation_ladder:
- Add explicit type annotation to the object literal and verify no 10605038 error
- Verify the type annotation covers all fields in the object literal
- Run the build or compile step for the affected module
regression_guard:
- Add a type-check step that verifies all object literals have explicit or inferrable
  types
evidence_refs:
- source_id: arkts-migration-guide
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  source_type: official_error_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: arkts-migration-guide-27
  short_excerpt: '### 需要显式标注对象字面量的类型 **规则：**`arkts-no-untyped-obj-literals` **级别：错误**
    **错误码：10605038** 在 ArkTS 中，需要显式标注对象字面量的类型，否则将导致编译时错误。在某些场景下，编译器可以根据上下文推断出字面量的类型。
    在以下上下文中不支持使用字面量初始化类和接口： * 初始化具有`any`、`Object`或`object`类型的任何对象 * 初始化带有方法的类或接口 *
    初始化包含自定义含参数的构造函数的类 * 初始化带`readonly`字段的类 **例子1** **TypeScript** ```typescript let
    o1 = {n: 42, s: ''foo''}; let o2: Object = {n: 42, s: ''foo''}; let o3: object
    = {n: 42, s: ''foo''}; let oo: Object[] = [{n: 1, s: ''1''}, {n: 2, s: ''2''}];
    ``` **ArkTS** ```typescript class C1 { n: number = 0 s: string = '''' } let o1:
    C1 = {n: 42, s: ''foo''}; let o2: C1 = {n: 42, s: ''foo''}; let o3: '
  quote_hash: sha256:fc929e97da99af1f1e6e72f09b1a278a33bc51ee6f88f31c88b490369133c997
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-no-untyped-obj-literals

## Failure Class
harmonyos/arkts-syntax

## Symptoms
- ArkTS compiler error: arkts-no-untyped-obj-literals (10605038) — object literals require explicit type annotation

## Fingerprints
- arkts-no-untyped-obj-literals
- 10605038
- object literal type
- 需要显式标注对象字面量的类型
- 编译时错误

## First Checks
- Check whether an object literal is assigned to a variable without a type annotation
- Check whether an object literal is passed as a function argument without an explicit type interface
- Check whether the context type (variable annotation or parameter type) is sufficient to infer the literal type

## Do Not Patch Yet
- Do not rely solely on contextual inference; add explicit type annotation when the context is ambiguous
- Do not convert object literals to class instances without checking whether an interface or class is more appropriate

## Evidence Needed
- Capture the compiler error showing arkts-no-untyped-obj-literals with error code 10605038
- Identify the variable or parameter expecting the object literal

## Minimal Fix Scope
- The object literal expression and its surrounding type context
- The interface or class definition used to annotate the literal type

## Validation Ladder
- Add explicit type annotation to the object literal and verify no 10605038 error
- Verify the type annotation covers all fields in the object literal
- Run the build or compile step for the affected module

## Regression Guard
- Add a type-check step that verifies all object literals have explicit or inferrable types

## Reviewer Notes
