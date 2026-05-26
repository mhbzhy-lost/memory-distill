- [swift-existential-any-diagnostic-1] Existential any (ExistentialAny)

- [swift-existential-any-diagnostic-2] any existential type syntax.

- [swift-existential-any-diagnostic-3] Overview

- [swift-existential-any-diagnostic-4] any was introduced in Swift 5.6 to explicitly mark "existential types", i.e., abstract boxed types that conform to a set of constraints. For source compatibility, these are not diagnosed by default except for existential types constrained to protocols with Self or associated type requirements (as this was introduced in the same version):

- [swift-existential-any-diagnostic-5] protocol Foo { associatedtype Bar func foo(_: Bar) } protocol Baz {} func pass(foo: Foo) {} // `any Foo` is required instead of `Foo` func pass(baz: Baz) {} // no warning or error by default for source compatibility

- [swift-existential-any-diagnostic-6] When enabled via -enable-upcoming-feature ExistentialAny , the upcoming language feature ExistentialAny will diagnose all existential types without any :

- [swift-existential-any-diagnostic-7] func pass(baz: Baz) {} // `any Baz` required instead of `Baz`

- [swift-existential-any-diagnostic-8] This will become the default in a future language mode.

- [swift-existential-any-diagnostic-9] Migration

- [swift-existential-any-diagnostic-10] -enable-upcoming-feature ExistentialAny:migrate

- [swift-existential-any-diagnostic-11] Enabling migration for ExistentialAny adds fix-its that prepend all existential types with any as required. No attempt is made to convert to generic ( some ) types.

- [swift-existential-any-diagnostic-12] See Also

- [swift-existential-any-diagnostic-13] SE-0335: Introduce existential any

- [swift-existential-any-diagnostic-14] any
