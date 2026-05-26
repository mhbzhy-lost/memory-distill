---
id: pydantic-class-not-fully-defined
kind: debug-recipe
status: accepted
stack:
- pydantic
failure_class: pydantic/model-schema
symptoms:
- PydanticUserError class-not-fully-defined raised when instantiating a model that
  references a forward or post-defined type
fingerprints:
- class-not-fully-defined
- PydanticUserError
- model_rebuild
- ForwardRef
- decorator-missing-field
first_checks:
- Check whether the referenced type is defined before the model class is instantiated
  or validated
- Check whether model_rebuild() is called after the forward-referenced type is defined
- Check whether @field_validator field names match actual model fields
do_not:
- Do not define a BaseModel subclass with Optional['ForwardRef'] without calling model_rebuild()
  after the target is defined
- Do not suppress the class-not-fully-defined error; it means the schema is incomplete
evidence_needed:
- Capture the PydanticUserError.message and PydanticUserError.code
- Identify the ForwardRef or type annotation that is missing
minimal_fix_scope:
- The model class with the forward-referenced type
- The type definition order or model_rebuild() call site
validation_ladder:
- Instantiate the model after adding model_rebuild() and verify no PydanticUserError
- Verify nested model validation works with forward references
- Run the model unit test for the affected forward-reference path
regression_guard:
- Add a model test that validates forward-referenced nested models after model_rebuild()
evidence_refs:
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-4
  short_excerpt: 'from typing import ForwardRef from pydantic import BaseModel, PydanticUserError
    UndefinedType = ForwardRef(''UndefinedType'') class Foobar(BaseModel): a: UndefinedType
    try: Foobar(a=1) except PydanticUserError as exc_info: assert exc_info.code ==
    ''class-not-fully-defined'''
  quote_hash: sha256:db785fb81d3de485884d8c49fc5a167bf1f0d07c3c12c66da8789bc073c350a1
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-6
  short_excerpt: 'from typing import Optional from pydantic import BaseModel, PydanticUserError
    class Foo(BaseModel): a: Optional[''Bar''] = None try: # this doesn''t work, see
    raised error foo = Foo(a={''b'': {''a'': None}}) except PydanticUserError as exc_info:
    assert exc_info.code == ''class-not-fully-defined'' class Bar(BaseModel): b: ''Foo''
    # this works, though foo = Foo(a={''b'': {''a'': None}})'
  quote_hash: sha256:e9880bbe2bde25dd6a1866db86cda4da44a9dd01ac0878d1f45cc7d40a78b08b
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-7
  short_excerpt: 'For BaseModel subclasses, it can be fixed by defining the type and
    then calling .model_rebuild() :'
  quote_hash: sha256:e6047d1a9bc8eb3e33899add787089dc8c3e418cc825cc19c316f6d52d242b52
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-8
  short_excerpt: 'from typing import Optional from pydantic import BaseModel class
    Foo(BaseModel): a: Optional[''Bar''] = None class Bar(BaseModel): b: ''Foo'' Foo.model_rebuild()
    foo = Foo(a={''b'': {''a'': None}})'
  quote_hash: sha256:d2fdf1c006e7af6cd443aca7824c60b42e7d47c4dce96d0abe22af815c2bce4f
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-13
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError try: class Model(BaseModel):
    @classmethod def __modify_schema__(cls, field_schema): field_schema.update(examples=[''example''])
    except PydanticUserError as exc_info: assert exc_info.code == ''custom-json-schema'''
  quote_hash: sha256:93d77864925ed498db3e6aaa3926a05a9889aaa39e10e0b414ddd205e63fa3a8
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-18
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, field_validator
    try: class Model(BaseModel): a: str b: str @field_validator([''a'', ''b'']) @classmethod
    def check_fields(cls, v): return v except PydanticUserError as exc_info: assert
    exc_info.code == ''decorator-invalid-fields'''
  quote_hash: sha256:a09b953a2d418fe650d4e58db92a82621f7e86229ee0868ff4ae3e9f5df044ea
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-23
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, field_validator
    try: class Model(BaseModel): a: str @field_validator @classmethod def checker(cls,
    v): return v except PydanticUserError as exc_info: assert exc_info.code == ''decorator-missing-arguments'''
  quote_hash: sha256:e012cf27b876cc2a67ab0f61d9e748e3f16d5dd6399d3f01aaf9b4d81989dd55
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-24
  short_excerpt: At least one field name (and optionally other field names and keyword
    arguments) should be provided.
  quote_hash: sha256:a88979109ecb881549294bc2e84d805ad3a906bc982c5f850fed309b10fdbb9b
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-28
  short_excerpt: 'from typing import Any from pydantic import BaseModel, PydanticUserError,
    field_validator try: class Model(BaseModel): a: str @field_validator(''b'') def
    check_b(cls, v: Any): return v except PydanticUserError as exc_info: assert exc_info.code
    == ''decorator-missing-field'''
  quote_hash: sha256:23b86710b48a80a736a17337c958c8af6c7853577079aec9ad4e13b445716774
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-33
  short_excerpt: 'from typing import Literal, Union from pydantic import BaseModel,
    Field, PydanticUserError class Cat(BaseModel): c: str class Dog(BaseModel): pet_type:
    Literal[''dog''] d: str try: class Model(BaseModel): pet: Union[Cat, Dog] = Field(discriminator=''pet_type'')
    number: int except PydanticUserError as exc_info: assert exc_info.code == ''discriminator-no-field'''
  quote_hash: sha256:6b41bd2b6938bbbf578df4066834bd73b3096ab262501eedc827d97d75234f67
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-36
  short_excerpt: 'from typing import Literal, Union from pydantic import AliasChoices,
    BaseModel, Field, PydanticUserError class Cat(BaseModel): pet_type: Literal[''cat'']
    = Field( validation_alias=AliasChoices(''Pet'', ''PET'') ) c: str class Dog(BaseModel):
    pet_type: Literal[''dog''] d: str try: class Model(BaseModel): pet: Union[Cat,
    Dog] = Field(discriminator=''pet_type'') number: int except PydanticUserError
    as exc_info: assert exc_info.code == ''discriminator-alias-type'''
  quote_hash: sha256:f1b212d1bbd96a7ea6a10f148f8055887dbcc0783fb81b649bf76d122c9ddb11
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-39
  short_excerpt: 'from typing import Literal, Union from pydantic import BaseModel,
    Field, PydanticUserError class Cat(BaseModel): pet_type: int c: str class Dog(BaseModel):
    pet_type: Literal[''dog''] d: str try: class Model(BaseModel): pet: Union[Cat,
    Dog] = Field(discriminator=''pet_type'') number: int except PydanticUserError
    as exc_info: assert exc_info.code == ''discriminator-needs-literal'''
  quote_hash: sha256:89a87be7f98589a19397f909ba18ca84d680076cc16ace7eaf9521fcd0d2ecc5
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-42
  short_excerpt: 'from typing import Literal, Union from pydantic import BaseModel,
    Field, PydanticUserError class Cat(BaseModel): pet_type: Literal[''cat''] = Field(validation_alias=''PET'')
    c: str class Dog(BaseModel): pet_type: Literal[''dog''] = Field(validation_alias=''Pet'')
    d: str try: class Model(BaseModel): pet: Union[Cat, Dog] = Field(discriminator=''pet_type'')
    number: int except PydanticUserError as exc_info: assert exc_info.code == ''discriminator-alias'''
  quote_hash: sha256:894c8e7f5a0ea6ff6a422f078267f37dc04f3f530b2bbe9215107b91af4d97ca
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-46
  short_excerpt: 'from typing import Literal, Union from pydantic import BaseModel,
    Field, PydanticUserError, field_validator class Cat(BaseModel): pet_type: Literal[''cat'']
    @field_validator(''pet_type'', mode=''before'') @classmethod def validate_pet_type(cls,
    v): if v == ''kitten'': return ''cat'' return v class Dog(BaseModel): pet_type:
    Literal[''dog''] try: class Model(BaseModel): pet: Union[Cat, Dog] = Field(discriminator=''pet_type'')
    number: int except PydanticUserError as exc_info: assert exc_info.code == ''discriminator-validator'''
  quote_hash: sha256:13aafff538a58761bdd1ae4e1af5c253902ac71b44d83a8d7e0d3a11f86d3ac3
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-51
  short_excerpt: 'from typing import Annotated, Union from pydantic import BaseModel,
    Discriminator, PydanticUserError, Tag def model_x_discriminator(v): if isinstance(v,
    str): return ''str'' if isinstance(v, (dict, BaseModel)): return ''model'' # tag
    missing for both union choices try: class DiscriminatedModel(BaseModel): x: Annotated[
    Union[str, ''DiscriminatedModel''], Discriminator(model_x_discriminator), ] except
    PydanticUserError as exc_info: assert exc_info.code == ''callable-discriminator-no-tag''
    # tag missing for `''DiscriminatedModel''` union choice try: class DiscriminatedModel(BaseModel):
    x: Annotated[ Union'
  quote_hash: sha256:1b04828b40df37e3786c73cddfbae1614dcce077c5ebb5f845a6cefc6f671322
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-56
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError class Foo(BaseModel):
    a: float try: class Bar(Foo): x: float = 12.3 a = 123.0 except PydanticUserError
    as exc_info: assert exc_info.code == ''model-field-overridden'''
  quote_hash: sha256:7a3cf01dd2adaefbc1e1c069dc41d3ce9d031911c4c176dd850cc1348fec26e0
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-59
  short_excerpt: 'from pydantic import BaseModel, Field, PydanticUserError try: class
    Model(BaseModel): a = Field(''foobar'') b = None except PydanticUserError as exc_info:
    assert exc_info.code == ''model-field-missing-annotation'''
  quote_hash: sha256:2f4fc8fba944812668f53b2603ca026d3d242ec1ec2aaf5c702865249d8e0ac4
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-66
  short_excerpt: 'from pydantic import BaseModel, ConfigDict, PydanticUserError try:
    class Model(BaseModel): model_config = ConfigDict(from_attributes=True) a: str
    class Config: from_attributes = True except PydanticUserError as exc_info: assert
    exc_info.code == ''config-both'''
  quote_hash: sha256:15e1346299de857f35c8b6c417e46be44391084b3e7ca16980373513d6f42505
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-70
  short_excerpt: 'from pydantic import BaseModel, Field, PydanticUserError try: class
    Model(BaseModel): x: str = Field(regex=''test'') except PydanticUserError as exc_info:
    assert exc_info.code == ''removed-kwargs'''
  quote_hash: sha256:7d9c5e0a6e01d2e28fa9daf84ce691fa9ec74138011e0f31a21db64decf8d4e1
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-79
  short_excerpt: 'from pydantic import BaseModel, ImportString, PydanticUserError
    class Model(BaseModel): a: ImportString try: Model.model_json_schema() except
    PydanticUserError as exc_info: assert exc_info.code == ''invalid-for-json-schema'''
  quote_hash: sha256:1575f1d6cf066bdc58614e86bf102b8e7ff8664244fb44dfa705978220373baa
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-84
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError try: BaseModel()
    except PydanticUserError as exc_info: assert exc_info.code == ''base-model-instantiated'''
  quote_hash: sha256:b61795b7d2cfd01995ecbc63dd0c3f5f18843f6a9eb78db34d3a103abc9954d2
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-87
  short_excerpt: 'from pydantic import BaseModel, PydanticUndefinedAnnotation class
    Model(BaseModel): a: ''B'' # noqa F821 try: Model.model_rebuild() except PydanticUndefinedAnnotation
    as exc_info: assert exc_info.code == ''undefined-annotation'''
  quote_hash: sha256:73ec60920d648e48e8edf628772e2e88c10aa3c96ad6e9f9f78c6fb0277586a4
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-90
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError try: class Model(BaseModel):
    x: 43 = 123 except PydanticUserError as exc_info: assert exc_info.code == ''schema-for-unknown-type'''
  quote_hash: sha256:3ea39b18c25e5a52e966351a705ac0b025d110d5afacbf88dd9f54b510911803
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-96
  short_excerpt: 'from pydantic import PydanticUserError, create_model try: create_model(''FooModel'',
    foo=(str, ''default value'', ''more'')) except PydanticUserError as exc_info:
    assert exc_info.code == ''create-model-field-definitions'''
  quote_hash: sha256:306f67a3a5f76107705db56fc1be222ad69fc89e98a00325e749f2c5714a418d
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-100
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, field_validator
    try: class Model(BaseModel): a: int = 1 @field_validator(''a'') def check_a(self,
    value): return value except PydanticUserError as exc_info: assert exc_info.code
    == ''validator-instance-method'''
  quote_hash: sha256:a3b48f24ec8c52e52389cffbd29023475a5638ae8cfd9be3393188abe9f91d75
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-103
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, field_validator
    try: class Model(BaseModel): a: int = 1 @field_validator(''a'', mode=''after'',
    json_schema_input_type=int) @classmethod def check_a(self, value): return value
    except PydanticUserError as exc_info: assert exc_info.code == ''validator-input-type'''
  quote_hash: sha256:edfcaacde1a580c3a35504d794416be4db68708e39aed479dadb223d28e2147c
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-112
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, model_serializer
    try: class MyModel(BaseModel): a: int @model_serializer def _serialize(slf, x,
    y, z): return slf except PydanticUserError as exc_info: assert exc_info.code ==
    ''model-serializer-instance-method'''
  quote_hash: sha256:a924841fe9ffcd78062a8a8130296dcb7ca3eef26b9f653cc78757b4a86c2f98
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-114
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, model_serializer
    try: class MyModel(BaseModel): a: int @model_serializer @classmethod def _serialize(self,
    x, y, z): return self except PydanticUserError as exc_info: assert exc_info.code
    == ''model-serializer-instance-method'''
  quote_hash: sha256:f7575bc93bd59c09ffb9ac4e85452c92b4f8c790cd706ba04ff12a58e111ed1d
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-121
  short_excerpt: 'import warnings from pydantic import BaseModel, PydanticUserError,
    validator warnings.filterwarnings(''ignore'', category=DeprecationWarning) try:
    class Model(BaseModel): a: int @validator(''a'') def check_a(cls, value, foo):
    return value except PydanticUserError as exc_info: assert exc_info.code == ''validator-v1-signature'''
  quote_hash: sha256:f993741cbe58d83dcefeefbb23fd63ac699626574374022eeeb6f91fbce7b176
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-124
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, field_validator
    try: class Model(BaseModel): a: str @field_validator(''a'') @classmethod def check_a(cls):
    return ''a'' except PydanticUserError as exc_info: assert exc_info.code == ''validator-signature'''
  quote_hash: sha256:e5354a7eef44471f2fa469fcf6d1cc11958653a30d6ee77f95fe8b261741c1aa
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-127
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, field_serializer
    try: class Model(BaseModel): x: int @field_serializer(''x'') def no_args(): return
    ''x'' except PydanticUserError as exc_info: assert exc_info.code == ''field-serializer-signature'''
  quote_hash: sha256:029e40bc27141edd8aed44bb0a8fedde8a1fac100feb5e33f81d1ba0cde40f1f
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-132
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, model_serializer
    try: class MyModel(BaseModel): a: int @model_serializer def _serialize(self, x,
    y, z): return self except PydanticUserError as exc_info: assert exc_info.code
    == ''model-serializer-signature'''
  quote_hash: sha256:d0e6aba32b8c9da9a6857d6d4f95e4bb571bc31e811421ebc193a81c839580aa
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-137
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, field_serializer
    try: class MyModel(BaseModel): x: int y: int @field_serializer(''x'', ''y'') def
    serializer1(v): return f''{v:,}'' @field_serializer(''x'') def serializer2(v):
    return v except PydanticUserError as exc_info: assert exc_info.code == ''multiple-field-serializers'''
  quote_hash: sha256:beeff6638a2b76f1f1b08f2cd1a3833477068bc94c576534de2f8db84378456b
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-140
  short_excerpt: 'from typing import Annotated from pydantic import BaseModel, FutureDate,
    PydanticUserError try: class Model(BaseModel): foo: Annotated[str, FutureDate()]
    except PydanticUserError as exc_info: assert exc_info.code == ''invalid-annotated-type'''
  quote_hash: sha256:6d45d3b2849b4dc8438f10c812a9c9633ee0fb89bdebaf4f34867f912086e169
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-143
  short_excerpt: 'from typing_extensions import TypedDict from pydantic import ConfigDict,
    PydanticUserError, TypeAdapter class MyTypedDict(TypedDict): x: int try: TypeAdapter(MyTypedDict,
    config=ConfigDict(strict=True)) except PydanticUserError as exc_info: assert exc_info.code
    == ''type-adapter-config-unused'''
  quote_hash: sha256:caabba7639b35d091da432089e80fee497e94421a11a23b32559c2087d5d3ace
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-148
  short_excerpt: 'from pydantic import PydanticUserError, RootModel try: class MyRootModel(RootModel):
    model_config = {''extra'': ''allow''} root: int except PydanticUserError as exc_info:
    assert exc_info.code == ''root-model-extra'''
  quote_hash: sha256:dff741230956493e2190f34543e8418cfbe08728ec1ee89910849d1b0fb340bf
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-159
  short_excerpt: 'pydantic.errors.PydanticUserError: Field a has `init=False` and
    dataclass has config setting `extra="allow"`. This combination is not allowed.'
  quote_hash: sha256:a608c2e54ce748c66ddc1156ab936ec677505140be689c80343ce383d23ca0d7
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-161
  short_excerpt: The init=False and init_var=True settings are mutually exclusive.
    Doing so results in the PydanticUserError shown in the example below.
  quote_hash: sha256:9c2ccfb1eaf0fc87404932a93a1e3e77904518fd8599e5c5f286a2541e56882f
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-162
  short_excerpt: 'from pydantic import Field from pydantic.dataclasses import dataclass
    @dataclass class Foo: bar: str = Field(init=False, init_var=True) """ pydantic.errors.PydanticUserError:
    Dataclass field bar has init=False and init_var=True, but these are mutually exclusive.
    """'
  quote_hash: sha256:229d74e696aca7467253087dec84d016ecdcd6c3e40e46d322be236ec803579b
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-165
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError try: class Model(BaseModel):
    model_config: str except PydanticUserError as exc_info: assert exc_info.code ==
    ''model-config-invalid-field-name'''
  quote_hash: sha256:c7ae6b3f910b790cd8737df3ff5313e3048d0f04c4c21f074d9ae760059f775d
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-168
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError, with_config try:
    @with_config({''allow_inf_nan'': True}) class Model(BaseModel): bar: str except
    PydanticUserError as exc_info: assert exc_info.code == ''with-config-on-model'''
  quote_hash: sha256:657eb35941aa4b983655b1956fc0553bfceab1fc64a011523cec85d663531f57
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-171
  short_excerpt: 'from pydantic import BaseModel, PydanticUserError from pydantic.dataclasses
    import dataclass try: @dataclass class Model(BaseModel): bar: str except PydanticUserError
    as exc_info: assert exc_info.code == ''dataclass-on-model'''
  quote_hash: sha256:7461200dd76bd8693f0e8d06d7f7a8247b29ac9037811561b9992e5ef9d9e099
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-176
  short_excerpt: 'from pydantic import PydanticUserError, validate_call # error try:
    class A: @validate_call @classmethod def f1(cls): ... except PydanticUserError
    as exc_info: assert exc_info.code == ''validate-call-type'' # correct @classmethod
    @validate_call def f2(cls): ...'
  quote_hash: sha256:340eaae3867ed9437e1c28413a50d945a916ad6e1fcc9ed2cfb81a2dddf291d4
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-179
  short_excerpt: 'from pydantic import PydanticUserError, validate_call # error try:
    @validate_call class A1: ... except PydanticUserError as exc_info: assert exc_info.code
    == ''validate-call-type'' # correct class A2: @validate_call def __init__(self):
    ... @validate_call def __new__(cls): ...'
  quote_hash: sha256:f7aaf29b782964987d1bea301e191a21f55aab87ac7963ff7c3275e053263268
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-182
  short_excerpt: 'from pydantic import PydanticUserError, validate_call # error try:
    class A1: def __call__(self): ... validate_call(A1()) except PydanticUserError
    as exc_info: assert exc_info.code == ''validate-call-type'' # correct class A2:
    @validate_call def __call__(self): ...'
  quote_hash: sha256:0a8a667897d20812bd8f67e088fa40f0dd84d99782b4599cf09f06a4b295cd5f
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-185
  short_excerpt: 'from pydantic import PydanticUserError, validate_call try: class
    A: def f(): ... validate_call(A().f) except PydanticUserError as exc_info: assert
    exc_info.code == ''validate-call-type'''
  quote_hash: sha256:1310f087fb6385f52b6f4c96126184a6973fe8f3075a1db57fa9c22027aba5a0
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-189
  short_excerpt: 'from typing_extensions import Unpack from pydantic import PydanticUserError,
    validate_call try: @validate_call def func(**kwargs: Unpack[int]): pass except
    PydanticUserError as exc_info: assert exc_info.code == ''unpack-typed-dict'''
  quote_hash: sha256:ed10bc656c55fa5c1adf136d7949be5a605a1ade06e8d6d6154f3d15f09d3c57
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-192
  short_excerpt: 'from typing_extensions import TypedDict, Unpack from pydantic import
    PydanticUserError, validate_call class TD(TypedDict): a: int try: @validate_call
    def func(a: int, **kwargs: Unpack[TD]): pass except PydanticUserError as exc_info:
    assert exc_info.code == ''overlapping-unpack-typed-dict'''
  quote_hash: sha256:8db4665c1a1a7352cc60d0a489fdecbd910f2e7879a8eec70737631b372d1b78
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-195
  short_excerpt: 'from typing_extensions import Self from pydantic import PydanticUserError,
    validate_call try: @validate_call def func(self: Self): pass except PydanticUserError
    as exc_info: assert exc_info.code == ''invalid-self-type'''
  quote_hash: sha256:7534797b0f30ddab4bfff7919136308cda16f919d4ff2c70119210fee305c0c2
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-197
  short_excerpt: 'from typing_extensions import Self from pydantic import BaseModel,
    PydanticUserError, validate_call try: class A(BaseModel): @validate_call def func(self,
    arg: Self): pass except PydanticUserError as exc_info: assert exc_info.code ==
    ''invalid-self-type'''
  quote_hash: sha256:55a47ebea89a7f1e839b96bfdc195724c1e498e6b04be44bb7f75aa5f2affb3a
- source_id: pydantic-usage-errors
  url: https://docs.pydantic.dev/latest/errors/usage_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/usage_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-usage-errors-201
  short_excerpt: 'from pydantic import BaseModel, ConfigDict, Field, PydanticUserError
    try: class Model(BaseModel): a: int = Field(alias=''A'') model_config = ConfigDict(
    validate_by_alias=False, validate_by_name=False ) except PydanticUserError as
    exc_info: assert exc_info.code == ''validate-by-alias-and-name-false'''
  quote_hash: sha256:ef4d8b9022b0097eb872beb7bbf1517927c4f3ad8c5643c58dfa5731d7fd2283
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# pydantic-class-not-fully-defined

## Failure Class
pydantic/model-schema

## Symptoms
- PydanticUserError class-not-fully-defined raised when instantiating a model that references a forward or post-defined type

## Fingerprints
- class-not-fully-defined
- PydanticUserError
- model_rebuild
- ForwardRef
- decorator-missing-field

## First Checks
- Check whether the referenced type is defined before the model class is instantiated or validated
- Check whether model_rebuild() is called after the forward-referenced type is defined
- Check whether @field_validator field names match actual model fields

## Do Not Patch Yet
- Do not define a BaseModel subclass with Optional['ForwardRef'] without calling model_rebuild() after the target is defined
- Do not suppress the class-not-fully-defined error; it means the schema is incomplete

## Evidence Needed
- Capture the PydanticUserError.message and PydanticUserError.code
- Identify the ForwardRef or type annotation that is missing

## Minimal Fix Scope
- The model class with the forward-referenced type
- The type definition order or model_rebuild() call site

## Validation Ladder
- Instantiate the model after adding model_rebuild() and verify no PydanticUserError
- Verify nested model validation works with forward references
- Run the model unit test for the affected forward-reference path

## Regression Guard
- Add a model test that validates forward-referenced nested models after model_rebuild()

## Reviewer Notes
