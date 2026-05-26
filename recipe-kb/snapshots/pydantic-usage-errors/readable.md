- [pydantic-usage-errors-1] Pydantic attempts to provide useful errors. The following sections provide details on common errors developers may encounter when working with Pydantic, along with suggestions for addressing the error condition.

- [pydantic-usage-errors-2] Class not fully defined

- [pydantic-usage-errors-3] This error is raised when a type referenced in an annotation of a pydantic-validated type (such as a subclass of BaseModel , or a pydantic dataclass ) is not defined:

- [pydantic-usage-errors-4] from typing import ForwardRef from pydantic import BaseModel, PydanticUserError UndefinedType = ForwardRef('UndefinedType') class Foobar(BaseModel): a: UndefinedType try: Foobar(a=1) except PydanticUserError as exc_info: assert exc_info.code == 'class-not-fully-defined'

- [pydantic-usage-errors-5] Or when the type has been defined after usage:

- [pydantic-usage-errors-6] from typing import Optional from pydantic import BaseModel, PydanticUserError class Foo(BaseModel): a: Optional['Bar'] = None try: # this doesn't work, see raised error foo = Foo(a={'b': {'a': None}}) except PydanticUserError as exc_info: assert exc_info.code == 'class-not-fully-defined' class Bar(BaseModel): b: 'Foo' # this works, though foo = Foo(a={'b': {'a': None}})

- [pydantic-usage-errors-7] For BaseModel subclasses, it can be fixed by defining the type and then calling .model_rebuild() :

- [pydantic-usage-errors-8] from typing import Optional from pydantic import BaseModel class Foo(BaseModel): a: Optional['Bar'] = None class Bar(BaseModel): b: 'Foo' Foo.model_rebuild() foo = Foo(a={'b': {'a': None}})

- [pydantic-usage-errors-9] In other cases, the error message should indicate how to rebuild the class with the appropriate type defined.

- [pydantic-usage-errors-10] Custom JSON Schema

- [pydantic-usage-errors-11] The __modify_schema__ method is no longer supported in V2. You should use the __get_pydantic_json_schema__ method instead.

- [pydantic-usage-errors-12] The __modify_schema__ used to receive a single argument representing the JSON schema. See the example below:

- [pydantic-usage-errors-13] from pydantic import BaseModel, PydanticUserError try: class Model(BaseModel): @classmethod def __modify_schema__(cls, field_schema): field_schema.update(examples=['example']) except PydanticUserError as exc_info: assert exc_info.code == 'custom-json-schema'

- [pydantic-usage-errors-14] The new method __get_pydantic_json_schema__ receives two arguments: the first is a dictionary denoted as CoreSchema , and the second a callable handler that receives a CoreSchema as parameter, and returns a JSON schema. See the example below:

- [pydantic-usage-errors-15] from typing import Any from pydantic_core import CoreSchema from pydantic import BaseModel, GetJsonSchemaHandler class Model(BaseModel): @classmethod def __get_pydantic_json_schema__( cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler ) -> dict[str, Any]: json_schema = super().__get_pydantic_json_schema__(core_schema, handler) json_schema = handler.resolve_ref_schema(json_schema) json_schema.update(examples=['example']) return json_schema print(Model.model_json_schema()) """ {'examples': ['example'], 'properties': {}, 'title': 'Model', 'type': 'object'} """

- [pydantic-usage-errors-16] Invalid decorator fields

- [pydantic-usage-errors-17] This error is raised when the field names provided to the @field_validator or @field_serializer decorators are not strings.

- [pydantic-usage-errors-18] from pydantic import BaseModel, PydanticUserError, field_validator try: class Model(BaseModel): a: str b: str @field_validator(['a', 'b']) @classmethod def check_fields(cls, v): return v except PydanticUserError as exc_info: assert exc_info.code == 'decorator-invalid-fields'

- [pydantic-usage-errors-19] Fields should be provided as separate string arguments:

- [pydantic-usage-errors-20] from pydantic import BaseModel, field_validator class Model(BaseModel): a: str b: str @field_validator('a', 'b') @classmethod def check_fields(cls, v): return v

- [pydantic-usage-errors-21] Decorator with no fields

- [pydantic-usage-errors-22] This error is raised when the @field_validator or @field_serializer decorators are used bare, without any arguments.

- [pydantic-usage-errors-23] from pydantic import BaseModel, PydanticUserError, field_validator try: class Model(BaseModel): a: str @field_validator @classmethod def checker(cls, v): return v except PydanticUserError as exc_info: assert exc_info.code == 'decorator-missing-arguments'

- [pydantic-usage-errors-24] At least one field name (and optionally other field names and keyword arguments) should be provided.

- [pydantic-usage-errors-25] from pydantic import BaseModel, field_validator class Model(BaseModel): a: str @field_validator('a') @classmethod def checker(cls, v): return v

- [pydantic-usage-errors-26] Decorator on missing field

- [pydantic-usage-errors-27] This error is raised when you define a decorator with a field that is not valid.

- [pydantic-usage-errors-28] from typing import Any from pydantic import BaseModel, PydanticUserError, field_validator try: class Model(BaseModel): a: str @field_validator('b') def check_b(cls, v: Any): return v except PydanticUserError as exc_info: assert exc_info.code == 'decorator-missing-field'

- [pydantic-usage-errors-29] You can use check_fields=False if you’re inheriting from the model and intended this.

- [pydantic-usage-errors-30] from typing import Any from pydantic import BaseModel, create_model, field_validator class Model(BaseModel): @field_validator('a', check_fields=False) def check_a(cls, v: Any): return v model = create_model('FooModel', a=(str, 'cake'), __base__=Model)

- [pydantic-usage-errors-31] Discriminator no field

- [pydantic-usage-errors-32] This error is raised when a model in discriminated unions doesn’t define a discriminator field.

- [pydantic-usage-errors-33] from typing import Literal, Union from pydantic import BaseModel, Field, PydanticUserError class Cat(BaseModel): c: str class Dog(BaseModel): pet_type: Literal['dog'] d: str try: class Model(BaseModel): pet: Union[Cat, Dog] = Field(discriminator='pet_type') number: int except PydanticUserError as exc_info: assert exc_info.code == 'discriminator-no-field'

- [pydantic-usage-errors-34] Discriminator alias type

- [pydantic-usage-errors-35] This error is raised when you define a non-string alias on a discriminator field.

- [pydantic-usage-errors-36] from typing import Literal, Union from pydantic import AliasChoices, BaseModel, Field, PydanticUserError class Cat(BaseModel): pet_type: Literal['cat'] = Field( validation_alias=AliasChoices('Pet', 'PET') ) c: str class Dog(BaseModel): pet_type: Literal['dog'] d: str try: class Model(BaseModel): pet: Union[Cat, Dog] = Field(discriminator='pet_type') number: int except PydanticUserError as exc_info: assert exc_info.code == 'discriminator-alias-type'

- [pydantic-usage-errors-37] Discriminator needs literal

- [pydantic-usage-errors-38] This error is raised when you define a non- Literal type on a discriminator field.

- [pydantic-usage-errors-39] from typing import Literal, Union from pydantic import BaseModel, Field, PydanticUserError class Cat(BaseModel): pet_type: int c: str class Dog(BaseModel): pet_type: Literal['dog'] d: str try: class Model(BaseModel): pet: Union[Cat, Dog] = Field(discriminator='pet_type') number: int except PydanticUserError as exc_info: assert exc_info.code == 'discriminator-needs-literal'

- [pydantic-usage-errors-40] Discriminator alias

- [pydantic-usage-errors-41] This error is raised when you define different aliases on discriminator fields.

- [pydantic-usage-errors-42] from typing import Literal, Union from pydantic import BaseModel, Field, PydanticUserError class Cat(BaseModel): pet_type: Literal['cat'] = Field(validation_alias='PET') c: str class Dog(BaseModel): pet_type: Literal['dog'] = Field(validation_alias='Pet') d: str try: class Model(BaseModel): pet: Union[Cat, Dog] = Field(discriminator='pet_type') number: int except PydanticUserError as exc_info: assert exc_info.code == 'discriminator-alias'

- [pydantic-usage-errors-43] Invalid discriminator validator

- [pydantic-usage-errors-44] This error is raised when you use a before, wrap, or plain validator on a discriminator field.

- [pydantic-usage-errors-45] This is disallowed because the discriminator field is used to determine the type of the model to use for validation, so you can’t use a validator that might change its value.

- [pydantic-usage-errors-46] from typing import Literal, Union from pydantic import BaseModel, Field, PydanticUserError, field_validator class Cat(BaseModel): pet_type: Literal['cat'] @field_validator('pet_type', mode='before') @classmethod def validate_pet_type(cls, v): if v == 'kitten': return 'cat' return v class Dog(BaseModel): pet_type: Literal['dog'] try: class Model(BaseModel): pet: Union[Cat, Dog] = Field(discriminator='pet_type') number: int except PydanticUserError as exc_info: assert exc_info.code == 'discriminator-validator'

- [pydantic-usage-errors-47] This can be worked around by using a standard Union , dropping the discriminator:

- [pydantic-usage-errors-48] from typing import Literal, Union from pydantic import BaseModel, field_validator class Cat(BaseModel): pet_type: Literal['cat'] @field_validator('pet_type', mode='before') @classmethod def validate_pet_type(cls, v): if v == 'kitten': return 'cat' return v class Dog(BaseModel): pet_type: Literal['dog'] class Model(BaseModel): pet: Union[Cat, Dog] assert Model(pet={'pet_type': 'kitten'}).pet.pet_type == 'cat'

- [pydantic-usage-errors-49] Callable discriminator case with no tag

- [pydantic-usage-errors-50] This error is raised when a Union that uses a callable Discriminator doesn’t have Tag annotations for all cases.

- [pydantic-usage-errors-51] from typing import Annotated, Union from pydantic import BaseModel, Discriminator, PydanticUserError, Tag def model_x_discriminator(v): if isinstance(v, str): return 'str' if isinstance(v, (dict, BaseModel)): return 'model' # tag missing for both union choices try: class DiscriminatedModel(BaseModel): x: Annotated[ Union[str, 'DiscriminatedModel'], Discriminator(model_x_discriminator), ] except PydanticUserError as exc_info: assert exc_info.code == 'callable-discriminator-no-tag' # tag missing for `'DiscriminatedModel'` union choice try: class DiscriminatedModel(BaseModel): x: Annotated[ Union[Annotated[str, Tag('str')], 'DiscriminatedModel'], Discriminator(model_x_discriminator), ] except PydanticUserError as exc_info: assert exc_info.code == 'callable-discriminator-no-tag' # tag missing for `str` union choice try: class DiscriminatedModel(BaseModel): x: Annotated[ Union[str, Annotated['DiscriminatedModel', Tag('model')]], Discriminator(model_x_discriminator), ] except PydanticUserError as exc_info: assert exc_info.code == 'callable-discriminator-no-tag'

- [pydantic-usage-errors-52] TypedDict version

- [pydantic-usage-errors-53] This error is raised when you use typing.TypedDict instead of typing_extensions.TypedDict on Python < 3.12.

- [pydantic-usage-errors-54] Model parent field overridden

- [pydantic-usage-errors-55] This error is raised when a field defined on a base class was overridden by a non-annotated attribute.

- [pydantic-usage-errors-56] from pydantic import BaseModel, PydanticUserError class Foo(BaseModel): a: float try: class Bar(Foo): x: float = 12.3 a = 123.0 except PydanticUserError as exc_info: assert exc_info.code == 'model-field-overridden'

- [pydantic-usage-errors-57] Model field missing annotation

- [pydantic-usage-errors-58] This error is raised when a field doesn’t have an annotation.

- [pydantic-usage-errors-59] from pydantic import BaseModel, Field, PydanticUserError try: class Model(BaseModel): a = Field('foobar') b = None except PydanticUserError as exc_info: assert exc_info.code == 'model-field-missing-annotation'

- [pydantic-usage-errors-60] If the field is not meant to be a field, you may be able to resolve the error by annotating it as a ClassVar :

- [pydantic-usage-errors-61] from typing import ClassVar from pydantic import BaseModel class Model(BaseModel): a: ClassVar[str]

- [pydantic-usage-errors-62] Or updating model_config['ignored_types'] :

- [pydantic-usage-errors-63] from pydantic import BaseModel, ConfigDict class IgnoredType: pass class MyModel(BaseModel): model_config = ConfigDict(ignored_types=(IgnoredType,)) _a = IgnoredType() _b: int = IgnoredType() _c: IgnoredType _d: IgnoredType = IgnoredType()

- [pydantic-usage-errors-64] Config and model_config both defined

- [pydantic-usage-errors-65] This error is raised when class Config and model_config are used together.

- [pydantic-usage-errors-66] from pydantic import BaseModel, ConfigDict, PydanticUserError try: class Model(BaseModel): model_config = ConfigDict(from_attributes=True) a: str class Config: from_attributes = True except PydanticUserError as exc_info: assert exc_info.code == 'config-both'

- [pydantic-usage-errors-67] Keyword arguments removed

- [pydantic-usage-errors-68] This error is raised when the keyword arguments are not available in Pydantic V2.

- [pydantic-usage-errors-69] For example, regex is removed from Pydantic V2:

- [pydantic-usage-errors-70] from pydantic import BaseModel, Field, PydanticUserError try: class Model(BaseModel): x: str = Field(regex='test') except PydanticUserError as exc_info: assert exc_info.code == 'removed-kwargs'

- [pydantic-usage-errors-71] Circular reference schema

- [pydantic-usage-errors-72] This error is raised when a circular reference is found that would otherwise result in an infinite recursion.

- [pydantic-usage-errors-73] For example, this is a valid type alias:

- [pydantic-usage-errors-74] type A = list[A] | None

- [pydantic-usage-errors-75] while these are not:

- [pydantic-usage-errors-76] type A = A type B = C type C = B

- [pydantic-usage-errors-77] JSON schema invalid type

- [pydantic-usage-errors-78] This error is raised when Pydantic fails to generate a JSON schema for some CoreSchema .

- [pydantic-usage-errors-79] from pydantic import BaseModel, ImportString, PydanticUserError class Model(BaseModel): a: ImportString try: Model.model_json_schema() except PydanticUserError as exc_info: assert exc_info.code == 'invalid-for-json-schema'

- [pydantic-usage-errors-80] JSON schema already used

- [pydantic-usage-errors-81] This error is raised when the JSON schema generator has already been used to generate a JSON schema. You must create a new instance to generate a new JSON schema.

- [pydantic-usage-errors-82] BaseModel instantiated

- [pydantic-usage-errors-83] This error is raised when you instantiate BaseModel directly. Pydantic models should inherit from BaseModel .

- [pydantic-usage-errors-84] from pydantic import BaseModel, PydanticUserError try: BaseModel() except PydanticUserError as exc_info: assert exc_info.code == 'base-model-instantiated'

- [pydantic-usage-errors-85] Undefined annotation

- [pydantic-usage-errors-86] This error is raised when handling undefined annotations during CoreSchema generation.

- [pydantic-usage-errors-87] from pydantic import BaseModel, PydanticUndefinedAnnotation class Model(BaseModel): a: 'B' # noqa F821 try: Model.model_rebuild() except PydanticUndefinedAnnotation as exc_info: assert exc_info.code == 'undefined-annotation'

- [pydantic-usage-errors-88] Schema for unknown type

- [pydantic-usage-errors-89] This error is raised when Pydantic fails to generate a CoreSchema for some type.

- [pydantic-usage-errors-90] from pydantic import BaseModel, PydanticUserError try: class Model(BaseModel): x: 43 = 123 except PydanticUserError as exc_info: assert exc_info.code == 'schema-for-unknown-type'

- [pydantic-usage-errors-91] Import error

- [pydantic-usage-errors-92] This error is raised when you try to import an object that was available in Pydantic V1, but has been removed in Pydantic V2.

- [pydantic-usage-errors-93] See the Migration Guide for more information.

- [pydantic-usage-errors-94] create_model field definitions

- [pydantic-usage-errors-95] This error is raised when you provide invalid field definitions in create_model() .

- [pydantic-usage-errors-96] from pydantic import PydanticUserError, create_model try: create_model('FooModel', foo=(str, 'default value', 'more')) except PydanticUserError as exc_info: assert exc_info.code == 'create-model-field-definitions'

- [pydantic-usage-errors-97] The fields definition syntax can be found in the dynamic model creation documentation.

- [pydantic-usage-errors-98] Validator on instance method

- [pydantic-usage-errors-99] This error is raised when you apply a validator on an instance method.

- [pydantic-usage-errors-100] from pydantic import BaseModel, PydanticUserError, field_validator try: class Model(BaseModel): a: int = 1 @field_validator('a') def check_a(self, value): return value except PydanticUserError as exc_info: assert exc_info.code == 'validator-instance-method'

- [pydantic-usage-errors-101] json_schema_input_type used with the wrong mode

- [pydantic-usage-errors-102] This error is raised when you explicitly specify a value for the json_schema_input_type argument and mode isn’t set to either 'before' , 'plain' or 'wrap' .

- [pydantic-usage-errors-103] from pydantic import BaseModel, PydanticUserError, field_validator try: class Model(BaseModel): a: int = 1 @field_validator('a', mode='after', json_schema_input_type=int) @classmethod def check_a(self, value): return value except PydanticUserError as exc_info: assert exc_info.code == 'validator-input-type'

- [pydantic-usage-errors-104] Documenting the JSON Schema input type is only possible for validators where the given value can be anything. That is why it isn’t available for after validators, where the value is first validated against the type annotation.

- [pydantic-usage-errors-105] Root validator, pre , skip_on_failure

- [pydantic-usage-errors-106] If you use @root_validator with pre=False (the default) you MUST specify skip_on_failure=True . The skip_on_failure=False option is no longer available.

- [pydantic-usage-errors-107] If you were not trying to set skip_on_failure=False , you can safely set skip_on_failure=True . If you do, this root validator will no longer be called if validation fails for any of the fields.

- [pydantic-usage-errors-108] Please see the Migration Guide for more details.

- [pydantic-usage-errors-109] model_serializer instance methods

- [pydantic-usage-errors-110] @model_serializer must be applied to instance methods.

- [pydantic-usage-errors-111] This error is raised when you apply model_serializer on an instance method without self :

- [pydantic-usage-errors-112] from pydantic import BaseModel, PydanticUserError, model_serializer try: class MyModel(BaseModel): a: int @model_serializer def _serialize(slf, x, y, z): return slf except PydanticUserError as exc_info: assert exc_info.code == 'model-serializer-instance-method'

- [pydantic-usage-errors-113] Or on a class method:

- [pydantic-usage-errors-114] from pydantic import BaseModel, PydanticUserError, model_serializer try: class MyModel(BaseModel): a: int @model_serializer @classmethod def _serialize(self, x, y, z): return self except PydanticUserError as exc_info: assert exc_info.code == 'model-serializer-instance-method'

- [pydantic-usage-errors-115] validator , field , config , and info

- [pydantic-usage-errors-116] The field and config parameters are not available in Pydantic V2. Please use the info parameter instead.

- [pydantic-usage-errors-117] You can access the configuration via info.config , but it is a dictionary instead of an object like it was in Pydantic V1.

- [pydantic-usage-errors-118] The field argument is no longer available.

- [pydantic-usage-errors-119] Pydantic V1 validator signature

- [pydantic-usage-errors-120] This error is raised when you use an unsupported signature for Pydantic V1-style validator.

- [pydantic-usage-errors-121] import warnings from pydantic import BaseModel, PydanticUserError, validator warnings.filterwarnings('ignore', category=DeprecationWarning) try: class Model(BaseModel): a: int @validator('a') def check_a(cls, value, foo): return value except PydanticUserError as exc_info: assert exc_info.code == 'validator-v1-signature'

- [pydantic-usage-errors-122] Unrecognized field_validator signature

- [pydantic-usage-errors-123] This error is raised when a field_validator or model_validator function has the wrong signature.

- [pydantic-usage-errors-124] from pydantic import BaseModel, PydanticUserError, field_validator try: class Model(BaseModel): a: str @field_validator('a') @classmethod def check_a(cls): return 'a' except PydanticUserError as exc_info: assert exc_info.code == 'validator-signature'

- [pydantic-usage-errors-125] Unrecognized field_serializer signature

- [pydantic-usage-errors-126] This error is raised when the field_serializer function has the wrong signature.

- [pydantic-usage-errors-127] from pydantic import BaseModel, PydanticUserError, field_serializer try: class Model(BaseModel): x: int @field_serializer('x') def no_args(): return 'x' except PydanticUserError as exc_info: assert exc_info.code == 'field-serializer-signature'

- [pydantic-usage-errors-128] Valid field serializer signatures are:

- [pydantic-usage-errors-129] from pydantic import FieldSerializationInfo, SerializerFunctionWrapHandler, field_serializer # an instance method with the default mode or `mode='plain'` @field_serializer('x') # or @field_serializer('x', mode='plain') def ser_x(self, value: Any, info: FieldSerializationInfo): ... # a static method or function with the default mode or `mode='plain'` @field_serializer('x') # or @field_serializer('x', mode='plain') @staticmethod def ser_x(value: Any, info: FieldSerializationInfo): ... # equivalent to def ser_x(value: Any, info: FieldSerializationInfo): ... serializer('x')(ser_x) # an instance method with `mode='wrap'` @field_serializer('x', mode='wrap') def ser_x(self, value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo): ... # a static method or function with `mode='wrap'` @field_serializer('x', mode='wrap') @staticmethod def ser_x(value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo): ... # equivalent to def ser_x(value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo): ... serializer('x')(ser_x) # For all of these, you can also choose to omit the `info` argument, for example: @field_serializer('x') def ser_x(self, value: Any): ... @field_serializer('x', mode='wrap') def ser_x(self, value: Any, handler: SerializerFunctionWrapHandler): ...

- [pydantic-usage-errors-130] Unrecognized model_serializer signature

- [pydantic-usage-errors-131] This error is raised when the model_serializer function has the wrong signature.

- [pydantic-usage-errors-132] from pydantic import BaseModel, PydanticUserError, model_serializer try: class MyModel(BaseModel): a: int @model_serializer def _serialize(self, x, y, z): return self except PydanticUserError as exc_info: assert exc_info.code == 'model-serializer-signature'

- [pydantic-usage-errors-133] Valid model serializer signatures are:

- [pydantic-usage-errors-134] from pydantic import SerializerFunctionWrapHandler, SerializationInfo, model_serializer # an instance method with the default mode or `mode='plain'` @model_serializer # or model_serializer(mode='plain') def mod_ser(self, info: SerializationInfo): ... # an instance method with `mode='wrap'` @model_serializer(mode='wrap') def mod_ser(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo): # For all of these, you can also choose to omit the `info` argument, for example: @model_serializer(mode='plain') def mod_ser(self): ... @model_serializer(mode='wrap') def mod_ser(self, handler: SerializerFunctionWrapHandler): ...

- [pydantic-usage-errors-135] Multiple field serializers

- [pydantic-usage-errors-136] This error is raised when multiple model_serializer functions are defined for a field.

- [pydantic-usage-errors-137] from pydantic import BaseModel, PydanticUserError, field_serializer try: class MyModel(BaseModel): x: int y: int @field_serializer('x', 'y') def serializer1(v): return f'{v:,}' @field_serializer('x') def serializer2(v): return v except PydanticUserError as exc_info: assert exc_info.code == 'multiple-field-serializers'

- [pydantic-usage-errors-138] Invalid annotated type

- [pydantic-usage-errors-139] This error is raised when an annotation cannot annotate a type.

- [pydantic-usage-errors-140] from typing import Annotated from pydantic import BaseModel, FutureDate, PydanticUserError try: class Model(BaseModel): foo: Annotated[str, FutureDate()] except PydanticUserError as exc_info: assert exc_info.code == 'invalid-annotated-type'

- [pydantic-usage-errors-141] config is unused with TypeAdapter

- [pydantic-usage-errors-142] You will get this error if you try to pass config to TypeAdapter when the type is a type that has its own config that cannot be overridden (currently this is only BaseModel , TypedDict and dataclass ):

- [pydantic-usage-errors-143] from typing_extensions import TypedDict from pydantic import ConfigDict, PydanticUserError, TypeAdapter class MyTypedDict(TypedDict): x: int try: TypeAdapter(MyTypedDict, config=ConfigDict(strict=True)) except PydanticUserError as exc_info: assert exc_info.code == 'type-adapter-config-unused'

- [pydantic-usage-errors-144] Instead you’ll need to subclass the type and override or set the config on it:

- [pydantic-usage-errors-145] from typing_extensions import TypedDict from pydantic import ConfigDict, TypeAdapter class MyTypedDict(TypedDict): x: int # or `model_config = ...` for BaseModel __pydantic_config__ = ConfigDict(strict=True) TypeAdapter(MyTypedDict) # ok

- [pydantic-usage-errors-146] Cannot specify model_config['extra'] with RootModel

- [pydantic-usage-errors-147] Because RootModel is not capable of storing or even accepting extra fields during initialization, we raise an error if you try to specify a value for the config setting 'extra' when creating a subclass of RootModel :

- [pydantic-usage-errors-148] from pydantic import PydanticUserError, RootModel try: class MyRootModel(RootModel): model_config = {'extra': 'allow'} root: int except PydanticUserError as exc_info: assert exc_info.code == 'root-model-extra'

- [pydantic-usage-errors-149] Cannot evaluate type annotation

- [pydantic-usage-errors-150] Because type annotations are evaluated after assignments, you might get unexpected results when using a type annotation name that clashes with one of your fields. We raise an error in the following case:

- [pydantic-usage-errors-151] from datetime import date from pydantic import BaseModel, Field class Model(BaseModel): date: date = Field(description='A date')

- [pydantic-usage-errors-152] As a workaround, you can either use an alias or change your import:

- [pydantic-usage-errors-153] import datetime # Or `from datetime import date as _date` from pydantic import BaseModel, Field class Model(BaseModel): date: datetime.date = Field(description='A date')

- [pydantic-usage-errors-154] Incompatible dataclass init and extra settings

- [pydantic-usage-errors-155] Pydantic does not allow the specification of the extra='allow' setting on a dataclass while any of the fields have init=False set.

- [pydantic-usage-errors-156] Thus, you may not do something like the following:

- [pydantic-usage-errors-157] from pydantic import ConfigDict, Field from pydantic.dataclasses import dataclass @dataclass(config=ConfigDict(extra='allow')) class A: a: int = Field(init=False, default=1)

- [pydantic-usage-errors-158] The above snippet results in the following error during schema building for the A dataclass:

- [pydantic-usage-errors-159] pydantic.errors.PydanticUserError: Field a has `init=False` and dataclass has config setting `extra="allow"`. This combination is not allowed.

- [pydantic-usage-errors-160] Incompatible init and init_var settings on dataclass field

- [pydantic-usage-errors-161] The init=False and init_var=True settings are mutually exclusive. Doing so results in the PydanticUserError shown in the example below.

- [pydantic-usage-errors-162] from pydantic import Field from pydantic.dataclasses import dataclass @dataclass class Foo: bar: str = Field(init=False, init_var=True) """ pydantic.errors.PydanticUserError: Dataclass field bar has init=False and init_var=True, but these are mutually exclusive. """

- [pydantic-usage-errors-163] model_config is used as a model field

- [pydantic-usage-errors-164] This error is raised when model_config is used as the name of a field.

- [pydantic-usage-errors-165] from pydantic import BaseModel, PydanticUserError try: class Model(BaseModel): model_config: str except PydanticUserError as exc_info: assert exc_info.code == 'model-config-invalid-field-name'

- [pydantic-usage-errors-166] with_config is used on a BaseModel subclass

- [pydantic-usage-errors-167] This error is raised when the with_config decorator is used on a class which is already a Pydantic model (use the model_config attribute instead).

- [pydantic-usage-errors-168] from pydantic import BaseModel, PydanticUserError, with_config try: @with_config({'allow_inf_nan': True}) class Model(BaseModel): bar: str except PydanticUserError as exc_info: assert exc_info.code == 'with-config-on-model'

- [pydantic-usage-errors-169] dataclass is used on a BaseModel subclass

- [pydantic-usage-errors-170] This error is raised when the Pydantic dataclass decorator is used on a class which is already a Pydantic model.

- [pydantic-usage-errors-171] from pydantic import BaseModel, PydanticUserError from pydantic.dataclasses import dataclass try: @dataclass class Model(BaseModel): bar: str except PydanticUserError as exc_info: assert exc_info.code == 'dataclass-on-model'

- [pydantic-usage-errors-172] Unsupported type for validate_call

- [pydantic-usage-errors-173] validate_call has some limitations on the callables it can validate. This error is raised when you try to use it with an unsupported callable. Currently the supported callables are functions (including lambdas, but not built-ins) and methods and instances of partial . In the case of partial , the function being partially applied must be one of the supported callables.

- [pydantic-usage-errors-174] @classmethod , @staticmethod , and @property

- [pydantic-usage-errors-175] These decorators must be put before validate_call .

- [pydantic-usage-errors-176] from pydantic import PydanticUserError, validate_call # error try: class A: @validate_call @classmethod def f1(cls): ... except PydanticUserError as exc_info: assert exc_info.code == 'validate-call-type' # correct @classmethod @validate_call def f2(cls): ...

- [pydantic-usage-errors-177] Classes

- [pydantic-usage-errors-178] While classes are callables themselves, validate_call can’t be applied on them, as it needs to know about which method to use ( __init__ or __new__ ) to fetch type annotations. If you want to validate the constructor of a class, you should put validate_call on top of the appropriate method instead.

- [pydantic-usage-errors-179] from pydantic import PydanticUserError, validate_call # error try: @validate_call class A1: ... except PydanticUserError as exc_info: assert exc_info.code == 'validate-call-type' # correct class A2: @validate_call def __init__(self): ... @validate_call def __new__(cls): ...

- [pydantic-usage-errors-180] Callable instances

- [pydantic-usage-errors-181] Although instances can be callable by implementing a __call__ method, currently the instances of these types cannot be validated with validate_call . This may change in the future, but for now, you should use validate_call explicitly on __call__ instead.

- [pydantic-usage-errors-182] from pydantic import PydanticUserError, validate_call # error try: class A1: def __call__(self): ... validate_call(A1()) except PydanticUserError as exc_info: assert exc_info.code == 'validate-call-type' # correct class A2: @validate_call def __call__(self): ...

- [pydantic-usage-errors-183] Invalid signature

- [pydantic-usage-errors-184] This is generally less common, but a possible reason is that you are trying to validate a method that doesn’t have at least one argument (usually self ).

- [pydantic-usage-errors-185] from pydantic import PydanticUserError, validate_call try: class A: def f(): ... validate_call(A().f) except PydanticUserError as exc_info: assert exc_info.code == 'validate-call-type'

- [pydantic-usage-errors-186] Unpack used without a TypedDict

- [pydantic-usage-errors-187] This error is raised when Unpack is used with something other than a TypedDict class object to type hint variadic keyword parameters.

- [pydantic-usage-errors-188] For reference, see the related specification section and PEP 692 .

- [pydantic-usage-errors-189] from typing_extensions import Unpack from pydantic import PydanticUserError, validate_call try: @validate_call def func(**kwargs: Unpack[int]): pass except PydanticUserError as exc_info: assert exc_info.code == 'unpack-typed-dict'

- [pydantic-usage-errors-190] Overlapping unpacked TypedDict fields and arguments

- [pydantic-usage-errors-191] This error is raised when the typed dictionary used to type hint variadic keywords parameters has field names overlapping with other parameters (unless positional only).

- [pydantic-usage-errors-192] from typing_extensions import TypedDict, Unpack from pydantic import PydanticUserError, validate_call class TD(TypedDict): a: int try: @validate_call def func(a: int, **kwargs: Unpack[TD]): pass except PydanticUserError as exc_info: assert exc_info.code == 'overlapping-unpack-typed-dict'

- [pydantic-usage-errors-193] Invalid Self type

- [pydantic-usage-errors-194] Currently, Self can only be used to annotate a field of a class (specifically, subclasses of BaseModel , NamedTuple , TypedDict , or dataclasses). Attempting to use Self in any other ways will raise this error.

- [pydantic-usage-errors-195] from typing_extensions import Self from pydantic import PydanticUserError, validate_call try: @validate_call def func(self: Self): pass except PydanticUserError as exc_info: assert exc_info.code == 'invalid-self-type'

- [pydantic-usage-errors-196] The following example of validate_call() will also raise this error, even though it is correct from a type-checking perspective. This may be supported in the future.

- [pydantic-usage-errors-197] from typing_extensions import Self from pydantic import BaseModel, PydanticUserError, validate_call try: class A(BaseModel): @validate_call def func(self, arg: Self): pass except PydanticUserError as exc_info: assert exc_info.code == 'invalid-self-type'

- [pydantic-usage-errors-198] validate_by_alias and validate_by_name both set to False

- [pydantic-usage-errors-199] This error is raised when you set validate_by_alias and validate_by_name to False in the configuration.

- [pydantic-usage-errors-200] This is not allowed because it would make it impossible to populate attributes.

- [pydantic-usage-errors-201] from pydantic import BaseModel, ConfigDict, Field, PydanticUserError try: class Model(BaseModel): a: int = Field(alias='A') model_config = ConfigDict( validate_by_alias=False, validate_by_name=False ) except PydanticUserError as exc_info: assert exc_info.code == 'validate-by-alias-and-name-false'
