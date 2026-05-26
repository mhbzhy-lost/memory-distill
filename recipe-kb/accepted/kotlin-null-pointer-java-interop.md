---
id: kotlin-null-pointer-java-interop
kind: debug-recipe
status: accepted
stack:
- kotlin
- android
failure_class: kotlin/null-safety
symptoms:
- Kotlin code receives NullPointerException when calling Java platform types without
  null checks
fingerprints:
- NullPointerException
- platform type
- Java interop
- '!! operator'
- null safety
first_checks:
- Check whether the value originates from a Java platform type (no nullability annotation)
- Check whether a non-null assertion operator !! is applied to a platform type value
- Check whether an explicit nullable type annotation (? suffix) is missing on the
  receiving side
do_not:
- Do not suppress NullPointerException with try-catch before adding null checks
- Do not assume Java platform types are non-null; always treat them as potentially
  nullable
evidence_needed:
- Identify the Java method or field that returns the platform type value
- Capture the stack trace showing NullPointerException at the Kotlin call site
minimal_fix_scope:
- The Kotlin receiver that consumes the Java platform type
- The null-safety annotation or safe call on the affected value
validation_ladder:
- Reproduce the NullPointerException with the failing input or call path
- Add a safe call (?.) or explicit null check and verify no exception
- Run the Kotlin/Java interop test for the affected call boundary
regression_guard:
- Add a test that exercises the Java interop boundary with null and non-null inputs
evidence_refs:
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-84
  short_excerpt: 'NullPointerException : This exception is thrown when an application
    attempts to use an object reference that has the null value. Even though Kotlin''s
    null safety features significantly reduce the risk of NullPointerExceptions, they
    can still occur either through deliberate use of the !! operator or when interacting
    with Java, which lacks Kotlin''s null safety. val text: String? = null println(text!!.length)
    // throws a NullPointerException'
  quote_hash: sha256:730a9db648706049c44c46af1f93c2d65c9b4c44172d9c16c081e45c2614985b
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-85
  short_excerpt: 'NullPointerException : This exception is thrown when an application
    attempts to use an object reference that has the null value. Even though Kotlin''s
    null safety features significantly reduce the risk of NullPointerExceptions, they
    can still occur either through deliberate use of the !! operator or when interacting
    with Java, which lacks Kotlin''s null safety.'
  quote_hash: sha256:30cb47f11d19de60ee78b6391ed9fa73e4ca97e192f8349b1f84cefa65ce36ff
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-86
  short_excerpt: NullPointerException
  quote_hash: sha256:ac29021f63657b6c3b0e938939993fbcaae289ed3dda75a4e2724a67472b9219
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-94
  short_excerpt: 'RuntimeException is usually caused by insufficient checks in the
    program code and can be prevented programmatically. Kotlin helps prevent common
    RuntimeExceptions like NullPointerException and provides compile-time warnings
    for potential runtime errors, such as division by zero. The following picture
    demonstrates a hierarchy of subtypes descended from RuntimeException :'
  quote_hash: sha256:69599646c9c2eafe07f8a48c89d8ea42b340f499fd637df3c6148e177eca0264
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-100
  short_excerpt: 'Exception type: java.lang.ArithmeticException'
  quote_hash: sha256:7a7281314cce9997f51197699cceba1f67e7544c40f06990f5974f4b9e14891c
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-106
  short_excerpt: Exception interoperability with Java, Swift, and Objective-C
  quote_hash: sha256:cde577635b220c3001ef4972e4ac5ab7c763bd2f232fd7fd201e2ccc5f3c53b7
- source_id: kotlin-exceptions-language-doc
  url: https://kotlinlang.org/docs/exceptions.html
  final_url: https://kotlinlang.org/docs/exceptions.html
  source_type: language_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: kotlin-exceptions-language-doc-107
  short_excerpt: Since Kotlin treats all exceptions as unchecked, it can lead to complications
    when such exceptions are called from languages that distinguish between checked
    and unchecked exceptions. To address this disparity in exception handling between
    Kotlin and languages like Java, Swift, and Objective-C, you can use the @Throws
    annotation. This annotation alerts callers about possible exceptions. For more
    information, see Calling Kotlin from Java and Interoperability with Swift/Objective-C
    .
  quote_hash: sha256:f4c107cbef4e1c3553eebc2ea00f348f09c2900a3400fed45ebdd68db6f89ce6
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# kotlin-null-pointer-java-interop

## Failure Class
kotlin/null-safety

## Symptoms
- Kotlin code receives NullPointerException when calling Java platform types without null checks

## Fingerprints
- NullPointerException
- platform type
- Java interop
- !! operator
- null safety

## First Checks
- Check whether the value originates from a Java platform type (no nullability annotation)
- Check whether a non-null assertion operator !! is applied to a platform type value
- Check whether an explicit nullable type annotation (? suffix) is missing on the receiving side

## Do Not Patch Yet
- Do not suppress NullPointerException with try-catch before adding null checks
- Do not assume Java platform types are non-null; always treat them as potentially nullable

## Evidence Needed
- Identify the Java method or field that returns the platform type value
- Capture the stack trace showing NullPointerException at the Kotlin call site

## Minimal Fix Scope
- The Kotlin receiver that consumes the Java platform type
- The null-safety annotation or safe call on the affected value

## Validation Ladder
- Reproduce the NullPointerException with the failing input or call path
- Add a safe call (?.) or explicit null check and verify no exception
- Run the Kotlin/Java interop test for the affected call boundary

## Regression Guard
- Add a test that exercises the Java interop boundary with null and non-null inputs

## Reviewer Notes
