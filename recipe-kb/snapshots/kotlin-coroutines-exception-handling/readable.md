- [kotlin-coroutines-exception-handling-1] https://github.com/Kotlin/kotlinx.coroutines/edit/master/docs/topics/

- [kotlin-coroutines-exception-handling-2] This section covers exception handling and cancellation on exceptions. We already know that a cancelled coroutine throws CancellationException in suspension points and that it is ignored by the coroutines' machinery. Here we look at what happens if an exception is thrown during cancellation or multiple children of the same coroutine throw an exception.

- [kotlin-coroutines-exception-handling-3] Exception propagation

- [kotlin-coroutines-exception-handling-4] Coroutine builders come in two flavors: propagating exceptions automatically ( launch ) or exposing them to users ( async and produce ). When these builders are used to create a root coroutine, that is not a child of another coroutine, the former builders treat exceptions as uncaught exceptions, similar to Java's Thread.uncaughtExceptionHandler , while the latter are relying on the user to consume the final exception, for example via await or receive ( produce and receive are covered in Channels section).

- [kotlin-coroutines-exception-handling-5] It can be demonstrated by a simple example that creates root coroutines using the GlobalScope :

- [kotlin-coroutines-exception-handling-6] GlobalScope is a delicate API that can backfire in non-trivial ways. Creating a root coroutine for the whole application is one of the rare legitimate uses for GlobalScope , so you must explicitly opt-in into using GlobalScope with @OptIn(DelicateCoroutinesApi::class) .

- [kotlin-coroutines-exception-handling-7] {style="note"}

- [kotlin-coroutines-exception-handling-8] import kotlinx.coroutines.* //sampleStart @OptIn(DelicateCoroutinesApi::class) fun main() = runBlocking { val job = GlobalScope.launch { // root coroutine with launch println("Throwing exception from launch") throw IndexOutOfBoundsException() // Will be printed to the console by Thread.defaultUncaughtExceptionHandler } job.join() println("Joined failed job") val deferred = GlobalScope.async { // root coroutine with async println("Throwing exception from async") throw ArithmeticException() // Nothing is printed, relying on user to call await } try { deferred.await() println("Unreached") } catch (e: ArithmeticException) { println("Caught ArithmeticException") } } //sampleEnd

- [kotlin-coroutines-exception-handling-9] {kotlin-runnable="true" kotlin-min-compiler-version="1.3"}

- [kotlin-coroutines-exception-handling-10] You can get the full code here .

- [kotlin-coroutines-exception-handling-11] The output of this code is (with debug ):

- [kotlin-coroutines-exception-handling-12] Throwing exception from launch Exception in thread "DefaultDispatcher-worker-1 @coroutine#2" java.lang.IndexOutOfBoundsException Joined failed job Throwing exception from async Caught ArithmeticException

- [kotlin-coroutines-exception-handling-13] CoroutineExceptionHandler

- [kotlin-coroutines-exception-handling-14] It is possible to customize the default behavior of printing uncaught exceptions to the console. CoroutineExceptionHandler context element on a root coroutine can be used as a generic catch block for this root coroutine and all its children where custom exception handling may take place. It is similar to Thread.uncaughtExceptionHandler . You cannot recover from the exception in the CoroutineExceptionHandler . The coroutine had already completed with the corresponding exception when the handler is called. Normally, the handler is used to log the exception, show some kind of error message, terminate, and/or restart the application.

- [kotlin-coroutines-exception-handling-15] Thread.uncaughtExceptionHandler

- [kotlin-coroutines-exception-handling-16] CoroutineExceptionHandler is invoked only on uncaught exceptions — exceptions that were not handled in any other way. In particular, all children coroutines (coroutines created in the context of another Job ) delegate handling of their exceptions to their parent coroutine, which also delegates to the parent, and so on until the root, so the CoroutineExceptionHandler installed in their context is never used. In addition to that, async builder always catches all exceptions and represents them in the resulting Deferred object, so its CoroutineExceptionHandler has no effect either.

- [kotlin-coroutines-exception-handling-17] Coroutines running in supervision scope do not propagate exceptions to their parent and are excluded from this rule. A further Supervision section of this document gives more details.

- [kotlin-coroutines-exception-handling-18] import kotlinx.coroutines.* @OptIn(DelicateCoroutinesApi::class) fun main() = runBlocking { //sampleStart val handler = CoroutineExceptionHandler { _, exception -> println("CoroutineExceptionHandler got $exception") } val job = GlobalScope.launch(handler) { // root coroutine, running in GlobalScope throw AssertionError() } val deferred = GlobalScope.async(handler) { // also root, but async instead of launch throw ArithmeticException() // Nothing will be printed, relying on user to call deferred.await() } joinAll(job, deferred) //sampleEnd }

- [kotlin-coroutines-exception-handling-19] The output of this code is:

- [kotlin-coroutines-exception-handling-20] CoroutineExceptionHandler got java.lang.AssertionError

- [kotlin-coroutines-exception-handling-21] Cancellation and exceptions

- [kotlin-coroutines-exception-handling-22] Cancellation is closely related to exceptions. Coroutines internally use CancellationException for cancellation, these exceptions are ignored by all handlers, so they should be used only as the source of additional debug information, which can be obtained by catch block. When a coroutine is cancelled using Job.cancel , it terminates, but it does not cancel its parent.

- [kotlin-coroutines-exception-handling-23] import kotlinx.coroutines.* fun main() = runBlocking { //sampleStart val job = launch { val child = launch { try { delay(Long.MAX_VALUE) } finally { println("Child is cancelled") } } yield() println("Cancelling child") child.cancel() child.join() yield() println("Parent is not cancelled") } job.join() //sampleEnd }

- [kotlin-coroutines-exception-handling-24] Cancelling child Child is cancelled Parent is not cancelled

- [kotlin-coroutines-exception-handling-25] If a coroutine encounters an exception other than CancellationException , it cancels its parent with that exception. This behaviour cannot be overridden and is used to provide stable coroutines hierarchies for structured concurrency . CoroutineExceptionHandler implementation is not used for child coroutines.

- [kotlin-coroutines-exception-handling-26] In these examples, CoroutineExceptionHandler is always installed to a coroutine that is created in GlobalScope . It does not make sense to install an exception handler to a coroutine that is launched in the scope of the main runBlocking , since the main coroutine is going to be always cancelled when its child completes with exception despite the installed handler.

- [kotlin-coroutines-exception-handling-27] The original exception is handled by the parent only when all its children terminate, which is demonstrated by the following example.

- [kotlin-coroutines-exception-handling-28] import kotlinx.coroutines.* @OptIn(DelicateCoroutinesApi::class) fun main() = runBlocking { //sampleStart val handler = CoroutineExceptionHandler { _, exception -> println("CoroutineExceptionHandler got $exception") } val job = GlobalScope.launch(handler) { launch { // the first child try { delay(Long.MAX_VALUE) } finally { withContext(NonCancellable) { println("Children are cancelled, but exception is not handled until all children terminate") delay(100) println("The first child finished its non cancellable block") } } } launch { // the second child delay(10) println("Second child throws an exception") throw ArithmeticException() } } job.join() //sampleEnd }

- [kotlin-coroutines-exception-handling-29] Second child throws an exception Children are cancelled, but exception is not handled until all children terminate The first child finished its non cancellable block CoroutineExceptionHandler got java.lang.ArithmeticException

- [kotlin-coroutines-exception-handling-30] Exceptions aggregation

- [kotlin-coroutines-exception-handling-31] When multiple children of a coroutine fail with an exception, the general rule is "the first exception wins", so the first exception gets handled. All additional exceptions that happen after the first one are attached to the first exception as suppressed ones.

- [kotlin-coroutines-exception-handling-32] import kotlinx.coroutines.* import java.io.* @OptIn(DelicateCoroutinesApi::class) fun main() = runBlocking { val handler = CoroutineExceptionHandler { _, exception -> println("CoroutineExceptionHandler got $exception with suppressed ${exception.suppressed.contentToString()}") } val job = GlobalScope.launch(handler) { launch { try { delay(Long.MAX_VALUE) // it gets cancelled when another sibling fails with IOException } finally { throw ArithmeticException() // the second exception } } launch { delay(100) throw IOException() // the first exception } delay(Long.MAX_VALUE) } job.join() }

- [kotlin-coroutines-exception-handling-33] CoroutineExceptionHandler got java.io.IOException with suppressed [java.lang.ArithmeticException]

- [kotlin-coroutines-exception-handling-34] Note that this mechanism currently only works on Java version 1.7+. The JS and Native restrictions are temporary and will be lifted in the future.

- [kotlin-coroutines-exception-handling-35] Cancellation exceptions are transparent and are unwrapped by default:

- [kotlin-coroutines-exception-handling-36] import kotlinx.coroutines.* import java.io.* @OptIn(DelicateCoroutinesApi::class) fun main() = runBlocking { //sampleStart val handler = CoroutineExceptionHandler { _, exception -> println("CoroutineExceptionHandler got $exception") } val job = GlobalScope.launch(handler) { val innerJob = launch { // all this stack of coroutines will get cancelled launch { launch { throw IOException() // the original exception } } } try { innerJob.join() } catch (e: CancellationException) { println("Rethrowing CancellationException with original cause") throw e // cancellation exception is rethrown, yet the original IOException gets to the handler } } job.join() //sampleEnd }

- [kotlin-coroutines-exception-handling-37] Rethrowing CancellationException with original cause CoroutineExceptionHandler got java.io.IOException

- [kotlin-coroutines-exception-handling-38] Supervision

- [kotlin-coroutines-exception-handling-39] As we have studied before, cancellation is a bidirectional relationship propagating through the whole hierarchy of coroutines. Let us take a look at the case when unidirectional cancellation is required.

- [kotlin-coroutines-exception-handling-40] A good example of such a requirement is a UI component with the job defined in its scope. If any of the UI's child tasks have failed, it is not always necessary to cancel (effectively kill) the whole UI component, but if the UI component is destroyed (and its job is cancelled), then it is necessary to cancel all child jobs as their results are no longer needed.

- [kotlin-coroutines-exception-handling-41] Another example is a server process that spawns multiple child jobs and needs to supervise their execution, tracking their failures and only restarting the failed ones.

- [kotlin-coroutines-exception-handling-42] Supervision job

- [kotlin-coroutines-exception-handling-43] The SupervisorJob can be used for these purposes. It is similar to a regular Job with the only exception that cancellation is propagated only downwards. This can easily be demonstrated using the following example:

- [kotlin-coroutines-exception-handling-44] import kotlinx.coroutines.* fun main() = runBlocking { //sampleStart val supervisor = SupervisorJob() with(CoroutineScope(coroutineContext + supervisor)) { // launch the first child -- its exception is ignored for this example (don't do this in practice!) val firstChild = launch(CoroutineExceptionHandler { _, _ -> }) { println("The first child is failing") throw AssertionError("The first child is cancelled") } // launch the second child val secondChild = launch { firstChild.join() // Cancellation of the first child is not propagated to the second child println("The first child is cancelled: ${firstChild.isCancelled}, but the second one is still active") try { delay(Long.MAX_VALUE) } finally { // But cancellation of the supervisor is propagated println("The second child is cancelled because the supervisor was cancelled") } } // wait until the first child fails & completes firstChild.join() println("Cancelling the supervisor") supervisor.cancel() secondChild.join() } //sampleEnd }

- [kotlin-coroutines-exception-handling-45] The first child is failing The first child is cancelled: true, but the second one is still active Cancelling the supervisor The second child is cancelled because the supervisor was cancelled

- [kotlin-coroutines-exception-handling-46] Supervision scope

- [kotlin-coroutines-exception-handling-47] Instead of coroutineScope , we can use supervisorScope for scoped concurrency. It propagates the cancellation in one direction only and cancels all its children only if it failed itself. It also waits for all children before completion just like coroutineScope does.

- [kotlin-coroutines-exception-handling-48] import kotlin.coroutines.* import kotlinx.coroutines.* fun main() = runBlocking { //sampleStart try { supervisorScope { val child = launch { try { println("The child is sleeping") delay(Long.MAX_VALUE) } finally { println("The child is cancelled") } } // Give our child a chance to execute and print using yield yield() println("Throwing an exception from the scope") throw AssertionError() } } catch(e: AssertionError) { println("Caught an assertion error") } //sampleEnd }

- [kotlin-coroutines-exception-handling-49] The child is sleeping Throwing an exception from the scope The child is cancelled Caught an assertion error

- [kotlin-coroutines-exception-handling-50] Another crucial difference between regular and supervisor jobs is exception handling. Every child should handle its exceptions by itself via the exception handling mechanism. This difference comes from the fact that child's failure does not propagate to the parent. It means that coroutines launched directly inside the supervisorScope do use the CoroutineExceptionHandler that is installed in their scope in the same way as root coroutines do (see the CoroutineExceptionHandler section for details).

- [kotlin-coroutines-exception-handling-51] import kotlin.coroutines.* import kotlinx.coroutines.* fun main() = runBlocking { //sampleStart val handler = CoroutineExceptionHandler { _, exception -> println("CoroutineExceptionHandler got $exception") } supervisorScope { val child = launch(handler) { println("The child throws an exception") throw AssertionError() } println("The scope is completing") } println("The scope is completed") //sampleEnd }

- [kotlin-coroutines-exception-handling-52] The scope is completing The child throws an exception CoroutineExceptionHandler got java.lang.AssertionError The scope is completed
