- [kotlin-exceptions-language-doc-1] Exception and error handling

- [kotlin-exceptions-language-doc-2] Exceptions help your code run more predictably, even when runtime errors occur that could disrupt program execution. Kotlin treats all exceptions as unchecked by default. Unchecked exceptions simplify the exception handling process: you can catch exceptions, but you don't need to explicitly handle or declare them.

- [kotlin-exceptions-language-doc-3] Working with exceptions consists of two primary actions:

- [kotlin-exceptions-language-doc-4] Throwing exceptions: indicate when a problem occurs.

- [kotlin-exceptions-language-doc-5] Catching exceptions: handle the unexpected exception manually by resolving the issue or notifying the developer or application user.

- [kotlin-exceptions-language-doc-6] Exceptions are represented by subclasses of the Exception class, which is a subclass of the Throwable class. For more information about the hierarchy, see the Exception hierarchy section. Since Exception is an open class , you can create custom exceptions to suit your application's specific needs.

- [kotlin-exceptions-language-doc-7] Exception

- [kotlin-exceptions-language-doc-8] Throwable

- [kotlin-exceptions-language-doc-9] open class

- [kotlin-exceptions-language-doc-10] Throw exceptions

- [kotlin-exceptions-language-doc-11] You can manually throw exceptions with the throw keyword. Throwing an exception indicates that an unexpected runtime error has occurred in the code. Exceptions are objects , and throwing one creates an instance of an exception class.

- [kotlin-exceptions-language-doc-12] You can throw an exception without any parameters:

- [kotlin-exceptions-language-doc-13] To better understand the source of the problem, include additional information, such as a custom message and the original cause:

- [kotlin-exceptions-language-doc-14] In this example, an IllegalArgumentException is thrown when the user inputs a negative value. You can create custom error messages and keep the original cause ( cause ) of the exception, which will be included in the stack trace .

- [kotlin-exceptions-language-doc-15] Throw exceptions with precondition functions

- [kotlin-exceptions-language-doc-16] Kotlin offers additional ways to automatically throw exceptions using precondition functions. Precondition functions include:

- [kotlin-exceptions-language-doc-17] Precondition function

- [kotlin-exceptions-language-doc-18] Use case

- [kotlin-exceptions-language-doc-19] Exception thrown

- [kotlin-exceptions-language-doc-20] require()

- [kotlin-exceptions-language-doc-21] Checks user input validity

- [kotlin-exceptions-language-doc-22] IllegalArgumentException

- [kotlin-exceptions-language-doc-23] check()

- [kotlin-exceptions-language-doc-24] Checks object or variable state validity

- [kotlin-exceptions-language-doc-25] IllegalStateException

- [kotlin-exceptions-language-doc-26] error()

- [kotlin-exceptions-language-doc-27] Indicates an illegal state or condition

- [kotlin-exceptions-language-doc-28] These functions are suitable for situations where the program's flow cannot continue if specific conditions aren't met. This streamlines your code and makes handling these checks efficient.

- [kotlin-exceptions-language-doc-29] Use the require() function to validate input arguments when they are crucial for the function's operation, and the function can't proceed if these arguments are invalid.

- [kotlin-exceptions-language-doc-30] If the condition in require() is not met, it throws an IllegalArgumentException :

- [kotlin-exceptions-language-doc-31] Use the check() function to validate the state of an object or variable. If the check fails, it indicates a logic error that needs to be addressed.

- [kotlin-exceptions-language-doc-32] If the condition specified in the check() function is false , it throws an IllegalStateException :

- [kotlin-exceptions-language-doc-33] The error() function is used to signal an illegal state or a condition in the code that logically should not occur. It's suitable for scenarios when you want to throw an exception intentionally in your code, such as when the code encounters an unexpected state. This function is particularly useful in when expressions, providing a clear way to handle cases that shouldn't logically happen.

- [kotlin-exceptions-language-doc-34] In the following example, the error() function is used to handle an undefined user role. If the role is not one of the predefined ones, an IllegalStateException is thrown:

- [kotlin-exceptions-language-doc-35] Handle exceptions using try-catch blocks

- [kotlin-exceptions-language-doc-36] When an exception is thrown, it interrupts the normal execution of the program. You can handle exceptions gracefully with the try and catch keywords to keep your program stable. The try block contains the code that might throw an exception, while the catch block catches and handles the exception if it occurs. The exception is caught by the first catch block that matches its specific type or a superclass of the exception.

- [kotlin-exceptions-language-doc-37] Here's how you can use the try and catch keywords together:

- [kotlin-exceptions-language-doc-38] It's a common approach to use try-catch as an expression, so it can return a value from either the try block or the catch block:

- [kotlin-exceptions-language-doc-39] You can use multiple catch handlers for the same try block. You can add as many catch blocks as needed to handle different exceptions distinctively. When you have multiple catch blocks, it's important to order them from the most specific to the least specific exception, following a top-to-bottom order in your code. This ordering aligns with the program's execution flow.

- [kotlin-exceptions-language-doc-40] Consider this example with custom exceptions :

- [kotlin-exceptions-language-doc-41] A general catch block handling WithdrawalException , catches all exceptions of its type, including specific ones like InsufficientFundsException , unless they are caught earlier by a more specific catch block.

- [kotlin-exceptions-language-doc-42] The finally block

- [kotlin-exceptions-language-doc-43] The finally block contains code that always executes, regardless of whether the try block completes successfully or throws an exception. With the finally block you can clean up code after the execution of try and catch blocks. This is especially important when working with resources like files or network connections, as finally guarantees they are properly closed or released.

- [kotlin-exceptions-language-doc-44] Here is how you would typically use the try-catch-finally blocks together:

- [kotlin-exceptions-language-doc-45] The returned value of a try expression is determined by the last executed expression in either the try or catch block. If no exceptions occur, the result comes from the try block; if an exception is handled, it comes from the catch block. The finally block is always executed, but it doesn't change the result of the try-catch block.

- [kotlin-exceptions-language-doc-46] Let's look at an example to demonstrate:

- [kotlin-exceptions-language-doc-47] If your code requires resource cleanup without handling exceptions, you can also use try with the finally block without catch blocks:

- [kotlin-exceptions-language-doc-48] As you can see, the finally block guarantees that the resource is closed, regardless of whether an exception occurs.

- [kotlin-exceptions-language-doc-49] In Kotlin, you have the flexibility to use only a catch block, only a finally block, or both, depending on your specific needs, but a try block must always be accompanied by at least one catch block or a finally block.

- [kotlin-exceptions-language-doc-50] Create custom exceptions

- [kotlin-exceptions-language-doc-51] In Kotlin, you can define custom exceptions by creating classes that extend the built-in Exception class. This allows you to create more specific error types tailored to your application's needs.

- [kotlin-exceptions-language-doc-52] To create one, you can define a class that extends Exception :

- [kotlin-exceptions-language-doc-53] In this example, there is a default error message, "My message", but you can leave it blank if you want.

- [kotlin-exceptions-language-doc-54] Custom exceptions can also be a subclass of any pre-existent exception subclass, like the ArithmeticException subclass:

- [kotlin-exceptions-language-doc-55] Custom exceptions behave just like built-in exceptions. You can throw them using the throw keyword, and handle them with try-catch-finally blocks. Let's look at an example to demonstrate:

- [kotlin-exceptions-language-doc-56] In applications with diverse error scenarios, creating a hierarchy of exceptions can help making the code clearer and more specific. You can achieve this by using an abstract class or a sealed class as a base for common exception features and creating specific subclasses for detailed exception types. Additionally, custom exceptions including parameters with default values offer flexibility, allowing initialization with varied messages, which enables more granular error handling.

- [kotlin-exceptions-language-doc-57] Let's look at an example using the sealed class AccountException as the base for an exception hierarchy, and class APIKeyExpiredException , a subclass, which showcases the use of parameters with default values for improved exception detail:

- [kotlin-exceptions-language-doc-58] The Nothing type

- [kotlin-exceptions-language-doc-59] In Kotlin, every expression has a type. The type of the expression throw IllegalArgumentException() is Nothing , a built-in type that is a subtype of all other types, also known as the bottom type . This means Nothing can be used as a return type or generic type where any other type is expected, without causing type errors.

- [kotlin-exceptions-language-doc-60] Nothing

- [kotlin-exceptions-language-doc-61] Nothing is a special type in Kotlin used to represent functions or expressions that never complete successfully, either because they always throw an exception or enter an endless execution path like an infinite loop. You can use Nothing to mark functions that are not yet implemented or are designed to always throw an exception, clearly indicating your intentions to both the compiler and code readers. If the compiler infers a Nothing type in a function signature, it will warn you. Explicitly defining Nothing as the return type can eliminate this warning.

- [kotlin-exceptions-language-doc-62] This Kotlin code demonstrates the use of the Nothing type, where the compiler marks the code following the function call as unreachable:

- [kotlin-exceptions-language-doc-63] Kotlin's TODO() function, which also uses the Nothing type, serves as a placeholder to highlight areas of the code that need future implementation:

- [kotlin-exceptions-language-doc-64] TODO()

- [kotlin-exceptions-language-doc-65] As you can see, the TODO() function always throws a NotImplementedError exception.

- [kotlin-exceptions-language-doc-66] NotImplementedError

- [kotlin-exceptions-language-doc-67] Exception classes

- [kotlin-exceptions-language-doc-68] Let's explore some common exception types found in Kotlin, which are all subclasses of the RuntimeException class:

- [kotlin-exceptions-language-doc-69] RuntimeException

- [kotlin-exceptions-language-doc-70] ArithmeticException : This exception occurs when an arithmetic operation is impossible to perform, like division by zero. val example = 2 / 0 // throws ArithmeticException

- [kotlin-exceptions-language-doc-71] ArithmeticException : This exception occurs when an arithmetic operation is impossible to perform, like division by zero.

- [kotlin-exceptions-language-doc-72] ArithmeticException

- [kotlin-exceptions-language-doc-73] IndexOutOfBoundsException : This exception is thrown to indicate that an index of some sort, such as an array or string is out of range. val myList = mutableListOf(1, 2, 3) myList.removeAt(3) // throws IndexOutOfBoundsException

- [kotlin-exceptions-language-doc-74] IndexOutOfBoundsException : This exception is thrown to indicate that an index of some sort, such as an array or string is out of range.

- [kotlin-exceptions-language-doc-75] IndexOutOfBoundsException

- [kotlin-exceptions-language-doc-76] NoSuchElementException : This exception is thrown when an element that does not exist in a particular collection is accessed. It occurs when using methods that expect a specific element, such as first() or last() . val emptyList = listOf<Int>() val firstElement = emptyList.first() // throws NoSuchElementException

- [kotlin-exceptions-language-doc-77] NoSuchElementException : This exception is thrown when an element that does not exist in a particular collection is accessed. It occurs when using methods that expect a specific element, such as first() or last() .

- [kotlin-exceptions-language-doc-78] NoSuchElementException

- [kotlin-exceptions-language-doc-79] first()

- [kotlin-exceptions-language-doc-80] last()

- [kotlin-exceptions-language-doc-81] NumberFormatException : This exception occurs when attempting to convert a string to a numeric type, but the string doesn't have an appropriate format. val string = "This is not a number" val number = string.toInt() // throws NumberFormatException

- [kotlin-exceptions-language-doc-82] NumberFormatException : This exception occurs when attempting to convert a string to a numeric type, but the string doesn't have an appropriate format.

- [kotlin-exceptions-language-doc-83] NumberFormatException

- [kotlin-exceptions-language-doc-84] NullPointerException : This exception is thrown when an application attempts to use an object reference that has the null value. Even though Kotlin's null safety features significantly reduce the risk of NullPointerExceptions, they can still occur either through deliberate use of the !! operator or when interacting with Java, which lacks Kotlin's null safety. val text: String? = null println(text!!.length) // throws a NullPointerException

- [kotlin-exceptions-language-doc-85] NullPointerException : This exception is thrown when an application attempts to use an object reference that has the null value. Even though Kotlin's null safety features significantly reduce the risk of NullPointerExceptions, they can still occur either through deliberate use of the !! operator or when interacting with Java, which lacks Kotlin's null safety.

- [kotlin-exceptions-language-doc-86] NullPointerException

- [kotlin-exceptions-language-doc-87] While all exceptions are unchecked in Kotlin, and you don't have to catch them explicitly, you still have the flexibility to catch them if desired.

- [kotlin-exceptions-language-doc-88] Exception hierarchy

- [kotlin-exceptions-language-doc-89] The root of the Kotlin exception hierarchy is the Throwable class. It has two direct subclasses, Error and Exception :

- [kotlin-exceptions-language-doc-90] Error

- [kotlin-exceptions-language-doc-91] The Error subclass represents serious fundamental problems that an application might not be able to recover from by itself. These are problems that you generally would not attempt to handle, such as OutOfMemoryError or StackOverflowError .

- [kotlin-exceptions-language-doc-92] OutOfMemoryError

- [kotlin-exceptions-language-doc-93] The Exception subclass is used for conditions that you might want to handle. Subtypes of the Exception type, such as the RuntimeException and IOException (Input/Output Exception), deal with exceptional events in applications.

- [kotlin-exceptions-language-doc-94] RuntimeException is usually caused by insufficient checks in the program code and can be prevented programmatically. Kotlin helps prevent common RuntimeExceptions like NullPointerException and provides compile-time warnings for potential runtime errors, such as division by zero. The following picture demonstrates a hierarchy of subtypes descended from RuntimeException :

- [kotlin-exceptions-language-doc-95] Stack trace

- [kotlin-exceptions-language-doc-96] The stack trace is a report generated by the runtime environment, used for debugging. It shows the sequence of function calls leading to a specific point in the program, especially where an error or exception occurred.

- [kotlin-exceptions-language-doc-97] Let's see an example where the stack trace is automatically printed because of an exception in a JVM environment:

- [kotlin-exceptions-language-doc-98] Running this code in a JVM environment produces the following output:

- [kotlin-exceptions-language-doc-99] The first line is the exception description, which includes:

- [kotlin-exceptions-language-doc-100] Exception type: java.lang.ArithmeticException

- [kotlin-exceptions-language-doc-101] Thread: main

- [kotlin-exceptions-language-doc-102] Exception message: "This is an arithmetic exception!"

- [kotlin-exceptions-language-doc-103] Each other line that starts with an at after the exception description is the stack trace. A single line is called a stack trace element or a stack frame :

- [kotlin-exceptions-language-doc-104] at MainKt.main (Main.kt:3) : This shows the method name ( MainKt.main ) and the source file and line number where the method was called ( Main.kt:3 ).

- [kotlin-exceptions-language-doc-105] at MainKt.main (Main.kt) : This shows that the exception occurs in the main() function of the Main.kt file.

- [kotlin-exceptions-language-doc-106] Exception interoperability with Java, Swift, and Objective-C

- [kotlin-exceptions-language-doc-107] Since Kotlin treats all exceptions as unchecked, it can lead to complications when such exceptions are called from languages that distinguish between checked and unchecked exceptions. To address this disparity in exception handling between Kotlin and languages like Java, Swift, and Objective-C, you can use the @Throws annotation. This annotation alerts callers about possible exceptions. For more information, see Calling Kotlin from Java and Interoperability with Swift/Objective-C .

- [kotlin-exceptions-language-doc-108] @Throws
