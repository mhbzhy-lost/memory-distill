- [kotlin-flow-exception-handling-1] https://github.com/Kotlin/kotlinx.coroutines/edit/master/docs/topics/

- [kotlin-flow-exception-handling-2] A suspending function asynchronously returns a single value, but how can we return multiple asynchronously computed values? This is where Kotlin Flows come in.

- [kotlin-flow-exception-handling-3] Representing multiple values

- [kotlin-flow-exception-handling-4] Multiple values can be represented in Kotlin using collections . For example, we can have a simple function that returns a List of three numbers and then print them all using forEach :

- [kotlin-flow-exception-handling-5] fun simple(): List<Int> = listOf(1, 2, 3) fun main() { simple().forEach { value -> println(value) } }

- [kotlin-flow-exception-handling-6] {kotlin-runnable="true" kotlin-min-compiler-version="1.3"}

- [kotlin-flow-exception-handling-7] You can get the full code here .

- [kotlin-flow-exception-handling-8] {style="note"}

- [kotlin-flow-exception-handling-9] This code outputs:

- [kotlin-flow-exception-handling-10] 1 2 3

- [kotlin-flow-exception-handling-11] Sequences

- [kotlin-flow-exception-handling-12] If we are computing the numbers with some CPU-consuming blocking code (each computation taking 100ms), then we can represent the numbers using a Sequence :

- [kotlin-flow-exception-handling-13] fun simple(): Sequence<Int> = sequence { // sequence builder for (i in 1..3) { Thread.sleep(100) // pretend we are computing it yield(i) // yield next value } } fun main() { simple().forEach { value -> println(value) } }

- [kotlin-flow-exception-handling-14] This code outputs the same numbers, but it waits 100ms before printing each one.

- [kotlin-flow-exception-handling-15] Suspending functions

- [kotlin-flow-exception-handling-16] However, this computation blocks the main thread that is running the code. When these values are computed by asynchronous code we can mark the simple function with a suspend modifier, so that it can perform its work without blocking and return the result as a list:

- [kotlin-flow-exception-handling-17] import kotlinx.coroutines.* //sampleStart suspend fun simple(): List<Int> { delay(1000) // pretend we are doing something asynchronous here return listOf(1, 2, 3) } fun main() = runBlocking<Unit> { simple().forEach { value -> println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-18] This code prints the numbers after waiting for a second.

- [kotlin-flow-exception-handling-19] Flows

- [kotlin-flow-exception-handling-20] Using the List<Int> result type, means we can only return all the values at once. To represent the stream of values that are being computed asynchronously, we can use a Flow<Int> type just like we would use a Sequence<Int> type for synchronously computed values:

- [kotlin-flow-exception-handling-21] Flow<Int>

- [kotlin-flow-exception-handling-22] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<Int> = flow { // flow builder for (i in 1..3) { delay(100) // pretend we are doing something useful here emit(i) // emit next value } } fun main() = runBlocking<Unit> { // Launch a concurrent coroutine to check if the main thread is blocked launch { for (k in 1..3) { println("I'm not blocked $k") delay(100) } } // Collect the flow simple().collect { value -> println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-23] This code waits 100ms before printing each number without blocking the main thread. This is verified by printing "I'm not blocked" every 100ms from a separate coroutine that is running in the main thread:

- [kotlin-flow-exception-handling-24] I'm not blocked 1 1 I'm not blocked 2 2 I'm not blocked 3 3

- [kotlin-flow-exception-handling-25] Notice the following differences in the code with the Flow from the earlier examples:

- [kotlin-flow-exception-handling-26] A builder function of Flow type is called flow .

- [kotlin-flow-exception-handling-27] Code inside a flow { ... } builder block can suspend.

- [kotlin-flow-exception-handling-28] The simple function is no longer marked with a suspend modifier.

- [kotlin-flow-exception-handling-29] Values are emitted from the flow using an emit function.

- [kotlin-flow-exception-handling-30] Values are collected from the flow using a collect function.

- [kotlin-flow-exception-handling-31] We can replace delay with Thread.sleep in the body of simple 's flow { ... } and see that the main thread is blocked in this case.

- [kotlin-flow-exception-handling-32] Flows are cold

- [kotlin-flow-exception-handling-33] Flows are cold streams similar to sequences — the code inside a flow builder does not run until the flow is collected. This becomes clear in the following example:

- [kotlin-flow-exception-handling-34] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<Int> = flow { println("Flow started") for (i in 1..3) { delay(100) emit(i) } } fun main() = runBlocking<Unit> { println("Calling simple function...") val flow = simple() println("Calling collect...") flow.collect { value -> println(value) } println("Calling collect again...") flow.collect { value -> println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-35] Which prints:

- [kotlin-flow-exception-handling-36] Calling simple function... Calling collect... Flow started 1 2 3 Calling collect again... Flow started 1 2 3

- [kotlin-flow-exception-handling-37] This is a key reason the simple function (which returns a flow) is not marked with suspend modifier. The simple() call itself returns quickly and does not wait for anything. The flow starts afresh every time it is collected and that is why we see "Flow started" every time we call collect again.

- [kotlin-flow-exception-handling-38] Flow cancellation basics

- [kotlin-flow-exception-handling-39] Flows adhere to the general cooperative cancellation of coroutines. As usual, flow collection can be cancelled when the flow is suspended in a cancellable suspending function (like delay ). The following example shows how the flow gets cancelled on a timeout when running in a withTimeoutOrNull block and stops executing its code:

- [kotlin-flow-exception-handling-40] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<Int> = flow { for (i in 1..3) { delay(100) println("Emitting $i") emit(i) } } fun main() = runBlocking<Unit> { withTimeoutOrNull(250) { // Timeout after 250ms simple().collect { value -> println(value) } } println("Done") } //sampleEnd

- [kotlin-flow-exception-handling-41] Notice how only two numbers get emitted by the flow in the simple function, producing the following output:

- [kotlin-flow-exception-handling-42] Emitting 1 1 Emitting 2 2 Done

- [kotlin-flow-exception-handling-43] See Flow cancellation checks section for more details.

- [kotlin-flow-exception-handling-44] Flow builders

- [kotlin-flow-exception-handling-45] The flow { ... } builder from the previous examples is the most basic one. There are other builders that allow flows to be declared:

- [kotlin-flow-exception-handling-46] The flowOf builder defines a flow that emits a fixed set of values.

- [kotlin-flow-exception-handling-47] Various collections and sequences can be converted to flows using the .asFlow() extension function.

- [kotlin-flow-exception-handling-48] For example, the snippet that prints the numbers 1 to 3 from a flow can be rewritten as follows:

- [kotlin-flow-exception-handling-49] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun main() = runBlocking<Unit> { //sampleStart // Convert an integer range to a flow (1..3).asFlow().collect { value -> println(value) } //sampleEnd }

- [kotlin-flow-exception-handling-50] Intermediate flow operators

- [kotlin-flow-exception-handling-51] Flows can be transformed using operators, in the same way as you would transform collections and sequences. Intermediate operators are applied to an upstream flow and return a downstream flow. These operators are cold, just like flows are. A call to such an operator is not a suspending function itself. It works quickly, returning the definition of a new transformed flow.

- [kotlin-flow-exception-handling-52] The basic operators have familiar names like map and filter . An important difference of these operators from sequences is that blocks of code inside these operators can call suspending functions.

- [kotlin-flow-exception-handling-53] For example, a flow of incoming requests can be mapped to its results with a map operator, even when performing a request is a long-running operation that is implemented by a suspending function:

- [kotlin-flow-exception-handling-54] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart suspend fun performRequest(request: Int): String { delay(1000) // imitate long-running asynchronous work return "response $request" } fun main() = runBlocking<Unit> { (1..3).asFlow() // a flow of requests .map { request -> performRequest(request) } .collect { response -> println(response) } } //sampleEnd

- [kotlin-flow-exception-handling-55] It produces the following three lines, each appearing one second after the previous:

- [kotlin-flow-exception-handling-56] response 1 response 2 response 3

- [kotlin-flow-exception-handling-57] Transform operator

- [kotlin-flow-exception-handling-58] Among the flow transformation operators, the most general one is called transform . It can be used to imitate simple transformations like map and filter , as well as implement more complex transformations. Using the transform operator, we can emit arbitrary values an arbitrary number of times.

- [kotlin-flow-exception-handling-59] For example, using transform we can emit a string before performing a long-running asynchronous request and follow it with a response:

- [kotlin-flow-exception-handling-60] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* suspend fun performRequest(request: Int): String { delay(1000) // imitate long-running asynchronous work return "response $request" } fun main() = runBlocking<Unit> { //sampleStart (1..3).asFlow() // a flow of requests .transform { request -> emit("Making request $request") emit(performRequest(request)) } .collect { response -> println(response) } //sampleEnd }

- [kotlin-flow-exception-handling-61] The output of this code is:

- [kotlin-flow-exception-handling-62] Making request 1 response 1 Making request 2 response 2 Making request 3 response 3

- [kotlin-flow-exception-handling-63] Size-limiting operators

- [kotlin-flow-exception-handling-64] Size-limiting intermediate operators like take cancel the execution of the flow when the corresponding limit is reached. Cancellation in coroutines is always performed by throwing an exception, so that all the resource-management functions (like try { ... } finally { ... } blocks) operate normally in case of cancellation:

- [kotlin-flow-exception-handling-65] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun numbers(): Flow<Int> = flow { try { emit(1) emit(2) println("This line will not execute") emit(3) } finally { println("Finally in numbers") } } fun main() = runBlocking<Unit> { numbers() .take(2) // take only the first two .collect { value -> println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-66] The output of this code clearly shows that the execution of the flow { ... } body in the numbers() function stopped after emitting the second number:

- [kotlin-flow-exception-handling-67] 1 2 Finally in numbers

- [kotlin-flow-exception-handling-68] Terminal flow operators

- [kotlin-flow-exception-handling-69] Terminal operators on flows are suspending functions that start a collection of the flow. The collect operator is the most basic one, but there are other terminal operators, which can make it easier:

- [kotlin-flow-exception-handling-70] Conversion to various collections like toList and toSet .

- [kotlin-flow-exception-handling-71] Operators to get the first value and to ensure that a flow emits a single value.

- [kotlin-flow-exception-handling-72] Reducing a flow to a value with reduce and fold .

- [kotlin-flow-exception-handling-73] For example:

- [kotlin-flow-exception-handling-74] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun main() = runBlocking<Unit> { //sampleStart val sum = (1..5).asFlow() .map { it * it } // squares of numbers from 1 to 5 .reduce { a, b -> a + b } // sum them (terminal operator) println(sum) //sampleEnd }

- [kotlin-flow-exception-handling-75] Prints a single number:

- [kotlin-flow-exception-handling-76] 55

- [kotlin-flow-exception-handling-77] Flows are sequential

- [kotlin-flow-exception-handling-78] Each individual collection of a flow is performed sequentially unless special operators that operate on multiple flows are used. The collection works directly in the coroutine that calls a terminal operator. No new coroutines are launched by default. Each emitted value is processed by all the intermediate operators from upstream to downstream and is then delivered to the terminal operator after.

- [kotlin-flow-exception-handling-79] See the following example that filters the even integers and maps them to strings:

- [kotlin-flow-exception-handling-80] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun main() = runBlocking<Unit> { //sampleStart (1..5).asFlow() .filter { println("Filter $it") it % 2 == 0 } .map { println("Map $it") "string $it" }.collect { println("Collect $it") } //sampleEnd }

- [kotlin-flow-exception-handling-81] Producing:

- [kotlin-flow-exception-handling-82] Filter 1 Filter 2 Map 2 Collect string 2 Filter 3 Filter 4 Map 4 Collect string 4 Filter 5

- [kotlin-flow-exception-handling-83] Flow context

- [kotlin-flow-exception-handling-84] Collection of a flow always happens in the context of the calling coroutine. For example, if there is a simple flow, then the following code runs in the context specified by the author of this code, regardless of the implementation details of the simple flow:

- [kotlin-flow-exception-handling-85] withContext(context) { simple().collect { value -> println(value) // run in the specified context } }

- [kotlin-flow-exception-handling-86] This property of a flow is called context preservation .

- [kotlin-flow-exception-handling-87] So, by default, code in the flow { ... } builder runs in the context that is provided by a collector of the corresponding flow. For example, consider the implementation of a simple function that prints the thread it is called on and emits three numbers:

- [kotlin-flow-exception-handling-88] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun log(msg: String) = println("[${Thread.currentThread().name}] $msg") //sampleStart fun simple(): Flow<Int> = flow { log("Started simple flow") for (i in 1..3) { emit(i) } } fun main() = runBlocking<Unit> { simple().collect { value -> log("Collected $value") } } //sampleEnd

- [kotlin-flow-exception-handling-89] Running this code produces:

- [kotlin-flow-exception-handling-90] [main @coroutine#1] Started simple flow [main @coroutine#1] Collected 1 [main @coroutine#1] Collected 2 [main @coroutine#1] Collected 3

- [kotlin-flow-exception-handling-91] Since simple().collect is called from the main thread, the body of simple 's flow is also called in the main thread. This is the perfect default for fast-running or asynchronous code that does not care about the execution context and does not block the caller.

- [kotlin-flow-exception-handling-92] A common pitfall when using withContext

- [kotlin-flow-exception-handling-93] However, the long-running CPU-consuming code might need to be executed in the context of Dispatchers.Default and UI-updating code might need to be executed in the context of Dispatchers.Main . Usually, withContext is used to change the context in the code using Kotlin coroutines, but code in the flow { ... } builder has to honor the context preservation property and is not allowed to emit from a different context.

- [kotlin-flow-exception-handling-94] Try running the following code:

- [kotlin-flow-exception-handling-95] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<Int> = flow { // The WRONG way to change context for CPU-consuming code in flow builder kotlinx.coroutines.withContext(Dispatchers.Default) { for (i in 1..3) { Thread.sleep(100) // pretend we are computing it in CPU-consuming way emit(i) // emit next value } } } fun main() = runBlocking<Unit> { simple().collect { value -> println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-96] This code produces the following exception:

- [kotlin-flow-exception-handling-97] Exception in thread "main" java.lang.IllegalStateException: Flow invariant is violated: Flow was collected in [CoroutineId(1), "coroutine#1":BlockingCoroutine{Active}@5511c7f8, BlockingEventLoop@2eac3323], but emission happened in [CoroutineId(1), "coroutine#1":DispatchedCoroutine{Active}@2dae0000, Dispatchers.Default]. Please refer to 'flow' documentation or use 'flowOn' instead at ...

- [kotlin-flow-exception-handling-98] flowOn operator

- [kotlin-flow-exception-handling-99] The exception refers to the flowOn function that shall be used to change the context of the flow emission. The correct way to change the context of a flow is shown in the example below, which also prints the names of the corresponding threads to show how it all works:

- [kotlin-flow-exception-handling-100] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun log(msg: String) = println("[${Thread.currentThread().name}] $msg") //sampleStart fun simple(): Flow<Int> = flow { for (i in 1..3) { Thread.sleep(100) // pretend we are computing it in CPU-consuming way log("Emitting $i") emit(i) // emit next value } }.flowOn(Dispatchers.Default) // RIGHT way to change context for CPU-consuming code in flow builder fun main() = runBlocking<Unit> { simple().collect { value -> log("Collected $value") } } //sampleEnd

- [kotlin-flow-exception-handling-101] Notice how flow { ... } works in the background thread, while collection happens in the main thread:

- [kotlin-flow-exception-handling-102] [DefaultDispatcher-worker-1 @coroutine#2] Emitting 1 [main @coroutine#1] Collected 1 [DefaultDispatcher-worker-1 @coroutine#2] Emitting 2 [main @coroutine#1] Collected 2 [DefaultDispatcher-worker-1 @coroutine#2] Emitting 3 [main @coroutine#1] Collected 3

- [kotlin-flow-exception-handling-103] Another thing to observe here is that the flowOn operator has changed the default sequential nature of the flow. Now collection happens in one coroutine ("coroutine#1") and emission happens in another coroutine ("coroutine#2") that is running in another thread concurrently with the collecting coroutine. The flowOn operator creates another coroutine for an upstream flow when it has to change the CoroutineDispatcher in its context.

- [kotlin-flow-exception-handling-104] Buffering

- [kotlin-flow-exception-handling-105] Running different parts of a flow in different coroutines can be helpful from the standpoint of the overall time it takes to collect the flow, especially when long-running asynchronous operations are involved. For example, consider a case when the emission by a simple flow is slow, taking 100 ms to produce an element; and collector is also slow, taking 300 ms to process an element. Let's see how long it takes to collect such a flow with three numbers:

- [kotlin-flow-exception-handling-106] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* import kotlin.system.* //sampleStart fun simple(): Flow<Int> = flow { for (i in 1..3) { delay(100) // pretend we are asynchronously waiting 100 ms emit(i) // emit next value } } fun main() = runBlocking<Unit> { val time = measureTimeMillis { simple().collect { value -> delay(300) // pretend we are processing it for 300 ms println(value) } } println("Collected in $time ms") } //sampleEnd

- [kotlin-flow-exception-handling-107] It produces something like this, with the whole collection taking around 1200 ms (three numbers, 400 ms for each):

- [kotlin-flow-exception-handling-108] 1 2 3 Collected in 1220 ms

- [kotlin-flow-exception-handling-109] We can use a buffer operator on a flow to run emitting code of the simple flow concurrently with collecting code, as opposed to running them sequentially:

- [kotlin-flow-exception-handling-110] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* import kotlin.system.* fun simple(): Flow<Int> = flow { for (i in 1..3) { delay(100) // pretend we are asynchronously waiting 100 ms emit(i) // emit next value } } fun main() = runBlocking<Unit> { //sampleStart val time = measureTimeMillis { simple() .buffer() // buffer emissions, don't wait .collect { value -> delay(300) // pretend we are processing it for 300 ms println(value) } } println("Collected in $time ms") //sampleEnd }

- [kotlin-flow-exception-handling-111] It produces the same numbers just faster, as we have effectively created a processing pipeline, having to only wait 100 ms for the first number and then spending only 300 ms to process each number. This way it takes around 1000 ms to run:

- [kotlin-flow-exception-handling-112] 1 2 3 Collected in 1071 ms

- [kotlin-flow-exception-handling-113] Note that the flowOn operator uses the same buffering mechanism when it has to change a CoroutineDispatcher , but here we explicitly request buffering without changing the execution context.

- [kotlin-flow-exception-handling-114] Conflation

- [kotlin-flow-exception-handling-115] When a flow represents partial results of the operation or operation status updates, it may not be necessary to process each value, but instead, only most recent ones. In this case, the conflate operator can be used to skip intermediate values when a collector is too slow to process them. Building on the previous example:

- [kotlin-flow-exception-handling-116] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* import kotlin.system.* fun simple(): Flow<Int> = flow { for (i in 1..3) { delay(100) // pretend we are asynchronously waiting 100 ms emit(i) // emit next value } } fun main() = runBlocking<Unit> { //sampleStart val time = measureTimeMillis { simple() .conflate() // conflate emissions, don't process each one .collect { value -> delay(300) // pretend we are processing it for 300 ms println(value) } } println("Collected in $time ms") //sampleEnd }

- [kotlin-flow-exception-handling-117] We see that while the first number was still being processed the second, and third were already produced, so the second one was conflated and only the most recent (the third one) was delivered to the collector:

- [kotlin-flow-exception-handling-118] 1 3 Collected in 758 ms

- [kotlin-flow-exception-handling-119] Processing the latest value

- [kotlin-flow-exception-handling-120] Conflation is one way to speed up processing when both the emitter and collector are slow. It does it by dropping emitted values. The other way is to cancel a slow collector and restart it every time a new value is emitted. There is a family of xxxLatest operators that perform the same essential logic of a xxx operator, but cancel the code in their block on a new value. Let's try changing conflate to collectLatest in the previous example:

- [kotlin-flow-exception-handling-121] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* import kotlin.system.* fun simple(): Flow<Int> = flow { for (i in 1..3) { delay(100) // pretend we are asynchronously waiting 100 ms emit(i) // emit next value } } fun main() = runBlocking<Unit> { //sampleStart val time = measureTimeMillis { simple() .collectLatest { value -> // cancel & restart on the latest value println("Collecting $value") delay(300) // pretend we are processing it for 300 ms println("Done $value") } } println("Collected in $time ms") //sampleEnd }

- [kotlin-flow-exception-handling-122] Since the body of collectLatest takes 300 ms, but new values are emitted every 100 ms, we see that the block is run on every value, but completes only for the last value:

- [kotlin-flow-exception-handling-123] Collecting 1 Collecting 2 Collecting 3 Done 3 Collected in 741 ms

- [kotlin-flow-exception-handling-124] Composing multiple flows

- [kotlin-flow-exception-handling-125] There are lots of ways to compose multiple flows.

- [kotlin-flow-exception-handling-126] Zip

- [kotlin-flow-exception-handling-127] Just like the Sequence.zip extension function in the Kotlin standard library, flows have a zip operator that combines the corresponding values of two flows:

- [kotlin-flow-exception-handling-128] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun main() = runBlocking<Unit> { //sampleStart val nums = (1..3).asFlow() // numbers 1..3 val strs = flowOf("one", "two", "three") // strings nums.zip(strs) { a, b -> "$a -> $b" } // compose a single string .collect { println(it) } // collect and print //sampleEnd }

- [kotlin-flow-exception-handling-129] This example prints:

- [kotlin-flow-exception-handling-130] 1 -> one 2 -> two 3 -> three

- [kotlin-flow-exception-handling-131] Combine

- [kotlin-flow-exception-handling-132] When flow represents the most recent value of a variable or operation (see also the related section on conflation ), it might be needed to perform a computation that depends on the most recent values of the corresponding flows and to recompute it whenever any of the upstream flows emit a value. The corresponding family of operators is called combine .

- [kotlin-flow-exception-handling-133] For example, if the numbers in the previous example update every 300ms, but strings update every 400 ms, then zipping them using the zip operator will still produce the same result, albeit results that are printed every 400 ms:

- [kotlin-flow-exception-handling-134] We use a onEach intermediate operator in this example to delay each element and make the code that emits sample flows more declarative and shorter.

- [kotlin-flow-exception-handling-135] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun main() = runBlocking<Unit> { //sampleStart val nums = (1..3).asFlow().onEach { delay(300) } // numbers 1..3 every 300 ms val strs = flowOf("one", "two", "three").onEach { delay(400) } // strings every 400 ms val startTime = System.currentTimeMillis() // remember the start time nums.zip(strs) { a, b -> "$a -> $b" } // compose a single string with "zip" .collect { value -> // collect and print println("$value at ${System.currentTimeMillis() - startTime} ms from start") } //sampleEnd }

- [kotlin-flow-exception-handling-136] However, when using a combine operator here instead of a zip :

- [kotlin-flow-exception-handling-137] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun main() = runBlocking<Unit> { //sampleStart val nums = (1..3).asFlow().onEach { delay(300) } // numbers 1..3 every 300 ms val strs = flowOf("one", "two", "three").onEach { delay(400) } // strings every 400 ms val startTime = System.currentTimeMillis() // remember the start time nums.combine(strs) { a, b -> "$a -> $b" } // compose a single string with "combine" .collect { value -> // collect and print println("$value at ${System.currentTimeMillis() - startTime} ms from start") } //sampleEnd }

- [kotlin-flow-exception-handling-138] We get quite a different output, where a line is printed at each emission from either nums or strs flows:

- [kotlin-flow-exception-handling-139] 1 -> one at 452 ms from start 2 -> one at 651 ms from start 2 -> two at 854 ms from start 3 -> two at 952 ms from start 3 -> three at 1256 ms from start

- [kotlin-flow-exception-handling-140] Flattening flows

- [kotlin-flow-exception-handling-141] Flows represent asynchronously received sequences of values, and so it is quite easy to get into a situation where each value triggers a request for another sequence of values. For example, we can have the following function that returns a flow of two strings 500 ms apart:

- [kotlin-flow-exception-handling-142] fun requestFlow(i: Int): Flow<String> = flow { emit("$i: First") delay(500) // wait 500 ms emit("$i: Second") }

- [kotlin-flow-exception-handling-143] Now if we have a flow of three integers and call requestFlow on each of them like this:

- [kotlin-flow-exception-handling-144] (1..3).asFlow().map { requestFlow(it) }

- [kotlin-flow-exception-handling-145] Then we will end up with a flow of flows ( Flow<Flow<String>> ) that needs to be flattened into a single flow for further processing. Collections and sequences have flatten and flatMap operators for this. However, due to the asynchronous nature of flows they call for different modes of flattening, and hence, a family of flattening operators on flows exists.

- [kotlin-flow-exception-handling-146] flatMapConcat

- [kotlin-flow-exception-handling-147] Concatenation of flows of flows is provided by the flatMapConcat and flattenConcat operators. They are the most direct analogues of the corresponding sequence operators. They wait for the inner flow to complete before starting to collect the next one as the following example shows:

- [kotlin-flow-exception-handling-148] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun requestFlow(i: Int): Flow<String> = flow { emit("$i: First") delay(500) // wait 500 ms emit("$i: Second") } fun main() = runBlocking<Unit> { //sampleStart val startTime = System.currentTimeMillis() // remember the start time (1..3).asFlow().onEach { delay(100) } // emit a number every 100 ms .flatMapConcat { requestFlow(it) } .collect { value -> // collect and print println("$value at ${System.currentTimeMillis() - startTime} ms from start") } //sampleEnd }

- [kotlin-flow-exception-handling-149] The sequential nature of flatMapConcat is clearly seen in the output:

- [kotlin-flow-exception-handling-150] 1: First at 121 ms from start 1: Second at 622 ms from start 2: First at 727 ms from start 2: Second at 1227 ms from start 3: First at 1328 ms from start 3: Second at 1829 ms from start

- [kotlin-flow-exception-handling-151] flatMapMerge

- [kotlin-flow-exception-handling-152] Another flattening operation is to concurrently collect all the incoming flows and merge their values into a single flow so that values are emitted as soon as possible. It is implemented by flatMapMerge and flattenMerge operators. They both accept an optional concurrency parameter that limits the number of concurrent flows that are collected at the same time (it is equal to DEFAULT_CONCURRENCY by default).

- [kotlin-flow-exception-handling-153] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun requestFlow(i: Int): Flow<String> = flow { emit("$i: First") delay(500) // wait 500 ms emit("$i: Second") } fun main() = runBlocking<Unit> { //sampleStart val startTime = System.currentTimeMillis() // remember the start time (1..3).asFlow().onEach { delay(100) } // a number every 100 ms .flatMapMerge { requestFlow(it) } .collect { value -> // collect and print println("$value at ${System.currentTimeMillis() - startTime} ms from start") } //sampleEnd }

- [kotlin-flow-exception-handling-154] The concurrent nature of flatMapMerge is obvious:

- [kotlin-flow-exception-handling-155] 1: First at 136 ms from start 2: First at 231 ms from start 3: First at 333 ms from start 1: Second at 639 ms from start 2: Second at 732 ms from start 3: Second at 833 ms from start

- [kotlin-flow-exception-handling-156] Note that the flatMapMerge calls its block of code ( { requestFlow(it) } in this example) sequentially, but collects the resulting flows concurrently, it is the equivalent of performing a sequential map { requestFlow(it) } first and then calling flattenMerge on the result.

- [kotlin-flow-exception-handling-157] flatMapLatest

- [kotlin-flow-exception-handling-158] In a similar way to the collectLatest operator, that was described in the section "Processing the latest value" , there is the corresponding "Latest" flattening mode where the collection of the previous flow is cancelled as soon as new flow is emitted. It is implemented by the flatMapLatest operator.

- [kotlin-flow-exception-handling-159] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun requestFlow(i: Int): Flow<String> = flow { emit("$i: First") delay(500) // wait 500 ms emit("$i: Second") } fun main() = runBlocking<Unit> { //sampleStart val startTime = System.currentTimeMillis() // remember the start time (1..3).asFlow().onEach { delay(100) } // a number every 100 ms .flatMapLatest { requestFlow(it) } .collect { value -> // collect and print println("$value at ${System.currentTimeMillis() - startTime} ms from start") } //sampleEnd }

- [kotlin-flow-exception-handling-160] The output here in this example is a good demonstration of how flatMapLatest works:

- [kotlin-flow-exception-handling-161] 1: First at 142 ms from start 2: First at 322 ms from start 3: First at 425 ms from start 3: Second at 931 ms from start

- [kotlin-flow-exception-handling-162] Note that flatMapLatest cancels all the code in its block ( { requestFlow(it) } in this example) when a new value is received. It makes no difference in this particular example, because the call to requestFlow itself is fast, not-suspending, and cannot be cancelled. However, a differnce in output would be visible if we were to use suspending functions like delay in requestFlow .

- [kotlin-flow-exception-handling-163] Flow exceptions

- [kotlin-flow-exception-handling-164] Flow collection can complete with an exception when an emitter or code inside the operators throw an exception. There are several ways to handle these exceptions.

- [kotlin-flow-exception-handling-165] Collector try and catch

- [kotlin-flow-exception-handling-166] A collector can use Kotlin's try/catch block to handle exceptions:

- [kotlin-flow-exception-handling-167] try/catch

- [kotlin-flow-exception-handling-168] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<Int> = flow { for (i in 1..3) { println("Emitting $i") emit(i) // emit next value } } fun main() = runBlocking<Unit> { try { simple().collect { value -> println(value) check(value <= 1) { "Collected $value" } } } catch (e: Throwable) { println("Caught $e") } } //sampleEnd

- [kotlin-flow-exception-handling-169] This code successfully catches an exception in collect terminal operator and, as we see, no more values are emitted after that:

- [kotlin-flow-exception-handling-170] Emitting 1 1 Emitting 2 2 Caught java.lang.IllegalStateException: Collected 2

- [kotlin-flow-exception-handling-171] Everything is caught

- [kotlin-flow-exception-handling-172] The previous example actually catches any exception happening in the emitter or in any intermediate or terminal operators. For example, let's change the code so that emitted values are mapped to strings, but the corresponding code produces an exception:

- [kotlin-flow-exception-handling-173] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<String> = flow { for (i in 1..3) { println("Emitting $i") emit(i) // emit next value } } .map { value -> check(value <= 1) { "Crashed on $value" } "string $value" } fun main() = runBlocking<Unit> { try { simple().collect { value -> println(value) } } catch (e: Throwable) { println("Caught $e") } } //sampleEnd

- [kotlin-flow-exception-handling-174] This exception is still caught and collection is stopped:

- [kotlin-flow-exception-handling-175] Emitting 1 string 1 Emitting 2 Caught java.lang.IllegalStateException: Crashed on 2

- [kotlin-flow-exception-handling-176] Exception transparency

- [kotlin-flow-exception-handling-177] But how can code of the emitter encapsulate its exception handling behavior?

- [kotlin-flow-exception-handling-178] Flows must be transparent to exceptions and it is a violation of the exception transparency to emit values in the flow { ... } builder from inside of a try/catch block. This guarantees that a collector throwing an exception can always catch it using try/catch as in the previous example.

- [kotlin-flow-exception-handling-179] The emitter can use a catch operator that preserves this exception transparency and allows encapsulation of its exception handling. The body of the catch operator can analyze an exception and react to it in different ways depending on which exception was caught:

- [kotlin-flow-exception-handling-180] Exceptions can be rethrown using throw .

- [kotlin-flow-exception-handling-181] Exceptions can be turned into emission of values using emit from the body of catch .

- [kotlin-flow-exception-handling-182] Exceptions can be ignored, logged, or processed by some other code.

- [kotlin-flow-exception-handling-183] For example, let us emit the text on catching an exception:

- [kotlin-flow-exception-handling-184] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun simple(): Flow<String> = flow { for (i in 1..3) { println("Emitting $i") emit(i) // emit next value } } .map { value -> check(value <= 1) { "Crashed on $value" } "string $value" } fun main() = runBlocking<Unit> { //sampleStart simple() .catch { e -> emit("Caught $e") } // emit on exception .collect { value -> println(value) } //sampleEnd }

- [kotlin-flow-exception-handling-185] The output of the example is the same, even though we do not have try/catch around the code anymore.

- [kotlin-flow-exception-handling-186] Transparent catch

- [kotlin-flow-exception-handling-187] The catch intermediate operator, honoring exception transparency, catches only upstream exceptions (that is an exception from all the operators above catch , but not below it). If the block in collect { ... } (placed below catch ) throws an exception then it escapes:

- [kotlin-flow-exception-handling-188] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<Int> = flow { for (i in 1..3) { println("Emitting $i") emit(i) } } fun main() = runBlocking<Unit> { simple() .catch { e -> println("Caught $e") } // does not catch downstream exceptions .collect { value -> check(value <= 1) { "Collected $value" } println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-189] A "Caught ..." message is not printed despite there being a catch operator:

- [kotlin-flow-exception-handling-190] Emitting 1 1 Emitting 2 Exception in thread "main" java.lang.IllegalStateException: Collected 2 at ...

- [kotlin-flow-exception-handling-191] Catching declaratively

- [kotlin-flow-exception-handling-192] We can combine the declarative nature of the catch operator with a desire to handle all the exceptions, by moving the body of the collect operator into onEach and putting it before the catch operator. Collection of this flow must be triggered by a call to collect() without parameters:

- [kotlin-flow-exception-handling-193] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun simple(): Flow<Int> = flow { for (i in 1..3) { println("Emitting $i") emit(i) } } fun main() = runBlocking<Unit> { //sampleStart simple() .onEach { value -> check(value <= 1) { "Collected $value" } println(value) } .catch { e -> println("Caught $e") } .collect() //sampleEnd }

- [kotlin-flow-exception-handling-194] Now we can see that a "Caught ..." message is printed and so we can catch all the exceptions without explicitly using a try/catch block:

- [kotlin-flow-exception-handling-195] Emitting 1 1 Emitting 2 Caught java.lang.IllegalStateException: Collected 2

- [kotlin-flow-exception-handling-196] Flow completion

- [kotlin-flow-exception-handling-197] When flow collection completes (normally or exceptionally) it may need to execute an action. As you may have already noticed, it can be done in two ways: imperative or declarative.

- [kotlin-flow-exception-handling-198] Imperative finally block

- [kotlin-flow-exception-handling-199] In addition to try / catch , a collector can also use a finally block to execute an action upon collect completion.

- [kotlin-flow-exception-handling-200] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<Int> = (1..3).asFlow() fun main() = runBlocking<Unit> { try { simple().collect { value -> println(value) } } finally { println("Done") } } //sampleEnd

- [kotlin-flow-exception-handling-201] This code prints three numbers produced by the simple flow followed by a "Done" string:

- [kotlin-flow-exception-handling-202] 1 2 3 Done

- [kotlin-flow-exception-handling-203] Declarative handling

- [kotlin-flow-exception-handling-204] For the declarative approach, flow has onCompletion intermediate operator that is invoked when the flow has completely collected.

- [kotlin-flow-exception-handling-205] The previous example can be rewritten using an onCompletion operator and produces the same output:

- [kotlin-flow-exception-handling-206] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* fun simple(): Flow<Int> = (1..3).asFlow() fun main() = runBlocking<Unit> { //sampleStart simple() .onCompletion { println("Done") } .collect { value -> println(value) } //sampleEnd }

- [kotlin-flow-exception-handling-207] The key advantage of onCompletion is a nullable Throwable parameter of the lambda that can be used to determine whether the flow collection was completed normally or exceptionally. In the following example the simple flow throws an exception after emitting the number 1:

- [kotlin-flow-exception-handling-208] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<Int> = flow { emit(1) throw RuntimeException() } fun main() = runBlocking<Unit> { simple() .onCompletion { cause -> if (cause != null) println("Flow completed exceptionally") } .catch { cause -> println("Caught exception") } .collect { value -> println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-209] As you may expect, it prints:

- [kotlin-flow-exception-handling-210] 1 Flow completed exceptionally Caught exception

- [kotlin-flow-exception-handling-211] The onCompletion operator, unlike catch , does not handle the exception. As we can see from the above example code, the exception still flows downstream. It will be delivered to further onCompletion operators and can be handled with a catch operator.

- [kotlin-flow-exception-handling-212] Successful completion

- [kotlin-flow-exception-handling-213] Another difference with catch operator is that onCompletion sees all exceptions and receives a null exception only on successful completion of the upstream flow (without cancellation or failure).

- [kotlin-flow-exception-handling-214] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun simple(): Flow<Int> = (1..3).asFlow() fun main() = runBlocking<Unit> { simple() .onCompletion { cause -> println("Flow completed with $cause") } .collect { value -> check(value <= 1) { "Collected $value" } println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-215] We can see the completion cause is not null, because the flow was aborted due to downstream exception:

- [kotlin-flow-exception-handling-216] 1 Flow completed with java.lang.IllegalStateException: Collected 2 Exception in thread "main" java.lang.IllegalStateException: Collected 2

- [kotlin-flow-exception-handling-217] Imperative versus declarative

- [kotlin-flow-exception-handling-218] Now we know how to collect flow, and handle its completion and exceptions in both imperative and declarative ways. The natural question here is, which approach is preferred and why? As a library, we do not advocate for any particular approach and believe that both options are valid and should be selected according to your own preferences and code style.

- [kotlin-flow-exception-handling-219] Launching flow

- [kotlin-flow-exception-handling-220] It is easy to use flows to represent asynchronous events that are coming from some source. In this case, we need an analogue of the addEventListener function that registers a piece of code with a reaction for incoming events and continues further work. The onEach operator can serve this role. However, onEach is an intermediate operator. We also need a terminal operator to collect the flow. Otherwise, just calling onEach has no effect.

- [kotlin-flow-exception-handling-221] If we use the collect terminal operator after onEach , then the code after it will wait until the flow is collected:

- [kotlin-flow-exception-handling-222] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart // Imitate a flow of events fun events(): Flow<Int> = (1..3).asFlow().onEach { delay(100) } fun main() = runBlocking<Unit> { events() .onEach { event -> println("Event: $event") } .collect() // <--- Collecting the flow waits println("Done") } //sampleEnd

- [kotlin-flow-exception-handling-223] As you can see, it prints:

- [kotlin-flow-exception-handling-224] Event: 1 Event: 2 Event: 3 Done

- [kotlin-flow-exception-handling-225] The launchIn terminal operator comes in handy here. By replacing collect with launchIn we can launch a collection of the flow in a separate coroutine, so that execution of further code immediately continues:

- [kotlin-flow-exception-handling-226] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* // Imitate a flow of events fun events(): Flow<Int> = (1..3).asFlow().onEach { delay(100) } //sampleStart fun main() = runBlocking<Unit> { events() .onEach { event -> println("Event: $event") } .launchIn(this) // <--- Launching the flow in a separate coroutine println("Done") } //sampleEnd

- [kotlin-flow-exception-handling-227] It prints:

- [kotlin-flow-exception-handling-228] Done Event: 1 Event: 2 Event: 3

- [kotlin-flow-exception-handling-229] The required parameter to launchIn must specify a CoroutineScope in which the coroutine to collect the flow is launched. In the above example this scope comes from the runBlocking coroutine builder, so while the flow is running, this runBlocking scope waits for completion of its child coroutine and keeps the main function from returning and terminating this example.

- [kotlin-flow-exception-handling-230] In actual applications a scope will come from an entity with a limited lifetime. As soon as the lifetime of this entity is terminated the corresponding scope is cancelled, cancelling the collection of the corresponding flow. This way the pair of onEach { ... }.launchIn(scope) works like the addEventListener . However, there is no need for the corresponding removeEventListener function, as cancellation and structured concurrency serve this purpose.

- [kotlin-flow-exception-handling-231] Note that launchIn also returns a Job , which can be used to cancel the corresponding flow collection coroutine only without cancelling the whole scope or to join it.

- [kotlin-flow-exception-handling-232] Flow cancellation checks

- [kotlin-flow-exception-handling-233] For convenience, the flow builder performs additional ensureActive checks for cancellation on each emitted value. It means that a busy loop emitting from a flow { ... } is cancellable:

- [kotlin-flow-exception-handling-234] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun foo(): Flow<Int> = flow { for (i in 1..5) { println("Emitting $i") emit(i) } } fun main() = runBlocking<Unit> { foo().collect { value -> if (value == 3) cancel() println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-235] We get only numbers up to 3 and a CancellationException after trying to emit number 4:

- [kotlin-flow-exception-handling-236] Emitting 1 1 Emitting 2 2 Emitting 3 3 Emitting 4 Exception in thread "main" kotlinx.coroutines.JobCancellationException: BlockingCoroutine was cancelled; job="coroutine#1":BlockingCoroutine{Cancelled}@6d7b4f4c

- [kotlin-flow-exception-handling-237] However, most other flow operators do not do additional cancellation checks on their own for performance reasons. For example, if you use IntRange.asFlow extension to write the same busy loop and don't suspend anywhere, then there are no checks for cancellation:

- [kotlin-flow-exception-handling-238] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun main() = runBlocking<Unit> { (1..5).asFlow().collect { value -> if (value == 3) cancel() println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-239] All numbers from 1 to 5 are collected and cancellation gets detected only before return from runBlocking :

- [kotlin-flow-exception-handling-240] 1 2 3 4 5 Exception in thread "main" kotlinx.coroutines.JobCancellationException: BlockingCoroutine was cancelled; job="coroutine#1":BlockingCoroutine{Cancelled}@3327bd23

- [kotlin-flow-exception-handling-241] In the case where you have a busy loop with coroutines you must explicitly check for cancellation. You can add .onEach { currentCoroutineContext().ensureActive() } , but there is a ready-to-use cancellable operator provided to do that:

- [kotlin-flow-exception-handling-242] import kotlinx.coroutines.* import kotlinx.coroutines.flow.* //sampleStart fun main() = runBlocking<Unit> { (1..5).asFlow().cancellable().collect { value -> if (value == 3) cancel() println(value) } } //sampleEnd

- [kotlin-flow-exception-handling-243] With the cancellable operator only the numbers from 1 to 3 are collected:

- [kotlin-flow-exception-handling-244] 1 2 3 Exception in thread "main" kotlinx.coroutines.JobCancellationException: BlockingCoroutine was cancelled; job="coroutine#1":BlockingCoroutine{Cancelled}@5ec0a365

- [kotlin-flow-exception-handling-245] Flow and Reactive Streams

- [kotlin-flow-exception-handling-246] For those who are familiar with Reactive Streams or reactive frameworks such as RxJava and project Reactor, design of the Flow may look very familiar.

- [kotlin-flow-exception-handling-247] Indeed, its design was inspired by Reactive Streams and its various implementations. But Flow main goal is to have as simple design as possible, be Kotlin and suspension friendly and respect structured concurrency. Achieving this goal would be impossible without reactive pioneers and their tremendous work. You can read the complete story in Reactive Streams and Kotlin Flows article.

- [kotlin-flow-exception-handling-248] While being different, conceptually, Flow is a reactive stream and it is possible to convert it to the reactive (spec and TCK compliant) Publisher and vice versa. Such converters are provided by kotlinx.coroutines out-of-the-box and can be found in corresponding reactive modules ( kotlinx-coroutines-reactive for Reactive Streams, kotlinx-coroutines-reactor for Project Reactor and kotlinx-coroutines-rx2 / kotlinx-coroutines-rx3 for RxJava2/RxJava3). Integration modules include conversions from and to Flow , integration with Reactor's Context and suspension-friendly ways to work with various reactive entities.
