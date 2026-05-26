---
id: swift-sendable-closure-race
kind: debug-recipe
status: accepted
stack:
- swift
- ios
failure_class: swift/concurrency
symptoms:
- 'Swift compiler error: reference to captured var in concurrently-executing code
  violates Sendable'
fingerprints:
- reference to captured var
- concurrently-executing code
- non-Sendable type
- '@Sendable closure'
- data race
first_checks:
- Check whether the closure is annotated with @Sendable or passed to Task { ... }
  or async context
- Check whether a mutable var is captured by the concurrently-executing closure (data
  race risk)
- Check whether the captured type conforms to Sendable
do_not:
- Do not wrap the closure in Task { } without @Sendable; the compiler will still report
  the violation
- Do not use nonisolated(unsafe) to suppress the error without proving thread safety
evidence_needed:
- Capture the compile error identifying the captured var and the @Sendable closure
- Identify the concurrency context (Task, async let, async sequence, actor)
minimal_fix_scope:
- The captured variable and its mutability in the closure site
- The actor isolation or synchronization mechanism around the capture
validation_ladder:
- Convert the mutable var to let or add actor isolation; verify compile succeeds
- Verify no data race at runtime with concurrent access
- Run the concurrency test or TSAN check covering the affected code
regression_guard:
- Add a concurrency test asserting no data race with @Sendable closure captures
evidence_refs:
- source_id: swift-sendable-closure-captures
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-sendable-closure-captures-1
  short_excerpt: Captures in a @Sendable closure (SendableClosureCaptures)
  quote_hash: sha256:53f60e5d6821a3acc388673875f7f7a51f9e1bba9bfef32a2324df44ccd8e289
- source_id: swift-sendable-closure-captures
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-sendable-closure-captures-3
  short_excerpt: '@Sendable closures can be called multiple times concurrently, so
    any captured values must also be safe to access concurrently. To prevent data
    races, the compiler prevents capturing mutable values in a @Sendable closure.'
  quote_hash: sha256:73af2ff69358c0436dfd0d563d583887e882d8ab5cbe8105b71e36be965f3fef
- source_id: swift-sendable-closure-captures
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-sendable-closure-captures-5
  short_excerpt: 'func callConcurrently( _ closure: @escaping @Sendable () -> Void
    ) { ... } func capture() { var result = 0 result += 1 callConcurrently { print(result)
    } }'
  quote_hash: sha256:0c8755ed59dd73daaacb03d838437c04ee8a30488ef0cd7e1fb6437ed91dd92c
- source_id: swift-sendable-closure-captures
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-sendable-closure-captures-6
  short_excerpt: 'The compiler diagnoses the capture of result in a @Sendable closure:'
  quote_hash: sha256:c1c7880ded93194578e24e7a672d07fa07bf055371a0142802aebf783025905a
- source_id: swift-sendable-closure-captures
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-sendable-closure-captures-7
  short_excerpt: '| callConcurrently { | print(result) | `- error: reference to captured
    var ''result'' in concurrently-executing code | } | }'
  quote_hash: sha256:80e0daed339ded6e03e0a4f3fb65b15d5e235f1be828eaeeb3bd024cc2fdd5ad
- source_id: swift-sendable-closure-captures
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-sendable-closure-captures-8
  short_excerpt: 'Because the closure is marked @Sendable , the implementation of
    callConcurrently can call closure multiple times concurrently. For example, multiple
    child tasks within a task group can call closure concurrently:'
  quote_hash: sha256:70103be57d3a7a5e90dbe27a23eaf04c034d66ba397b6b87b36eacf201e727be
- source_id: swift-sendable-closure-captures
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-sendable-closure-captures-9
  short_excerpt: 'func callConcurrently( _ closure: @escaping @Sendable () -> Void
    ) { Task { await withDiscardingTaskGroup { group in for _ in 0..<10 { group.addTask
    { closure() } } } } }'
  quote_hash: sha256:4fb4c37ef12c8b1934e6d081e15d0f572eb61c4a278c8578ab7178495b2ed538
- source_id: swift-sendable-closure-captures
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-sendable-closure-captures-14
  short_excerpt: 'The compiler diagnoses the capture of model in a @Sendable closure:'
  quote_hash: sha256:faf9366486457e3d9b6c00aa94c9ffa571f9d4352b0e2404a29f354f59459b07
- source_id: swift-sendable-closure-captures
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/sendable-closure-captures.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-sendable-closure-captures-15
  short_excerpt: '| func capture(model: MyModel) async { | callConcurrently { | model.log()
    | `- error: capture of ''model'' with non-Sendable type ''MyModel'' in a ''@Sendable''
    closure | } | }'
  quote_hash: sha256:76684df00d5a50d8206d7727d348d87804ac88f4c7f4cc2878b69f8f0b78c63f
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# swift-sendable-closure-race

## Failure Class
swift/concurrency

## Symptoms
- Swift compiler error: reference to captured var in concurrently-executing code violates Sendable

## Fingerprints
- reference to captured var
- concurrently-executing code
- non-Sendable type
- @Sendable closure
- data race

## First Checks
- Check whether the closure is annotated with @Sendable or passed to Task { ... } or async context
- Check whether a mutable var is captured by the concurrently-executing closure (data race risk)
- Check whether the captured type conforms to Sendable

## Do Not Patch Yet
- Do not wrap the closure in Task { } without @Sendable; the compiler will still report the violation
- Do not use nonisolated(unsafe) to suppress the error without proving thread safety

## Evidence Needed
- Capture the compile error identifying the captured var and the @Sendable closure
- Identify the concurrency context (Task, async let, async sequence, actor)

## Minimal Fix Scope
- The captured variable and its mutability in the closure site
- The actor isolation or synchronization mechanism around the capture

## Validation Ladder
- Convert the mutable var to let or add actor isolation; verify compile succeeds
- Verify no data race at runtime with concurrent access
- Run the concurrency test or TSAN check covering the affected code

## Regression Guard
- Add a concurrency test asserting no data race with @Sendable closure captures

## Reviewer Notes
