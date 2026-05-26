---
id: swift-actor-isolation-violation
kind: debug-recipe
status: accepted
stack:
- swift
- ios
failure_class: swift/concurrency
symptoms:
- 'Swift compiler error: actor-isolated property or method cannot be accessed from
  a non-isolated or different isolation context'
fingerprints:
- actor-isolated
- non-isolated context
- MainActor-isolated
- actor isolation violation
- cannot be referenced from
first_checks:
- Check whether the access is from a nonisolated function or a different actor
- Check whether the accessed member is marked @MainActor or belongs to an actor struct/class
- Check whether await is used at the call site to cross the isolation boundary
do_not:
- Do not mark the member nonisolated unless it truly requires no synchronization
- Do not bypass actor isolation by calling through global functions without proving
  thread safety
evidence_needed:
- Capture the compile error naming the actor-isolated member and the accessing context
- Identify the isolation domains of both the caller and the accessed member
minimal_fix_scope:
- The cross-isolation access site needing await
- The isolation annotation of the affected member or the calling context
validation_ladder:
- Add await at the call site or mark the caller with the matching actor; verify compile
  succeeds
- Verify the actor's invariants are preserved at runtime
- Run the concurrency test covering the cross-actor access
regression_guard:
- Add a compile-time test asserting the access requires await across isolation domains
evidence_refs:
- source_id: swift-actor-isolated-call
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-actor-isolated-call-1
  short_excerpt: Calling an actor-isolated method from a synchronous nonisolated context
    (ActorIsolatedCall)
  quote_hash: sha256:cf009e159a2520633c28683b1d16e3d4574c0282a5efe875e20a9ca22233c54d
- source_id: swift-actor-isolated-call
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-actor-isolated-call-3
  short_excerpt: Accessing actor-isolated state from outside the actor can cause data
    races in your program. Resolve this error by calling actor-isolated functions
    on the actor.
  quote_hash: sha256:02901b15e6a540695ab4fde9af73ae00dd1ce04f1708494699294915310a5298
- source_id: swift-actor-isolated-call
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-actor-isolated-call-4
  short_excerpt: Calls to actor-isolated methods from outside the actor must be done
    asynchronously. Otherwise, access to actor state can happen concurrently and lead
    to data races. These rules also apply to global actors like the main actor.
  quote_hash: sha256:3bbb411452c9a4341a9481f10b35f293dc1d7830b549884cf3e4e4f9305b61f0
- source_id: swift-actor-isolated-call
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-actor-isolated-call-6
  short_excerpt: '@MainActor class MyModel { func update() { ... } } func runUpdate(model:
    MyModel) { model.update() }'
  quote_hash: sha256:ab30ebd260531613a3e34d4727c1f388dd159a25fcc98d2e58a3880e99d5c895
- source_id: swift-actor-isolated-call
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-actor-isolated-call-8
  short_excerpt: '| func runUpdate(model: MyModel) { | model.update() | `- error:
    call to main actor-isolated instance method ''update()'' in a synchronous nonisolated
    context | }'
  quote_hash: sha256:952c4d95b023527e6c31a507b86718c86da42c5cf376d4a46927914eb9f8a357
- source_id: swift-actor-isolated-call
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-actor-isolated-call-9
  short_excerpt: The runUpdate function doesn't specify any actor isolation, so it
    is nonisolated by default. nonisolated methods can be called from any concurrency
    domain. To prevent data races, nonisolated methods cannot access actor isolated
    state in their implementation. If runUpdate is called from off the main actor,
    calling model.update() could mutate main actor state at the same time as another
    task running on the main actor.
  quote_hash: sha256:2109a01f60a32121d676d203a741f0813c13befc88999283da1ce8b0c4bcb169
- source_id: swift-actor-isolated-call
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-actor-isolated-call-10
  short_excerpt: 'To resolve the error, runUpdate has to make sure the call to model.update()
    is on the main actor. One way to do that is to add main actor isolation to the
    runUpdate function:'
  quote_hash: sha256:344a498da857d23d7c4d9c6b5619ec12853d5e4e79eae2093bdf2ac90a7934fc
- source_id: swift-actor-isolated-call
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-actor-isolated-call-11
  short_excerpt: '@MainActor func runUpdate(model: MyModel) { model.update() }'
  quote_hash: sha256:bed27ec9ece0fea08e5380c78b42825418777116942fdbd7564b9644928f1aeb
- source_id: swift-actor-isolated-call
  url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/userdocs/diagnostics/actor-isolated-call.md
  source_type: compiler_diagnostic
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-actor-isolated-call-13
  short_excerpt: 'func runUpdate(model: MyModel) { Task { @MainActor in model.update()
    } }'
  quote_hash: sha256:76c6baa897246abb6f2487096dae8555f8dec2148ded27eebc863daa9bd03c88
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# swift-actor-isolation-violation

## Failure Class
swift/concurrency

## Symptoms
- Swift compiler error: actor-isolated property or method cannot be accessed from a non-isolated or different isolation context

## Fingerprints
- actor-isolated
- non-isolated context
- MainActor-isolated
- actor isolation violation
- cannot be referenced from

## First Checks
- Check whether the access is from a nonisolated function or a different actor
- Check whether the accessed member is marked @MainActor or belongs to an actor struct/class
- Check whether await is used at the call site to cross the isolation boundary

## Do Not Patch Yet
- Do not mark the member nonisolated unless it truly requires no synchronization
- Do not bypass actor isolation by calling through global functions without proving thread safety

## Evidence Needed
- Capture the compile error naming the actor-isolated member and the accessing context
- Identify the isolation domains of both the caller and the accessed member

## Minimal Fix Scope
- The cross-isolation access site needing await
- The isolation annotation of the affected member or the calling context

## Validation Ladder
- Add await at the call site or mark the caller with the matching actor; verify compile succeeds
- Verify the actor's invariants are preserved at runtime
- Run the concurrency test covering the cross-actor access

## Regression Guard
- Add a compile-time test asserting the access requires await across isolation domains

## Reviewer Notes
