---
id: pydantic-custom-error-messages
kind: debug-recipe
status: accepted
stack:
- pydantic
failure_class: pydantic/error-messages
symptoms:
- Pydantic ValidationError default messages are not suitable for the API response
  or client display
fingerprints:
- customize error messages
- ErrorDetails
- error_count
- e.errors()
- ctx
- CUSTOM_MESSAGES
first_checks:
- Check whether the default error messages are acceptable before building a custom
  handler
- Check the error['type'] field for a match against a custom messages dictionary
- Check whether ctx fields are correctly substituted in custom messages
do_not:
- Do not mutate the original ValidationError object when building custom messages
- Do not forget to include the error['loc'] when transforming errors for API responses
evidence_needed:
- Capture the default e.errors() output before transforming
- Capture the custom messages dictionary and the transformed output
minimal_fix_scope:
- The custom error message mapping dictionary
- The error transformation function that maps ValidationError.errors() to the API
  response
validation_ladder:
- Trigger a validation failure and compare default vs custom error output
- Verify all error types present in the input are covered by the custom mapping
- Run the endpoint or model test that exercises the error path
regression_guard:
- Add a test that asserts custom error messages appear for the covered error types
evidence_refs:
- source_id: pydantic-errors
  url: https://docs.pydantic.dev/latest/errors/errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-errors-5
  short_excerpt: ErrorDetails
  quote_hash: sha256:0820b42a6761bc8304d504db1c4d506b130f5d4ae6b6684449ce7a1e2e35a725
- source_id: pydantic-errors
  url: https://docs.pydantic.dev/latest/errors/errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-errors-9
  short_excerpt: 'The ErrorDetails object is a dictionary. It contains the following:'
  quote_hash: sha256:43389e8b11243adf4574be2e3c55965c6edc3a655c70be86369429ae337cf373
- source_id: pydantic-errors
  url: https://docs.pydantic.dev/latest/errors/errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-errors-23
  short_excerpt: Customize error messages
  quote_hash: sha256:9b99381ae40948924a00bccb0fb68a09007883f60563d423517955719b47a5c8
- source_id: pydantic-errors
  url: https://docs.pydantic.dev/latest/errors/errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-errors-24
  short_excerpt: You can customize error messages by creating a custom error handler.
  quote_hash: sha256:3d830809c656592bcc2628238c55fb98bd6df1d1b56f707a393626cfe26a72cb
- source_id: pydantic-errors
  url: https://docs.pydantic.dev/latest/errors/errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-errors-25
  short_excerpt: 'from pydantic_core import ErrorDetails from pydantic import BaseModel,
    HttpUrl, ValidationError CUSTOM_MESSAGES = { ''int_parsing'': ''This is not an
    integer! 🤦'', ''url_scheme'': ''Hey, use the right URL scheme! I wanted {expected_schemes}.'',
    } def convert_errors( e: ValidationError, custom_messages: dict[str, str] ) ->
    list[ErrorDetails]: new_errors: list[ErrorDetails] = [] for error in e.errors():
    custom_message = custom_messages.get(error[''type'']) if custom_message: ctx =
    error.get(''ctx'') error[''msg''] = ( custom_message.format(**ctx) if ctx else
    custom_message ) new_errors.append(error) return ne'
  quote_hash: sha256:f8ac8ea3556111b868931a368bf65f6f46693b0ea4e9991cafebb0bba5c76af0
- source_id: pydantic-errors
  url: https://docs.pydantic.dev/latest/errors/errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-errors-26
  short_excerpt: A common use case would be to translate error messages. For example,
    in the above example, we could translate the error messages replacing the CUSTOM_MESSAGES
    dictionary with a dictionary of translations.
  quote_hash: sha256:6d322bad217a3cca79fccc8bf57de2b943c5fc5b241048d1b3fcc1c4a30b7614
- source_id: pydantic-errors
  url: https://docs.pydantic.dev/latest/errors/errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-errors-28
  short_excerpt: 'from typing import Any, Union from pydantic import BaseModel, ValidationError
    def loc_to_dot_sep(loc: tuple[Union[str, int], ...]) -> str: path = '''' for i,
    x in enumerate(loc): if isinstance(x, str): if i > 0: path += ''.'' path += x
    elif isinstance(x, int): path += f''[{x}]'' else: raise TypeError(''Unexpected
    type'') return path def convert_errors(e: ValidationError) -> list[dict[str, Any]]:
    new_errors: list[dict[str, Any]] = e.errors() for error in new_errors: error[''loc'']
    = loc_to_dot_sep(error[''loc'']) return new_errors class TestNestedModel(BaseModel):
    key: str value: str class TestModel(BaseMo'
  quote_hash: sha256:dbb9071f590a8291b6266578daad97102f9d68a8af07667818b1bf55729edc79
- source_id: pydantic-errors
  url: https://docs.pydantic.dev/latest/errors/errors/
  final_url: https://pydantic.dev/docs/validation/latest/errors/errors/
  source_type: official_error_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: pydantic-errors-30
  short_excerpt: With our custom loc_to_dot_sep function, we've modified the form
    of the loc representation.
  quote_hash: sha256:d34e73fc342b7aec8f09ef033191d74739e7c4a7a7611b54baad16ac625fa6e3
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# pydantic-custom-error-messages

## Failure Class
pydantic/error-messages

## Symptoms
- Pydantic ValidationError default messages are not suitable for the API response or client display

## Fingerprints
- customize error messages
- ErrorDetails
- error_count
- e.errors()
- ctx
- CUSTOM_MESSAGES

## First Checks
- Check whether the default error messages are acceptable before building a custom handler
- Check the error['type'] field for a match against a custom messages dictionary
- Check whether ctx fields are correctly substituted in custom messages

## Do Not Patch Yet
- Do not mutate the original ValidationError object when building custom messages
- Do not forget to include the error['loc'] when transforming errors for API responses

## Evidence Needed
- Capture the default e.errors() output before transforming
- Capture the custom messages dictionary and the transformed output

## Minimal Fix Scope
- The custom error message mapping dictionary
- The error transformation function that maps ValidationError.errors() to the API response

## Validation Ladder
- Trigger a validation failure and compare default vs custom error output
- Verify all error types present in the input are covered by the custom mapping
- Run the endpoint or model test that exercises the error path

## Regression Guard
- Add a test that asserts custom error messages appear for the covered error types

## Reviewer Notes
