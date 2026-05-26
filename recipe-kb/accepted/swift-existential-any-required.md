---
id: swift-existential-any-required
kind: debug-recipe
status: accepted
stack:
- swift
- ios
failure_class: swift/type-system
symptoms:
- 'Swift 5.6+ compiler error: protocol used as a type requires any keyword before
  the protocol name'
fingerprints:
- any
- existential type
- protocol used as a type
- ExistentialAny
- protocol as type
first_checks:
- 'Check whether a protocol name is used directly as a type (e.g. let x: MyProtocol)
  without any prefix'
- Check whether the code targets Swift 5.6+ with ExistentialAny upcoming feature enabled
- 'Check whether a generic constraint uses protocol as type instead of where T: MyProtocol'
do_not:
- Do not replace protocol existential with a struct wrapper without understanding
  the performance implications (existential boxes)
- 'Do not add any to generic type parameters; use <T: MyProtocol> constraint syntax
  instead'
evidence_needed:
- Capture the compile error showing the protocol name used as a type
- Identify whether the type site is a variable declaration, parameter type, or return
  type
minimal_fix_scope:
- The protocol type annotation site needing any prefix
- Any generic constraint that uses the protocol as a type constraint
validation_ladder:
- Add any keyword before the protocol name and verify compile succeeds
- Verify runtime behavior is unchanged
- Run the module test covering the affected type signature
regression_guard:
- Add a compile-time test that verifies no bare protocol-as-type usage remains
evidence_refs:
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-1
  short_excerpt: Existential any (ExistentialAny)
  quote_hash: sha256:abf9cd90f1ac3f92faaccdbd1381b32dea72cbc5baf06a771381fe647bdb1d71
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-2
  short_excerpt: any existential type syntax.
  quote_hash: sha256:cfce41ee4a59b00d77f64ad5913fbda4ba0103712df071f1b8557e458fac715e
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-4
  short_excerpt: 'any was introduced in Swift 5.6 to explicitly mark "existential
    types", i.e., abstract boxed types that conform to a set of constraints. For source
    compatibility, these are not diagnosed by default except for existential types
    constrained to protocols with Self or associated type requirements (as this was
    introduced in the same version):'
  quote_hash: sha256:641436936d492bcc742968710b32610f5d64a045d3a1b62a50e23f766672c5d1
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-5
  short_excerpt: 'protocol Foo { associatedtype Bar func foo(_: Bar) } protocol Baz
    {} func pass(foo: Foo) {} // `any Foo` is required instead of `Foo` func pass(baz:
    Baz) {} // no warning or error by default for source compatibility'
  quote_hash: sha256:089463925bf25745dd79d2bd3aa9bfed6674b57f65969eff981e3f86af20179b
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-6
  short_excerpt: 'When enabled via -enable-upcoming-feature ExistentialAny , the upcoming
    language feature ExistentialAny will diagnose all existential types without any
    :'
  quote_hash: sha256:e9cd45b8860dd19dfd401f606459aec3029b9e5e67c071edb0083981fdb9a665
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-7
  short_excerpt: 'func pass(baz: Baz) {} // `any Baz` required instead of `Baz`'
  quote_hash: sha256:26eb1c48752e5b315bbc33cf7045bfd2b574f1c19b3f4272ca5b49994fad513b
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-10
  short_excerpt: -enable-upcoming-feature ExistentialAny:migrate
  quote_hash: sha256:9ef1bef5d01d25c6b9b281402f44f2dd797ad7e0e3ee0bb1acafc68643f1f8dc
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-11
  short_excerpt: Enabling migration for ExistentialAny adds fix-its that prepend all
    existential types with any as required. No attempt is made to convert to generic
    ( some ) types.
  quote_hash: sha256:7094cb200b9c675fe6cd058602940a4f1f3bc929082dfbc8149e645a4f2abe6c
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-13
  short_excerpt: 'SE-0335: Introduce existential any'
  quote_hash: sha256:ed05f50a6881d7771ef0d797c27aea25196def15d7a8523c38ee9e88952fd623
- source_id: swift-existential-any-diagnostic
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/existential-any.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-existential-any-diagnostic-14
  short_excerpt: any
  quote_hash: sha256:d6a7cd2a7371b1a15d543196979ff74fdb027023ebf187d5d329be11055c77fd
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# swift-existential-any-required

## Failure Class
swift/type-system

## Symptoms
- Swift 5.6+ compiler error: protocol used as a type requires any keyword before the protocol name

## Fingerprints
- any
- existential type
- protocol used as a type
- ExistentialAny
- protocol as type

## First Checks
- Check whether a protocol name is used directly as a type (e.g. let x: MyProtocol) without any prefix
- Check whether the code targets Swift 5.6+ with ExistentialAny upcoming feature enabled
- Check whether a generic constraint uses protocol as type instead of where T: MyProtocol

## Do Not Patch Yet
- Do not replace protocol existential with a struct wrapper without understanding the performance implications (existential boxes)
- Do not add any to generic type parameters; use <T: MyProtocol> constraint syntax instead

## Evidence Needed
- Capture the compile error showing the protocol name used as a type
- Identify whether the type site is a variable declaration, parameter type, or return type

## Minimal Fix Scope
- The protocol type annotation site needing any prefix
- Any generic constraint that uses the protocol as a type constraint

## Validation Ladder
- Add any keyword before the protocol name and verify compile succeeds
- Verify runtime behavior is unchanged
- Run the module test covering the affected type signature

## Regression Guard
- Add a compile-time test that verifies no bare protocol-as-type usage remains

## Reviewer Notes
