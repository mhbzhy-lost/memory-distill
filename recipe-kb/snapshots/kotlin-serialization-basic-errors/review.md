# 快照人审：kotlin-serialization-basic-errors

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
- 最终 URL: https://raw.githubusercontent.com/Kotlin/kotlinx.serialization/master/docs/basic-serialization.md
- 来源类型: library_doc
- 采集时间: 2026-05-26T13:49:14.876449Z
- HTTP 状态: 200
- 内容哈希: sha256:6b22e35bb77a8c27c5bc5ee567b12bb4e0ac977f2f8dc4247ee3d0b9ca7bad04
- 技术栈: kotlin, android
- 抽取段落数: 125

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 125
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 6/6 条 expected_failure_hints

## 预期线索命中
- `Serializer for class ... is not found`
  - [kotlin-serialization-basic-errors-32] Exception in thread "main" kotlinx.serialization.SerializationException: Serializer for class 'Project' is not found. Please ensure that class is marked as '@Serializable' and that the serialization compiler plugin is...
  - [kotlin-serialization-basic-errors-36] The @Serializable annotation instructs the Kotlin Serialization plugin to automatically generate and hook up a serializer for this class. Now the output of the example is the corresponding JSON.
- `Please ensure that class is marked as '@Serializable'`
  - [kotlin-serialization-basic-errors-32] Exception in thread "main" kotlinx.serialization.SerializationException: Serializer for class 'Project' is not found. Please ensure that class is marked as '@Serializable' and that the serialization compiler plugin is...
- `MissingFieldException`
  - [kotlin-serialization-basic-errors-67] Exception in thread "main" kotlinx.serialization.MissingFieldException: Field 'language' is required for type with serial name 'example.exampleClasses04.Project', but it was missing at path: $
  - [kotlin-serialization-basic-errors-78] Exception in thread "main" kotlinx.serialization.MissingFieldException: Field 'language' is required for type with serial name 'example.exampleClasses07.Project', but it was missing at path: $
- `JsonDecodingException Unexpected JSON token`
  - [kotlin-serialization-basic-errors-83] Exception in thread "main" kotlinx.serialization.json.JsonDecodingException: Unexpected JSON token at offset 42: Encountered an unknown key 'language' at path: $ Use 'ignoreUnknownKeys = true' in 'Json {}' builder or...
  - [kotlin-serialization-basic-errors-101] Exception in thread "main" kotlinx.serialization.json.JsonDecodingException: Unexpected JSON token at offset 52: Expected string literal but 'null' literal was found at path: $.language Use 'coerceInputValues = true'...
- `Encountered an unknown key`
  - [kotlin-serialization-basic-errors-83] Exception in thread "main" kotlinx.serialization.json.JsonDecodingException: Unexpected JSON token at offset 42: Encountered an unknown key 'language' at path: $ Use 'ignoreUnknownKeys = true' in 'Json {}' builder or...
- `Expected string literal but 'null' literal was found`
  - [kotlin-serialization-basic-errors-101] Exception in thread "main" kotlinx.serialization.json.JsonDecodingException: Unexpected JSON token at offset 52: Expected string literal but 'null' literal was found at path: $.language Use 'coerceInputValues = true'...

## 段落样例
- [kotlin-serialization-basic-errors-1] Basic Serialization
- [kotlin-serialization-basic-errors-2] This is the first chapter of the Kotlin Serialization Guide . This chapter shows the basic use of Kotlin Serialization and explains its core concepts.
- [kotlin-serialization-basic-errors-3] Table of contents
- [kotlin-serialization-basic-errors-4] Basics JSON encoding JSON decoding
- [kotlin-serialization-basic-errors-5] JSON encoding
- [kotlin-serialization-basic-errors-6] JSON decoding
- [kotlin-serialization-basic-errors-7] Serializable classes Backing fields are serialized Constructor properties requirement Data validation Optional properties Optional property initializer call Required properties Transient properties Defaults are not en...
- [kotlin-serialization-basic-errors-8] Backing fields are serialized

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
