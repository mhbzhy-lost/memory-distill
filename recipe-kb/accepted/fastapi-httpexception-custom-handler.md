---
id: fastapi-httpexception-custom-handler
kind: debug-recipe
status: accepted
stack:
- fastapi
failure_class: fastapi/error-handling
symptoms:
- FastAPI path operation raises HTTPException but client receives unexpected response
  format
fingerprints:
- HTTPException
- raise HTTPException
- custom exception handler
- exception_handler
- detail
first_checks:
- Check the HTTPException status_code and detail parameter at the raise site
- Check whether a custom exception_handler overrides the default HTTPException or
  RequestValidationError handler
- Check whether headers are correctly passed via the headers parameter
do_not:
- Do not return an HTTPException as a value; it must be raised with raise
- Do not override RequestValidationError handler without re-raising or returning all
  validation errors
evidence_needed:
- Capture the HTTP response status and JSON detail returned to the client
- Identify whether a custom exception_handler intercepts or swallows the exception
minimal_fix_scope:
- The path operation function that raises the HTTPException
- The app-level exception_handler that transforms the exception to a response
validation_ladder:
- Reproduce the error endpoint with the failing request in development
- Inspect the HTTP response status and JSON body
- Run the endpoint smoke test or integration test
regression_guard:
- Add an endpoint test that asserts the correct HTTP status and detail body
evidence_refs:
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-13
  short_excerpt: Use HTTPException ¶
  quote_hash: sha256:26328f587775d0eb1cda2a2d8ac637cca652dfc987d64d1fc95f251ae874aa2a
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-14
  short_excerpt: To return HTTP responses with errors to the client you use HTTPException
    .
  quote_hash: sha256:de60eea5eac1f264c0b58f44450b9c1eed9c1c189c10b5445cfd31b706c92f34
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-15
  short_excerpt: Import HTTPException ¶
  quote_hash: sha256:5acada7427e685b49ceba489e5c39235f626f583b32b7236f31eeb3683237d12
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-16
  short_excerpt: 'from fastapi import FastAPI , HTTPException app = FastAPI () items
    = { "foo" : "The Foo Wrestlers" } @app . get ( "/items/ {item_id} " ) async def
    read_item ( item_id : str ): if item_id not in items : raise HTTPException ( status_code
    = 404 , detail = "Item not found" ) return { "item" : items [ item_id ]}'
  quote_hash: sha256:c3926abe4d5115730273b85e1a537c3b70840ee280c10ee0243fcfc3453d1e7c
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-17
  short_excerpt: Raise an HTTPException in your code ¶
  quote_hash: sha256:b351ff10e73f9d34f2ff53b19269db5d5ef4cbd16dde4ba5c162ad4c3fcadd4a
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-18
  short_excerpt: HTTPException is a normal Python exception with additional data relevant
    for APIs.
  quote_hash: sha256:be65ae9cdad4bcc42febc1c6de8db29fad699169325e6fc2655495f478e94b93
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-20
  short_excerpt: This also means that if you are inside a utility function that you
    are calling inside of your path operation function , and you raise the HTTPException
    from inside of that utility function, it won't run the rest of the code in the
    path operation function , it will terminate that request right away and send the
    HTTP error from the HTTPException to the client.
  quote_hash: sha256:f23fb11f6fce3aaf32c0e82baddc05b605061879c2543c84b8b13df7bdd3c71b
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-29
  short_excerpt: When raising an HTTPException , you can pass any value that can be
    converted to JSON as the parameter detail , not only str .
  quote_hash: sha256:00a08224ebe9bdba18dfebea854c412bb152a0830eb156d9b3dc5678d76e7cd9
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-36
  short_excerpt: 'from fastapi import FastAPI , HTTPException app = FastAPI () items
    = { "foo" : "The Foo Wrestlers" } @app . get ( "/items-header/ {item_id} " ) async
    def read_item_header ( item_id : str ): if item_id not in items : raise HTTPException
    ( status_code = 404 , detail = "Item not found" , headers = { "X-Error" : "There
    goes my error" }, ) return { "item" : items [ item_id ]}'
  quote_hash: sha256:ac6a5f2671cfb0eb0102a7d84b6fae194adcf09100f2e01f80dea0ccabff50d7
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-37
  short_excerpt: Install custom exception handlers ¶
  quote_hash: sha256:08a5632d6559abb346fee393471e5c998e518cfee44b53d59c1d253f873fd025
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-38
  short_excerpt: You can add custom exception handlers with the same exception utilities
    from Starlette .
  quote_hash: sha256:e553360b29bc365ee23003949deb24b866d2719b0cc2110f15d2f218ec7e1925
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-39
  short_excerpt: Let's say you have a custom exception UnicornException that you (or
    a library you use) might raise .
  quote_hash: sha256:263bc90a41a6aea6def729fde21a1779c587bb25d4f85e5fa9a842d025c2319a
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-41
  short_excerpt: 'You could add a custom exception handler with @app.exception_handler()
    :'
  quote_hash: sha256:e7116605fbe01969551d18ab8a4a3b39960380ebfdb0b3c6faa2b1dd9c627ceb
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-50
  short_excerpt: Override the default exception handlers ¶
  quote_hash: sha256:3827eaeff0ca901e0118532ada9a1181d25fd993b34ad95596309239bcd53ffe
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-51
  short_excerpt: FastAPI has some default exception handlers.
  quote_hash: sha256:f20819a679fe40a5f1f142e16d68f82701e2fa326f4c580262a79c5ccc866849
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-52
  short_excerpt: These handlers are in charge of returning the default JSON responses
    when you raise an HTTPException and when the request has invalid data.
  quote_hash: sha256:0d82da2d96e715f39c7b8abd53afb83100f92347afff509368600a9f8880e513
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-53
  short_excerpt: You can override these exception handlers with your own.
  quote_hash: sha256:b433cc22f816bc26fffc8dfaad15575756092554379727ff7ce1e0cf713d05db
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-54
  short_excerpt: Override request validation exceptions ¶
  quote_hash: sha256:1ad0852c633e7af69dd0d0f987f58d7109050197628cd9bd51beca6cf8f1092e
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-55
  short_excerpt: When a request contains invalid data, FastAPI internally raises a
    RequestValidationError .
  quote_hash: sha256:62d4936c1d336c494d1d77e74f0cdaaab536758e214540189514f0b4ced27dd7
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-56
  short_excerpt: And it also includes a default exception handler for it.
  quote_hash: sha256:5c3ea6c5a4eba2166f1bc8df1902b1425931bbc760a7230d0bc24c24f034055d
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-57
  short_excerpt: To override it, import the RequestValidationError and use it with
    @app.exception_handler(RequestValidationError) to decorate the exception handler.
  quote_hash: sha256:5903f649f389933ddde3fa55de6ad9ef0559b6f747f7ed628e6028a0205f5267
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-58
  short_excerpt: The exception handler will receive a Request and the exception.
  quote_hash: sha256:d9f03580b51c018added6dd001fdf02a896add2114069eab3bb9ca3386b3576c
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-59
  short_excerpt: 'from fastapi import FastAPI , HTTPException from fastapi.exceptions
    import RequestValidationError from fastapi.responses import PlainTextResponse
    from starlette.exceptions import HTTPException as StarletteHTTPException app =
    FastAPI () @app . exception_handler ( StarletteHTTPException ) async def http_exception_handler
    ( request , exc ): return PlainTextResponse ( str ( exc . detail ), status_code
    = exc . status_code ) @app . exception_handler ( RequestValidationError ) async
    def validation_exception_handler ( request , exc : RequestValidationError ): message
    = "Validation errors:" for error i'
  quote_hash: sha256:7dce916178a407a02bbd9121be21029da0284c526335679d7b00a406a5fcdf20
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-64
  short_excerpt: Override the HTTPException error handler ¶
  quote_hash: sha256:495e8bc1c6fae1a641e08a82c34c23eddded2dbee63e9ad571d78669f280b044
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-65
  short_excerpt: The same way, you can override the HTTPException handler.
  quote_hash: sha256:8da8376537d7551e9071c63c2635c7c4a71ec1a75bb61bc6054a50c606a53195
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-70
  short_excerpt: Have in mind that the RequestValidationError contains the information
    of the file name and line where the validation error happens so that you can show
    it in your logs with the relevant information if you want to.
  quote_hash: sha256:e0dbb84c5c841f3af455c039cf8a1c0b747193d3fc0ee5c64b120a527e6ac648
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-72
  short_excerpt: Use the RequestValidationError body ¶
  quote_hash: sha256:4c509cd3e88fa7fd8214aeb11a943c0e6e8f5f45fb7d910dd93dd47a628ec98b
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-73
  short_excerpt: The RequestValidationError contains the body it received with invalid
    data.
  quote_hash: sha256:00c6e6ff1311a682a7e547ec43ff7eb0806dfd2372635b169136e7fd9668cda1
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-75
  short_excerpt: 'from fastapi import FastAPI , Request from fastapi.encoders import
    jsonable_encoder from fastapi.exceptions import RequestValidationError from fastapi.responses
    import JSONResponse from pydantic import BaseModel app = FastAPI () @app . exception_handler
    ( RequestValidationError ) async def validation_exception_handler ( request :
    Request , exc : RequestValidationError ): return JSONResponse ( status_code =
    422 , content = jsonable_encoder ({ "detail" : exc . errors (), "body" : exc .
    body }), ) class Item ( BaseModel ): title : str size : int @app . post ( "/items/"
    ) async def create_item ( i'
  quote_hash: sha256:7365ea7d8aeda0d7ac2336c57cf28268e2947afe7f7607031fdd9b33f489a2e4
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-80
  short_excerpt: HTTPException
  quote_hash: sha256:35404c94a11d0de5e2bd46d85602a95bc54b60805ef4221e5a73414b56509113
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-81
  short_excerpt: FastAPI has its own HTTPException .
  quote_hash: sha256:3846cf6843779f8ee928a33fa5eda68e0daa2cd9f40721243d6910dc882873c8
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-82
  short_excerpt: And FastAPI 's HTTPException error class inherits from Starlette's
    HTTPException error class.
  quote_hash: sha256:59e8f3d91ccd73772726233cd582a83083a63a50afd022e2568e5096777695ef
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-83
  short_excerpt: The only difference is that FastAPI 's HTTPException accepts any
    JSON-able data for the detail field, while Starlette's HTTPException only accepts
    strings for it.
  quote_hash: sha256:1f43c5fd6466307b4536430adf7783698469637f57c00c23bc381dabf0c27163
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-84
  short_excerpt: So, you can keep raising FastAPI 's HTTPException as normally in
    your code.
  quote_hash: sha256:a9cd6fd9bc243b43cafe1a25638aa6d9328d37768fddd1b4a346cdb336fb4853
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-85
  short_excerpt: But when you register an exception handler, you should register it
    for Starlette's HTTPException .
  quote_hash: sha256:87f444314667e3b10ab51892bf26e221315b479781a9d2db990fd1576cdef1f7
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-86
  short_excerpt: This way, if any part of Starlette's internal code, or a Starlette
    extension or plug-in, raises a Starlette HTTPException , your handler will be
    able to catch and handle it.
  quote_hash: sha256:a1cd7e6b0b7cdd517b59630e9f469d801ac0cb9f7eccaab23cd2265b18324ac3
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-87
  short_excerpt: 'In this example, to be able to have both HTTPException s in the
    same code, Starlette''s exceptions is renamed to StarletteHTTPException :'
  quote_hash: sha256:27ef2e884e16371b2f7b66b241598190adae966a83357266f7ff0f47b8416c2f
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-88
  short_excerpt: from starlette.exceptions import HTTPException as StarletteHTTPException
  quote_hash: sha256:9e737f610a63250d22ddc74546009d86414f960aabdfcf577d61fcdb3dfab920
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-89
  short_excerpt: Reuse FastAPI 's exception handlers ¶
  quote_hash: sha256:5103cee3faab8ea6fcfe307f99a3fe322f466b5e8b58881328cbfa84db203e5e
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-90
  short_excerpt: 'If you want to use the exception along with the same default exception
    handlers from FastAPI , you can import and reuse the default exception handlers
    from fastapi.exception_handlers :'
  quote_hash: sha256:2a6dcb942496dd5aff9025daba9391b84dfa5009ad46d2f24cd9bd90486d5262
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-91
  short_excerpt: 'from fastapi import FastAPI , HTTPException from fastapi.exception_handlers
    import ( http_exception_handler , request_validation_exception_handler , ) from
    fastapi.exceptions import RequestValidationError from starlette.exceptions import
    HTTPException as StarletteHTTPException app = FastAPI () @app . exception_handler
    ( StarletteHTTPException ) async def custom_http_exception_handler ( request ,
    exc ): print ( f "OMG! An HTTP error!: { repr ( exc ) } " ) return await http_exception_handler
    ( request , exc ) @app . exception_handler ( RequestValidationError ) async def
    validation_exception_hand'
  quote_hash: sha256:17d3d56269c334de4966021af6c73bbcc9252227bfad553557b25b76eef7596e
- source_id: fastapi-handling-errors
  url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  final_url: https://fastapi.tiangolo.com/tutorial/handling-errors/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-handling-errors-92
  short_excerpt: In this example you are just printing the error with a very expressive
    message, but you get the idea. You can use the exception and then just reuse the
    default exception handlers.
  quote_hash: sha256:c0405d012d2510f39a6edb22fd511201e97d8a7be65fccd50e8fb4da463f5218
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# fastapi-httpexception-custom-handler

## Failure Class
fastapi/error-handling

## Symptoms
- FastAPI path operation raises HTTPException but client receives unexpected response format

## Fingerprints
- HTTPException
- raise HTTPException
- custom exception handler
- exception_handler
- detail

## First Checks
- Check the HTTPException status_code and detail parameter at the raise site
- Check whether a custom exception_handler overrides the default HTTPException or RequestValidationError handler
- Check whether headers are correctly passed via the headers parameter

## Do Not Patch Yet
- Do not return an HTTPException as a value; it must be raised with raise
- Do not override RequestValidationError handler without re-raising or returning all validation errors

## Evidence Needed
- Capture the HTTP response status and JSON detail returned to the client
- Identify whether a custom exception_handler intercepts or swallows the exception

## Minimal Fix Scope
- The path operation function that raises the HTTPException
- The app-level exception_handler that transforms the exception to a response

## Validation Ladder
- Reproduce the error endpoint with the failing request in development
- Inspect the HTTP response status and JSON body
- Run the endpoint smoke test or integration test

## Regression Guard
- Add an endpoint test that asserts the correct HTTP status and detail body

## Reviewer Notes
