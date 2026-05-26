---
id: pydantic-validation-error-type
kind: debug-recipe
status: accepted
stack:
- pydantic
failure_class: pydantic/validation
symptoms:
- Pydantic raises ValidationError with an unexpected error type during model instantiation
  or validation
fingerprints:
- ValidationError
- int_parsing
- bool_type
- missing
- greater_than
- validation error
first_checks:
- Check the error type field in exc.errors()[0]['type'] against the Pydantic validation
  error catalog
- Check the loc tuple to find which field path failed validation
- Check whether strict mode is enabled and affects the allowed input types
do_not:
- Do not catch ValidationError broadly without inspecting the individual error types
- Do not assume coercion will always succeed; check type constraints on Field definitions
evidence_needed:
- Capture exc.errors() to see all validation errors, their types, locs, and messages
- Identify the model field annotations and Field constraints that failed
minimal_fix_scope:
- The model field definition and type annotation
- The input data structure passed to model_validate or model instantiation
validation_ladder:
- Instantiate the model with failing data and inspect the ValidationError
- Verify the fix eliminates all errors of the same type
- Run the model unit test covering the affected field
regression_guard:
- Add a model test that asserts correct ValidationError.type for invalid input
evidence_refs:
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-4
  short_excerpt: 'from typing import NamedTuple from pydantic import BaseModel, ValidationError
    class MyNamedTuple(NamedTuple): x: int class MyModel(BaseModel): field: MyNamedTuple
    try: MyModel.model_validate({''field'': ''invalid''}) except ValidationError as
    exc: print(repr(exc.errors()[0][''type''])) #> ''arguments_type'''
  quote_hash: sha256:c916b6883374a5def53efa7e4dc25b7e0a50d4189a1155360159dadda6a82d76
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-7
  short_excerpt: 'from pydantic import BaseModel, ValidationError, field_validator
    class Model(BaseModel): x: int @field_validator(''x'') @classmethod def force_x_positive(cls,
    v): assert v > 0 return v try: Model(x=-1) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''assertion_error'''
  quote_hash: sha256:677ad929b5717df51a6b4080e746dcef9a9fcb9ff26b05909bf1f7a8ae43e274
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-10
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: bool Model(x=''true'') # OK try: Model(x=''test'') except ValidationError as
    exc: print(repr(exc.errors()[0][''type''])) #> ''bool_parsing'''
  quote_hash: sha256:a2f8db1c52596893749cfa82cd9142968f17ec5b0617a287495896d127436dfd
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-11
  short_excerpt: bool_type
  quote_hash: sha256:78337903eefb6c177bb09d0315793da788c46261255d5861618e99aee840f87d
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-13
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: bool try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''bool_type'''
  quote_hash: sha256:4a3bfe9c60849384dbcb20390cdbfe5171405665821ddd1442111d625a4b0054
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-17
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: bytes model_config = {''val_json_bytes'': ''hex''} try: Model(x=''a'') except
    ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''bytes_invalid_encoding'''
  quote_hash: sha256:d3b16276f090d7e94a3b45d8fbde6a53091240e18e5c4a0302ab568b1c9aabfd
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-20
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: bytes = Field(max_length=3) try: Model(x=b''test'') except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''bytes_too_long'''
  quote_hash: sha256:3d4e2c9219877844a66cdcaa987f1d983ea47522cd00216b7f52d03dc2fdefd8
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-23
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: bytes = Field(min_length=3) try: Model(x=b''t'') except ValidationError as
    exc: print(repr(exc.errors()[0][''type''])) #> ''bytes_too_short'''
  quote_hash: sha256:349bf6e798db792781946ac345a7568a3d0aed0a9411892493986359d0396a9a
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-26
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: bytes try: Model(x=123) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''bytes_type'''
  quote_hash: sha256:b67ff0d5e15559be4ee637eacdd28af261f128df753a3ae2eb2583bae2574fd3
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-30
  short_excerpt: 'from typing import Any, Callable from pydantic import BaseModel,
    ImportString, ValidationError class Model(BaseModel): x: ImportString[Callable[[Any],
    Any]] Model(x=''math:cos'') # OK try: Model(x=''os.path'') except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''callable_type'''
  quote_hash: sha256:74d983fdb70f9d4e7b07a8f0b571576c25e8f22ad08e41b5934578ed857a297c
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-33
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    num: complex try: # Complex numbers in json are expected to be valid complex strings.
    # This value `abc` is not a valid complex string. Model.model_validate_json(''{"num":
    "abc"}'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''complex_str_parsing'''
  quote_hash: sha256:e3a399a59b741e072beade3b84a51400f2cd11527635eb7b37d71a470be44eac
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-36
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    num: complex try: Model(num=False) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''complex_type'''
  quote_hash: sha256:2ea18872f4de207b513ecd5fe82a0cf0563dea41c36d99b18390e9b7446fc7dd
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-39
  short_excerpt: 'import pydantic.dataclasses from pydantic import TypeAdapter, ValidationError
    @pydantic.dataclasses.dataclass class MyDataclass: x: str adapter = TypeAdapter(MyDataclass)
    print(adapter.validate_python(MyDataclass(x=''test''), strict=True)) #> MyDataclass(x=''test'')
    print(adapter.validate_python({''x'': ''test''})) #> MyDataclass(x=''test'') try:
    adapter.validate_python({''x'': ''test''}, strict=True) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''dataclass_exact_type'''
  quote_hash: sha256:a80ac5e886f027d87b9a4972dc217e5877b235f5841722840c27bb2a2d0c9d1a
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-42
  short_excerpt: 'from pydantic import ValidationError, dataclasses @dataclasses.dataclass
    class Inner: x: int @dataclasses.dataclass class Outer: y: Inner Outer(y=Inner(x=1))
    # OK try: Outer(y=1) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''dataclass_type'''
  quote_hash: sha256:8f8266ebb169a3741a06068db06f42bb92152183807b56b4ab2d17cae92f7336
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-45
  short_excerpt: 'from datetime import date, datetime from pydantic import BaseModel,
    ValidationError class Model(BaseModel): x: date Model(x=''2023-01-01'') # OK Model(x=datetime(2023,
    1, 1)) # OK try: Model(x=datetime(2023, 1, 1, 12)) except ValidationError as exc:
    print(repr(exc.errors()[0][''type''])) #> ''date_from_datetime_inexact'''
  quote_hash: sha256:d8f2c3934e5c09e08c06cf1957300079c004bf3e50796135c55380f1cb6a2116
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-48
  short_excerpt: 'from datetime import date from pydantic import BaseModel, ValidationError
    class Model(BaseModel): x: date try: Model(x=''XX1494012000'') except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''date_from_datetime_parsing'''
  quote_hash: sha256:09c5d656c0d8c2bff958c2c97caa904dbe42d8d24b039f852f2fc76cb21fdfdf
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-51
  short_excerpt: 'from datetime import date from pydantic import BaseModel, FutureDate,
    ValidationError class Model(BaseModel): x: FutureDate try: Model(x=date(2000,
    1, 1)) except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #>
    ''date_future'''
  quote_hash: sha256:779dd12812b3bad9bb8e936e4220011ca48b68a3667dcd6bda61cd71fba02385
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-54
  short_excerpt: 'import json from datetime import date from pydantic import BaseModel,
    Field, ValidationError class Model(BaseModel): x: date = Field(strict=True) try:
    Model.model_validate_json(json.dumps({''x'': ''1''})) except ValidationError as
    exc: print(repr(exc.errors()[0][''type''])) #> ''date_parsing'''
  quote_hash: sha256:2e71abfc1dc973bad79b762fc78594333163f6dafbf25eecf9804726f4316261
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-57
  short_excerpt: 'from datetime import date, timedelta from pydantic import BaseModel,
    PastDate, ValidationError class Model(BaseModel): x: PastDate try: Model(x=date.today()
    + timedelta(1)) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''date_past'''
  quote_hash: sha256:7cfa8621e56ced9b1efbd8dd29c8bf82c982fd1fcbe80d6713a66f4fde5ef055
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-60
  short_excerpt: 'from datetime import date from pydantic import BaseModel, ValidationError
    class Model(BaseModel): x: date try: Model(x=None) except ValidationError as exc:
    print(repr(exc.errors()[0][''type''])) #> ''date_type'''
  quote_hash: sha256:9dd74b2ba8cc77b7882a95babb0794fb74cb48db6079975f8bb5fc073bcf06e9
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-64
  short_excerpt: 'from datetime import datetime from pydantic import BaseModel, ValidationError
    class Model(BaseModel): x: datetime try: # there is no 13th month Model(x=''2023-13-01'')
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''datetime_from_date_parsing'''
  quote_hash: sha256:8e7120ce5e4def87322dee035eb242526e7ef5094f74a01899964538d9ace6d0
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-67
  short_excerpt: 'from datetime import datetime from pydantic import BaseModel, FutureDatetime,
    ValidationError class Model(BaseModel): x: FutureDatetime try: Model(x=datetime(2000,
    1, 1)) except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #>
    ''datetime_future'''
  quote_hash: sha256:717b7d0013c8db82d7b9cb92920903c6827395097076561d7d8f9776fad08537
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-70
  short_excerpt: 'from datetime import datetime, tzinfo from pydantic import AwareDatetime,
    BaseModel, ValidationError class CustomTz(tzinfo): # utcoffset is not implemented!
    def tzname(self, _dt): return ''CustomTZ'' class Model(BaseModel): x: AwareDatetime
    try: Model(x=datetime(2023, 1, 1, tzinfo=CustomTz())) except ValidationError as
    exc: print(repr(exc.errors()[0][''type''])) #> ''datetime_object_invalid'''
  quote_hash: sha256:e91f52428eeab6c20100df85cea0c973ebc12426950fc6dccf5329a1b04b35f9
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-73
  short_excerpt: 'import json from datetime import datetime from pydantic import BaseModel,
    Field, ValidationError class Model(BaseModel): x: datetime = Field(strict=True)
    try: Model.model_validate_json(json.dumps({''x'': ''not a datetime''})) except
    ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''datetime_parsing'''
  quote_hash: sha256:cc8290d7d54ec0b477629a8f8938250f27ce8603b4ebe8709ec0d207b79b88ea
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-76
  short_excerpt: 'from datetime import datetime, timedelta from pydantic import BaseModel,
    PastDatetime, ValidationError class Model(BaseModel): x: PastDatetime try: Model(x=datetime.now()
    + timedelta(100)) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''datetime_past'''
  quote_hash: sha256:94bf0f5cfe0122ce78836f7c1208784e55f4d02e1b24a4d4874fb6f7fa3e9aa7
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-79
  short_excerpt: 'from datetime import datetime from pydantic import BaseModel, ValidationError
    class Model(BaseModel): x: datetime try: Model(x=None) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''datetime_type'''
  quote_hash: sha256:567208775e0ca196825e588c0cdfa1e94589c895bc3e6165541fd4d4a825515c
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-83
  short_excerpt: 'from decimal import Decimal from pydantic import BaseModel, Field,
    ValidationError class Model(BaseModel): x: Decimal = Field(max_digits=3) try:
    Model(x=''42.1234'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''decimal_max_digits'''
  quote_hash: sha256:c393769ae2fe258d4248399cd34babdc1833fcd3b28cf170cb8f87e77de305f2
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-86
  short_excerpt: 'from decimal import Decimal from pydantic import BaseModel, Field,
    ValidationError class Model(BaseModel): x: Decimal = Field(decimal_places=3) try:
    Model(x=''42.1234'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''decimal_max_places'''
  quote_hash: sha256:c5184f50c28ffece51a82ef4dc0e48848b0d7956fbd10cfccb5a9aa77f41abea
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-89
  short_excerpt: 'from decimal import Decimal from pydantic import BaseModel, Field,
    ValidationError class Model(BaseModel): x: Decimal = Field(decimal_places=3) try:
    Model(x=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''decimal_parsing'''
  quote_hash: sha256:88ce0e894fb3ab75e9936d512ac3d5d2ace2ec4bcfb9889730fcec061b7df9de
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-92
  short_excerpt: 'from decimal import Decimal from pydantic import BaseModel, Field,
    ValidationError class Model(BaseModel): x: Decimal = Field(decimal_places=3) try:
    Model(x=[1, 2, 3]) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''decimal_type'''
  quote_hash: sha256:fe20e8b74b2e987d68f0a23ffa5e97f83e3df9733b78ab50c9061a23659dc718
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-96
  short_excerpt: 'from decimal import Decimal from pydantic import BaseModel, Field,
    ValidationError class Model(BaseModel): x: Decimal = Field(max_digits=6, decimal_places=3)
    try: Model(x=''12345.6'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''decimal_whole_digits'''
  quote_hash: sha256:57184a77aefa1b5ad24c26ad966753b746e5a0a102edb4b37ac12aae644b4d78
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-99
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    a: int = Field(gt=10) b: int = Field(default_factory=lambda data: data[''a''])
    try: Model(a=1) except ValidationError as exc: print(exc) """ 2 validation errors
    for Model a Input should be greater than 10 [type=greater_than, input_value=1,
    input_type=int] b The default factory uses validated data, but at least one validation
    error occurred [type=default_factory_not_called] """ print(repr(exc.errors()[1][''type'']))
    #> ''default_factory_not_called'''
  quote_hash: sha256:01f8fa9217c2145190db35af42aea9acd82e2252e4177bd5c20bd3ba609a43ff
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-102
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: dict try: Model(x=[''1'', ''2'']) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''dict_type'''
  quote_hash: sha256:dafed859de9e872c84c4a93b4f322f3eac305506cdc62d19781838d8e0e41a85
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-105
  short_excerpt: 'from enum import Enum from pydantic import BaseModel, ValidationError
    class MyEnum(str, Enum): option = ''option'' class Model(BaseModel): x: MyEnum
    try: Model(x=''other_option'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''enum'''
  quote_hash: sha256:77a5d34c5d8d541e8f52e2ab1bc47dc78986d21d72841a87c02f3362daba8471
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-108
  short_excerpt: 'from pydantic import BaseModel, ConfigDict, ValidationError class
    Model(BaseModel): x: str model_config = ConfigDict(extra=''forbid'') try: Model(x=''test'',
    y=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''extra_forbidden'''
  quote_hash: sha256:fc22dfd652cdaf4b2b8149af406dd9f9ff1ec0985b940c76c8a426fc33161674
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-112
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: int try: Model(x=2.2250738585072011e308) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''finite_number'''
  quote_hash: sha256:e7579fc03eeb49d3f808e6e0cc050af9035554acb08c87cebfd35a0364963cc2
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-115
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: float try: Model(x=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''float_parsing'''
  quote_hash: sha256:748b4fc2910ba343870b8789edfa0a12d74a61a32b4bd04817bc0ffe71377178
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-118
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: float try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''float_type'''
  quote_hash: sha256:790b721f2482d6746933506b7e404bee2f48e78ee72bbdd4c27abc9077cc88b6
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-121
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: str = Field(''test'', frozen=True) model = Model() try: model.x = ''test1''
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''frozen_field''
    try: del model.x except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''frozen_field'''
  quote_hash: sha256:8388431af0f81e1772ac2cdfcbfb2040212bbb43a0aeef8295cf5d211e79e5d5
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-124
  short_excerpt: 'from pydantic import BaseModel, ConfigDict, ValidationError class
    Model(BaseModel): x: int model_config = ConfigDict(frozen=True) m = Model(x=1)
    try: m.x = 2 except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''frozen_instance'' try: del m.x except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''frozen_instance'''
  quote_hash: sha256:d986fe867964cf9d485dc928a54b4fbcdfdf6da0fd72830da8926300b1ad50d9
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-127
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: frozenset try: model = Model(x=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''frozen_set_type'''
  quote_hash: sha256:5a898e981a051c3c8dd94f50accaa26108bb407a5209598f289c27aecb1a6e4d
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-130
  short_excerpt: 'from pydantic import BaseModel, ConfigDict, ValidationError class
    Foobar: def __init__(self): self.x = 1 @property def y(self): raise RuntimeError(''intentional
    error'') class Model(BaseModel): x: int y: str model_config = ConfigDict(from_attributes=True)
    try: Model.model_validate(Foobar()) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''get_attribute_error'''
  quote_hash: sha256:c187fad3d2919710cbd0a4e9c75ade24b6717ad5c0083117ea8d926fc818a011
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-131
  short_excerpt: greater_than
  quote_hash: sha256:2bb72793ee1e7618d7a260289fd1c81b92712cb26491cd01872473a56bf3dc95
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-133
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: int = Field(gt=10) try: Model(x=10) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''greater_than'''
  quote_hash: sha256:9a2e38528518437150b4aa34f9203c9f7fc1303e9388650fa23007e8e9b4820a
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-134
  short_excerpt: greater_than_equal
  quote_hash: sha256:0e51589ac60667a4af9981e0ea17e36268762ecdbdf2f1787fe3b2982f8190e3
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-136
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: int = Field(ge=10) try: Model(x=9) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''greater_than_equal'''
  quote_hash: sha256:bf26b7c64e4d03f36d04db7af9a4c86de2a63d03f8011a21f0cd9f048064d9c8
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-139
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: int try: Model(x=0.5) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''int_from_float'''
  quote_hash: sha256:576592616cf7dcabefc1764dda7230af6aa309e352399d50346363337a4b4864
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-140
  short_excerpt: int_parsing
  quote_hash: sha256:fbc4ab98b15ca653e13cf0833374edfbbe5bd741dfc3e6a7b50a4adf3f59c554
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-142
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: int try: Model(x=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''int_parsing'''
  quote_hash: sha256:23fb1d11224bc621a0faed4dda0439adbb80bbb734d21cee9796a89733123346
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-143
  short_excerpt: int_parsing_size
  quote_hash: sha256:9bd19bcaa647ee87bffc895f83d02a032a9909d078fb7eb6fc7ff8e1db477075
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-145
  short_excerpt: 'import json from pydantic import BaseModel, ValidationError class
    Model(BaseModel): x: int # from Python assert Model(x=''1'' * 4_300).x == int(''1''
    * 4_300) # OK too_long = ''1'' * 4_301 try: Model(x=too_long) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''int_parsing_size'' # from
    JSON try: Model.model_validate_json(json.dumps({''x'': too_long})) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''int_parsing_size'''
  quote_hash: sha256:7b6dc9bf14a2fd8035aaf2720f9b37a9d47330439a6121f06dad2bb90b2f6aa5
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-148
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: int try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''int_type'''
  quote_hash: sha256:b0a0fb30e76ef1feb1ea9c19789b012743b82f28e4ff9521a9e4758fd6ae1d00
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-151
  short_excerpt: 'from pydantic import BaseModel, ConfigDict, ValidationError class
    Model(BaseModel): x: int model_config = ConfigDict(extra=''allow'') try: Model.model_validate({''x'':
    1, b''y'': 2}) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''invalid_key'''
  quote_hash: sha256:9f9b728e16e45ef199f7c0631e1a6d64e746f770e3747254f155835c38b0dc16
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-154
  short_excerpt: 'from pydantic import BaseModel, ConfigDict, ValidationError class
    Nested: x: str class Model(BaseModel): y: Nested model_config = ConfigDict(arbitrary_types_allowed=True)
    try: Model(y=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''is_instance_of'''
  quote_hash: sha256:0018e9531d3bda6815efa059dde10d8c962464f16e10cfa268b1c67fd28a0439
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-157
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Nested: x:
    str class Model(BaseModel): y: type[Nested] try: Model(y=''test'') except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''is_subclass_of'''
  quote_hash: sha256:ed298db0b0d3ba8957e2857c073d06a41d66d63e69795bf520732df664c5ff34
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-160
  short_excerpt: 'from collections.abc import Iterable from pydantic import BaseModel,
    ValidationError class Model(BaseModel): y: Iterable[str] try: Model(y=123) except
    ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''iterable_type'''
  quote_hash: sha256:12b6190a568d86ba4e35d85b65ef78c5f3319b45ef44c6833c18bd5149206d9f
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-163
  short_excerpt: 'from pydantic import BaseModel, ValidationError def gen(): yield
    1 raise RuntimeError(''error'') class Model(BaseModel): x: list[int] try: Model(x=gen())
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''iteration_error'''
  quote_hash: sha256:f63b0ab3f582e00e91e95d47ff1964da090c5762bae463f4e59a4b2890052141
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-166
  short_excerpt: 'from pydantic import BaseModel, Json, ValidationError class Model(BaseModel):
    x: Json try: Model(x=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''json_invalid'''
  quote_hash: sha256:f35c9e06cce3bd2813b0ae5a835b527915b2feb87fb9d0bb91e0ec99f73d55cb
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-169
  short_excerpt: 'from pydantic import BaseModel, Json, ValidationError class Model(BaseModel):
    x: Json try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''json_type'''
  quote_hash: sha256:d0b84d8aacb5bffa3f150118a396f4c27a734e6e132c4a3bf4f3b4f2bba44502
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-172
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: int = Field(lt=10) try: Model(x=10) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''less_than'''
  quote_hash: sha256:3c6fa3634824e2b13122ecd65ec45b0a5f931d245143500204a70c638e03c6c5
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-175
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: int = Field(le=10) try: Model(x=11) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''less_than_equal'''
  quote_hash: sha256:c0bb855368d9219ea788380a839aea93da7a107477f52c08f434996aa945b1de
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-178
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: list[int] try: Model(x=1) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''list_type'''
  quote_hash: sha256:dc9f5b99fc63c560e32f0dc882f992d705778d51520e89b7fabe9de52fa1a811
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-181
  short_excerpt: 'from typing import Literal from pydantic import BaseModel, ValidationError
    class Model(BaseModel): x: Literal[''a'', ''b''] Model(x=''a'') # OK try: Model(x=''c'')
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''literal_error'''
  quote_hash: sha256:e6ac947e9a7da563816bddc73a0a9a4fd1695d93916dee65aa456a43e005d6aa
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-184
  short_excerpt: 'from collections.abc import Mapping from pydantic import BaseModel,
    ValidationError class BadMapping(Mapping): def items(self): raise ValueError()
    def __iter__(self): raise ValueError() def __getitem__(self, key): raise ValueError()
    def __len__(self): return 1 class Model(BaseModel): x: dict[str, str] try: Model(x=BadMapping())
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''mapping_type'''
  quote_hash: sha256:1f19183cf37a5b92d51ae0b31ad2c41d999fc12811a63eb3eb4937e574e9db75
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-185
  short_excerpt: missing
  quote_hash: sha256:ffa63583dfa6706b87d284b86b0d693a161e4840aad2c5cf6b5d27c3b9621f7d
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-186
  short_excerpt: 'This error is raised when there are required fields missing from
    the input value:'
  quote_hash: sha256:5c053f93a362bc5330e4ae25219abf06b9d41e4d1d64deff887c1b2c68eef531
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-187
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: str try: Model() except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''missing'''
  quote_hash: sha256:0ac5acaf3b8d2c665d67c9642a4f21ab53e1cd1eafb933a086a4f2c3158ffa00
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-188
  short_excerpt: missing_argument
  quote_hash: sha256:c35a95ce801f566f40f30c336811232536e08bd8a73fb77b7ac27f1003a9569b
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-190
  short_excerpt: 'from pydantic import ValidationError, validate_call @validate_call
    def foo(a: int): return a try: foo() except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''missing_argument'''
  quote_hash: sha256:6eeb2ed592b6b474da23f5d77601eb15220845984d07e5fc1bc1fed2dc3bb54a
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-191
  short_excerpt: missing_keyword_only_argument
  quote_hash: sha256:8b05c6e6a57d3ed9c6670d2772355f8e3d3dcc8b5e26d476a4e97555f7342852
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-193
  short_excerpt: 'from pydantic import ValidationError, validate_call @validate_call
    def foo(*, a: int): return a try: foo() except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''missing_keyword_only_argument'''
  quote_hash: sha256:c3764d9731201d20810d2a6627dbf65943d88d4426a22c681921fb08006ff4be
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-194
  short_excerpt: missing_positional_only_argument
  quote_hash: sha256:213b894c3990c68bd7f8c8b9370a1a09ef1350277e19a7541d83225aee792e70
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-196
  short_excerpt: 'from pydantic import ValidationError, validate_call @validate_call
    def foo(a: int, /): return a try: foo() except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''missing_positional_only_argument'''
  quote_hash: sha256:6204ff25000e63b2b0047809462a30ae9845252c3348a31d7bc46a21fef90ae3
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-197
  short_excerpt: missing_sentinel_error
  quote_hash: sha256:3d440b9a75b5794a571e4489861629035f75e9a4ce5530a0a8945bf76ee962c8
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-198
  short_excerpt: 'This error is raised when the experimental MISSING sentinel is the
    only value allowed, and wasn’t provided during validation:'
  quote_hash: sha256:87936163d3e780e480d2a286d5db4473ace84e0ed4919d0b8de6d7e422de7cba
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-199
  short_excerpt: 'from pydantic import BaseModel, ValidationError from pydantic.experimental.missing_sentinel
    import MISSING class Model(BaseModel): f: MISSING try: Model(f=1) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''missing_sentinel_error'''
  quote_hash: sha256:86f1d54b78f91959f542a2fbf97a041cc7279c298c557f460d24a1fadc6b57b6
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-202
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    a: int b: int # simply validating a dict print(Model.model_validate({''a'': 1,
    ''b'': 2})) #> a=1 b=2 class CustomObj: def __init__(self, a, b): self.a = a self.b
    = b # using from attributes to extract fields from an objects print(Model.model_validate(CustomObj(3,
    4), from_attributes=True)) #> a=3 b=4 try: Model.model_validate(''not an object'',
    from_attributes=True) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''model_attributes_type'''
  quote_hash: sha256:4f961e3f778d9e2e740b5fa577f20896fa3b9b4963f3ebacee2889916cf9d52f
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-205
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    a: int b: int # simply validating a dict m = Model.model_validate({''a'': 1, ''b'':
    2}) print(m) #> a=1 b=2 # validating an existing model instance print(Model.model_validate(m))
    #> a=1 b=2 try: Model.model_validate(''not an object'') except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''model_type'''
  quote_hash: sha256:ad8814f76b6af3285a36738563b3c761b89988196ee468a61f06fa288417c3e8
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-208
  short_excerpt: 'from pydantic import ValidationError, validate_call @validate_call
    def foo(a: int): return a try: foo(1, a=2) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''multiple_argument_values'''
  quote_hash: sha256:f770fa39f0f454615288d87c3aa6886b4d9924266f0f499cd8ab8583bf37ba4b
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-211
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: int = Field(multiple_of=5) try: Model(x=1) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''multiple_of'''
  quote_hash: sha256:b7970a452f63c376ecb57b6166e5e980433e48481bd527df3c7516af88bee05d
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-214
  short_excerpt: 'import json from pydantic import BaseModel, ValidationError class
    Model(BaseModel): bm: type[BaseModel] try: Model.model_validate_json(json.dumps({''bm'':
    ''not a basemodel class''})) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''needs_python_object'''
  quote_hash: sha256:a7f51ae94340b26a9a5e16a0748f3220492e02205553754cec3f81a8386608b0
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-217
  short_excerpt: 'from pydantic import ConfigDict, ValidationError, dataclasses @dataclasses.dataclass(config=ConfigDict(validate_assignment=True))
    class MyDataclass: x: int m = MyDataclass(x=1) try: m.y = 10 except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''no_such_attribute'''
  quote_hash: sha256:3c43c8cb90b5c6e88c1cd36c81a2f75ef2b12cda7e980b2cad521a4803c4b8d4
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-220
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: None try: Model(x=1) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''none_required'''
  quote_hash: sha256:2e105e5af65ce2ce4a852f98c2ae057a93ddcbee1fb4979767139c821c640e98
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-223
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: list[''Model''] d = {''x'': []} d[''x''].append(d) try: Model(**d) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''recursion_loop'''
  quote_hash: sha256:f058daff80cb19de970a4c0e843d6a61ec8ad68709c48cb36e8ed2fe32e48743
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-226
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: set[object] class Unhashable: __hash__ = None try: Model(x=[{''a'': ''b''},
    Unhashable()]) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''set_item_not_hashable'' print(repr(exc.errors()[1][''type''])) #> ''set_item_not_hashable'''
  quote_hash: sha256:177645a28753158844d56b26f9a2fad31d4285bf5138a8ac4c3cba28b6889316
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-229
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: set[int] try: Model(x=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''set_type'''
  quote_hash: sha256:234ba189100bdf56c551e37ba79a1f291a6900dae184c12f5deb77d3fd0a6c05
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-232
  short_excerpt: 'from typing import Annotated from pydantic import BaseModel, StringConstraints,
    ValidationError class Model(BaseModel): v: Annotated[str, StringConstraints(ascii_only=True)]
    try: Model(v=''caf\u00e9'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''string_not_ascii'''
  quote_hash: sha256:413bc44e87fa5eeeb54c880d8ecec332672fddaf6c12b6eb86f9bbb93a45837e
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-235
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: str = Field(pattern=''test'') try: Model(x=''1'') except ValidationError as
    exc: print(repr(exc.errors()[0][''type''])) #> ''string_pattern_mismatch'''
  quote_hash: sha256:45044078dfcb8474422aa8768d0526b73caf5589a04792c1759a7dff6c1999e1
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-238
  short_excerpt: 'from enum import Enum from pydantic import BaseModel, Field, ValidationError
    class MyEnum(str, Enum): foo = ''foo'' class Model(BaseModel): x: str = Field(strict=True)
    try: Model(x=MyEnum.foo) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''string_sub_type'''
  quote_hash: sha256:5441cd61b11c4bfc2242dd5e9b995efc82d00dd807b7f98d24b7af5348de44ff
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-241
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: str = Field(max_length=3) try: Model(x=''test'') except ValidationError as
    exc: print(repr(exc.errors()[0][''type''])) #> ''string_too_long'''
  quote_hash: sha256:a01d63127efa817787f406dde7f7780e9e56f7b940f3f0e110f52a02723385be
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-244
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: str = Field(min_length=3) try: Model(x=''t'') except ValidationError as exc:
    print(repr(exc.errors()[0][''type''])) #> ''string_too_short'''
  quote_hash: sha256:c071b27be5e16466c37e05c142528184eaa743b1d9099fafaa46e3d8648eca69
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-247
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: str try: Model(x=1) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''string_type'''
  quote_hash: sha256:4d41fea0b61fa4f7ceb1897c90d64b62211a580f51b24139bc5acca5a37289e3
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-251
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: str try: Model(x=b''\x81'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''string_unicode'''
  quote_hash: sha256:2d8577748b8b6b531b78775e736265190f75bfeb00f140483b6be38f744c5ee0
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-254
  short_excerpt: 'from datetime import timedelta from pydantic import BaseModel, ValidationError
    class Model(BaseModel): x: timedelta try: Model(x=''t'') except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''time_delta_parsing'''
  quote_hash: sha256:2ca78f54b886f691887463a1c1a5bdb4a796fd45cef937d6e1294ab3aa2e27e2
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-257
  short_excerpt: 'from datetime import timedelta from pydantic import BaseModel, ValidationError
    class Model(BaseModel): x: timedelta try: Model(x=None) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''time_delta_type'''
  quote_hash: sha256:555f009454facda7564b44d013c48e7ba05cb1bad39718d132d84d47f5acab37
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-261
  short_excerpt: 'from datetime import time from pydantic import BaseModel, ValidationError
    class Model(BaseModel): x: time try: Model(x=''25:20:30.400'') except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''time_parsing'''
  quote_hash: sha256:f7207fc514d864e6878e67904df7ede5b1fd759de6bd8538b1c44c2af8f20fa2
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-264
  short_excerpt: 'from datetime import time from pydantic import BaseModel, ValidationError
    class Model(BaseModel): x: time try: Model(x=None) except ValidationError as exc:
    print(repr(exc.errors()[0][''type''])) #> ''time_type'''
  quote_hash: sha256:9d135c3948bea3f81543d76567405f60b00abe6649850b3d0b5ba3c48ec91ae5
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-268
  short_excerpt: 'from datetime import datetime from pydantic import AwareDatetime,
    BaseModel, ValidationError class Model(BaseModel): x: AwareDatetime try: Model(x=datetime.now())
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''timezone_aware'''
  quote_hash: sha256:c5deff7b0b42fdd580137ecbf052ffbef1d7c7f36e60028859e39d2bb041cd27
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-271
  short_excerpt: 'from datetime import datetime, timezone from pydantic import BaseModel,
    NaiveDatetime, ValidationError class Model(BaseModel): x: NaiveDatetime try: Model(x=datetime.now(tz=timezone.utc))
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''timezone_naive'''
  quote_hash: sha256:b2a59da2dfaa168090f62fbfbb77e3036b8cf278834b9fa21ed451640f4535a1
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-274
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: list[int] = Field(max_length=3) try: Model(x=[1, 2, 3, 4]) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''too_long'''
  quote_hash: sha256:d4ac28e3ec3e37b6f2718ff24b356c52508489f8d90b05ffc86ba56412facd1d
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-277
  short_excerpt: 'from pydantic import BaseModel, Field, ValidationError class Model(BaseModel):
    x: list[int] = Field(min_length=3) try: Model(x=[1, 2]) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''too_short'''
  quote_hash: sha256:9aa4a41f577776d5a096e16414a19480520b46a0829d1d5ada7764559193c3ce
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-280
  short_excerpt: 'from pydantic import BaseModel, ValidationError class Model(BaseModel):
    x: tuple[int] try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''tuple_type'''
  quote_hash: sha256:e53a6dc09f7d1225e61008b4ee18c95544c5e1dbcf205d0040f0470c36a14bae
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-284
  short_excerpt: 'from pydantic import ValidationError, validate_call @validate_call
    def foo(a: int, /): return a try: foo(a=2) except ValidationError as exc: print(repr(exc.errors()[1][''type'']))
    #> ''unexpected_keyword_argument'''
  quote_hash: sha256:332ae4a779ce8b769766208917cb53b0a3eb0a6ff17b544f794e61487ff6aa33
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-286
  short_excerpt: 'from pydantic import TypeAdapter, ValidationError from pydantic.dataclasses
    import dataclass @dataclass(config={''extra'': ''forbid''}) class Foo: bar: int
    try: TypeAdapter(Foo).validate_python({''bar'': 1, ''foobar'': 2}) except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''unexpected_keyword_argument'''
  quote_hash: sha256:35d122d815ffade57e1e0267e45653afafdcbd6d45f0396d92dca6c209a9901f
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-289
  short_excerpt: 'from pydantic import ValidationError, validate_call @validate_call
    def foo(*, a: int): return a try: foo(2) except ValidationError as exc: print(repr(exc.errors()[1][''type'']))
    #> ''unexpected_positional_argument'''
  quote_hash: sha256:78c62533856abf9cb477033be48fe653cb7be606ec22666df4f74cdec7d9a211
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-292
  short_excerpt: 'from typing import Literal, Union from pydantic import BaseModel,
    Field, ValidationError class BlackCat(BaseModel): pet_type: Literal[''blackcat'']
    class WhiteCat(BaseModel): pet_type: Literal[''whitecat''] class Model(BaseModel):
    cat: Union[BlackCat, WhiteCat] = Field(discriminator=''pet_type'') try: Model(cat={''pet_type'':
    ''dog''}) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''union_tag_invalid'''
  quote_hash: sha256:8c2469a759e131cc01ec0791b75200d87a2e64c2499d12fd3d393254a8da54d7
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-295
  short_excerpt: 'from typing import Literal, Union from pydantic import BaseModel,
    Field, ValidationError class BlackCat(BaseModel): pet_type: Literal[''blackcat'']
    class WhiteCat(BaseModel): pet_type: Literal[''whitecat''] class Model(BaseModel):
    cat: Union[BlackCat, WhiteCat] = Field(discriminator=''pet_type'') try: Model(cat={''name'':
    ''blackcat''}) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''union_tag_not_found'''
  quote_hash: sha256:e208d9bc35e7790e84ca065117eda0dd0f08ee9be855c201c82868c64a4a555b
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-298
  short_excerpt: 'from pydantic import AnyUrl, BaseModel, ValidationError class Model(BaseModel):
    x: AnyUrl try: Model(x=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''url_parsing'''
  quote_hash: sha256:74de530376c02b8e5f7b8fd56712a91235aefee8ce6ffaab9c123c2433f238d9
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-301
  short_excerpt: 'from pydantic import BaseModel, HttpUrl, ValidationError class Model(BaseModel):
    x: HttpUrl try: Model(x=''ftp://example.com'') except ValidationError as exc:
    print(repr(exc.errors()[0][''type''])) #> ''url_scheme'''
  quote_hash: sha256:314e99dcb0cc1003e2f9a7239c6d900370e0c2ca8a0007fc7da05bf98a681cf3
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-304
  short_excerpt: 'from pydantic import BaseModel, Field, HttpUrl, ValidationError
    class Model(BaseModel): x: HttpUrl = Field(strict=True) try: Model(x=''http:////example.com'')
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''url_syntax_violation'''
  quote_hash: sha256:1ebc886966d1b66a54d2295b6ef0e3d61dd649e8ff5a2364db06e77f15b00ed1
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-307
  short_excerpt: 'from pydantic import BaseModel, HttpUrl, ValidationError class Model(BaseModel):
    x: HttpUrl try: Model(x=''x'' * 2084) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''url_too_long'''
  quote_hash: sha256:50f1be828f6e7a2fe059d8bb8e9bd300e6a5c435d0459c78daebfb273e5bfd65
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-310
  short_excerpt: 'from pydantic import BaseModel, HttpUrl, ValidationError class Model(BaseModel):
    x: HttpUrl try: Model(x=None) except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''url_type'''
  quote_hash: sha256:7c17217c130f5b96ed5e2614b49987c3772f500e8cc45de5f4c9690742199eb5
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-313
  short_excerpt: 'from uuid import UUID from pydantic import BaseModel, ValidationError
    class Model(BaseModel): u: UUID try: Model(u=''12345678-124-1234-1234-567812345678'')
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''uuid_parsing'''
  quote_hash: sha256:0eb87050b48defdd7d83706bdc2b897b6987f2479b928823105c036d157ca5fe
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-316
  short_excerpt: 'from uuid import UUID from pydantic import BaseModel, ValidationError
    class Model(BaseModel): u: UUID try: Model(u=1234567812412341234567812345678)
    except ValidationError as exc: print(repr(exc.errors()[0][''type''])) #> ''uuid_type'''
  quote_hash: sha256:108500dfd19b436595186b9d837bab441ce6b8791596f404b3c74062f42c9cab
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-319
  short_excerpt: 'from pydantic import UUID5, BaseModel, ValidationError class Model(BaseModel):
    u: UUID5 try: Model(u=''a6cc5730-2261-11ee-9c43-2eb5a363657c'') except ValidationError
    as exc: print(repr(exc.errors()[0][''type''])) #> ''uuid_version'''
  quote_hash: sha256:599521b5f17db6f82a496b1bb09a561fe3af3737d799205507be1b3e1074ca10
- source_id: pydantic-validation-errors
  url: https://docs.pydantic.dev/latest/errors/validation_errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/validation_errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-validation-errors-322
  short_excerpt: 'from pydantic import BaseModel, ValidationError, field_validator
    class Model(BaseModel): x: str @field_validator(''x'') @classmethod def repeat_b(cls,
    v): raise ValueError() try: Model(x=''test'') except ValidationError as exc: print(repr(exc.errors()[0][''type'']))
    #> ''value_error'''
  quote_hash: sha256:9c388586d334a55c864a5e06a68c900ce000c7e8de3fabe74b4122faeb45b31e
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# pydantic-validation-error-type

## Failure Class
pydantic/validation

## Symptoms
- Pydantic raises ValidationError with an unexpected error type during model instantiation or validation

## Fingerprints
- ValidationError
- int_parsing
- bool_type
- missing
- greater_than
- validation error

## First Checks
- Check the error type field in exc.errors()[0]['type'] against the Pydantic validation error catalog
- Check the loc tuple to find which field path failed validation
- Check whether strict mode is enabled and affects the allowed input types

## Do Not Patch Yet
- Do not catch ValidationError broadly without inspecting the individual error types
- Do not assume coercion will always succeed; check type constraints on Field definitions

## Evidence Needed
- Capture exc.errors() to see all validation errors, their types, locs, and messages
- Identify the model field annotations and Field constraints that failed

## Minimal Fix Scope
- The model field definition and type annotation
- The input data structure passed to model_validate or model instantiation

## Validation Ladder
- Instantiate the model with failing data and inspect the ValidationError
- Verify the fix eliminates all errors of the same type
- Run the model unit test covering the affected field

## Regression Guard
- Add a model test that asserts correct ValidationError.type for invalid input

## Reviewer Notes
