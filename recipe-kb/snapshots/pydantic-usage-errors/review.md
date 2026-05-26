# 快照人审：pydantic-usage-errors

## 快照质量检查
- 来源 URL: https://docs.pydantic.dev/latest/errors/usage_errors/
- 最终 URL: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
- 来源类型: official_error_doc
- 采集时间: 2026-05-26T08:42:53.083772Z
- HTTP 状态: 200
- 内容哈希: sha256:cdd9c859d7d6ba441b6bc8139592b7ec5680af93ba53e9fdab60c9030c7c6641
- 技术栈: pydantic
- 抽取段落数: 201

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 201
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 4/4 条 expected_failure_hints

## 预期线索命中
- `PydanticUserError`
  - [pydantic-usage-errors-4] from typing import ForwardRef from pydantic import BaseModel, PydanticUserError UndefinedType = ForwardRef('UndefinedType') class Foobar(BaseModel): a: UndefinedType try: Foobar(a=1) except PydanticUserError as exc_in...
  - [pydantic-usage-errors-6] from typing import Optional from pydantic import BaseModel, PydanticUserError class Foo(BaseModel): a: Optional['Bar'] = None try: # this doesn't work, see raised error foo = Foo(a={'b': {'a': None}}) except PydanticU...
  - [pydantic-usage-errors-13] from pydantic import BaseModel, PydanticUserError try: class Model(BaseModel): @classmethod def __modify_schema__(cls, field_schema): field_schema.update(examples=['example']) except PydanticUserError as exc_info: ass...
- `class-not-fully-defined`
  - [pydantic-usage-errors-4] from typing import ForwardRef from pydantic import BaseModel, PydanticUserError UndefinedType = ForwardRef('UndefinedType') class Foobar(BaseModel): a: UndefinedType try: Foobar(a=1) except PydanticUserError as exc_in...
  - [pydantic-usage-errors-6] from typing import Optional from pydantic import BaseModel, PydanticUserError class Foo(BaseModel): a: Optional['Bar'] = None try: # this doesn't work, see raised error foo = Foo(a={'b': {'a': None}}) except PydanticU...
- `decorator-missing-field`
  - [pydantic-usage-errors-28] from typing import Any from pydantic import BaseModel, PydanticUserError, field_validator try: class Model(BaseModel): a: str @field_validator('b') def check_b(cls, v: Any): return v except PydanticUserError as exc_in...
- `model_rebuild`
  - [pydantic-usage-errors-7] For BaseModel subclasses, it can be fixed by defining the type and then calling .model_rebuild() :
  - [pydantic-usage-errors-8] from typing import Optional from pydantic import BaseModel class Foo(BaseModel): a: Optional['Bar'] = None class Bar(BaseModel): b: 'Foo' Foo.model_rebuild() foo = Foo(a={'b': {'a': None}})
  - [pydantic-usage-errors-87] from pydantic import BaseModel, PydanticUndefinedAnnotation class Model(BaseModel): a: 'B' # noqa F821 try: Model.model_rebuild() except PydanticUndefinedAnnotation as exc_info: assert exc_info.code == 'undefined-anno...

## 段落样例
- [pydantic-usage-errors-1] Pydantic attempts to provide useful errors. The following sections provide details on common errors developers may encounter when working with Pydantic, along with suggestions for addressing the error condition.
- [pydantic-usage-errors-2] Class not fully defined
- [pydantic-usage-errors-3] This error is raised when a type referenced in an annotation of a pydantic-validated type (such as a subclass of BaseModel , or a pydantic dataclass ) is not defined:
- [pydantic-usage-errors-4] from typing import ForwardRef from pydantic import BaseModel, PydanticUserError UndefinedType = ForwardRef('UndefinedType') class Foobar(BaseModel): a: UndefinedType try: Foobar(a=1) except PydanticUserError as exc_in...
- [pydantic-usage-errors-5] Or when the type has been defined after usage:
- [pydantic-usage-errors-6] from typing import Optional from pydantic import BaseModel, PydanticUserError class Foo(BaseModel): a: Optional['Bar'] = None try: # this doesn't work, see raised error foo = Foo(a={'b': {'a': None}}) except PydanticU...
- [pydantic-usage-errors-7] For BaseModel subclasses, it can be fixed by defining the type and then calling .model_rebuild() :
- [pydantic-usage-errors-8] from typing import Optional from pydantic import BaseModel class Foo(BaseModel): a: Optional['Bar'] = None class Bar(BaseModel): b: 'Foo' Foo.model_rebuild() foo = Foo(a={'b': {'a': None}})

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
