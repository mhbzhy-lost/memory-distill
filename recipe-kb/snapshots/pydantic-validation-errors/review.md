# 快照人审：pydantic-validation-errors

## 快照质量检查
- 来源 URL: https://docs.pydantic.dev/latest/errors/validation_errors/
- 最终 URL: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
- 来源类型: official_error_doc
- 采集时间: 2026-05-26T08:42:53.083772Z
- HTTP 状态: 200
- 内容哈希: sha256:387338daf573c75d2fe263ed12dcb764ab2e1c22ee06ab9bc74aa388bbdad769
- 技术栈: pydantic
- 抽取段落数: 322

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 322
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 5/5 条 expected_failure_hints

## 预期线索命中
- `ValidationError`
  - [pydantic-validation-errors-4] from typing import NamedTuple from pydantic import BaseModel, ValidationError class MyNamedTuple(NamedTuple): x: int class MyModel(BaseModel): field: MyNamedTuple try: MyModel.model_validate({'field': 'invalid'}) exce...
  - [pydantic-validation-errors-7] from pydantic import BaseModel, ValidationError, field_validator class Model(BaseModel): x: int @field_validator('x') @classmethod def force_x_positive(cls, v): assert v > 0 return v try: Model(x=-1) except Validation...
  - [pydantic-validation-errors-10] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: bool Model(x='true') # OK try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'bool_parsing'
- `int_parsing`
  - [pydantic-validation-errors-140] int_parsing
  - [pydantic-validation-errors-142] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: int try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'int_parsing'
  - [pydantic-validation-errors-143] int_parsing_size
- `bool_type`
  - [pydantic-validation-errors-11] bool_type
  - [pydantic-validation-errors-13] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: bool try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'bool_type'
- `missing`
  - [pydantic-validation-errors-185] missing
  - [pydantic-validation-errors-186] This error is raised when there are required fields missing from the input value:
  - [pydantic-validation-errors-187] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: str try: Model() except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'missing'
- `greater_than`
  - [pydantic-validation-errors-99] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): a: int = Field(gt=10) b: int = Field(default_factory=lambda data: data['a']) try: Model(a=1) except ValidationError as exc: print(exc) """...
  - [pydantic-validation-errors-131] greater_than
  - [pydantic-validation-errors-133] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: int = Field(gt=10) try: Model(x=10) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'greater_than'

## 段落样例
- [pydantic-validation-errors-1] Pydantic attempts to provide useful validation errors. Below are details on common validation errors users may encounter when working with pydantic, together with some suggestions on how to fix them.
- [pydantic-validation-errors-2] arguments_type
- [pydantic-validation-errors-3] This error is raised when an object that would be passed as arguments to a function during validation is not a tuple , list , or dict . Because NamedTuple uses function calls in its implementation, that is one way to...
- [pydantic-validation-errors-4] from typing import NamedTuple from pydantic import BaseModel, ValidationError class MyNamedTuple(NamedTuple): x: int class MyModel(BaseModel): field: MyNamedTuple try: MyModel.model_validate({'field': 'invalid'}) exce...
- [pydantic-validation-errors-5] assertion_error
- [pydantic-validation-errors-6] This error is raised when a failing assert statement is encountered during validation:
- [pydantic-validation-errors-7] from pydantic import BaseModel, ValidationError, field_validator class Model(BaseModel): x: int @field_validator('x') @classmethod def force_x_positive(cls, v): assert v > 0 return v try: Model(x=-1) except Validation...
- [pydantic-validation-errors-8] bool_parsing

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
