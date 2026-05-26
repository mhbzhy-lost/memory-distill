- [swift-new-diagnostic-arch-1] New Diagnostic Architecture Overview

- [swift-new-diagnostic-arch-2] Diagnostics play a very important role in a programming language experience. It’s vital for developer productivity that the compiler can produce proper guidance in any situation, especially incomplete or invalid code.

- [swift-new-diagnostic-arch-3] In this blog post we would like to share a couple of important updates on improvements to diagnostics being worked on for the upcoming Swift 5.2 release. This includes a new strategy for diagnosing failures in the compiler, originally introduced as part of Swift 5.1 release, that yields some exciting new results and improved error messages.

- [swift-new-diagnostic-arch-4] The Challenge

- [swift-new-diagnostic-arch-5] Swift is a very expressive language with a rich type system that has many features like class inheritance, protocol conformances, generics, and overloading. Though we as programmers try our best to write well-formed programs, sometimes we need a little help. Luckily, the compiler knows exactly what Swift code is valid and invalid. The problem is how best to tell you what has gone wrong, where it happened, and how you can fix it.

- [swift-new-diagnostic-arch-6] Many parts of the compiler ensure the correctness of your program, but the focus of this work has been improving the type checker . The Swift type checker enforces rules about how types are used in source code, and it is responsible for letting you know when those rules are violated.

- [swift-new-diagnostic-arch-7] For example, the following code:

- [swift-new-diagnostic-arch-8] struct S < T > { init ( _ : [ T ]) {} } var i = 42 _ = S < Int > ([ i ! ])

- [swift-new-diagnostic-arch-9] Produces the following diagnostic:

- [swift-new-diagnostic-arch-10] error: type of expression is ambiguous without more context

- [swift-new-diagnostic-arch-11] While this diagnostic points out a genuine error, it’s not helpful because it is not specific or actionable. This is because the old type checker used to guess the exact location of an error. This worked in many cases, but there were still numerous kinds of programming mistakes that users would write which it could not accurately identify. In order to address this, a new diagnostic infrastructure is in the works. Rather than guessing where an error occurs, the type checker attempts to “fix” problems right at the point where they are encountered, while remembering the fixes it has applied. This not only allows the type checker to pinpoint errors in more kinds of programs, it also allows it to surface more failures where previously it would simply stop after reporting the first error.

- [swift-new-diagnostic-arch-12] Type Inference Overview

- [swift-new-diagnostic-arch-13] Since the new diagnostic infrastructure is tightly coupled with the type checker, we have to take a brief detour and talk about type inference. Note that this is a brief introduction; for more details please refer to the compiler’s documentation on the type checker .

- [swift-new-diagnostic-arch-14] Swift implements bi-directional type inference using a constraint-based type checker that is reminiscent of the classical Hindley-Milner type inference algorithm :

- [swift-new-diagnostic-arch-15] The type checker converts the source code into a constraint system , which represents relationships among the types in the code.

- [swift-new-diagnostic-arch-16] A type relationship is expressed via a type constraint , which either places a requirement on a single type (e.g., it is an integer literal type) or relates two types (e.g., one is a convertible to the other).

- [swift-new-diagnostic-arch-17] The types described in constraints can be any type in the Swift type system, including tuple types, function types, enum/struct/class types, protocol types, and generic types. Additionally, a type can be a type variable denoted as $<name> .

- [swift-new-diagnostic-arch-18] Type variables can be used in place of any other type, e.g., a tuple type ($Foo, Int) involving the type variable $Foo .

- [swift-new-diagnostic-arch-19] The Constraint System performs three steps:

- [swift-new-diagnostic-arch-20] Constraint Generation

- [swift-new-diagnostic-arch-21] Constraint Solving

- [swift-new-diagnostic-arch-22] Solution Application

- [swift-new-diagnostic-arch-23] For diagnostics, the only interesting stages are Constraint Generation and Solving.

- [swift-new-diagnostic-arch-24] Given an input expression (and sometimes additional contextual information), the constraint solver generates:

- [swift-new-diagnostic-arch-25] A set of type variables that represent an abstract type of each sub-expression

- [swift-new-diagnostic-arch-26] A set of type constraints that describe the relationships between those type variables

- [swift-new-diagnostic-arch-27] The most common type of constraint is a binary constraint , which relates two types and is denoted as:

- [swift-new-diagnostic-arch-28] type1 <constraint kind > type2

- [swift-new-diagnostic-arch-29] Commonly used binary constraints are:

- [swift-new-diagnostic-arch-30] $X <bind to> Y - Binds type variable $X to a fixed type Y

- [swift-new-diagnostic-arch-31] X <convertible to> Y - A conversion constraint requires that the first type X be convertible to the second Y , which includes subtyping and equality

- [swift-new-diagnostic-arch-32] X <conforms to> Y - Specifies that the first type X must conform to the protocol Y

- [swift-new-diagnostic-arch-33] (Arg1, Arg2, ...) → Result <applicable to> $Function - An “applicable function” constraint requires that both types are function types with the same input and output types

- [swift-new-diagnostic-arch-34] Once constraint generation is complete, the solver attempts to assign concrete types to each of the type variables in the constraint system and form a solution that satisfies all of the constraints.

- [swift-new-diagnostic-arch-35] Let’s consider the following example function:

- [swift-new-diagnostic-arch-36] func foo ( _ str : String ) { str + 1 }

- [swift-new-diagnostic-arch-37] For a human, it becomes apparent pretty quickly that there is a problem with the expression str + 1 and where that problem is located, but the inference engine can only rely on a constraint simplification algorithm to determine what is wrong.

- [swift-new-diagnostic-arch-38] As we have established previously, the constraint solver starts by generating constraints (see Constraint Generation stage) for str , 1 and + . Each distinct sub-element of the input expression, like str , is represented either by:

- [swift-new-diagnostic-arch-39] a concrete type (known ahead of time)

- [swift-new-diagnostic-arch-40] a type variable denoted with $<name> which can assume any type that satisfies the constraints associated with it.

- [swift-new-diagnostic-arch-41] After the Constraint Generation stage completes, the constraint system for the expression str + 1 will have a combination of type variables and constraints. Let’s look at those now.

- [swift-new-diagnostic-arch-42] Type Variables

- [swift-new-diagnostic-arch-43] $Str represents the type of variable str , which is the first argument in the call to +

- [swift-new-diagnostic-arch-44] $One represents the type of literal 1 , which is the second argument in the call to +

- [swift-new-diagnostic-arch-45] $Result represents the result type of the call to operator +

- [swift-new-diagnostic-arch-46] $Plus represents the type of the operator + itself, which is a set of possible overload choices to attempt.

- [swift-new-diagnostic-arch-47] Constraints

- [swift-new-diagnostic-arch-48] $Str <bind to> String Argument str has a fixed String type.

- [swift-new-diagnostic-arch-49] Argument str has a fixed String type.

- [swift-new-diagnostic-arch-50] $One <conforms to> ExpressibleByIntegerLiteral Since integer literals like 1 in Swift could assume any type conforming to the ExpressibleByIntegerLiteral protocol (e.g. Int or Double ), the solver can only rely on that information at the beginning.

- [swift-new-diagnostic-arch-51] Since integer literals like 1 in Swift could assume any type conforming to the ExpressibleByIntegerLiteral protocol (e.g. Int or Double ), the solver can only rely on that information at the beginning.

- [swift-new-diagnostic-arch-52] $Plus <bind to> disjunction((String, String) -> String, (Int, Int) -> Int, ...) Operator + forms a disjoint set of choices, where each element represents the type of an individual overload.

- [swift-new-diagnostic-arch-53] Operator + forms a disjoint set of choices, where each element represents the type of an individual overload.

- [swift-new-diagnostic-arch-54] ($Str, $One) -> $Result <applicable to> $Plus The type of $Result is not yet known; it will be determined by testing each overload of $Plus with argument tuple ($Str, $One) .

- [swift-new-diagnostic-arch-55] The type of $Result is not yet known; it will be determined by testing each overload of $Plus with argument tuple ($Str, $One) .

- [swift-new-diagnostic-arch-56] Note that all constraints and type variables are linked with particular locations in the input expression:

- [swift-new-diagnostic-arch-57] The inference algorithm attempts to find suitable types for all type variables in the constraint system and test them against associated constraints. In our example, $One could get a type of Int or Double because both of these types satisfy the ExpressibleByIntegerLiteral protocol conformance requirement. However, simply enumerating through all of the possible types for each of the “empty” type variables in the constraint system is very inefficient since there could be many types to try when a particular type variable is under-constrained. For example, $Result has no restrictions, so it could potentially assume any type. To work around this problem, the constraint solver first tries disjunction choices, which allows the solver to narrow down the set of possible types for each type variable involved. In the case of $Result , this brings the number of possible types down to only the result types associated with overloads choices of $Plus instead of all possible types.

- [swift-new-diagnostic-arch-58] Now, it’s time to run the inference algorithm to determine types for $One and $Result .

- [swift-new-diagnostic-arch-59] A Single Round of Inference Algorithm Execution:

- [swift-new-diagnostic-arch-60] Let’s start by binding $Plus to its first disjunction choice of (String, String) -> String

- [swift-new-diagnostic-arch-61] Now the applicable to constraint could be tested because $Plus has been bound to a concrete type. Simplification of the ($Str, $One) -> $Result <applicable to> $Plus constraint ends up matching two function types ($Str, $One) -> $Result and (String, String) -> String which proceeds as follows: Add a new conversion constraint to match argument 0 to parameter 0 - $Str <convertible to> String Add a new conversion constraint to match argument 1 to parameter 1 - $One <convertible to> String Equate $Result to String since result types have to be equal

- [swift-new-diagnostic-arch-62] Now the applicable to constraint could be tested because $Plus has been bound to a concrete type. Simplification of the ($Str, $One) -> $Result <applicable to> $Plus constraint ends up matching two function types ($Str, $One) -> $Result and (String, String) -> String which proceeds as follows:

- [swift-new-diagnostic-arch-63] Add a new conversion constraint to match argument 0 to parameter 0 - $Str <convertible to> String

- [swift-new-diagnostic-arch-64] Add a new conversion constraint to match argument 1 to parameter 1 - $One <convertible to> String

- [swift-new-diagnostic-arch-65] Equate $Result to String since result types have to be equal

- [swift-new-diagnostic-arch-66] Some of the newly generated constraints could be immediately tested/simplified e.g. $Str <convertible to> String is true because $Str already has a fixed type of String and String is convertible to itself $Result could be assigned a type of String based on equality constraint

- [swift-new-diagnostic-arch-67] Some of the newly generated constraints could be immediately tested/simplified e.g.

- [swift-new-diagnostic-arch-68] $Str <convertible to> String is true because $Str already has a fixed type of String and String is convertible to itself

- [swift-new-diagnostic-arch-69] $Result could be assigned a type of String based on equality constraint

- [swift-new-diagnostic-arch-70] At this point the only remaining constraints are: $One <convertible to> String $One <conforms to> ExpressibleByIntegerLiteral

- [swift-new-diagnostic-arch-71] At this point the only remaining constraints are:

- [swift-new-diagnostic-arch-72] $One <convertible to> String

- [swift-new-diagnostic-arch-73] $One <conforms to> ExpressibleByIntegerLiteral

- [swift-new-diagnostic-arch-74] The possible types for $One are Int , Double , and String . This is interesting, because none of these possible types satisfy all of the remaining constraints; Int and Double both are not convertible to String , and String does not conform to ExpressibleByIntegerLiteral protocol

- [swift-new-diagnostic-arch-75] After attempting all possible types for $One , the solver stops and considers the current set of types and overload choices a failure. The solver then backtracks and attempts the next disjunction choice for $Plus .

- [swift-new-diagnostic-arch-76] We can see that the error location would be determined by the solver as it executes inference algorithm. Since none of the possible types match for $One it should be considered an error location (because it cannot be bound to any type). Complex expressions could have many more than one such location because existing errors result in new ones as the inference algorithm progresses. To narrow down error locations in situations like that, the solver would only pick solutions with the smallest possible number thereof.

- [swift-new-diagnostic-arch-77] At this point it’s more or less clear how error locations are identified, but it’s not yet obvious how to help the solver make forward progress in such scenarios so it can derive a complete solution.

- [swift-new-diagnostic-arch-78] The Approach

- [swift-new-diagnostic-arch-79] The new diagnostic infrastructure employs what we are going to call a constraint fix to try and resolve inconsistent situations where the solver gets stuck with no other types to attempt. The fix for our example is to ignore that String doesn’t conform to the ExpressibleByIntegerLiteral protocol. The purpose of a fix is to be able to capture all useful information about the error location from the solver and use that later for diagnostics. That is the main difference between current and new approaches. The former would try to guess where the error is located, where the new approach has a symbiotic relationship with the solver which provides all of the error locations to it.

- [swift-new-diagnostic-arch-80] As we noted before, all of the type variables and constraints carry information about their relationship to the sub-expression they have originated from. Such a relation combined with type information makes it straightforward to provide tailored diagnostics and fix-its to all of the problems diagnosed via the new diagnostic framework.

- [swift-new-diagnostic-arch-81] In our example, it has been determined that the type variable $One is an error location, so the diagnostic can examine how $One is used in the input expression: $One represents an argument at position #2 in call to operator + , and it’s known that the problem is related to the fact that String doesn’t conform to ExpressibleByIntegerLiteral protocol. Based on all this information it’s possible to form either of the two following diagnostics:

- [swift-new-diagnostic-arch-82] error: binary operator '+' cannot be applied to arguments 'String' and 'Int'

- [swift-new-diagnostic-arch-83] with a note about the second argument not conforming to the ExpressibleByIntegerLiteral protocol, or the simpler:

- [swift-new-diagnostic-arch-84] error: argument type 'String' does not conform to 'ExpressibleByIntegerLiteral'

- [swift-new-diagnostic-arch-85] with the diagnostic referring to the second argument.

- [swift-new-diagnostic-arch-86] We picked the first alternative and produce a diagnostic about the operator and a note for each partially matching overload choice. Let’s take a closer look at the inner workings of the described approach.

- [swift-new-diagnostic-arch-87] Anatomy of a Diagnostic

- [swift-new-diagnostic-arch-88] When a constraint failure is detected, a constraint fix is created that captures information about a failure:

- [swift-new-diagnostic-arch-89] The kind of failure that occurred

- [swift-new-diagnostic-arch-90] The location in the source code where the failure came from

- [swift-new-diagnostic-arch-91] The types and declarations involved in the failure

- [swift-new-diagnostic-arch-92] The constraint solver accumulates these fixes. Once it arrives at a solution, it looks at the fixes that were part of a solution and produces actionable errors or warnings. Let’s take a look at how this all works together. Consider the following example:

- [swift-new-diagnostic-arch-93] func foo ( _ : inout Int ) {} var x : Int = 0 foo ( x )

- [swift-new-diagnostic-arch-94] The problem here is related to an argument x which cannot be passed as an argument to inout parameter without an explicit & .

- [swift-new-diagnostic-arch-95] Let’s now look at the type variables and constraints for this constraint system.

- [swift-new-diagnostic-arch-96] There are three type variables:

- [swift-new-diagnostic-arch-97] $X := Int $Foo := (inout Int) -> Void $Result

- [swift-new-diagnostic-arch-98] The three type variables have the following constraint:

- [swift-new-diagnostic-arch-99] ($X) -> $Result <applicable to> $Foo

- [swift-new-diagnostic-arch-100] The inference algorithm is going to try and match ($X) -> $Result to (inout Int) -> Void , which results in the following new constraints:

- [swift-new-diagnostic-arch-101] Int <convertible to> inout Int $Result <equal to> Void

- [swift-new-diagnostic-arch-102] Int cannot be converted into inout Int , so the constraint solver records the failure as a missing & and ignores the <convertible to> constraint.

- [swift-new-diagnostic-arch-103] &

- [swift-new-diagnostic-arch-104] With that constraint ignored, the remainder of the constraint system can be solved. Then the type checker looks at the recorded fixes and emits an error that describes the problem (a missing & ) along with a Fix-It to insert the & :

- [swift-new-diagnostic-arch-105] error: passing value of type 'Int' to an inout parameter requires explicit '&' foo(x) ^ &

- [swift-new-diagnostic-arch-106] This example had a single type error in it, but this diagnostics architecture can also account for multiple distinct type errors in the code. Consider a slightly more complicated example:

- [swift-new-diagnostic-arch-107] func foo ( _ : inout Int , bar : String ) {} var x : Int = 0 foo ( x , "bar" )

- [swift-new-diagnostic-arch-108] While solving this constraint system, the type checker will again record a failure for the missing & on the first argument to foo . Additionally, it will record a failure for the missing argument label bar . Once both failures have been recorded, the remainder of the constraint system is solved. The type checker then produces errors (with Fix-Its) for the two problems that need to be addressed to fix this code:

- [swift-new-diagnostic-arch-109] error: passing value of type 'Int' to an inout parameter requires explicit '&' foo(x) ^ & error: missing argument label 'bar:' in call foo(x, "bar") ^ bar:

- [swift-new-diagnostic-arch-110] Recording every specific failure and then continuing on to solve the remaining constraint system implies that addressing those failures will produce a well-typed solution. That allows the type checker to produce actionable diagnostics, often with fixes, that lead the developer toward correct code.

- [swift-new-diagnostic-arch-111] Examples Of Improved Diagnostics

- [swift-new-diagnostic-arch-112] Missing label(s)

- [swift-new-diagnostic-arch-113] Consider the following invalid code:

- [swift-new-diagnostic-arch-114] func foo ( answer : Int ) -> String { return "a" } func foo ( answer : String ) -> String { return "b" } let _ : [ String ] = [ 42 ] . map { foo ( $0 ) }

- [swift-new-diagnostic-arch-115] Previously, this resulted in the following diagnostic:

- [swift-new-diagnostic-arch-116] error: argument labels '(_:)' do not match any available overloads`

- [swift-new-diagnostic-arch-117] This is now diagnosed as:

- [swift-new-diagnostic-arch-118] error: missing argument label 'answer:' in call let _: [String] = [42].map { foo($0) } ^ answer:

- [swift-new-diagnostic-arch-119] Argument-to-Parameter Conversion Mismatch

- [swift-new-diagnostic-arch-120] let x : [ Int ] = [ 1 , 2 , 3 , 4 ] let y : UInt = 4 _ = x . filter { ( $0 + y ) > 42 }

- [swift-new-diagnostic-arch-121] error: binary operator '+' cannot be applied to operands of type 'Int' and 'UInt'`

- [swift-new-diagnostic-arch-122] error: cannot convert value of type 'UInt' to expected argument type 'Int' _ = x.filter { ($0 + y) > 42 } ^ Int( )

- [swift-new-diagnostic-arch-123] Invalid Optional Unwrap

- [swift-new-diagnostic-arch-124] error: cannot force unwrap value of non-optional type 'Int' _ = S<Int>([i!]) ~^

- [swift-new-diagnostic-arch-125] Missing Members

- [swift-new-diagnostic-arch-126] class A {} class B : A { override init () {} func foo () -> A { return A () } } struct S < T > { init ( _ a : T ... ) {} } func bar < T > ( _ t : T ) { _ = S ( B (), . foo (), A ()) }

- [swift-new-diagnostic-arch-127] error: generic parameter ’T’ could not be inferred

- [swift-new-diagnostic-arch-128] error: type 'A' has no member 'foo' _ = S(B(), .foo(), A()) ~^~~~~

- [swift-new-diagnostic-arch-129] protocol P {} func foo < T : P > ( _ x : T ) -> T { return x } func bar < T > ( x : T ) -> T { return foo ( x ) }

- [swift-new-diagnostic-arch-130] error: generic parameter 'T' could not be inferred

- [swift-new-diagnostic-arch-131] error: argument type 'T' does not conform to expected type 'P' return foo(x) ^

- [swift-new-diagnostic-arch-132] Conditional Conformances

- [swift-new-diagnostic-arch-133] extension BinaryInteger { var foo : Self { return self <= 1 ? 1 : ( 2 ... self ) . reduce ( 1 , * ) } }

- [swift-new-diagnostic-arch-134] error: ambiguous reference to member '...'

- [swift-new-diagnostic-arch-135] error: referencing instance method 'reduce' on 'ClosedRange' requires that 'Self.Stride' conform to 'SignedInteger' : (2...self).reduce(1, *) ^ Swift.ClosedRange:1:11: note: requirement from conditional conformance of 'ClosedRange<Self>' to 'Sequence' extension ClosedRange : Sequence where Bound : Strideable, Bound.Stride : SignedInteger { ^

- [swift-new-diagnostic-arch-136] SwiftUI Examples

- [swift-new-diagnostic-arch-137] Consider the following invalid SwiftUI code:

- [swift-new-diagnostic-arch-138] import SwiftUI struct Foo : View { var body : some View { ForEach ( 1 ... 5 ) { Circle () . rotation ( . degrees ( $0 )) } } }

- [swift-new-diagnostic-arch-139] error: Cannot convert value of type '(Double) -> RotatedShape<Circle>' to expected argument type '() -> _'

- [swift-new-diagnostic-arch-140] error: cannot convert value of type 'Int' to expected argument type 'Double' Circle().rotation(.degrees($0)) ^ Double( )

- [swift-new-diagnostic-arch-141] import SwiftUI struct S : View { var body : some View { ZStack { Rectangle () . frame ( width : 220.0 , height : 32.0 ) . foregroundColor ( . systemRed ) HStack { Text ( "A" ) Spacer () Text ( "B" ) } . padding () } . scaledToFit () } }

- [swift-new-diagnostic-arch-142] Previously, this used to be diagnosed as a completely unrelated problem:

- [swift-new-diagnostic-arch-143] error: 'Double' is not convertible to 'CGFloat?' Rectangle().frame(width: 220.0, height: 32.0) ^~~~~

- [swift-new-diagnostic-arch-144] The new diagnostic now correctly points out that there is no such color as systemRed :

- [swift-new-diagnostic-arch-145] error: type 'Color?' has no member 'systemRed' .foregroundColor(.systemRed) ~^~~~~~~~~

- [swift-new-diagnostic-arch-146] Missing arguments

- [swift-new-diagnostic-arch-147] import SwiftUI struct S : View { @State private var showDetail = false var body : some View { Button ( action : { self . showDetail . toggle () }) { Image ( systemName : "chevron.right.circle" ) . imageScale ( . large ) . rotationEffect ( . degrees ( showDetail ? 90 : 0 )) . scaleEffect ( showDetail ? 1.5 : 1 ) . padding () . animation ( . spring ) } } }

- [swift-new-diagnostic-arch-148] error: member 'spring' expects argument of type '(response: Double, dampingFraction: Double, blendDuration: Double)' .animation(.spring) ^

- [swift-new-diagnostic-arch-149] Conclusion

- [swift-new-diagnostic-arch-150] The new diagnostic infrastructure is designed to overcome all of the shortcomings of the old approach. The way it’s structured is intended to make it easy to improve/port existing diagnostics and to be used by new feature implementors to provide great diagnostics right off the bat. It shows very promising results with all of the diagnostics we have ported so far, and we are hard at work porting more every day.

- [swift-new-diagnostic-arch-151] Questions?

- [swift-new-diagnostic-arch-152] Please feel free to post questions about this post on the associated thread on the Swift forums .

- [swift-new-diagnostic-arch-153] Authors

- [swift-new-diagnostic-arch-154] Continue Reading
