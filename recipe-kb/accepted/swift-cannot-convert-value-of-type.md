---
id: swift-cannot-convert-value-of-type
kind: debug-recipe
status: accepted
stack:
- swift
- ios
failure_class: swift/type-checking
symptoms:
- Swift compiler reports Cannot convert value of type X to expected type Y with unclear
  fix-it suggestion
fingerprints:
- Cannot convert value of type
- binary operator cannot be applied
- missing argument label
- type has no member
- cannot force unwrap
first_checks:
- Check whether the mismatch is due to optional vs non-optional type (Int? vs Int)
- Check whether the mismatch is due to protocol conformance missing (concrete type
  vs protocol existential)
- Check whether force unwrap (!) is applied to a value that is not optional
do_not:
- Do not add as! force cast without understanding why the types do not match
- Do not suppress the diagnostic with @_silgen_name or @objc without fixing the underlying
  type mismatch
evidence_needed:
- Capture the full compile error with the expected and actual types
- Identify the expression or argument site where the type mismatch occurs
minimal_fix_scope:
- The expression or call site producing the type mismatch
- The variable or parameter type annotation that constrains the expression
validation_ladder:
- Fix the type annotation, unwrap, or convert explicitly; verify compile succeeds
- Verify runtime behavior matches the corrected type
- Run the unit test covering the affected expression
regression_guard:
- Add a compile-time test asserting the corrected type at the expression boundary
evidence_refs:
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-108
  short_excerpt: 'While solving this constraint system, the type checker will again
    record a failure for the missing & on the first argument to foo . Additionally,
    it will record a failure for the missing argument label bar . Once both failures
    have been recorded, the remainder of the constraint system is solved. The type
    checker then produces errors (with Fix-Its) for the two problems that need to
    be addressed to fix this code:'
  quote_hash: sha256:ec23b9cc9f9f6aa345624886693e65d0e17129d8debfe230cc34910549712c6f
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-109
  short_excerpt: 'error: passing value of type ''Int'' to an inout parameter requires
    explicit ''&'' foo(x) ^ & error: missing argument label ''bar:'' in call foo(x,
    "bar") ^ bar:'
  quote_hash: sha256:c3081da8c4907c1ca9bbe08c8d9bb81f2dab0c50aef06ee662a36813384a08af
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-118
  short_excerpt: 'error: missing argument label ''answer:'' in call let _: [String]
    = [42].map { foo($0) } ^ answer:'
  quote_hash: sha256:93f70cee1e748177a810bed7e83903ea851546708db27d18005cb2fd619d0ce2
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-122
  short_excerpt: 'error: cannot convert value of type ''UInt'' to expected argument
    type ''Int'' _ = x.filter { ($0 + y) > 42 } ^ Int( )'
  quote_hash: sha256:0b3b5c31f5f93c035db0bd566d4b74f19026ccf895aed499322db57249d6d6a6
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-124
  short_excerpt: 'error: cannot force unwrap value of non-optional type ''Int'' _
    = S<Int>([i!]) ~^'
  quote_hash: sha256:bf1f8a4557314188df23b9b560e37eaecd881c00cd1efab40e9344770796dec5
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-128
  short_excerpt: 'error: type ''A'' has no member ''foo'' _ = S(B(), .foo(), A())
    ~^~~~~'
  quote_hash: sha256:f5137a0a25e9793a5da69525d92b966043091f71858c9087d23df794e79bce04
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-139
  short_excerpt: 'error: Cannot convert value of type ''(Double) -> RotatedShape<Circle>''
    to expected argument type ''() -> _'''
  quote_hash: sha256:47f2add9dfc59994272f4870d0908fde81357fff5dea6874e25dd5db42a1e505
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-140
  short_excerpt: 'error: cannot convert value of type ''Int'' to expected argument
    type ''Double'' Circle().rotation(.degrees($0)) ^ Double( )'
  quote_hash: sha256:17f8596bb92f8b1f3c4360b1f42018bb77ef8452ae14a7d978a8d698e0b95e93
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-145
  short_excerpt: 'error: type ''Color?'' has no member ''systemRed'' .foregroundColor(.systemRed)
    ~^~~~~~~~~'
  quote_hash: sha256:6ee1f7a21ee9650f6061095e72489c279db315b190173916ced9fd4e6d90fbc4
- source_id: swift-new-diagnostic-arch
  url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  final_url: https://www.swift.org/blog/new-diagnostic-arch-overview/
  source_type: official_blog_post
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-new-diagnostic-arch-146
  short_excerpt: Missing arguments
  quote_hash: sha256:91947157a3404cfa5a734aa5e21b4a73cc1b9156567198d78793b1bfab525e09
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# swift-cannot-convert-value-of-type

## Failure Class
swift/type-checking

## Symptoms
- Swift compiler reports Cannot convert value of type X to expected type Y with unclear fix-it suggestion

## Fingerprints
- Cannot convert value of type
- binary operator cannot be applied
- missing argument label
- type has no member
- cannot force unwrap

## First Checks
- Check whether the mismatch is due to optional vs non-optional type (Int? vs Int)
- Check whether the mismatch is due to protocol conformance missing (concrete type vs protocol existential)
- Check whether force unwrap (!) is applied to a value that is not optional

## Do Not Patch Yet
- Do not add as! force cast without understanding why the types do not match
- Do not suppress the diagnostic with @_silgen_name or @objc without fixing the underlying type mismatch

## Evidence Needed
- Capture the full compile error with the expected and actual types
- Identify the expression or argument site where the type mismatch occurs

## Minimal Fix Scope
- The expression or call site producing the type mismatch
- The variable or parameter type annotation that constrains the expression

## Validation Ladder
- Fix the type annotation, unwrap, or convert explicitly; verify compile succeeds
- Verify runtime behavior matches the corrected type
- Run the unit test covering the affected expression

## Regression Guard
- Add a compile-time test asserting the corrected type at the expression boundary

## Reviewer Notes
