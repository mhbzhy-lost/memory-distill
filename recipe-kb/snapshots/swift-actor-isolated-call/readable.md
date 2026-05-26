- [swift-actor-isolated-call-1] Calling an actor-isolated method from a synchronous nonisolated context (ActorIsolatedCall)

- [swift-actor-isolated-call-2] Overview

- [swift-actor-isolated-call-3] Accessing actor-isolated state from outside the actor can cause data races in your program. Resolve this error by calling actor-isolated functions on the actor.

- [swift-actor-isolated-call-4] Calls to actor-isolated methods from outside the actor must be done asynchronously. Otherwise, access to actor state can happen concurrently and lead to data races. These rules also apply to global actors like the main actor.

- [swift-actor-isolated-call-5] For example:

- [swift-actor-isolated-call-6] @MainActor class MyModel { func update() { ... } } func runUpdate(model: MyModel) { model.update() }

- [swift-actor-isolated-call-7] Building the above code produces an error about calling a main actor isolated method from outside the actor:

- [swift-actor-isolated-call-8] | func runUpdate(model: MyModel) { | model.update() | `- error: call to main actor-isolated instance method 'update()' in a synchronous nonisolated context | }

- [swift-actor-isolated-call-9] The runUpdate function doesn't specify any actor isolation, so it is nonisolated by default. nonisolated methods can be called from any concurrency domain. To prevent data races, nonisolated methods cannot access actor isolated state in their implementation. If runUpdate is called from off the main actor, calling model.update() could mutate main actor state at the same time as another task running on the main actor.

- [swift-actor-isolated-call-10] To resolve the error, runUpdate has to make sure the call to model.update() is on the main actor. One way to do that is to add main actor isolation to the runUpdate function:

- [swift-actor-isolated-call-11] @MainActor func runUpdate(model: MyModel) { model.update() }

- [swift-actor-isolated-call-12] Alternatively, if the runUpdate function is meant to be called from arbitrary concurrent contexts, create a task isolated to the main actor to call model.update() :

- [swift-actor-isolated-call-13] func runUpdate(model: MyModel) { Task { @MainActor in model.update() } }
