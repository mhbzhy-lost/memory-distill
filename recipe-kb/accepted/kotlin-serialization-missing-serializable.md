---
id: kotlin-serialization-missing-serializable
kind: debug-recipe
status: accepted
stack:
- kotlin
- android
failure_class: kotlin/serialization
symptoms:
- Kotlin serialization fails because Serializer for class is not found; the class
  is not marked @Serializable
fingerprints:
- Serializer for class
- is not found
- marked as @Serializable
- MissingFieldException
- JsonDecodingException
first_checks:
- Check whether the class is annotated with @Serializable
- Check whether the kotlinx.serialization compiler plugin is applied in the build
- Check whether all non-nullable fields have values in the JSON input
do_not:
- Do not pass a class without @Serializable to Json.encodeToString or decodeFromString
- Do not make nullable fields non-nullable to fix MissingFieldException; handle the
  missing value explicitly
evidence_needed:
- Capture the compile or runtime error showing the class name that is missing @Serializable
- Identify the JSON input that triggers the decode failure
minimal_fix_scope:
- The class definition needing @Serializable annotation
- The build.gradle(.kts) serialization plugin configuration
validation_ladder:
- Add @Serializable annotation and verify compile succeeds
- Decode a sample JSON input and verify all fields are correctly populated
- Run the serialization unit test for the affected class
regression_guard:
- Add a serialization test asserting round-trip encode/decode for the affected class
evidence_refs:
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-32
  short_excerpt: 'Exception in thread "main" kotlinx.serialization.SerializationException:
    Serializer for class ''Project'' is not found. Please ensure that class is marked
    as ''@Serializable'' and that the serialization compiler plugin is applied.'
  quote_hash: sha256:6c715e483212b8fd54244067d639dd9e4b9316e1f1ec9355f0090fb640a81551
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-33
  short_excerpt: Serializable classes have to be explicitly marked. Kotlin Serialization
    does not use reflection, so you cannot accidentally deserialize a class which
    was not supposed to be serializable. We fix it by adding the @Serializable annotation.
  quote_hash: sha256:f33f1964b00dc9ec394875c4e34e210b9aa64b251fbfde7336b6630264af6cea
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-34
  short_excerpt: '@Serializable'
  quote_hash: sha256:b94554f75d3c6c3eeaae57a0f1f8f1465cada673ad73f82f859c41ef44999a62
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-35
  short_excerpt: '@Serializable class Project(val name: String, val language: String)
    fun main() { val data = Project("kotlinx.serialization", "Kotlin") println(Json.encodeToString(data))
    }'
  quote_hash: sha256:5ea48db5043e3ca69f51a18d204d90871a5be2b50fe1b939cc6ba6b0485c8a12
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-36
  short_excerpt: The @Serializable annotation instructs the Kotlin Serialization plugin
    to automatically generate and hook up a serializer for this class. Now the output
    of the example is the corresponding JSON.
  quote_hash: sha256:472f9a2ca02d2dd821708627fb865b08f236c0f7205be165b992d293f8553836
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-41
  short_excerpt: '@Serializable data class Project(val name: String, val language:
    String) fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization","language":"Kotlin"}
    """) println(data) }'
  quote_hash: sha256:f075d4916cf176c391c8bfbd18a4974b54897325d5c56954acc739aed605dc9a
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-45
  short_excerpt: This section goes into more details on how different @Serializable
    classes are handled.
  quote_hash: sha256:ceea0738bdee2a5480852bbe3f22488c0d76bdb1b1707ae8fdc60aeef5c59cc4
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-47
  short_excerpt: '@Serializable class Project( // name is a property with backing
    field -- serialized var name: String ) { var stars: Int = 0 // property with a
    backing field -- serialized val path: String // getter only, no backing field
    -- not serialized get() = "kotlin/$name" var id by ::name // delegated property
    -- not serialized } fun main() { val data = Project("kotlinx.serialization").apply
    { stars = 9000 } println(Json.encodeToString(data)) }'
  quote_hash: sha256:3fd5bdf283226427e8d0c859470891e916d6e9913669603602dab13bc152397a
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-51
  short_excerpt: '@Serializable class Project(path: String) { val owner: String =
    path.substringBefore(''/'') val name: String = path.substringAfter(''/'') }'
  quote_hash: sha256:e70150c8d10873a15628f5793211056a9b9dbf80ba7aec7c081af8329dc65a27
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-52
  short_excerpt: This class does not compile because the @Serializable annotation
    requires that all parameters of the class's primary constructor be properties.
    A simple workaround is to define a private primary constructor with the class's
    properties, and turn the constructor we wanted into the secondary one.
  quote_hash: sha256:7e77341cd2ec9b594881256e82ef923c89ef7c9342285ee2490ad84484984523
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-53
  short_excerpt: '@Serializable class Project private constructor(val owner: String,
    val name: String) { constructor(path: String) : this( owner = path.substringBefore(''/''),
    name = path.substringAfter(''/'') ) val path: String get() = "$owner/$name" }'
  quote_hash: sha256:073f452f86bf2ff6fcb0185878673e3a48f0b7a9904811471a20e5e09dce51ba
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-59
  short_excerpt: '@Serializable class Project(val name: String) { init { require(name.isNotEmpty())
    { "name cannot be empty" } } }'
  quote_hash: sha256:2b1bf6a506cd8b5939c5b99468b78f8c24e8f2cae06900c0436776e467041c90
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-65
  short_excerpt: '@Serializable data class Project(val name: String, val language:
    String) fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization"}
    """) println(data) }'
  quote_hash: sha256:0ff9c5baa8398c2b0e999f690e4417ca791bb32b321c13d64dbb4dc6249ea047
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-67
  short_excerpt: 'Exception in thread "main" kotlinx.serialization.MissingFieldException:
    Field ''language'' is required for type with serial name ''example.exampleClasses04.Project'',
    but it was missing at path: $'
  quote_hash: sha256:9cb313d8452e404528fef2a78f1845c1259607a8c74513d4b612f7e24906271c
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-69
  short_excerpt: '@Serializable data class Project(val name: String, val language:
    String = "Kotlin") fun main() { val data = Json.decodeFromString<Project>("""
    {"name":"kotlinx.serialization"} """) println(data) }'
  quote_hash: sha256:8f1196f5e361c1b88c4744b3b31168754b302b8fdb44d86e775439032becad37
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-72
  short_excerpt: 'fun computeLanguage(): String { println("Computing") return "Kotlin"
    } @Serializable data class Project(val name: String, val language: String = computeLanguage())
    fun main() { val data = Json.decodeFromString<Project>(""" {"name":"kotlinx.serialization","language":"Kotlin"}
    """) println(data) }'
  quote_hash: sha256:032b999fa6a11a92d4e83471f3ceea24d072e9c8d5149a2044a5f9427ee0c5f4
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-76
  short_excerpt: '@Serializable data class Project(val name: String, @Required val
    language: String = "Kotlin") fun main() { val data = Json.decodeFromString<Project>("""
    {"name":"kotlinx.serialization"} """) println(data) }'
  quote_hash: sha256:d059c8b5483859c3929c8c9479d4b12fc4db60f266ccd866b0436bd8aba2f8c1
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-78
  short_excerpt: 'Exception in thread "main" kotlinx.serialization.MissingFieldException:
    Field ''language'' is required for type with serial name ''example.exampleClasses07.Project'',
    but it was missing at path: $'
  quote_hash: sha256:dab41a892c29d266d420d81fc7fb72485f6a0c0afe538cde5967807e5b7ec554
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-81
  short_excerpt: '@Serializable data class Project(val name: String, @Transient val
    language: String = "Kotlin") fun main() { val data = Json.decodeFromString<Project>("""
    {"name":"kotlinx.serialization","language":"Kotlin"} """) println(data) }'
  quote_hash: sha256:3e459af604c563bb71de7d72808d92160ae9568b323130a4b849503c0905025e
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-83
  short_excerpt: 'Exception in thread "main" kotlinx.serialization.json.JsonDecodingException:
    Unexpected JSON token at offset 42: Encountered an unknown key ''language'' at
    path: $ Use ''ignoreUnknownKeys = true'' in ''Json {}'' builder or ''@JsonIgnoreUnknownKeys''
    annotation to ignore unknown keys.'
  quote_hash: sha256:7bbd07a7bb7104be5eb34815a4ca5c68abf34952c6b4eb937d3306006251e009
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-84
  short_excerpt: The 'ignoreUnknownKeys' feature is explained in the Ignoring Unknown
    Keys section section.
  quote_hash: sha256:185c78af2237694a88335657de212a28f66216eda9e9544a3ea1de7bc4e61b6e
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-86
  short_excerpt: '@Serializable data class Project(val name: String, val language:
    String = "Kotlin") fun main() { val data = Project("kotlinx.serialization") println(Json.encodeToString(data))
    }'
  quote_hash: sha256:b3b9a95fcb3ef425d20dd006da50c9ed81633102f00fe63e2e86c3f7f4df1a20
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-90
  short_excerpt: '@Serializable data class Project( val name: String, @EncodeDefault
    val language: String = "Kotlin" )'
  quote_hash: sha256:c3fa9563ea9ee53a73c486a4676933fa41d6ac23d9d965bfcf08dcec9c5f8ff2
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-92
  short_excerpt: '@Serializable data class User( val name: String, @EncodeDefault(NEVER)
    val projects: List<Project> = emptyList() ) fun main() { val userA = User("Alice",
    listOf(Project("kotlinx.serialization"))) val userB = User("Bob") println(Json.encodeToString(userA))
    println(Json.encodeToString(userB)) }'
  quote_hash: sha256:1f1c953e8257abae36c53e5ba70f89428ada337027f46bcfd2f2db64e7da33c2
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-96
  short_excerpt: '@Serializable class Project(val name: String, val renamedTo: String?
    = null) fun main() { val data = Project("kotlinx.serialization") println(Json.encodeToString(data))
    }'
  quote_hash: sha256:a8b5766d57381f7bedbcdad6d4ccef7a7c13748a18f7950ee186a54c41944614
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-99
  short_excerpt: '@Serializable data class Project(val name: String, val language:
    String = "Kotlin") fun main() { val data = Json.decodeFromString<Project>("""
    {"name":"kotlinx.serialization","language":null} """) println(data) }'
  quote_hash: sha256:c7ade5b677ca9742f95fcd9d86d5e928942181905ae524e580a77a2525219b2a
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-101
  short_excerpt: 'Exception in thread "main" kotlinx.serialization.json.JsonDecodingException:
    Unexpected JSON token at offset 52: Expected string literal but ''null'' literal
    was found at path: $.language Use ''coerceInputValues = true'' in ''Json {}''
    builder to coerce nulls if property has a default value.'
  quote_hash: sha256:040d40747d9c5108b2311bbfeceaf0b91e9b264e02deaadbe71f1cd4d2d33dc3
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-103
  short_excerpt: Serializable classes can reference other classes in their serializable
    properties. The referenced classes must be also marked as @Serializable .
  quote_hash: sha256:c5c4f1329a00b7483828bf9564aebc94a24064aa1409ed5b58f99e3ce3cce5fa
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-104
  short_excerpt: '@Serializable class Project(val name: String, val owner: User) @Serializable
    class User(val name: String) fun main() { val owner = User("kotlin") val data
    = Project("kotlinx.serialization", owner) println(Json.encodeToString(data)) }'
  quote_hash: sha256:d433c959add2d63382934b119d7f17468e6d324ba8721092527ff0b8a511978d
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-109
  short_excerpt: '@Serializable class Project(val name: String, val owner: User, val
    maintainer: User) @Serializable class User(val name: String) fun main() { val
    owner = User("kotlin") val data = Project("kotlinx.serialization", owner, owner)
    println(Json.encodeToString(data)) }'
  quote_hash: sha256:801b7c066cb2b3b8519a5c60d7ddf3427a0d92868fe9e9893313c4c02bf98ed9
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-114
  short_excerpt: '@Serializable class Box<T>(val contents: T)'
  quote_hash: sha256:2073cf87ee31fe771a8283ac4e70944259f9b8ef24c371e7e8c6c40fac5462fc
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-116
  short_excerpt: '@Serializable class Data( val a: Box<Int>, val b: Box<Project> )
    fun main() { val data = Data(Box(42), Box(Project("kotlinx.serialization", "Kotlin")))
    println(Json.encodeToString(data)) }'
  quote_hash: sha256:2bb01055631551562bfcf4074beb79d1e5e5188802cd7a683469fdb7d03cfdf6
- source_id: kotlin-serialization-basic-errors
  url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  final_url: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
  source_type: library_doc
  captured_at: '2026-05-26T13:49:14.876449Z'
  section_anchor: root
  span_id: kotlin-serialization-basic-errors-122
  short_excerpt: '@Serializable class Project(val name: String, @SerialName("lang")
    val language: String) fun main() { val data = Project("kotlinx.serialization",
    "Kotlin") println(Json.encodeToString(data)) }'
  quote_hash: sha256:663d54defa1bff51124915d748464e962f3b9dbdc1f874eb5d02b5d22203b714
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# kotlin-serialization-missing-serializable

## Failure Class
kotlin/serialization

## Symptoms
- Kotlin serialization fails because Serializer for class is not found; the class is not marked @Serializable

## Fingerprints
- Serializer for class
- is not found
- marked as @Serializable
- MissingFieldException
- JsonDecodingException

## First Checks
- Check whether the class is annotated with @Serializable
- Check whether the kotlinx.serialization compiler plugin is applied in the build
- Check whether all non-nullable fields have values in the JSON input

## Do Not Patch Yet
- Do not pass a class without @Serializable to Json.encodeToString or decodeFromString
- Do not make nullable fields non-nullable to fix MissingFieldException; handle the missing value explicitly

## Evidence Needed
- Capture the compile or runtime error showing the class name that is missing @Serializable
- Identify the JSON input that triggers the decode failure

## Minimal Fix Scope
- The class definition needing @Serializable annotation
- The build.gradle(.kts) serialization plugin configuration

## Validation Ladder
- Add @Serializable annotation and verify compile succeeds
- Decode a sample JSON input and verify all fields are correctly populated
- Run the serialization unit test for the affected class

## Regression Guard
- Add a serialization test asserting round-trip encode/decode for the affected class

## Reviewer Notes
