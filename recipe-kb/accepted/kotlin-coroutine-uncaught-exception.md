---
id: kotlin-coroutine-uncaught-exception
kind: debug-recipe
status: accepted
stack:
- kotlin
- android
failure_class: kotlin/coroutines
symptoms:
- Coroutine throws uncaught exception that crashes the process instead of being handled
  by parent scope
fingerprints:
- CoroutineExceptionHandler got uncaught exception
- CoroutineExceptionHandler
- SupervisorJob cancellation
- supervisorScope
- coroutineScope
first_checks:
- Check whether a CoroutineExceptionHandler is installed on the root CoroutineScope
  or Job
- Check whether the failing coroutine is inside a supervisorScope (child failure does
  not cancel parent) vs coroutineScope (child failure propagates)
- Check whether a CancellationException is being swallowed instead of re-thrown
do_not:
- Do not catch CancellationException and suppress it; always re-throw after logging
- Do not install CoroutineExceptionHandler on a child Job; it only works on the root
evidence_needed:
- Capture the process crash log showing CoroutineExceptionHandler got uncaught exception
- Identify whether the failure is in a child coroutine and how it propagates to the
  scope
minimal_fix_scope:
- The root CoroutineScope or the supervisorScope boundary where the failure should
  be contained
- The coroutine launch block that throws the uncaught exception
validation_ladder:
- Reproduce the uncaught exception with the failing coroutine input
- Add a SupervisorJob or supervisorScope and verify the exception is contained
- Run the coroutine test covering the failure path
regression_guard:
- Add a coroutine test asserting the exception is handled and does not cancel the
  parent scope
evidence_refs:
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-2
  short_excerpt: This section covers exception handling and cancellation on exceptions.
    We already know that a cancelled coroutine throws CancellationException in suspension
    points and that it is ignored by the coroutines' machinery. Here we look at what
    happens if an exception is thrown during cancellation or multiple children of
    the same coroutine throw an exception.
  quote_hash: sha256:22a74ec6289a9fc523f316e281539ac9451ecc0071dc9303decb937a97cd5ea0
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-4
  short_excerpt: 'Coroutine builders come in two flavors: propagating exceptions automatically
    ( launch ) or exposing them to users ( async and produce ). When these builders
    are used to create a root coroutine, that is not a child of another coroutine,
    the former builders treat exceptions as uncaught exceptions, similar to Java''s
    Thread.uncaughtExceptionHandler , while the latter are relying on the user to
    consume the final exception, for example via await or receive ( produce and receive
    are covered in Channels section).'
  quote_hash: sha256:83f8d982ecd84a492468364534ab28f62a24c7c7bfde2cc6673631466c4badbf
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-13
  short_excerpt: CoroutineExceptionHandler
  quote_hash: sha256:7c7c14e52d8bde4ad60100d4394423359a1f5184f8aaf4939f44e1e8c027760b
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-14
  short_excerpt: It is possible to customize the default behavior of printing uncaught
    exceptions to the console. CoroutineExceptionHandler context element on a root
    coroutine can be used as a generic catch block for this root coroutine and all
    its children where custom exception handling may take place. It is similar to
    Thread.uncaughtExceptionHandler . You cannot recover from the exception in the
    CoroutineExceptionHandler . The coroutine had already completed with the corresponding
    exception when the handler is called. Normally, the handler is used to log the
    exception, show some kind of error message, termi
  quote_hash: sha256:0e53681e050fb0865348619525ca0431fbc832934cc138f41e523b7794c8e716
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-16
  short_excerpt: CoroutineExceptionHandler is invoked only on uncaught exceptions
    — exceptions that were not handled in any other way. In particular, all children
    coroutines (coroutines created in the context of another Job ) delegate handling
    of their exceptions to their parent coroutine, which also delegates to the parent,
    and so on until the root, so the CoroutineExceptionHandler installed in their
    context is never used. In addition to that, async builder always catches all exceptions
    and represents them in the resulting Deferred object, so its CoroutineExceptionHandler
    has no effect either.
  quote_hash: sha256:349e900c04921a51a8adef0885033c1e227a0d3b962efc63f679d4b896e7a4ef
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-18
  short_excerpt: import kotlinx.coroutines.* @OptIn(DelicateCoroutinesApi::class)
    fun main() = runBlocking { //sampleStart val handler = CoroutineExceptionHandler
    { _, exception -> println("CoroutineExceptionHandler got $exception") } val job
    = GlobalScope.launch(handler) { // root coroutine, running in GlobalScope throw
    AssertionError() } val deferred = GlobalScope.async(handler) { // also root, but
    async instead of launch throw ArithmeticException() // Nothing will be printed,
    relying on user to call deferred.await() } joinAll(job, deferred) //sampleEnd
    }
  quote_hash: sha256:d84de9694b940820858962f4b81660e68775db3d4f76cead989d2303b9c91ac4
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-20
  short_excerpt: CoroutineExceptionHandler got java.lang.AssertionError
  quote_hash: sha256:c2f1b1a36b69dcb98f35269f52cc7c1dc6c3595a0c8ad393a4774c7b654866bf
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-22
  short_excerpt: Cancellation is closely related to exceptions. Coroutines internally
    use CancellationException for cancellation, these exceptions are ignored by all
    handlers, so they should be used only as the source of additional debug information,
    which can be obtained by catch block. When a coroutine is cancelled using Job.cancel
    , it terminates, but it does not cancel its parent.
  quote_hash: sha256:165e63380599893967aa2e26a64a18731ec7a087edbfb49b8c40f72e704726b5
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-25
  short_excerpt: If a coroutine encounters an exception other than CancellationException
    , it cancels its parent with that exception. This behaviour cannot be overridden
    and is used to provide stable coroutines hierarchies for structured concurrency
    . CoroutineExceptionHandler implementation is not used for child coroutines.
  quote_hash: sha256:51e8830a94e1df52e8b86e774fa22b0c948c53ebb9b09e9d6537524b37e02c16
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-26
  short_excerpt: In these examples, CoroutineExceptionHandler is always installed
    to a coroutine that is created in GlobalScope . It does not make sense to install
    an exception handler to a coroutine that is launched in the scope of the main
    runBlocking , since the main coroutine is going to be always cancelled when its
    child completes with exception despite the installed handler.
  quote_hash: sha256:d1cc6f27b56bc6a8032d29445555e3986dad6b1a27eafd9577f13870021cea77
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-28
  short_excerpt: import kotlinx.coroutines.* @OptIn(DelicateCoroutinesApi::class)
    fun main() = runBlocking { //sampleStart val handler = CoroutineExceptionHandler
    { _, exception -> println("CoroutineExceptionHandler got $exception") } val job
    = GlobalScope.launch(handler) { launch { // the first child try { delay(Long.MAX_VALUE)
    } finally { withContext(NonCancellable) { println("Children are cancelled, but
    exception is not handled until all children terminate") delay(100) println("The
    first child finished its non cancellable block") } } } launch { // the second
    child delay(10) println("Second child throws an e
  quote_hash: sha256:396959a7675cc86a5bdeaaaf3998e5fd391bc8f58e2517b6917617f315471aea
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-29
  short_excerpt: Second child throws an exception Children are cancelled, but exception
    is not handled until all children terminate The first child finished its non cancellable
    block CoroutineExceptionHandler got java.lang.ArithmeticException
  quote_hash: sha256:1d60e82b1201cc5958d9ed5cf62d6e46ec2bea5ca89b1ca94bfcd42d601d181b
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-32
  short_excerpt: import kotlinx.coroutines.* import java.io.* @OptIn(DelicateCoroutinesApi::class)
    fun main() = runBlocking { val handler = CoroutineExceptionHandler { _, exception
    -> println("CoroutineExceptionHandler got $exception with suppressed ${exception.suppressed.contentToString()}")
    } val job = GlobalScope.launch(handler) { launch { try { delay(Long.MAX_VALUE)
    // it gets cancelled when another sibling fails with IOException } finally { throw
    ArithmeticException() // the second exception } } launch { delay(100) throw IOException()
    // the first exception } delay(Long.MAX_VALUE) } job.join() }
  quote_hash: sha256:1ae767d3152a0dc38e5e72d17b1534ca49998d223c8ca6c038c98d7da60043f2
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-33
  short_excerpt: CoroutineExceptionHandler got java.io.IOException with suppressed
    [java.lang.ArithmeticException]
  quote_hash: sha256:4ab186502bef61416392f414b5017f4e1b6f67681d642ff237eebd42921064e8
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-36
  short_excerpt: 'import kotlinx.coroutines.* import java.io.* @OptIn(DelicateCoroutinesApi::class)
    fun main() = runBlocking { //sampleStart val handler = CoroutineExceptionHandler
    { _, exception -> println("CoroutineExceptionHandler got $exception") } val job
    = GlobalScope.launch(handler) { val innerJob = launch { // all this stack of coroutines
    will get cancelled launch { launch { throw IOException() // the original exception
    } } } try { innerJob.join() } catch (e: CancellationException) { println("Rethrowing
    CancellationException with original cause") throw e // cancellation exception
    is rethrown, yet the or'
  quote_hash: sha256:a2422f7acfa147ae0953c1e0b622b2d9559562e613910fa8a716c1d021472b29
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-37
  short_excerpt: Rethrowing CancellationException with original cause CoroutineExceptionHandler
    got java.io.IOException
  quote_hash: sha256:ae8ceb23604dff87856ea6c153295297ab3a004277a41e7c2d38a3edfa5c52ca
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-43
  short_excerpt: 'The SupervisorJob can be used for these purposes. It is similar
    to a regular Job with the only exception that cancellation is propagated only
    downwards. This can easily be demonstrated using the following example:'
  quote_hash: sha256:fe36eadba0a1d3299b830be49eb4b59e418b68e8c9557497df246490383b9710
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-44
  short_excerpt: 'import kotlinx.coroutines.* fun main() = runBlocking { //sampleStart
    val supervisor = SupervisorJob() with(CoroutineScope(coroutineContext + supervisor))
    { // launch the first child -- its exception is ignored for this example (don''t
    do this in practice!) val firstChild = launch(CoroutineExceptionHandler { _, _
    -> }) { println("The first child is failing") throw AssertionError("The first
    child is cancelled") } // launch the second child val secondChild = launch { firstChild.join()
    // Cancellation of the first child is not propagated to the second child println("The
    first child is cancelled: ${'
  quote_hash: sha256:91d466c1233df459a888235a0e720cea719a4fb83c2ddebbbda043057ee31245
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-47
  short_excerpt: Instead of coroutineScope , we can use supervisorScope for scoped
    concurrency. It propagates the cancellation in one direction only and cancels
    all its children only if it failed itself. It also waits for all children before
    completion just like coroutineScope does.
  quote_hash: sha256:5c39bc2f13233b1f4843a5671629ade6219de35f049d6730b28a03bb6b915cbf
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-48
  short_excerpt: 'import kotlin.coroutines.* import kotlinx.coroutines.* fun main()
    = runBlocking { //sampleStart try { supervisorScope { val child = launch { try
    { println("The child is sleeping") delay(Long.MAX_VALUE) } finally { println("The
    child is cancelled") } } // Give our child a chance to execute and print using
    yield yield() println("Throwing an exception from the scope") throw AssertionError()
    } } catch(e: AssertionError) { println("Caught an assertion error") } //sampleEnd
    }'
  quote_hash: sha256:d9aa6a6fa38d1d43e0edbebcf2196aac4deeda2505e7705e91e625d2439d2949
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-50
  short_excerpt: Another crucial difference between regular and supervisor jobs is
    exception handling. Every child should handle its exceptions by itself via the
    exception handling mechanism. This difference comes from the fact that child's
    failure does not propagate to the parent. It means that coroutines launched directly
    inside the supervisorScope do use the CoroutineExceptionHandler that is installed
    in their scope in the same way as root coroutines do (see the CoroutineExceptionHandler
    section for details).
  quote_hash: sha256:edaad8ac77d50497de90a13b590773b08941fda2c2d32a467fb30c2a2ff35374
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-51
  short_excerpt: import kotlin.coroutines.* import kotlinx.coroutines.* fun main()
    = runBlocking { //sampleStart val handler = CoroutineExceptionHandler { _, exception
    -> println("CoroutineExceptionHandler got $exception") } supervisorScope { val
    child = launch(handler) { println("The child throws an exception") throw AssertionError()
    } println("The scope is completing") } println("The scope is completed") //sampleEnd
    }
  quote_hash: sha256:71d2c5cde1a32995caff1a9561641cedc3f867814b75a28ccee1b3bd3361ef5d
- source_id: kotlin-coroutines-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/exception-handling.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-coroutines-exception-handling-52
  short_excerpt: The scope is completing The child throws an exception CoroutineExceptionHandler
    got java.lang.AssertionError The scope is completed
  quote_hash: sha256:292ff36c390a220ae5e4771ca67b6bd5de33fe0b8c4624d2412690dc61494b7f
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# kotlin-coroutine-uncaught-exception

## Failure Class
kotlin/coroutines

## Symptoms
- Coroutine throws uncaught exception that crashes the process instead of being handled by parent scope

## Fingerprints
- CoroutineExceptionHandler got uncaught exception
- CoroutineExceptionHandler
- SupervisorJob cancellation
- supervisorScope
- coroutineScope

## First Checks
- Check whether a CoroutineExceptionHandler is installed on the root CoroutineScope or Job
- Check whether the failing coroutine is inside a supervisorScope (child failure does not cancel parent) vs coroutineScope (child failure propagates)
- Check whether a CancellationException is being swallowed instead of re-thrown

## Do Not Patch Yet
- Do not catch CancellationException and suppress it; always re-throw after logging
- Do not install CoroutineExceptionHandler on a child Job; it only works on the root

## Evidence Needed
- Capture the process crash log showing CoroutineExceptionHandler got uncaught exception
- Identify whether the failure is in a child coroutine and how it propagates to the scope

## Minimal Fix Scope
- The root CoroutineScope or the supervisorScope boundary where the failure should be contained
- The coroutine launch block that throws the uncaught exception

## Validation Ladder
- Reproduce the uncaught exception with the failing coroutine input
- Add a SupervisorJob or supervisorScope and verify the exception is contained
- Run the coroutine test covering the failure path

## Regression Guard
- Add a coroutine test asserting the exception is handled and does not cancel the parent scope

## Reviewer Notes
