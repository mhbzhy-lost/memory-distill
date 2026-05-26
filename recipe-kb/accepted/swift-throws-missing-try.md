---
id: swift-throws-missing-try
kind: debug-recipe
status: accepted
stack:
- swift
- ios
failure_class: swift/error-handling
symptoms:
- Calling a throwing function without try keyword or outside do-catch block produces
  compile error
fingerprints:
- Call can throw
- try keyword required
- function can throw
- non-throwing context
- throws keyword
first_checks:
- Check whether the calling function is marked throws
- Check whether the call site wraps the throwing call in do { try ... } catch { ...
  }
- Check whether try? or try! is used where the error cannot be ignored
do_not:
- Do not use try! in production code unless the function's contract guarantees success
- Do not catch all errors broadly; match specific error types to avoid masking unrelated
  failures
evidence_needed:
- Capture the compile error message identifying the throwing function call site
- Identify whether the enclosing function is marked throws to propagate errors
minimal_fix_scope:
- The throwing function call site
- The enclosing do-catch block or the calling function's throws declaration
validation_ladder:
- Add try keyword and appropriate error handling; verify compile succeeds
- Test the code path with both success and failure inputs
- Run the unit test covering the throwing function boundary
regression_guard:
- Add a test that exercises both the throwing and success paths of the function call
evidence_refs:
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-30
  short_excerpt: 'A function can be declared to throw by writing throws on the function
    declaration or type:'
  quote_hash: sha256:2f1ffd73088ae4ad9dec484ed01dbf66e05c0f9e3617d51042cd3aaba68520ab
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-31
  short_excerpt: func foo() -> Int { // This function is not permitted to throw. func
    bar() throws -> Int { // This function is permitted to throw.
  quote_hash: sha256:49d7b2e4dcfdf350d3a410c55549f585b5d53cdc88b7e504537ade0e177f01fd
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-32
  short_excerpt: 'throws is written before the arrow to give a sensible and consistent
    grammar for function types and implicit () result types, e.g.:'
  quote_hash: sha256:9ab054efdee5fdd5ab01c1ed54116ac251d534c3393dc26a8fc6b69c08fdf48f
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-33
  short_excerpt: 'func baz() throws { // Takes a ''callback'' function that can throw.
    // ''fred'' itself can also throw. func fred(_ callback: (UInt8) throws -> ())
    throws { // These are distinct types. let a : () -> () -> () let b : () throws
    -> () -> () let c : () -> () throws -> () let d : () throws -> () throws -> ()'
  quote_hash: sha256:88935632a753ef92421a5caf4d62b9689ec73e0fc99d977cd9491c4bfb74bf54
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-34
  short_excerpt: 'For curried functions, throws only applies to the innermost function.
    This function has type (Int) -> (Int) throws -> Int :'
  quote_hash: sha256:37f10232dc3416afa8202be6bec9d142e7478c0ed6449fac61ffd5b501622e87
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-35
  short_excerpt: 'func jerry(_ i: Int)(j: Int) throws -> Int {'
  quote_hash: sha256:3aab9a928cdccd322bf488017d04fbe1ef0a42bfdcb5b0bdaeb1c4e91e2d0ebe
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-36
  short_excerpt: 'throws is tracked as part of the type system: a function value must
    also declare whether it can throw. Functions that cannot throw are a subtype of
    functions that can, so you can use a function that can''t throw anywhere you could
    use a function that can:'
  quote_hash: sha256:f1d76d451b2363f576ca4189015eab02a11508c94c1192338ab406b7e43e15c7
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-37
  short_excerpt: 'func rachel() -> Int { return 12 } func donna(_ generator: () throws
    -> Int) -> Int { ... } donna(rachel)'
  quote_hash: sha256:03078c43b4b5bb0fe64eb307a1236d2708ae5b4ef2fccf6f721bc9b1910f0098
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-41
  short_excerpt: func foo() { func foo() throws {
  quote_hash: sha256:aa46025152857c3027c373ae5a1ac709a08a65698ec00373d9794f96c995959f
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-43
  short_excerpt: 'It is valuable to be able to overload higher-order functions based
    on whether an argument function throws, so this is allowed:'
  quote_hash: sha256:a6463fb2451e91c0c2d31163be36f53cf6ad0ec534271fe7367d4575722654b4
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-44
  short_excerpt: 'func foo(_ callback: () throws -> Bool) { func foo(_ callback: ()
    -> Bool) {'
  quote_hash: sha256:e883c085095ec806b4e5e0600827f213dfc18461b45255fb3bebb7ef8254c2b2
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-45
  short_excerpt: rethrows
  quote_hash: sha256:ed4566cbf15bfe1d8ae65e30701e21d69ebd4db46eb5775841700ea51cd42470
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-46
  short_excerpt: 'Functions which take a throwing function argument (including as
    an autoclosure) can be marked as rethrows :'
  quote_hash: sha256:199e7c30d30d6b2a6f9d9f7484532588e2058c34155f881b3ef90cab1aec9587
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-47
  short_excerpt: 'extension Array { func map<U>(_ fn: ElementType throws -> U) rethrows
    -> [U] }'
  quote_hash: sha256:a25435c07f44041023023333447d668b8f55433500ac5553e65e86e53fa521a8
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-48
  short_excerpt: It is an error if a function declared rethrows does not include a
    throwing function in at least one of its parameter clauses.
  quote_hash: sha256:2ff2b67b32bfb6c2189b0e5559dd3dfc68cce74b4fbba7298bdc0659c0b7fdc5
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-49
  short_excerpt: rethrows is identical to throws , except that the function promises
    to only throw if one of its argument functions throws.
  quote_hash: sha256:ddfb6a707f3ded38454306bbff5a14becb9a691a72983758a92be71b35a74b61
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-53
  short_excerpt: 'it is implemented within f (i.e. it is either f or a function or
    closure defined therein) and it does not throw except by either: calling a function
    that is rethrowing-only for f or calling a function that is rethrows , passing
    only functions that are rethrowing-only for f .'
  quote_hash: sha256:642b8b7f02bb415895d67b9a255666500cd504ba9e3932cd8aa50957952c8cd4
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-55
  short_excerpt: calling a function that is rethrows , passing only functions that
    are rethrowing-only for f .
  quote_hash: sha256:6914f371d370b3fa96d5aa81c7b07799efe2d5b1927ee854932a5150b1bacd44
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-56
  short_excerpt: It is an error if a rethrows function is not rethrowing-only for
    itself.
  quote_hash: sha256:e7d8bba106801eb93c0a4e65f7bf89c56e5588093559bcb27f110dd5c9901532
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-57
  short_excerpt: 'A rethrows function is considered to be a throwing function. However,
    a direct call to a rethrows function is considered to not throw if it is fully
    applied and none of the function arguments can throw. For example:'
  quote_hash: sha256:a837ec9a2c0fdc310435192f4faad5f747795927726c13ad813632df376139f6
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-59
  short_excerpt: For now, rethrows is a property of declared functions, not of function
    values. Binding a variable (even a constant) to a function loses the information
    that the function was rethrows , and calls to it will use the normal rules, meaning
    that they will be considered to throw regardless of whether a non-throwing function
    is passed.
  quote_hash: sha256:2b5b5633d7ae69356ada017aa0d74b5725737e40992d18ca223a099b186dfa11
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-60
  short_excerpt: For the purposes of override and conformance checking, rethrows lies
    between throws and non- throws . That is, an ordinary throwing method cannot override
    a rethrows method, which cannot override a non-throwing method; but an ordinary
    throwing method can be overridden by a rethrows method, which can be overridden
    by a non-throwing method. Equivalent rules apply for protocol conformance.
  quote_hash: sha256:3748fd8ae0017052f8ca1dde1e89f1c7f2102efd0049a16642b5247dce9b91d3
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-64
  short_excerpt: As mentioned above, attempting to throw an error out of a function
    not marked throws is a static compiler error.
  quote_hash: sha256:76511b4d5cd78b5665942d49ae61547e92927cc33a55b4b154d0431094ad2be8
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-67
  short_excerpt: 'The try keyword is used for other purposes which it seems to fit
    far better (see below), so catch clauses are instead attached to a generalized
    do statement:'
  quote_hash: sha256:27bc52beb18d8be0fc100fc1c46544b2e7d30c1af1be5d7e520ccc7148a84705
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-69
  short_excerpt: As with switch statements, Swift makes an effort to understand whether
    catch clauses are exhaustive. If it can determine it is, then the compiler considers
    the error to be handled. If not, the error automatically propagates out of scope,
    either to a lexically enclosing catch clause or out of the containing function
    (which must be marked throws ).
  quote_hash: sha256:3f8eb4afcbbcfcf97ba86db1638a60eeafb78080ab26add358fb91ad1e9202da
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-79
  short_excerpt: 'Therefore, while Swift automatically propagates errors, it requires
    that statements and expressions that can implicitly throw be marked with the try
    keyword. For example:'
  quote_hash: sha256:d0e91834023f4b94013b71553d60abd1b0bdda63b9f6ddecd1fa560caaa895b8
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-80
  short_excerpt: func readStuff() throws { // loadFile can throw an error. If so,
    it propagates out of readStuff. try loadFile("mystuff.txt") // This is a semantic
    error; the 'try' keyword is required // to indicate that it can throw. var y =
    stream.readFloat() // This is okay; the try covers the entire statement. try y
    += stream.readFloat() // This try applies to readBool(). if try stream.readBool()
    { // This try applies to both of these calls. let x = try stream.readInt() + stream.readInt()
    } if let err = stream.getOutOfBandError() { // Of course, the programmer doesn't
    have to mark explicit throws. throw er
  quote_hash: sha256:f32030eade6c35e6668513f5e1ff997849f3b275d507ce4d2992cf3e0578b5f8
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-106
  short_excerpt: 'We believe that we can cover the vast majority of Objective-C APIs
    with NSError** out-parameters by importing them as throws and removing the error
    clause from their signature. That is, a method like this one from NSAttributedString
    :'
  quote_hash: sha256:6cab7b11ad4b41e7e2f2d0575a287e1d6c5e5ab79a753f1d0a4d42fcf5756ecb
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-109
  short_excerpt: 'func dataFromRange( _ range: NSRange, documentAttributes dict: NSDictionary
    ) throws -> NSData'
  quote_hash: sha256:e9dd9b709155d0cd45c3027f91442824d2a7348ba5cd215f352d40cb5ab70942
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-133
  short_excerpt: func duplicateAndReturnError() throws -> NSDocument
  quote_hash: sha256:6e09757d3f12d1a090188c499152e88bebff50b60a84bf814fc4399f590b2004
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-137
  short_excerpt: func validateForDelete() throws
  quote_hash: sha256:082415b36dff1444f58c3944336c4e7b15b7f89fbedfbf483119821a5a14891c
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-142
  short_excerpt: 'We should make it easy to write higher-order functions that behave
    polymorphically with respect to whether their arguments throw. This can be done
    in a fairly simple way: a function can declare that it throws if any of a set
    of named arguments do. As an example (using strawman syntax):'
  quote_hash: sha256:6ccb8806324691e15c56c829d20ce94d65982ef66a5a9e04c513a44c54aba356
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-143
  short_excerpt: 'func map<T, U>(_ array: [T], fn: T -> U) throwsIf(fn) -> [U] { ...
    }'
  quote_hash: sha256:d183e9ebbba311a31a308e4c98d1eddc46f269602864fe30e62d6106eaa0569b
- source_id: swift-error-handling-design
  url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  final_url: https://raw.githubusercontent.com/swiftlang/swift/main/docs/ErrorHandling.md
  source_type: compiler_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: swift-error-handling-design-152
  short_excerpt: The error-handling model doesn't cause major problems for this. The
    compiler can infer that the closure throws, and autoreleasepool can be overloaded
    on whether its argument closure throws; the overload that takes a throwing closures
    would itself throw.
  quote_hash: sha256:348393dbbd7d7c17e4cf99985ea7982e17d560bef91e42d9c93e38b452447342
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# swift-throws-missing-try

## Failure Class
swift/error-handling

## Symptoms
- Calling a throwing function without try keyword or outside do-catch block produces compile error

## Fingerprints
- Call can throw
- try keyword required
- function can throw
- non-throwing context
- throws keyword

## First Checks
- Check whether the calling function is marked throws
- Check whether the call site wraps the throwing call in do { try ... } catch { ... }
- Check whether try? or try! is used where the error cannot be ignored

## Do Not Patch Yet
- Do not use try! in production code unless the function's contract guarantees success
- Do not catch all errors broadly; match specific error types to avoid masking unrelated failures

## Evidence Needed
- Capture the compile error message identifying the throwing function call site
- Identify whether the enclosing function is marked throws to propagate errors

## Minimal Fix Scope
- The throwing function call site
- The enclosing do-catch block or the calling function's throws declaration

## Validation Ladder
- Add try keyword and appropriate error handling; verify compile succeeds
- Test the code path with both success and failure inputs
- Run the unit test covering the throwing function boundary

## Regression Guard
- Add a test that exercises both the throwing and success paths of the function call

## Reviewer Notes
