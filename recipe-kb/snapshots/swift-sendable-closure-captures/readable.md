- [swift-sendable-closure-captures-1] Captures in a @Sendable closure (SendableClosureCaptures)

- [swift-sendable-closure-captures-2] Overview

- [swift-sendable-closure-captures-3] @Sendable closures can be called multiple times concurrently, so any captured values must also be safe to access concurrently. To prevent data races, the compiler prevents capturing mutable values in a @Sendable closure.

- [swift-sendable-closure-captures-4] For example:

- [swift-sendable-closure-captures-5] func callConcurrently( _ closure: @escaping @Sendable () -> Void ) { ... } func capture() { var result = 0 result += 1 callConcurrently { print(result) } }

- [swift-sendable-closure-captures-6] The compiler diagnoses the capture of result in a @Sendable closure:

- [swift-sendable-closure-captures-7] | callConcurrently { | print(result) | `- error: reference to captured var 'result' in concurrently-executing code | } | }

- [swift-sendable-closure-captures-8] Because the closure is marked @Sendable , the implementation of callConcurrently can call closure multiple times concurrently. For example, multiple child tasks within a task group can call closure concurrently:

- [swift-sendable-closure-captures-9] func callConcurrently( _ closure: @escaping @Sendable () -> Void ) { Task { await withDiscardingTaskGroup { group in for _ in 0..<10 { group.addTask { closure() } } } } }

- [swift-sendable-closure-captures-10] If the type of the capture is Sendable and the closure only needs the value of the variable at the point of capture, resolve the error by explicitly capturing the variable by value in the closure's capture list:

- [swift-sendable-closure-captures-11] func capture() { var result = 0 result += 1 callConcurrently { [result] in print(result) } }

- [swift-sendable-closure-captures-12] This strategy does not apply to captures with non- Sendable type. Consider the following example:

- [swift-sendable-closure-captures-13] class MyModel { func log() { ... } } func capture(model: MyModel) async { callConcurrently { model.log() } }

- [swift-sendable-closure-captures-14] The compiler diagnoses the capture of model in a @Sendable closure:

- [swift-sendable-closure-captures-15] | func capture(model: MyModel) async { | callConcurrently { | model.log() | `- error: capture of 'model' with non-Sendable type 'MyModel' in a '@Sendable' closure | } | }

- [swift-sendable-closure-captures-16] If a type with mutable state can be referenced concurrently, but all access to mutable state happens on the main actor, isolate the type to the main actor and mark the methods that don't access mutable state as nonisolated :

- [swift-sendable-closure-captures-17] @MainActor class MyModel { nonisolated func log() { ... } } func capture(model: MyModel) async { callConcurrently { model.log() } }

- [swift-sendable-closure-captures-18] The compiler will guarantee that the implementation of log does not access any main actor state.

- [swift-sendable-closure-captures-19] If you manually ensure data-race safety, such as by using an external synchronization mechanism, you can use nonisolated(unsafe) to opt out of concurrency checking:

- [swift-sendable-closure-captures-20] class MyModel { func log() { ... } } func capture(model: MyModel) async { nonisolated(unsafe) let model = model callConcurrently { model.log() } }
