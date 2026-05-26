---
id: kotlin-require-check-precondition
kind: debug-recipe
status: accepted
stack:
- kotlin
- android
failure_class: kotlin/preconditions
symptoms:
- Kotlin require() throws IllegalArgumentException or check() throws IllegalStateException
  unexpectedly
fingerprints:
- require() throws
- IllegalArgumentException
- check() precondition
- IllegalStateException
- precondition
first_checks:
- Check whether require() is used for argument validation (IllegalArgumentException)
- Check whether check() is used for state validation (IllegalStateException)
- Check whether the lazyMessage lambda captures stale state when the condition evaluates
  late
do_not:
- Do not use require() for state checks; use check() instead
- Do not use check() for input validation; use require() instead
evidence_needed:
- Capture the exception message from require() or check() to identify the precondition
- Identify the call site where the precondition fails
minimal_fix_scope:
- The require() or check() call site and its condition expression
- The caller that passes the violating argument or reaches the invalid state
validation_ladder:
- Reproduce the IllegalArgumentException or IllegalStateException with the failing
  input
- Fix the caller input or state transition and verify no exception
- Run the unit test covering the precondition path
regression_guard:
- Add a test that asserts IllegalArgumentException from require() and IllegalStateException
  from check()
evidence_refs:
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-14
  short_excerpt: In this example, an IllegalArgumentException is thrown when the user
    inputs a negative value. You can create custom error messages and keep the original
    cause ( cause ) of the exception, which will be included in the stack trace .
  quote_hash: sha256:13353ed662e6ec6b65e307e08366f473fa269109801b22cd3a459b09c5072810
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-15
  short_excerpt: Throw exceptions with precondition functions
  quote_hash: sha256:725611ee6b4647472df1f0bd34ffaf760c55edd57584c5345d1cc87d81e2a329
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-16
  short_excerpt: 'Kotlin offers additional ways to automatically throw exceptions
    using precondition functions. Precondition functions include:'
  quote_hash: sha256:38f4fa517990137258a7a0fdbde17e7fbe958126ab144f3fc88ea9e37d52bbfe
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-17
  short_excerpt: Precondition function
  quote_hash: sha256:884615720d4e4dd89ceb477b0a837089dcc77e37120fcc16c1821bd441cc71e9
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-20
  short_excerpt: require()
  quote_hash: sha256:504d7bd0c662bfbd14eacbadebe86108af84b977c7215f14bd1305170f1f1989
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-21
  short_excerpt: Checks user input validity
  quote_hash: sha256:ff5022b0eb547524e44744f22805094280862670acb12311c24c0e09159e47e1
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-22
  short_excerpt: IllegalArgumentException
  quote_hash: sha256:1f0d89d80de40929aa34407c63915268fb848d0e16b2105d841a3270e4351d58
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-23
  short_excerpt: check()
  quote_hash: sha256:916933605f98fc0318da0030d1d6a3daf933b8c89b2ad87bbbca7b15aef48498
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-24
  short_excerpt: Checks object or variable state validity
  quote_hash: sha256:0787874bbb37f8d00e7ceb2fcffcfaed87b184af2fc4137f9363f763166a85ae
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-25
  short_excerpt: IllegalStateException
  quote_hash: sha256:53c67e0fa33f180eaa4f2d65f1cc66cd00b98c64d89eb795532bf0f1d4e9d9bd
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-28
  short_excerpt: These functions are suitable for situations where the program's flow
    cannot continue if specific conditions aren't met. This streamlines your code
    and makes handling these checks efficient.
  quote_hash: sha256:fa45200fcfa3a9afa97edc9d453075357b18e91e6203a9cbc1664bcb6218ad15
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-29
  short_excerpt: Use the require() function to validate input arguments when they
    are crucial for the function's operation, and the function can't proceed if these
    arguments are invalid.
  quote_hash: sha256:3938b8c425aa0753bbe2486ddcb23499bb23c2033e24637ff4c13bc9ad7db6ef
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-30
  short_excerpt: 'If the condition in require() is not met, it throws an IllegalArgumentException
    :'
  quote_hash: sha256:fbf7c173040442b70933e79ccbf488218beef9a1e6d3d3fdf27aa607a2c4ef63
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-31
  short_excerpt: Use the check() function to validate the state of an object or variable.
    If the check fails, it indicates a logic error that needs to be addressed.
  quote_hash: sha256:58a2f1f581fa4ec0673cc6d864c18e653a2b9956a5566bae820436f43ed2c454
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-32
  short_excerpt: 'If the condition specified in the check() function is false , it
    throws an IllegalStateException :'
  quote_hash: sha256:74530f2fb941bfa3932dce7c2dd6bf8f6bf396ae9c11b27093a71d1e5be45c53
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# kotlin-require-check-precondition

## Failure Class
kotlin/preconditions

## Symptoms
- Kotlin require() throws IllegalArgumentException or check() throws IllegalStateException unexpectedly

## Fingerprints
- require() throws
- IllegalArgumentException
- check() precondition
- IllegalStateException
- precondition

## First Checks
- Check whether require() is used for argument validation (IllegalArgumentException)
- Check whether check() is used for state validation (IllegalStateException)
- Check whether the lazyMessage lambda captures stale state when the condition evaluates late

## Do Not Patch Yet
- Do not use require() for state checks; use check() instead
- Do not use check() for input validation; use require() instead

## Evidence Needed
- Capture the exception message from require() or check() to identify the precondition
- Identify the call site where the precondition fails

## Minimal Fix Scope
- The require() or check() call site and its condition expression
- The caller that passes the violating argument or reaches the invalid state

## Validation Ladder
- Reproduce the IllegalArgumentException or IllegalStateException with the failing input
- Fix the caller input or state transition and verify no exception
- Run the unit test covering the precondition path

## Regression Guard
- Add a test that asserts IllegalArgumentException from require() and IllegalStateException from check()

## Reviewer Notes
