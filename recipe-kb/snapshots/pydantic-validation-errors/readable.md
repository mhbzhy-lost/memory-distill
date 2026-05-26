- [pydantic-validation-errors-1] Pydantic attempts to provide useful validation errors. Below are details on common validation errors users may encounter when working with pydantic, together with some suggestions on how to fix them.

- [pydantic-validation-errors-2] arguments_type

- [pydantic-validation-errors-3] This error is raised when an object that would be passed as arguments to a function during validation is not a tuple , list , or dict . Because NamedTuple uses function calls in its implementation, that is one way to produce this error:

- [pydantic-validation-errors-4] from typing import NamedTuple from pydantic import BaseModel, ValidationError class MyNamedTuple(NamedTuple): x: int class MyModel(BaseModel): field: MyNamedTuple try: MyModel.model_validate({'field': 'invalid'}) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'arguments_type'

- [pydantic-validation-errors-5] assertion_error

- [pydantic-validation-errors-6] This error is raised when a failing assert statement is encountered during validation:

- [pydantic-validation-errors-7] from pydantic import BaseModel, ValidationError, field_validator class Model(BaseModel): x: int @field_validator('x') @classmethod def force_x_positive(cls, v): assert v > 0 return v try: Model(x=-1) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'assertion_error'

- [pydantic-validation-errors-8] bool_parsing

- [pydantic-validation-errors-9] This error is raised when the input value is a string that is not valid for coercion to a boolean:

- [pydantic-validation-errors-10] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: bool Model(x='true') # OK try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'bool_parsing'

- [pydantic-validation-errors-11] bool_type

- [pydantic-validation-errors-12] This error is raised when the input value’s type is not valid for a bool field:

- [pydantic-validation-errors-13] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: bool try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'bool_type'

- [pydantic-validation-errors-14] This error is also raised for strict fields when the input value is not an instance of bool .

- [pydantic-validation-errors-15] bytes_invalid_encoding

- [pydantic-validation-errors-16] This error is raised when a bytes value is invalid under the configured encoding. In the following example, 'a' is invalid hex (odd number of digits).

- [pydantic-validation-errors-17] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: bytes model_config = {'val_json_bytes': 'hex'} try: Model(x='a') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'bytes_invalid_encoding'

- [pydantic-validation-errors-18] bytes_too_long

- [pydantic-validation-errors-19] This error is raised when the length of a bytes value is greater than the field’s max_length constraint:

- [pydantic-validation-errors-20] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: bytes = Field(max_length=3) try: Model(x=b'test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'bytes_too_long'

- [pydantic-validation-errors-21] bytes_too_short

- [pydantic-validation-errors-22] This error is raised when the length of a bytes value is less than the field’s min_length constraint:

- [pydantic-validation-errors-23] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: bytes = Field(min_length=3) try: Model(x=b't') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'bytes_too_short'

- [pydantic-validation-errors-24] bytes_type

- [pydantic-validation-errors-25] This error is raised when the input value’s type is not valid for a bytes field:

- [pydantic-validation-errors-26] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: bytes try: Model(x=123) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'bytes_type'

- [pydantic-validation-errors-27] This error is also raised for strict fields when the input value is not an instance of bytes .

- [pydantic-validation-errors-28] callable_type

- [pydantic-validation-errors-29] This error is raised when the input value is not valid as a Callable :

- [pydantic-validation-errors-30] from typing import Any, Callable from pydantic import BaseModel, ImportString, ValidationError class Model(BaseModel): x: ImportString[Callable[[Any], Any]] Model(x='math:cos') # OK try: Model(x='os.path') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'callable_type'

- [pydantic-validation-errors-31] complex_str_parsing

- [pydantic-validation-errors-32] This error is raised when the input value is a string but cannot be parsed as a complex number because it does not follow the rule in Python:

- [pydantic-validation-errors-33] from pydantic import BaseModel, ValidationError class Model(BaseModel): num: complex try: # Complex numbers in json are expected to be valid complex strings. # This value `abc` is not a valid complex string. Model.model_validate_json('{"num": "abc"}') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'complex_str_parsing'

- [pydantic-validation-errors-34] complex_type

- [pydantic-validation-errors-35] This error is raised when the input value cannot be interpreted as a complex number:

- [pydantic-validation-errors-36] from pydantic import BaseModel, ValidationError class Model(BaseModel): num: complex try: Model(num=False) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'complex_type'

- [pydantic-validation-errors-37] dataclass_exact_type

- [pydantic-validation-errors-38] This error is raised when validating a dataclass with strict=True and the input is not an instance of the dataclass:

- [pydantic-validation-errors-39] import pydantic.dataclasses from pydantic import TypeAdapter, ValidationError @pydantic.dataclasses.dataclass class MyDataclass: x: str adapter = TypeAdapter(MyDataclass) print(adapter.validate_python(MyDataclass(x='test'), strict=True)) #> MyDataclass(x='test') print(adapter.validate_python({'x': 'test'})) #> MyDataclass(x='test') try: adapter.validate_python({'x': 'test'}, strict=True) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'dataclass_exact_type'

- [pydantic-validation-errors-40] dataclass_type

- [pydantic-validation-errors-41] This error is raised when the input value is not valid for a dataclass field:

- [pydantic-validation-errors-42] from pydantic import ValidationError, dataclasses @dataclasses.dataclass class Inner: x: int @dataclasses.dataclass class Outer: y: Inner Outer(y=Inner(x=1)) # OK try: Outer(y=1) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'dataclass_type'

- [pydantic-validation-errors-43] date_from_datetime_inexact

- [pydantic-validation-errors-44] This error is raised when the input datetime value provided for a date field has a nonzero time component. For a timestamp to parse into a field of type date , the time components must all be zero:

- [pydantic-validation-errors-45] from datetime import date, datetime from pydantic import BaseModel, ValidationError class Model(BaseModel): x: date Model(x='2023-01-01') # OK Model(x=datetime(2023, 1, 1)) # OK try: Model(x=datetime(2023, 1, 1, 12)) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'date_from_datetime_inexact'

- [pydantic-validation-errors-46] date_from_datetime_parsing

- [pydantic-validation-errors-47] This error is raised when the input value is a string that cannot be parsed for a date field:

- [pydantic-validation-errors-48] from datetime import date from pydantic import BaseModel, ValidationError class Model(BaseModel): x: date try: Model(x='XX1494012000') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'date_from_datetime_parsing'

- [pydantic-validation-errors-49] date_future

- [pydantic-validation-errors-50] This error is raised when the input value provided for a FutureDate field is not in the future:

- [pydantic-validation-errors-51] from datetime import date from pydantic import BaseModel, FutureDate, ValidationError class Model(BaseModel): x: FutureDate try: Model(x=date(2000, 1, 1)) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'date_future'

- [pydantic-validation-errors-52] date_parsing

- [pydantic-validation-errors-53] This error is raised when validating JSON where the input value is string that cannot be parsed for a date field:

- [pydantic-validation-errors-54] import json from datetime import date from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: date = Field(strict=True) try: Model.model_validate_json(json.dumps({'x': '1'})) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'date_parsing'

- [pydantic-validation-errors-55] date_past

- [pydantic-validation-errors-56] This error is raised when the value provided for a PastDate field is not in the past:

- [pydantic-validation-errors-57] from datetime import date, timedelta from pydantic import BaseModel, PastDate, ValidationError class Model(BaseModel): x: PastDate try: Model(x=date.today() + timedelta(1)) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'date_past'

- [pydantic-validation-errors-58] date_type

- [pydantic-validation-errors-59] This error is raised when the input value’s type is not valid for a date field:

- [pydantic-validation-errors-60] from datetime import date from pydantic import BaseModel, ValidationError class Model(BaseModel): x: date try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'date_type'

- [pydantic-validation-errors-61] This error is also raised for strict fields when the input value is not an instance of date .

- [pydantic-validation-errors-62] datetime_from_date_parsing

- [pydantic-validation-errors-63] This error is raised when the input value is a string that cannot be parsed for a datetime field:

- [pydantic-validation-errors-64] from datetime import datetime from pydantic import BaseModel, ValidationError class Model(BaseModel): x: datetime try: # there is no 13th month Model(x='2023-13-01') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'datetime_from_date_parsing'

- [pydantic-validation-errors-65] datetime_future

- [pydantic-validation-errors-66] This error is raised when the value provided for a FutureDatetime field is not in the future:

- [pydantic-validation-errors-67] from datetime import datetime from pydantic import BaseModel, FutureDatetime, ValidationError class Model(BaseModel): x: FutureDatetime try: Model(x=datetime(2000, 1, 1)) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'datetime_future'

- [pydantic-validation-errors-68] datetime_object_invalid

- [pydantic-validation-errors-69] This error is raised when something about the datetime object is not valid:

- [pydantic-validation-errors-70] from datetime import datetime, tzinfo from pydantic import AwareDatetime, BaseModel, ValidationError class CustomTz(tzinfo): # utcoffset is not implemented! def tzname(self, _dt): return 'CustomTZ' class Model(BaseModel): x: AwareDatetime try: Model(x=datetime(2023, 1, 1, tzinfo=CustomTz())) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'datetime_object_invalid'

- [pydantic-validation-errors-71] datetime_parsing

- [pydantic-validation-errors-72] This error is raised when the value is a string that cannot be parsed for a datetime field:

- [pydantic-validation-errors-73] import json from datetime import datetime from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: datetime = Field(strict=True) try: Model.model_validate_json(json.dumps({'x': 'not a datetime'})) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'datetime_parsing'

- [pydantic-validation-errors-74] datetime_past

- [pydantic-validation-errors-75] This error is raised when the value provided for a PastDatetime field is not in the past:

- [pydantic-validation-errors-76] from datetime import datetime, timedelta from pydantic import BaseModel, PastDatetime, ValidationError class Model(BaseModel): x: PastDatetime try: Model(x=datetime.now() + timedelta(100)) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'datetime_past'

- [pydantic-validation-errors-77] datetime_type

- [pydantic-validation-errors-78] This error is raised when the input value’s type is not valid for a datetime field:

- [pydantic-validation-errors-79] from datetime import datetime from pydantic import BaseModel, ValidationError class Model(BaseModel): x: datetime try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'datetime_type'

- [pydantic-validation-errors-80] This error is also raised for strict fields when the input value is not an instance of datetime .

- [pydantic-validation-errors-81] decimal_max_digits

- [pydantic-validation-errors-82] This error is raised when the value provided for a Decimal has too many digits:

- [pydantic-validation-errors-83] from decimal import Decimal from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: Decimal = Field(max_digits=3) try: Model(x='42.1234') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'decimal_max_digits'

- [pydantic-validation-errors-84] decimal_max_places

- [pydantic-validation-errors-85] This error is raised when the value provided for a Decimal has too many digits after the decimal point:

- [pydantic-validation-errors-86] from decimal import Decimal from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: Decimal = Field(decimal_places=3) try: Model(x='42.1234') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'decimal_max_places'

- [pydantic-validation-errors-87] decimal_parsing

- [pydantic-validation-errors-88] This error is raised when the value provided for a Decimal could not be parsed as a decimal number:

- [pydantic-validation-errors-89] from decimal import Decimal from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: Decimal = Field(decimal_places=3) try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'decimal_parsing'

- [pydantic-validation-errors-90] decimal_type

- [pydantic-validation-errors-91] This error is raised when the value provided for a Decimal is of the wrong type:

- [pydantic-validation-errors-92] from decimal import Decimal from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: Decimal = Field(decimal_places=3) try: Model(x=[1, 2, 3]) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'decimal_type'

- [pydantic-validation-errors-93] This error is also raised for strict fields when the input value is not an instance of Decimal .

- [pydantic-validation-errors-94] decimal_whole_digits

- [pydantic-validation-errors-95] This error is raised when the value provided for a Decimal has more digits before the decimal point than max_digits - decimal_places (as long as both are specified):

- [pydantic-validation-errors-96] from decimal import Decimal from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: Decimal = Field(max_digits=6, decimal_places=3) try: Model(x='12345.6') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'decimal_whole_digits'

- [pydantic-validation-errors-97] default_factory_not_called

- [pydantic-validation-errors-98] This error is raised when a default factory taking validated data can’t be called, because validation failed on previous fields:

- [pydantic-validation-errors-99] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): a: int = Field(gt=10) b: int = Field(default_factory=lambda data: data['a']) try: Model(a=1) except ValidationError as exc: print(exc) """ 2 validation errors for Model a Input should be greater than 10 [type=greater_than, input_value=1, input_type=int] b The default factory uses validated data, but at least one validation error occurred [type=default_factory_not_called] """ print(repr(exc.errors()[1]['type'])) #> 'default_factory_not_called'

- [pydantic-validation-errors-100] dict_type

- [pydantic-validation-errors-101] This error is raised when the input value’s type is not dict for a dict field:

- [pydantic-validation-errors-102] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: dict try: Model(x=['1', '2']) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'dict_type'

- [pydantic-validation-errors-103] enum

- [pydantic-validation-errors-104] This error is raised when the input value does not exist in an enum field members:

- [pydantic-validation-errors-105] from enum import Enum from pydantic import BaseModel, ValidationError class MyEnum(str, Enum): option = 'option' class Model(BaseModel): x: MyEnum try: Model(x='other_option') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'enum'

- [pydantic-validation-errors-106] extra_forbidden

- [pydantic-validation-errors-107] This error is raised when the input value contains extra fields, but model_config['extra'] == 'forbid' :

- [pydantic-validation-errors-108] from pydantic import BaseModel, ConfigDict, ValidationError class Model(BaseModel): x: str model_config = ConfigDict(extra='forbid') try: Model(x='test', y='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'extra_forbidden'

- [pydantic-validation-errors-109] You can read more about the extra configuration in the Extra Attributes section.

- [pydantic-validation-errors-110] finite_number

- [pydantic-validation-errors-111] This error is raised when the value is infinite, or too large to be represented as a 64-bit floating point number during validation:

- [pydantic-validation-errors-112] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: int try: Model(x=2.2250738585072011e308) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'finite_number'

- [pydantic-validation-errors-113] float_parsing

- [pydantic-validation-errors-114] This error is raised when the value is a string that can’t be parsed as a float :

- [pydantic-validation-errors-115] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: float try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'float_parsing'

- [pydantic-validation-errors-116] float_type

- [pydantic-validation-errors-117] This error is raised when the input value’s type is not valid for a float field:

- [pydantic-validation-errors-118] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: float try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'float_type'

- [pydantic-validation-errors-119] frozen_field

- [pydantic-validation-errors-120] This error is raised when you attempt to assign a value to a field with frozen=True , or to delete such a field:

- [pydantic-validation-errors-121] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: str = Field('test', frozen=True) model = Model() try: model.x = 'test1' except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'frozen_field' try: del model.x except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'frozen_field'

- [pydantic-validation-errors-122] frozen_instance

- [pydantic-validation-errors-123] This error is raised when frozen is set in the configuration and you attempt to delete or assign a new value to any of the fields:

- [pydantic-validation-errors-124] from pydantic import BaseModel, ConfigDict, ValidationError class Model(BaseModel): x: int model_config = ConfigDict(frozen=True) m = Model(x=1) try: m.x = 2 except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'frozen_instance' try: del m.x except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'frozen_instance'

- [pydantic-validation-errors-125] frozen_set_type

- [pydantic-validation-errors-126] This error is raised when the input value’s type is not valid for a frozenset field:

- [pydantic-validation-errors-127] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: frozenset try: model = Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'frozen_set_type'

- [pydantic-validation-errors-128] get_attribute_error

- [pydantic-validation-errors-129] This error is raised when model_config['from_attributes'] == True and an error is raised while reading the attributes:

- [pydantic-validation-errors-130] from pydantic import BaseModel, ConfigDict, ValidationError class Foobar: def __init__(self): self.x = 1 @property def y(self): raise RuntimeError('intentional error') class Model(BaseModel): x: int y: str model_config = ConfigDict(from_attributes=True) try: Model.model_validate(Foobar()) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'get_attribute_error'

- [pydantic-validation-errors-131] greater_than

- [pydantic-validation-errors-132] This error is raised when the value is not greater than the field’s gt constraint:

- [pydantic-validation-errors-133] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: int = Field(gt=10) try: Model(x=10) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'greater_than'

- [pydantic-validation-errors-134] greater_than_equal

- [pydantic-validation-errors-135] This error is raised when the value is not greater than or equal to the field’s ge constraint:

- [pydantic-validation-errors-136] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: int = Field(ge=10) try: Model(x=9) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'greater_than_equal'

- [pydantic-validation-errors-137] int_from_float

- [pydantic-validation-errors-138] This error is raised when you provide a float value for an int field:

- [pydantic-validation-errors-139] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: int try: Model(x=0.5) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'int_from_float'

- [pydantic-validation-errors-140] int_parsing

- [pydantic-validation-errors-141] This error is raised when the value can’t be parsed as int :

- [pydantic-validation-errors-142] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: int try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'int_parsing'

- [pydantic-validation-errors-143] int_parsing_size

- [pydantic-validation-errors-144] This error is raised when attempting to parse a python or JSON value from a string outside the maximum range that Python str to int parsing permits:

- [pydantic-validation-errors-145] import json from pydantic import BaseModel, ValidationError class Model(BaseModel): x: int # from Python assert Model(x='1' * 4_300).x == int('1' * 4_300) # OK too_long = '1' * 4_301 try: Model(x=too_long) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'int_parsing_size' # from JSON try: Model.model_validate_json(json.dumps({'x': too_long})) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'int_parsing_size'

- [pydantic-validation-errors-146] int_type

- [pydantic-validation-errors-147] This error is raised when the input value’s type is not valid for an int field:

- [pydantic-validation-errors-148] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: int try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'int_type'

- [pydantic-validation-errors-149] invalid_key

- [pydantic-validation-errors-150] This error is raised when attempting to validate a dict that has a key that is not an instance of str :

- [pydantic-validation-errors-151] from pydantic import BaseModel, ConfigDict, ValidationError class Model(BaseModel): x: int model_config = ConfigDict(extra='allow') try: Model.model_validate({'x': 1, b'y': 2}) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'invalid_key'

- [pydantic-validation-errors-152] is_instance_of

- [pydantic-validation-errors-153] This error is raised when the input value is not an instance of the expected type:

- [pydantic-validation-errors-154] from pydantic import BaseModel, ConfigDict, ValidationError class Nested: x: str class Model(BaseModel): y: Nested model_config = ConfigDict(arbitrary_types_allowed=True) try: Model(y='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'is_instance_of'

- [pydantic-validation-errors-155] is_subclass_of

- [pydantic-validation-errors-156] This error is raised when the input value is not a subclass of the expected type:

- [pydantic-validation-errors-157] from pydantic import BaseModel, ValidationError class Nested: x: str class Model(BaseModel): y: type[Nested] try: Model(y='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'is_subclass_of'

- [pydantic-validation-errors-158] iterable_type

- [pydantic-validation-errors-159] This error is raised when the input value is not valid as an Iterable :

- [pydantic-validation-errors-160] from collections.abc import Iterable from pydantic import BaseModel, ValidationError class Model(BaseModel): y: Iterable[str] try: Model(y=123) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'iterable_type'

- [pydantic-validation-errors-161] iteration_error

- [pydantic-validation-errors-162] This error is raised when an error occurs during iteration:

- [pydantic-validation-errors-163] from pydantic import BaseModel, ValidationError def gen(): yield 1 raise RuntimeError('error') class Model(BaseModel): x: list[int] try: Model(x=gen()) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'iteration_error'

- [pydantic-validation-errors-164] json_invalid

- [pydantic-validation-errors-165] This error is raised when the input value is not a valid JSON string:

- [pydantic-validation-errors-166] from pydantic import BaseModel, Json, ValidationError class Model(BaseModel): x: Json try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'json_invalid'

- [pydantic-validation-errors-167] json_type

- [pydantic-validation-errors-168] This error is raised when the input value is of a type that cannot be parsed as JSON:

- [pydantic-validation-errors-169] from pydantic import BaseModel, Json, ValidationError class Model(BaseModel): x: Json try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'json_type'

- [pydantic-validation-errors-170] less_than

- [pydantic-validation-errors-171] This error is raised when the input value is not less than the field’s lt constraint:

- [pydantic-validation-errors-172] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: int = Field(lt=10) try: Model(x=10) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'less_than'

- [pydantic-validation-errors-173] less_than_equal

- [pydantic-validation-errors-174] This error is raised when the input value is not less than or equal to the field’s le constraint:

- [pydantic-validation-errors-175] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: int = Field(le=10) try: Model(x=11) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'less_than_equal'

- [pydantic-validation-errors-176] list_type

- [pydantic-validation-errors-177] This error is raised when the input value’s type is not valid for a list field:

- [pydantic-validation-errors-178] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: list[int] try: Model(x=1) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'list_type'

- [pydantic-validation-errors-179] literal_error

- [pydantic-validation-errors-180] This error is raised when the input value is not one of the expected literal values:

- [pydantic-validation-errors-181] from typing import Literal from pydantic import BaseModel, ValidationError class Model(BaseModel): x: Literal['a', 'b'] Model(x='a') # OK try: Model(x='c') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'literal_error'

- [pydantic-validation-errors-182] mapping_type

- [pydantic-validation-errors-183] This error is raised when a problem occurs during validation due to a failure in a call to the methods from the Mapping protocol, such as .items() :

- [pydantic-validation-errors-184] from collections.abc import Mapping from pydantic import BaseModel, ValidationError class BadMapping(Mapping): def items(self): raise ValueError() def __iter__(self): raise ValueError() def __getitem__(self, key): raise ValueError() def __len__(self): return 1 class Model(BaseModel): x: dict[str, str] try: Model(x=BadMapping()) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'mapping_type'

- [pydantic-validation-errors-185] missing

- [pydantic-validation-errors-186] This error is raised when there are required fields missing from the input value:

- [pydantic-validation-errors-187] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: str try: Model() except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'missing'

- [pydantic-validation-errors-188] missing_argument

- [pydantic-validation-errors-189] This error is raised when a required positional-or-keyword argument is not passed to a function decorated with validate_call :

- [pydantic-validation-errors-190] from pydantic import ValidationError, validate_call @validate_call def foo(a: int): return a try: foo() except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'missing_argument'

- [pydantic-validation-errors-191] missing_keyword_only_argument

- [pydantic-validation-errors-192] This error is raised when a required keyword-only argument is not passed to a function decorated with validate_call :

- [pydantic-validation-errors-193] from pydantic import ValidationError, validate_call @validate_call def foo(*, a: int): return a try: foo() except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'missing_keyword_only_argument'

- [pydantic-validation-errors-194] missing_positional_only_argument

- [pydantic-validation-errors-195] This error is raised when a required positional-only argument is not passed to a function decorated with validate_call :

- [pydantic-validation-errors-196] from pydantic import ValidationError, validate_call @validate_call def foo(a: int, /): return a try: foo() except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'missing_positional_only_argument'

- [pydantic-validation-errors-197] missing_sentinel_error

- [pydantic-validation-errors-198] This error is raised when the experimental MISSING sentinel is the only value allowed, and wasn’t provided during validation:

- [pydantic-validation-errors-199] from pydantic import BaseModel, ValidationError from pydantic.experimental.missing_sentinel import MISSING class Model(BaseModel): f: MISSING try: Model(f=1) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'missing_sentinel_error'

- [pydantic-validation-errors-200] model_attributes_type

- [pydantic-validation-errors-201] This error is raised when the input value is not a valid dictionary, model instance, or instance that fields can be extracted from:

- [pydantic-validation-errors-202] from pydantic import BaseModel, ValidationError class Model(BaseModel): a: int b: int # simply validating a dict print(Model.model_validate({'a': 1, 'b': 2})) #> a=1 b=2 class CustomObj: def __init__(self, a, b): self.a = a self.b = b # using from attributes to extract fields from an objects print(Model.model_validate(CustomObj(3, 4), from_attributes=True)) #> a=3 b=4 try: Model.model_validate('not an object', from_attributes=True) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'model_attributes_type'

- [pydantic-validation-errors-203] model_type

- [pydantic-validation-errors-204] This error is raised when the input to a model is not an instance of the model or dict:

- [pydantic-validation-errors-205] from pydantic import BaseModel, ValidationError class Model(BaseModel): a: int b: int # simply validating a dict m = Model.model_validate({'a': 1, 'b': 2}) print(m) #> a=1 b=2 # validating an existing model instance print(Model.model_validate(m)) #> a=1 b=2 try: Model.model_validate('not an object') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'model_type'

- [pydantic-validation-errors-206] multiple_argument_values

- [pydantic-validation-errors-207] This error is raised when you provide multiple values for a single argument while calling a function decorated with validate_call :

- [pydantic-validation-errors-208] from pydantic import ValidationError, validate_call @validate_call def foo(a: int): return a try: foo(1, a=2) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'multiple_argument_values'

- [pydantic-validation-errors-209] multiple_of

- [pydantic-validation-errors-210] This error is raised when the input is not a multiple of a field’s multiple_of constraint:

- [pydantic-validation-errors-211] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: int = Field(multiple_of=5) try: Model(x=1) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'multiple_of'

- [pydantic-validation-errors-212] needs_python_object

- [pydantic-validation-errors-213] This type of error is raised when validation is attempted from a format that cannot be converted to a Python object. For example, we cannot check isinstance or issubclass from JSON:

- [pydantic-validation-errors-214] import json from pydantic import BaseModel, ValidationError class Model(BaseModel): bm: type[BaseModel] try: Model.model_validate_json(json.dumps({'bm': 'not a basemodel class'})) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'needs_python_object'

- [pydantic-validation-errors-215] no_such_attribute

- [pydantic-validation-errors-216] This error is raised when validate_assignment=True in the config, and you attempt to assign a value to an attribute that is not an existing field:

- [pydantic-validation-errors-217] from pydantic import ConfigDict, ValidationError, dataclasses @dataclasses.dataclass(config=ConfigDict(validate_assignment=True)) class MyDataclass: x: int m = MyDataclass(x=1) try: m.y = 10 except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'no_such_attribute'

- [pydantic-validation-errors-218] none_required

- [pydantic-validation-errors-219] This error is raised when the input value is not None for a field that requires None :

- [pydantic-validation-errors-220] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: None try: Model(x=1) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'none_required'

- [pydantic-validation-errors-221] recursion_loop

- [pydantic-validation-errors-222] This error is raised when a cyclic reference is detected:

- [pydantic-validation-errors-223] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: list['Model'] d = {'x': []} d['x'].append(d) try: Model(**d) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'recursion_loop'

- [pydantic-validation-errors-224] set_item_not_hashable

- [pydantic-validation-errors-225] This error is raised when an unhashable value is validated against a set or a frozenset :

- [pydantic-validation-errors-226] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: set[object] class Unhashable: __hash__ = None try: Model(x=[{'a': 'b'}, Unhashable()]) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'set_item_not_hashable' print(repr(exc.errors()[1]['type'])) #> 'set_item_not_hashable'

- [pydantic-validation-errors-227] set_type

- [pydantic-validation-errors-228] This error is raised when the value type is not valid for a set field:

- [pydantic-validation-errors-229] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: set[int] try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'set_type'

- [pydantic-validation-errors-230] string_not_ascii

- [pydantic-validation-errors-231] This error is raised when the input string contains non-ASCII characters:

- [pydantic-validation-errors-232] from typing import Annotated from pydantic import BaseModel, StringConstraints, ValidationError class Model(BaseModel): v: Annotated[str, StringConstraints(ascii_only=True)] try: Model(v='caf\u00e9') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'string_not_ascii'

- [pydantic-validation-errors-233] string_pattern_mismatch

- [pydantic-validation-errors-234] This error is raised when the input value doesn’t match the field’s pattern constraint:

- [pydantic-validation-errors-235] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: str = Field(pattern='test') try: Model(x='1') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'string_pattern_mismatch'

- [pydantic-validation-errors-236] string_sub_type

- [pydantic-validation-errors-237] This error is raised when the value is an instance of a strict subtype of str when the field is strict:

- [pydantic-validation-errors-238] from enum import Enum from pydantic import BaseModel, Field, ValidationError class MyEnum(str, Enum): foo = 'foo' class Model(BaseModel): x: str = Field(strict=True) try: Model(x=MyEnum.foo) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'string_sub_type'

- [pydantic-validation-errors-239] string_too_long

- [pydantic-validation-errors-240] This error is raised when the input value is a string whose length is greater than the field’s max_length constraint:

- [pydantic-validation-errors-241] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: str = Field(max_length=3) try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'string_too_long'

- [pydantic-validation-errors-242] string_too_short

- [pydantic-validation-errors-243] This error is raised when the input value is a string whose length is less than the field’s min_length constraint:

- [pydantic-validation-errors-244] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: str = Field(min_length=3) try: Model(x='t') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'string_too_short'

- [pydantic-validation-errors-245] string_type

- [pydantic-validation-errors-246] This error is raised when the input value’s type is not valid for a str field:

- [pydantic-validation-errors-247] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: str try: Model(x=1) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'string_type'

- [pydantic-validation-errors-248] This error is also raised for strict fields when the input value is not an instance of str .

- [pydantic-validation-errors-249] string_unicode

- [pydantic-validation-errors-250] This error is raised when the value cannot be parsed as a Unicode string:

- [pydantic-validation-errors-251] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: str try: Model(x=b'\x81') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'string_unicode'

- [pydantic-validation-errors-252] time_delta_parsing

- [pydantic-validation-errors-253] This error is raised when the input value is a string that cannot be parsed for a timedelta field:

- [pydantic-validation-errors-254] from datetime import timedelta from pydantic import BaseModel, ValidationError class Model(BaseModel): x: timedelta try: Model(x='t') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'time_delta_parsing'

- [pydantic-validation-errors-255] time_delta_type

- [pydantic-validation-errors-256] This error is raised when the input value’s type is not valid for a timedelta field:

- [pydantic-validation-errors-257] from datetime import timedelta from pydantic import BaseModel, ValidationError class Model(BaseModel): x: timedelta try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'time_delta_type'

- [pydantic-validation-errors-258] This error is also raised for strict fields when the input value is not an instance of timedelta .

- [pydantic-validation-errors-259] time_parsing

- [pydantic-validation-errors-260] This error is raised when the input value is a string that cannot be parsed for a time field:

- [pydantic-validation-errors-261] from datetime import time from pydantic import BaseModel, ValidationError class Model(BaseModel): x: time try: Model(x='25:20:30.400') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'time_parsing'

- [pydantic-validation-errors-262] time_type

- [pydantic-validation-errors-263] This error is raised when the value type is not valid for a time field:

- [pydantic-validation-errors-264] from datetime import time from pydantic import BaseModel, ValidationError class Model(BaseModel): x: time try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'time_type'

- [pydantic-validation-errors-265] This error is also raised for strict fields when the input value is not an instance of time .

- [pydantic-validation-errors-266] timezone_aware

- [pydantic-validation-errors-267] This error is raised when the datetime value provided for a timezone-aware datetime field doesn’t have timezone information:

- [pydantic-validation-errors-268] from datetime import datetime from pydantic import AwareDatetime, BaseModel, ValidationError class Model(BaseModel): x: AwareDatetime try: Model(x=datetime.now()) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'timezone_aware'

- [pydantic-validation-errors-269] timezone_naive

- [pydantic-validation-errors-270] This error is raised when the datetime value provided for a timezone-naive datetime field has timezone info:

- [pydantic-validation-errors-271] from datetime import datetime, timezone from pydantic import BaseModel, NaiveDatetime, ValidationError class Model(BaseModel): x: NaiveDatetime try: Model(x=datetime.now(tz=timezone.utc)) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'timezone_naive'

- [pydantic-validation-errors-272] too_long

- [pydantic-validation-errors-273] This error is raised when the input value’s length is greater than the field’s max_length constraint:

- [pydantic-validation-errors-274] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: list[int] = Field(max_length=3) try: Model(x=[1, 2, 3, 4]) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'too_long'

- [pydantic-validation-errors-275] too_short

- [pydantic-validation-errors-276] This error is raised when the value length is less than the field’s min_length constraint:

- [pydantic-validation-errors-277] from pydantic import BaseModel, Field, ValidationError class Model(BaseModel): x: list[int] = Field(min_length=3) try: Model(x=[1, 2]) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'too_short'

- [pydantic-validation-errors-278] tuple_type

- [pydantic-validation-errors-279] This error is raised when the input value’s type is not valid for a tuple field:

- [pydantic-validation-errors-280] from pydantic import BaseModel, ValidationError class Model(BaseModel): x: tuple[int] try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'tuple_type'

- [pydantic-validation-errors-281] This error is also raised for strict fields when the input value is not an instance of tuple .

- [pydantic-validation-errors-282] unexpected_keyword_argument

- [pydantic-validation-errors-283] This error is raised when you provide a value by keyword for a positional-only argument while calling a function decorated with validate_call :

- [pydantic-validation-errors-284] from pydantic import ValidationError, validate_call @validate_call def foo(a: int, /): return a try: foo(a=2) except ValidationError as exc: print(repr(exc.errors()[1]['type'])) #> 'unexpected_keyword_argument'

- [pydantic-validation-errors-285] It is also raised when using pydantic.dataclasses and extra=forbid :

- [pydantic-validation-errors-286] from pydantic import TypeAdapter, ValidationError from pydantic.dataclasses import dataclass @dataclass(config={'extra': 'forbid'}) class Foo: bar: int try: TypeAdapter(Foo).validate_python({'bar': 1, 'foobar': 2}) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'unexpected_keyword_argument'

- [pydantic-validation-errors-287] unexpected_positional_argument

- [pydantic-validation-errors-288] This error is raised when you provide a positional value for a keyword-only argument while calling a function decorated with validate_call :

- [pydantic-validation-errors-289] from pydantic import ValidationError, validate_call @validate_call def foo(*, a: int): return a try: foo(2) except ValidationError as exc: print(repr(exc.errors()[1]['type'])) #> 'unexpected_positional_argument'

- [pydantic-validation-errors-290] union_tag_invalid

- [pydantic-validation-errors-291] This error is raised when the input’s discriminator is not one of the expected values:

- [pydantic-validation-errors-292] from typing import Literal, Union from pydantic import BaseModel, Field, ValidationError class BlackCat(BaseModel): pet_type: Literal['blackcat'] class WhiteCat(BaseModel): pet_type: Literal['whitecat'] class Model(BaseModel): cat: Union[BlackCat, WhiteCat] = Field(discriminator='pet_type') try: Model(cat={'pet_type': 'dog'}) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'union_tag_invalid'

- [pydantic-validation-errors-293] union_tag_not_found

- [pydantic-validation-errors-294] This error is raised when it is not possible to extract a discriminator value from the input:

- [pydantic-validation-errors-295] from typing import Literal, Union from pydantic import BaseModel, Field, ValidationError class BlackCat(BaseModel): pet_type: Literal['blackcat'] class WhiteCat(BaseModel): pet_type: Literal['whitecat'] class Model(BaseModel): cat: Union[BlackCat, WhiteCat] = Field(discriminator='pet_type') try: Model(cat={'name': 'blackcat'}) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'union_tag_not_found'

- [pydantic-validation-errors-296] url_parsing

- [pydantic-validation-errors-297] This error is raised when the input value cannot be parsed as a URL:

- [pydantic-validation-errors-298] from pydantic import AnyUrl, BaseModel, ValidationError class Model(BaseModel): x: AnyUrl try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'url_parsing'

- [pydantic-validation-errors-299] url_scheme

- [pydantic-validation-errors-300] This error is raised when the URL scheme is not valid for the URL type of the field:

- [pydantic-validation-errors-301] from pydantic import BaseModel, HttpUrl, ValidationError class Model(BaseModel): x: HttpUrl try: Model(x='ftp://example.com') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'url_scheme'

- [pydantic-validation-errors-302] url_syntax_violation

- [pydantic-validation-errors-303] This error is raised when the URL syntax is not valid:

- [pydantic-validation-errors-304] from pydantic import BaseModel, Field, HttpUrl, ValidationError class Model(BaseModel): x: HttpUrl = Field(strict=True) try: Model(x='http:////example.com') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'url_syntax_violation'

- [pydantic-validation-errors-305] url_too_long

- [pydantic-validation-errors-306] This error is raised when the URL length is greater than 2083:

- [pydantic-validation-errors-307] from pydantic import BaseModel, HttpUrl, ValidationError class Model(BaseModel): x: HttpUrl try: Model(x='x' * 2084) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'url_too_long'

- [pydantic-validation-errors-308] url_type

- [pydantic-validation-errors-309] This error is raised when the input value’s type is not valid for a URL field:

- [pydantic-validation-errors-310] from pydantic import BaseModel, HttpUrl, ValidationError class Model(BaseModel): x: HttpUrl try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'url_type'

- [pydantic-validation-errors-311] uuid_parsing

- [pydantic-validation-errors-312] This error is raised when the input value’s type is not valid for a UUID field:

- [pydantic-validation-errors-313] from uuid import UUID from pydantic import BaseModel, ValidationError class Model(BaseModel): u: UUID try: Model(u='12345678-124-1234-1234-567812345678') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'uuid_parsing'

- [pydantic-validation-errors-314] uuid_type

- [pydantic-validation-errors-315] This error is raised when the input value’s type is not valid instance for a UUID field (str, bytes or UUID):

- [pydantic-validation-errors-316] from uuid import UUID from pydantic import BaseModel, ValidationError class Model(BaseModel): u: UUID try: Model(u=1234567812412341234567812345678) except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'uuid_type'

- [pydantic-validation-errors-317] uuid_version

- [pydantic-validation-errors-318] This error is raised when the input value’s type is not match UUID version:

- [pydantic-validation-errors-319] from pydantic import UUID5, BaseModel, ValidationError class Model(BaseModel): u: UUID5 try: Model(u='a6cc5730-2261-11ee-9c43-2eb5a363657c') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'uuid_version'

- [pydantic-validation-errors-320] value_error

- [pydantic-validation-errors-321] This error is raised when a ValueError is raised during validation:

- [pydantic-validation-errors-322] from pydantic import BaseModel, ValidationError, field_validator class Model(BaseModel): x: str @field_validator('x') @classmethod def repeat_b(cls, v): raise ValueError() try: Model(x='test') except ValidationError as exc: print(repr(exc.errors()[0]['type'])) #> 'value_error'
