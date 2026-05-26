- [kotlin-serialization-basic-errors-1] Basic Serialization

- [kotlin-serialization-basic-errors-2] This is the first chapter of the Kotlin Serialization Guide . This chapter shows the basic use of Kotlin Serialization and explains its core concepts.

- [kotlin-serialization-basic-errors-3] Table of contents

- [kotlin-serialization-basic-errors-4] Basics JSON encoding JSON decoding

- [kotlin-serialization-basic-errors-5] JSON encoding

- [kotlin-serialization-basic-errors-6] JSON decoding

- [kotlin-serialization-basic-errors-7] Serializable classes Backing fields are serialized Constructor properties requirement Data validation Optional properties Optional property initializer call Required properties Transient properties Defaults are not encoded by default Nullable properties Type safety is enforced Referenced objects No compression of repeated references Generic classes Serial field names

- [kotlin-serialization-basic-errors-8] Backing fields are serialized

- [kotlin-serialization-basic-errors-9] Constructor properties requirement

- [kotlin-serialization-basic-errors-10] Data validation

- [kotlin-serialization-basic-errors-11] Optional properties

- [kotlin-serialization-basic-errors-12] Optional property initializer call

- [kotlin-serialization-basic-errors-13] Required properties

- [kotlin-serialization-basic-errors-14] Transient properties

- [kotlin-serialization-basic-errors-15] Defaults are not encoded by default

- [kotlin-serialization-basic-errors-16] Nullable properties

- [kotlin-serialization-basic-errors-17] Type safety is enforced

- [kotlin-serialization-basic-errors-18] Referenced objects

- [kotlin-serialization-basic-errors-19] No compression of repeated references

- [kotlin-serialization-basic-errors-20] Generic classes

- [kotlin-serialization-basic-errors-21] Serial field names

- [kotlin-serialization-basic-errors-22] Basics

- [kotlin-serialization-basic-errors-23] To convert an object tree to a string or to a sequence of bytes, it must come through two mutually intertwined processes. In the first step, an object is serialized —it is converted into a serial sequence of its constituting primitive values. This process is common for all data formats and its result depends on the object being serialized. A serializer controls this process. The second step is called encoding —it is the conversion of the corresponding sequence of primitives into the output format representation. An encoder controls this process. Whenever the distinction is not important, both the terms of encoding and serialization are used interchangeably.

- [kotlin-serialization-basic-errors-24] +---------+ Serialization +------------+ Encoding +---------------+ | Objects | --------------> | Primitives | ---------> | Output format | +---------+ +------------+ +---------------+

- [kotlin-serialization-basic-errors-25] The reverse process starts with parsing of the input format and decoding of primitive values, followed by deserialization of the resulting stream into objects. We'll see details of this process later.

- [kotlin-serialization-basic-errors-26] For now, we start with JSON encoding.

- [kotlin-serialization-basic-errors-27] The whole process of converting data into a specific format is called encoding . For JSON we encode data using the Json.encodeToString extension function. It serializes the object that is passed as its parameter under the hood and encodes it to a JSON string.

- [kotlin-serialization-basic-errors-28] Let's start with a class describing a project and try to get its JSON representation.

- [kotlin-serialization-basic-errors-29] class Project(val name: String, val language: String) fun main() { val data = Project("kotlinx.serialization", "Kotlin") println(Json.encodeToString(data)) }

- [kotlin-serialization-basic-errors-30] You can get the full code here .

- [kotlin-serialization-basic-errors-31] When we run this code we get the exception.

- [kotlin-serialization-basic-errors-32] Exception in thread "main" kotlinx.serialization.SerializationException: Serializer for class 'Project' is not found. Please ensure that class is marked as '@Serializable' and that the serialization compiler plugin is applied.

- [kotlin-serialization-basic-errors-33] Serializable classes have to be explicitly marked. Kotlin Serialization does not use reflection, so you cannot accidentally deserialize a class which was not supposed to be serializable. We fix it by adding the @Serializable annotation.

- [kotlin-serialization-basic-errors-34] @Serializable

- [kotlin-serialization-basic-errors-35] @Serializable class Project(val name: String, val language: String) fun main() { val data = Project("kotlinx.serialization", "Kotlin") println(Json.encodeToString(data)) }

- [kotlin-serialization-basic-errors-36] The @Serializable annotation instructs the Kotlin Serialization plugin to automatically generate and hook up a serializer for this class. Now the output of the example is the corresponding JSON.

- [kotlin-serialization-basic-errors-37] {"name":"kotlinx.serialization","language":"Kotlin"}

- [kotlin-serialization-basic-errors-38] There is a whole chapter about the Serializers . For now, it is enough to know that they are automatically generated by the Kotlin Serialization plugin.

- [kotlin-serialization-basic-errors-39] The reverse process is called decoding . To decode a JSON string into an object, we'll use the Json.decodeFromString extension function. To specify which type we want to get as a result, we provide a type parameter to this function.

- [kotlin-serialization-basic-errors-40] As we'll see later, serialization works with different kinds of classes. Here we are marking our Project class as a data class , not because it is required, but because we want to print its contents to verify how it decodes.

- [kotlin-serialization-basic-errors-41] @Serializable data class Project(val name: String, val language: String) fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization","language":"Kotlin"} """) println(data) }

- [kotlin-serialization-basic-errors-42] Running this code we get back the object.

- [kotlin-serialization-basic-errors-43] Project(name=kotlinx.serialization, language=Kotlin)

- [kotlin-serialization-basic-errors-44] Serializable classes

- [kotlin-serialization-basic-errors-45] This section goes into more details on how different @Serializable classes are handled.

- [kotlin-serialization-basic-errors-46] Only a class's properties with backing fields are serialized, so properties with a getter/setter that don't have a backing field and delegated properties are not serialized, as the following example shows.

- [kotlin-serialization-basic-errors-47] @Serializable class Project( // name is a property with backing field -- serialized var name: String ) { var stars: Int = 0 // property with a backing field -- serialized val path: String // getter only, no backing field -- not serialized get() = "kotlin/$name" var id by ::name // delegated property -- not serialized } fun main() { val data = Project("kotlinx.serialization").apply { stars = 9000 } println(Json.encodeToString(data)) }

- [kotlin-serialization-basic-errors-48] We can clearly see that only the name and stars properties are present in the JSON output.

- [kotlin-serialization-basic-errors-49] {"name":"kotlinx.serialization","stars":9000}

- [kotlin-serialization-basic-errors-50] If we want to define the Project class so that it takes a path string, and then deconstructs it into the corresponding properties, we might be tempted to write something like the code below.

- [kotlin-serialization-basic-errors-51] @Serializable class Project(path: String) { val owner: String = path.substringBefore('/') val name: String = path.substringAfter('/') }

- [kotlin-serialization-basic-errors-52] This class does not compile because the @Serializable annotation requires that all parameters of the class's primary constructor be properties. A simple workaround is to define a private primary constructor with the class's properties, and turn the constructor we wanted into the secondary one.

- [kotlin-serialization-basic-errors-53] @Serializable class Project private constructor(val owner: String, val name: String) { constructor(path: String) : this( owner = path.substringBefore('/'), name = path.substringAfter('/') ) val path: String get() = "$owner/$name" }

- [kotlin-serialization-basic-errors-54] Serialization works with a private primary constructor, and still serializes only backing fields.

- [kotlin-serialization-basic-errors-55] fun main() { println(Json.encodeToString(Project("kotlin/kotlinx.serialization"))) }

- [kotlin-serialization-basic-errors-56] This example produces the expected output.

- [kotlin-serialization-basic-errors-57] {"owner":"kotlin","name":"kotlinx.serialization"}

- [kotlin-serialization-basic-errors-58] Another case where you might want to introduce a primary constructor parameter without a property is when you want to validate its value before storing it to a property. To make it serializable you shall replace it with a property in the primary constructor, and move the validation to an init { ... } block.

- [kotlin-serialization-basic-errors-59] @Serializable class Project(val name: String) { init { require(name.isNotEmpty()) { "name cannot be empty" } } }

- [kotlin-serialization-basic-errors-60] A deserialization process works like a regular constructor in Kotlin and calls all init blocks, ensuring that you cannot get an invalid class as a result of deserialization. Let's try it.

- [kotlin-serialization-basic-errors-61] fun main() { val data = Json.decodeFromString<Project>(""" {"name":""} """) println(data) }

- [kotlin-serialization-basic-errors-62] Running this code produces the exception:

- [kotlin-serialization-basic-errors-63] Exception in thread "main" java.lang.IllegalArgumentException: name cannot be empty

- [kotlin-serialization-basic-errors-64] An object can be deserialized only when all its properties are present in the input. For example, run the following code.

- [kotlin-serialization-basic-errors-65] @Serializable data class Project(val name: String, val language: String) fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization"} """) println(data) }

- [kotlin-serialization-basic-errors-66] It produces the exception:

- [kotlin-serialization-basic-errors-67] Exception in thread "main" kotlinx.serialization.MissingFieldException: Field 'language' is required for type with serial name 'example.exampleClasses04.Project', but it was missing at path: $

- [kotlin-serialization-basic-errors-68] This problem can be fixed by adding a default value to the property, which automatically makes it optional for serialization.

- [kotlin-serialization-basic-errors-69] @Serializable data class Project(val name: String, val language: String = "Kotlin") fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization"} """) println(data) }

- [kotlin-serialization-basic-errors-70] It produces the following output with the default value for the language property.

- [kotlin-serialization-basic-errors-71] When an optional property is present in the input, the corresponding initializer for this property is not even called. This is a feature designed for performance, so be careful not to rely on side effects in initializers. Consider the example below.

- [kotlin-serialization-basic-errors-72] fun computeLanguage(): String { println("Computing") return "Kotlin" } @Serializable data class Project(val name: String, val language: String = computeLanguage()) fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization","language":"Kotlin"} """) println(data) }

- [kotlin-serialization-basic-errors-73] Since the language property was specified in the input, we don't see the "Computing" string printed in the output.

- [kotlin-serialization-basic-errors-74] A property with a default value can be required in a serial format with the @Required annotation. Let us change the previous example by marking the language property as @Required .

- [kotlin-serialization-basic-errors-75] @Required

- [kotlin-serialization-basic-errors-76] @Serializable data class Project(val name: String, @Required val language: String = "Kotlin") fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization"} """) println(data) }

- [kotlin-serialization-basic-errors-77] We get the following exception.

- [kotlin-serialization-basic-errors-78] Exception in thread "main" kotlinx.serialization.MissingFieldException: Field 'language' is required for type with serial name 'example.exampleClasses07.Project', but it was missing at path: $

- [kotlin-serialization-basic-errors-79] A property can be excluded from serialization by marking it with the @Transient annotation (don't confuse it with kotlin.jvm.Transient ). Transient properties must have a default value.

- [kotlin-serialization-basic-errors-80] @Transient

- [kotlin-serialization-basic-errors-81] @Serializable data class Project(val name: String, @Transient val language: String = "Kotlin") fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization","language":"Kotlin"} """) println(data) }

- [kotlin-serialization-basic-errors-82] Attempts to explicitly specify its value in the serial format, even if the specified value is equal to the default one, produces the following exception.

- [kotlin-serialization-basic-errors-83] Exception in thread "main" kotlinx.serialization.json.JsonDecodingException: Unexpected JSON token at offset 42: Encountered an unknown key 'language' at path: $ Use 'ignoreUnknownKeys = true' in 'Json {}' builder or '@JsonIgnoreUnknownKeys' annotation to ignore unknown keys.

- [kotlin-serialization-basic-errors-84] The 'ignoreUnknownKeys' feature is explained in the Ignoring Unknown Keys section section.

- [kotlin-serialization-basic-errors-85] Default values are not encoded by default in JSON. This behavior is motivated by the fact that in most real-life scenarios such configuration reduces visual clutter, and saves the amount of data being serialized.

- [kotlin-serialization-basic-errors-86] @Serializable data class Project(val name: String, val language: String = "Kotlin") fun main() { val data = Project("kotlinx.serialization") println(Json.encodeToString(data)) }

- [kotlin-serialization-basic-errors-87] It produces the following output, which does not have the language property because its value is equal to the default one.

- [kotlin-serialization-basic-errors-88] {"name":"kotlinx.serialization"}

- [kotlin-serialization-basic-errors-89] See JSON's Encoding defaults section on how this behavior can be configured for JSON. Additionally, this behavior can be controlled without taking format settings into account. For that purposes, EncodeDefault annotation can be used:

- [kotlin-serialization-basic-errors-90] @Serializable data class Project( val name: String, @EncodeDefault val language: String = "Kotlin" )

- [kotlin-serialization-basic-errors-91] This annotation instructs the framework to always serialize property, regardless of its value or format settings. It's also possible to tweak it into the opposite behavior using EncodeDefault.Mode parameter:

- [kotlin-serialization-basic-errors-92] @Serializable data class User( val name: String, @EncodeDefault(NEVER) val projects: List<Project> = emptyList() ) fun main() { val userA = User("Alice", listOf(Project("kotlinx.serialization"))) val userB = User("Bob") println(Json.encodeToString(userA)) println(Json.encodeToString(userB)) }

- [kotlin-serialization-basic-errors-93] As you can see, language property is preserved and projects is omitted:

- [kotlin-serialization-basic-errors-94] {"name":"Alice","projects":[{"name":"kotlinx.serialization","language":"Kotlin"}]} {"name":"Bob"}

- [kotlin-serialization-basic-errors-95] Nullable properties are natively supported by Kotlin Serialization.

- [kotlin-serialization-basic-errors-96] @Serializable class Project(val name: String, val renamedTo: String? = null) fun main() { val data = Project("kotlinx.serialization") println(Json.encodeToString(data)) }

- [kotlin-serialization-basic-errors-97] This example does not encode null in JSON because Defaults are not encoded .

- [kotlin-serialization-basic-errors-98] Kotlin Serialization strongly enforces the type safety of the Kotlin programming language. In particular, let us try to decode a null value from a JSON object into a non-nullable Kotlin property language .

- [kotlin-serialization-basic-errors-99] @Serializable data class Project(val name: String, val language: String = "Kotlin") fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization","language":null} """) println(data) }

- [kotlin-serialization-basic-errors-100] Even though the language property has a default value, it is still an error to attempt to assign the null value to it.

- [kotlin-serialization-basic-errors-101] Exception in thread "main" kotlinx.serialization.json.JsonDecodingException: Unexpected JSON token at offset 52: Expected string literal but 'null' literal was found at path: $.language Use 'coerceInputValues = true' in 'Json {}' builder to coerce nulls if property has a default value.

- [kotlin-serialization-basic-errors-102] It might be desired, when decoding 3rd-party JSONs, to coerce null to a default value. The corresponding feature is explained in the Coercing input values section.

- [kotlin-serialization-basic-errors-103] Serializable classes can reference other classes in their serializable properties. The referenced classes must be also marked as @Serializable .

- [kotlin-serialization-basic-errors-104] @Serializable class Project(val name: String, val owner: User) @Serializable class User(val name: String) fun main() { val owner = User("kotlin") val data = Project("kotlinx.serialization", owner) println(Json.encodeToString(data)) }

- [kotlin-serialization-basic-errors-105] When encoded to JSON it results in a nested JSON object.

- [kotlin-serialization-basic-errors-106] {"name":"kotlinx.serialization","owner":{"name":"kotlin"}}

- [kotlin-serialization-basic-errors-107] References to non-serializable classes can be marked as Transient properties , or a custom serializer can be provided for them as shown in the Serializers chapter.

- [kotlin-serialization-basic-errors-108] Kotlin Serialization is designed for encoding and decoding of plain data. It does not support reconstruction of arbitrary object graphs with repeated object references. For example, let us try to serialize an object that references the same owner instance twice.

- [kotlin-serialization-basic-errors-109] @Serializable class Project(val name: String, val owner: User, val maintainer: User) @Serializable class User(val name: String) fun main() { val owner = User("kotlin") val data = Project("kotlinx.serialization", owner, owner) println(Json.encodeToString(data)) }

- [kotlin-serialization-basic-errors-110] We simply get the owner value encoded twice.

- [kotlin-serialization-basic-errors-111] {"name":"kotlinx.serialization","owner":{"name":"kotlin"},"maintainer":{"name":"kotlin"}}

- [kotlin-serialization-basic-errors-112] Attempt to serialize a circular structure will result in stack overflow. You can use the Transient properties to exclude some references from serialization.

- [kotlin-serialization-basic-errors-113] Generic classes in Kotlin provide type-polymorphic behavior, which is enforced by Kotlin Serialization at compile-time. For example, consider a generic serializable class Box<T> .

- [kotlin-serialization-basic-errors-114] @Serializable class Box<T>(val contents: T)

- [kotlin-serialization-basic-errors-115] The Box<T> class can be used with builtin types like Int , as well as with user-defined types like Project .

- [kotlin-serialization-basic-errors-116] @Serializable class Data( val a: Box<Int>, val b: Box<Project> ) fun main() { val data = Data(Box(42), Box(Project("kotlinx.serialization", "Kotlin"))) println(Json.encodeToString(data)) }

- [kotlin-serialization-basic-errors-117] The actual type that we get in JSON depends on the actual compile-time type parameter that was specified for Box .

- [kotlin-serialization-basic-errors-118] {"a":{"contents":42},"b":{"contents":{"name":"kotlinx.serialization","language":"Kotlin"}}}

- [kotlin-serialization-basic-errors-119] If the actual generic type is not serializable a compile-time error will be produced.

- [kotlin-serialization-basic-errors-120] The names of the properties used in encoded representation, JSON in our examples, are the same as their names in the source code by default. The name that is used for serialization is called a serial name , and can be changed using the @SerialName annotation. For example, we can have a language property in the source with an abbreviated serial name.

- [kotlin-serialization-basic-errors-121] @SerialName

- [kotlin-serialization-basic-errors-122] @Serializable class Project(val name: String, @SerialName("lang") val language: String) fun main() { val data = Project("kotlinx.serialization", "Kotlin") println(Json.encodeToString(data)) }

- [kotlin-serialization-basic-errors-123] Now we see that an abbreviated name lang is used in the JSON output.

- [kotlin-serialization-basic-errors-124] {"name":"kotlinx.serialization","lang":"Kotlin"}

- [kotlin-serialization-basic-errors-125] The next chapter covers Builtin classes .
