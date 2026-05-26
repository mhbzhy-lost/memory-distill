---
id: arkts-no-types-in-catch
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/arkts-syntax
symptoms:
- 'ArkTS compiler error: arkts-no-types-in-catch (10605079) — type annotation in catch
  clause is not supported'
fingerprints:
- arkts-no-types-in-catch
- '10605079'
- catch type
- catch 语句中标注类型
- 不支持 catch 类型标注
first_checks:
- 'Check whether a catch clause has a type annotation like catch(e: any) or catch(e:
  Error)'
- Check whether the catch block uses e as a typed value without narrowing
- Check whether instanceof or as cast is used to narrow the caught value inside the
  block
do_not:
- Do not annotate the catch parameter with any type; omit the annotation entirely
  in ArkTS
- Do not assume the caught value is Error; always use instanceof Error before accessing
  .message
evidence_needed:
- Capture the compiler error showing arkts-no-types-in-catch with error code 10605079
- Identify the catch parameter and how it is used in the block
minimal_fix_scope:
- The catch clause parameter and its type annotation
- The catch block that needs instanceof narrowing
validation_ladder:
- Remove the type annotation from catch parameter and add instanceof narrowing inside
  the block; verify no 10605079 error
- Verify the error handling still works for all expected Error subtypes
- Run the build or compile step for the affected module
regression_guard:
- Add a type-check step that flags typed catch parameters in .ets files
evidence_refs:
- source_id: arkts-migration-guide
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
  source_type: official_error_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: arkts-migration-guide-44
  short_excerpt: '### 不支持在catch语句标注类型 **规则：**`arkts-no-types-in-catch` **级别：错误** **错误码：10605079**
    TypeScript的catch语句中，只能标注`any`或`unknown`类型。ArkTS不支持这些类型，应省略类型标注。 **TypeScript**
    ```typescript try { // ... } catch (a: unknown) { // 处理异常 } ``` **ArkTS** ```typescript
    try { // ... } catch (a) { // 处理异常 } ```'
  quote_hash: sha256:fb26ae52be8d130f672a3b345d7535bcc8c4f67b0a84950d1355913a7cd2ab7b
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-no-types-in-catch

## Failure Class
harmonyos/arkts-syntax

## Symptoms
- ArkTS compiler error: arkts-no-types-in-catch (10605079) — type annotation in catch clause is not supported

## Fingerprints
- arkts-no-types-in-catch
- 10605079
- catch type
- catch 语句中标注类型
- 不支持 catch 类型标注

## First Checks
- Check whether a catch clause has a type annotation like catch(e: any) or catch(e: Error)
- Check whether the catch block uses e as a typed value without narrowing
- Check whether instanceof or as cast is used to narrow the caught value inside the block

## Do Not Patch Yet
- Do not annotate the catch parameter with any type; omit the annotation entirely in ArkTS
- Do not assume the caught value is Error; always use instanceof Error before accessing .message

## Evidence Needed
- Capture the compiler error showing arkts-no-types-in-catch with error code 10605079
- Identify the catch parameter and how it is used in the block

## Minimal Fix Scope
- The catch clause parameter and its type annotation
- The catch block that needs instanceof narrowing

## Validation Ladder
- Remove the type annotation from catch parameter and add instanceof narrowing inside the block; verify no 10605079 error
- Verify the error handling still works for all expected Error subtypes
- Run the build or compile step for the affected module

## Regression Guard
- Add a type-check step that flags typed catch parameters in .ets files

## Reviewer Notes
