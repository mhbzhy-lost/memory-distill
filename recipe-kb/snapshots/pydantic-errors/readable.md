- [pydantic-errors-1] Pydantic will raise a ValidationError whenever it finds an error in the data it’s validating.

- [pydantic-errors-2] That ValidationError will contain information about all the errors and how they happened.

- [pydantic-errors-3] You can access these errors in several ways:

- [pydantic-errors-4] errors()

- [pydantic-errors-5] ErrorDetails

- [pydantic-errors-6] error_count()

- [pydantic-errors-7] json()

- [pydantic-errors-8] str(e)

- [pydantic-errors-9] The ErrorDetails object is a dictionary. It contains the following:

- [pydantic-errors-10] ctx

- [pydantic-errors-11] input

- [pydantic-errors-12] loc

- [pydantic-errors-13] msg

- [pydantic-errors-14] type

- [pydantic-errors-15] url

- [pydantic-errors-16] The first item in the loc list will be the field where the error occurred, and if the field is a sub-model , subsequent items will be present to indicate the nested location of the error.

- [pydantic-errors-17] As a demonstration:

- [pydantic-errors-18] from pydantic import BaseModel, Field, ValidationError, field_validator class Location(BaseModel): lat: float = 0.1 lng: float = 10.1 class Model(BaseModel): is_required: float gt_int: int = Field(gt=42) list_of_ints: list[int] a_float: float recursive_model: Location @field_validator('a_float', mode='after') @classmethod def validate_float(cls, value: float) -> float: if value > 2.0: raise ValueError('Invalid float value') return value data = { 'list_of_ints': ['1', 2, 'bad'], 'a_float': 3.0, 'recursive_model': {'lat': 4.2, 'lng': 'New York'}, 'gt_int': 21, } try: Model(**data) except ValidationError as e: print(e) """ 5 validation errors for Model is_required Field required [type=missing, input_value={'list_of_ints': ['1', 2,...ew York'}, 'gt_int': 21}, input_type=dict] gt_int Input should be greater than 42 [type=greater_than, input_value=21, input_type=int] list_of_ints.2 Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='bad', input_type=str] a_float Value error, Invalid float value [type=value_error, input_value=3.0, input_type=float] recursive_model.lng Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='New York', input_type=str] """ try: Model(**data) except ValidationError as e: print(e.errors()) """ [ { 'type': 'missing', 'loc': ('is_required',), 'msg': 'Field required', 'input': { 'list_of_ints': ['1', 2, 'bad'], 'a_float': 3.0, 'recursive_model': {'lat': 4.2, 'lng': 'New York'}, 'gt_int': 21, }, 'url': 'https://errors.pydantic.dev/2/v/missing', }, { 'type': 'greater_than', 'loc': ('gt_int',), 'msg': 'Input should be greater than 42', 'input': 21, 'ctx': {'gt': 42}, 'url': 'https://errors.pydantic.dev/2/v/greater_than', }, { 'type': 'int_parsing', 'loc': ('list_of_ints', 2), 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'bad', 'url': 'https://errors.pydantic.dev/2/v/int_parsing', }, { 'type': 'value_error', 'loc': ('a_float',), 'msg': 'Value error, Invalid float value', 'input': 3.0, 'ctx': {'error': ValueError('Invalid float value')}, 'url': 'https://errors.pydantic.dev/2/v/value_error', }, { 'type': 'float_parsing', 'loc': ('recursive_model', 'lng'), 'msg': 'Input should be a valid number, unable to parse string as a number', 'input': 'New York', 'url': 'https://errors.pydantic.dev/2/v/float_parsing', }, ] """

- [pydantic-errors-19] Error messages

- [pydantic-errors-20] Pydantic attempts to provide useful default error messages for validation and usage errors, which can be found here:

- [pydantic-errors-21] Validation Errors : Errors that happen during data validation.

- [pydantic-errors-22] Usage Errors : Errors that happen when using Pydantic.

- [pydantic-errors-23] Customize error messages

- [pydantic-errors-24] You can customize error messages by creating a custom error handler.

- [pydantic-errors-25] from pydantic_core import ErrorDetails from pydantic import BaseModel, HttpUrl, ValidationError CUSTOM_MESSAGES = { 'int_parsing': 'This is not an integer! 🤦', 'url_scheme': 'Hey, use the right URL scheme! I wanted {expected_schemes}.', } def convert_errors( e: ValidationError, custom_messages: dict[str, str] ) -> list[ErrorDetails]: new_errors: list[ErrorDetails] = [] for error in e.errors(): custom_message = custom_messages.get(error['type']) if custom_message: ctx = error.get('ctx') error['msg'] = ( custom_message.format(**ctx) if ctx else custom_message ) new_errors.append(error) return new_errors class Model(BaseModel): a: int b: HttpUrl try: Model(a='wrong', b='ftp://example.com') except ValidationError as e: errors = convert_errors(e, CUSTOM_MESSAGES) print(errors) """ [ { 'type': 'int_parsing', 'loc': ('a',), 'msg': 'This is not an integer! 🤦', 'input': 'wrong', 'url': 'https://errors.pydantic.dev/2/v/int_parsing', }, { 'type': 'url_scheme', 'loc': ('b',), 'msg': "Hey, use the right URL scheme! I wanted 'http' or 'https'.", 'input': 'ftp://example.com', 'ctx': {'expected_schemes': "'http' or 'https'"}, 'url': 'https://errors.pydantic.dev/2/v/url_scheme', }, ] """

- [pydantic-errors-26] A common use case would be to translate error messages. For example, in the above example, we could translate the error messages replacing the CUSTOM_MESSAGES dictionary with a dictionary of translations.

- [pydantic-errors-27] Another example is customizing the way that the 'loc' value of an error is represented.

- [pydantic-errors-28] from typing import Any, Union from pydantic import BaseModel, ValidationError def loc_to_dot_sep(loc: tuple[Union[str, int], ...]) -> str: path = '' for i, x in enumerate(loc): if isinstance(x, str): if i > 0: path += '.' path += x elif isinstance(x, int): path += f'[{x}]' else: raise TypeError('Unexpected type') return path def convert_errors(e: ValidationError) -> list[dict[str, Any]]: new_errors: list[dict[str, Any]] = e.errors() for error in new_errors: error['loc'] = loc_to_dot_sep(error['loc']) return new_errors class TestNestedModel(BaseModel): key: str value: str class TestModel(BaseModel): items: list[TestNestedModel] data = {'items': [{'key': 'foo', 'value': 'bar'}, {'key': 'baz'}]} try: TestModel.model_validate(data) except ValidationError as e: print(e.errors()) # (1) """ [ { 'type': 'missing', 'loc': ('items', 1, 'value'), 'msg': 'Field required', 'input': {'key': 'baz'}, 'url': 'https://errors.pydantic.dev/2/v/missing', } ] """ pretty_errors = convert_errors(e) print(pretty_errors) # (2) """ [ { 'type': 'missing', 'loc': 'items[1].value', 'msg': 'Field required', 'input': {'key': 'baz'}, 'url': 'https://errors.pydantic.dev/2/v/missing', } ] """

- [pydantic-errors-29] By default, e.errors() produces a list of errors with loc values that take the form of tuples.

- [pydantic-errors-30] With our custom loc_to_dot_sep function, we've modified the form of the loc representation.
