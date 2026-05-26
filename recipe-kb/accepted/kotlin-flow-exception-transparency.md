---
id: kotlin-flow-exception-transparency
kind: debug-recipe
status: accepted
stack:
- kotlin
- android
failure_class: kotlin/flow
symptoms:
- Flow throws Flow exception transparency violation because an exception was emitted
  from an unexpected place
fingerprints:
- Flow exception transparency violation
- Flow invariant is violated
- emission happened in
- flowOn instead
- catch operator
first_checks:
- Check whether the exception originated inside the flow { } builder vs upstream operators
- Check whether catch only catches upstream exceptions (it does not catch downstream
  collect failures)
- Check whether flowOn was used instead of withContext to change the execution context
do_not:
- Do not use withContext inside a flow { } builder; use flowOn instead
- Do not catch exceptions in collect {} and expect the flow to continue; use catch
  operator before collect
evidence_needed:
- Capture the Flow exception transparency violation stack trace
- Identify which flow operator or collect site threw the exception
minimal_fix_scope:
- The flow { } builder block or the operator chain
- The catch operator placement relative to upstream and downstream failures
validation_ladder:
- Reproduce the exception with the failing flow emission
- Move the catch operator upstream and verify the exception is handled
- Run the flow test covering the failure path
regression_guard:
- Add a flow test asserting the catch operator handles the specific error type
evidence_refs:
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-85
  short_excerpt: withContext(context) { simple().collect { value -> println(value)
    // run in the specified context } }
  quote_hash: sha256:bc8581c8938a6554c04311392ade9ef23ead2e9bf10875410b741b6ccef4a5fb
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-92
  short_excerpt: A common pitfall when using withContext
  quote_hash: sha256:2953f28f43c108cccdfca80a35ef1eec205e59c6e8b47d5458a72acb311d1633
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-93
  short_excerpt: However, the long-running CPU-consuming code might need to be executed
    in the context of Dispatchers.Default and UI-updating code might need to be executed
    in the context of Dispatchers.Main . Usually, withContext is used to change the
    context in the code using Kotlin coroutines, but code in the flow { ... } builder
    has to honor the context preservation property and is not allowed to emit from
    a different context.
  quote_hash: sha256:39771533114edf15cc3bb3c3d8074d188c2384b1559301831ff4cc390d800919
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-95
  short_excerpt: 'import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart
    fun simple(): Flow<Int> = flow { // The WRONG way to change context for CPU-consuming
    code in flow builder kotlinx.coroutines.withContext(Dispatchers.Default) { for
    (i in 1..3) { Thread.sleep(100) // pretend we are computing it in CPU-consuming
    way emit(i) // emit next value } } } fun main() = runBlocking<Unit> { simple().collect
    { value -> println(value) } } //sampleEnd'
  quote_hash: sha256:fbbcf82fa6ec4fcc9d3656bece10c9ad1ffe53e024025c08246c81249b143bc8
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-97
  short_excerpt: 'Exception in thread "main" java.lang.IllegalStateException: Flow
    invariant is violated: Flow was collected in [CoroutineId(1), "coroutine#1":BlockingCoroutine{Active}@5511c7f8,
    BlockingEventLoop@2eac3323], but emission happened in [CoroutineId(1), "coroutine#1":DispatchedCoroutine{Active}@2dae0000,
    Dispatchers.Default]. Please refer to ''flow'' documentation or use ''flowOn''
    instead at ...'
  quote_hash: sha256:2cea6ca67e95e455f35ed3da67ca1f47278378046afc309b6e9e55aec18ad3ce
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-98
  short_excerpt: flowOn operator
  quote_hash: sha256:ebcc10a5f1966ececb6c8e0bab297389a0aa6f823f0d23a27e3798d65a7e87a1
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-99
  short_excerpt: 'The exception refers to the flowOn function that shall be used to
    change the context of the flow emission. The correct way to change the context
    of a flow is shown in the example below, which also prints the names of the corresponding
    threads to show how it all works:'
  quote_hash: sha256:b34faef6eebd1445c5d9389abe81572ad4ce80218778ef1f89e921b89550d7a5
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-100
  short_excerpt: 'import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun
    log(msg: String) = println("[${Thread.currentThread().name}] $msg") //sampleStart
    fun simple(): Flow<Int> = flow { for (i in 1..3) { Thread.sleep(100) // pretend
    we are computing it in CPU-consuming way log("Emitting $i") emit(i) // emit next
    value } }.flowOn(Dispatchers.Default) // RIGHT way to change context for CPU-consuming
    code in flow builder fun main() = runBlocking<Unit> { simple().collect { value
    -> log("Collected $value") } } //sampleEnd'
  quote_hash: sha256:fea746428debdbabc7675775489f4c0192d470617e5416e1d210d4bf04d62c30
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-103
  short_excerpt: Another thing to observe here is that the flowOn operator has changed
    the default sequential nature of the flow. Now collection happens in one coroutine
    ("coroutine#1") and emission happens in another coroutine ("coroutine#2") that
    is running in another thread concurrently with the collecting coroutine. The flowOn
    operator creates another coroutine for an upstream flow when it has to change
    the CoroutineDispatcher in its context.
  quote_hash: sha256:078497da9b77c69d7359a6534d9cfc127dc151a7d93d8a53a19da86b08460879
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-113
  short_excerpt: Note that the flowOn operator uses the same buffering mechanism when
    it has to change a CoroutineDispatcher , but here we explicitly request buffering
    without changing the execution context.
  quote_hash: sha256:d62a4848c71208d6f9608425706513cbc93f54be65d6dcdf9bf800286546e224
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-179
  short_excerpt: 'The emitter can use a catch operator that preserves this exception
    transparency and allows encapsulation of its exception handling. The body of the
    catch operator can analyze an exception and react to it in different ways depending
    on which exception was caught:'
  quote_hash: sha256:68198a5424e385c4943403589e0ae2d4875e53ffe869a514443eb03beceec5be
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-189
  short_excerpt: 'A "Caught ..." message is not printed despite there being a catch
    operator:'
  quote_hash: sha256:e912193655cccf70680f542cbf8303ab15408c5c4547ce50709e7e0608535a2d
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-192
  short_excerpt: 'We can combine the declarative nature of the catch operator with
    a desire to handle all the exceptions, by moving the body of the collect operator
    into onEach and putting it before the catch operator. Collection of this flow
    must be triggered by a call to collect() without parameters:'
  quote_hash: sha256:d6ebb5b229e2ef735ddb726604c04ef15c682e483b3ec4ae575d711ae1cab74f
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-211
  short_excerpt: The onCompletion operator, unlike catch , does not handle the exception.
    As we can see from the above example code, the exception still flows downstream.
    It will be delivered to further onCompletion operators and can be handled with
    a catch operator.
  quote_hash: sha256:3e33bfb22e4bb8bd091f2793aace4e0f3c3b195337b8d3b8306cb560509eb975
- source_id: kotlin-flow-exception-handling
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/flow.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-flow-exception-handling-213
  short_excerpt: Another difference with catch operator is that onCompletion sees
    all exceptions and receives a null exception only on successful completion of
    the upstream flow (without cancellation or failure).
  quote_hash: sha256:c1bdccd390fe4c450bc1ca4090123877be45918655cc961bbb8ef7eb384aae69
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# kotlin-flow-exception-transparency

## Failure Class
kotlin/flow

## Symptoms
- Flow throws Flow exception transparency violation because an exception was emitted from an unexpected place

## Fingerprints
- Flow exception transparency violation
- Flow invariant is violated
- emission happened in
- flowOn instead
- catch operator

## First Checks
- Check whether the exception originated inside the flow { } builder vs upstream operators
- Check whether catch only catches upstream exceptions (it does not catch downstream collect failures)
- Check whether flowOn was used instead of withContext to change the execution context

## Do Not Patch Yet
- Do not use withContext inside a flow { } builder; use flowOn instead
- Do not catch exceptions in collect {} and expect the flow to continue; use catch operator before collect

## Evidence Needed
- Capture the Flow exception transparency violation stack trace
- Identify which flow operator or collect site threw the exception

## Minimal Fix Scope
- The flow { } builder block or the operator chain
- The catch operator placement relative to upstream and downstream failures

## Validation Ladder
- Reproduce the exception with the failing flow emission
- Move the catch operator upstream and verify the exception is handled
- Run the flow test covering the failure path

## Regression Guard
- Add a flow test asserting the catch operator handles the specific error type

## Reviewer Notes
