---
id: fastapi-wrong-response-class
kind: debug-recipe
status: accepted
stack:
- fastapi
failure_class: fastapi/response-format
symptoms:
- FastAPI returns unexpected Content-Type or data format because wrong Response subclass
  is used
fingerprints:
- HTMLResponse
- PlainTextResponse
- JSONResponse
- StreamingResponse
- FileResponse
- response_class
first_checks:
- Check the response_class parameter on the path operation decorator
- Check whether returning a Response subclass directly bypasses response_model serialization
- Check whether the correct Content-Type is expected by the consuming client
do_not:
- Do not return a JSONResponse directly when a response_model is declared unless you
  want to bypass Pydantic serialization
- Do not use StreamingResponse for data that fits in memory as a plain JSONResponse
evidence_needed:
- Capture the HTTP response Content-Type header
- Identify whether the response was returned directly or via response_class
minimal_fix_scope:
- The path operation decorator response_class parameter
- The return type annotation or direct Response subclass returned
validation_ladder:
- Inspect the response Content-Type header in development
- Verify the response body matches the documented schema
- Run the endpoint test for the affected route
regression_guard:
- Add an endpoint test that asserts Content-Type and response shape
evidence_refs:
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-3
  short_excerpt: You can override it by returning a Response directly as seen in Return
    a Response directly .
  quote_hash: sha256:c529bc27c80fed6791dabd789f4b18b9a352694d2cd6fb62a0a0707dba641722
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-4
  short_excerpt: But if you return a Response directly (or any subclass, like JSONResponse
    ), the data won't be automatically converted (even if you declare a response_model
    ), and the documentation won't be automatically generated (for example, including
    the specific "media type", in the HTTP header Content-Type as part of the generated
    OpenAPI).
  quote_hash: sha256:733b46f304995a3d7532f1234c92b93930ce9b864c2a79c783dc6e745194ee63
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-5
  short_excerpt: But you can also declare the Response that you want to be used (e.g.
    any Response subclass), in the path operation decorator using the response_class
    parameter.
  quote_hash: sha256:c381edbc0339e8141b31f565886ae95d8cc65074b5ca0a925e6ba0227293a264
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-12
  short_excerpt: If you don't declare a response model, FastAPI will use the jsonable_encoder
    explained in JSON Compatible Encoder and put it in a JSONResponse .
  quote_hash: sha256:db262f6224ce9da53fdb79294baf88c1d382b4e52d6b75e72fa04dd4244f8f46
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-13
  short_excerpt: If you declare a response_class with a JSON media type ( application/json
    ), like is the case with the JSONResponse , the data you return will be automatically
    converted (and filtered) with any Pydantic response_model that you declared in
    the path operation decorator . But the data won't be serialized to JSON bytes
    with Pydantic, instead it will be converted with the jsonable_encoder and then
    passed to the JSONResponse class, which will serialize it to bytes using the standard
    JSON library in Python.
  quote_hash: sha256:fd8c275dcba079df892b9ca594c07fc541abc27c4816020523a1f183e06ee06a
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-15
  short_excerpt: In short, if you want the maximum performance, use a Response Model
    and don't declare a response_class in the path operation decorator .
  quote_hash: sha256:4a2aad523c13e2b316727791a67c67f8b0b37d46edba70de1689719d3055e576
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-19
  short_excerpt: To return a response with HTML directly from FastAPI , use HTMLResponse
    .
  quote_hash: sha256:086d88c5a5fa9629d002ef98b9214bd88d0af65e22b95bb3aebab7b82a3ea662
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-20
  short_excerpt: Import HTMLResponse .
  quote_hash: sha256:a2d356e01f9711cc956bb78881132bbc190b88963c1ebdda862696ef2bffd325
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-21
  short_excerpt: Pass HTMLResponse as the parameter response_class of your path operation
    decorator .
  quote_hash: sha256:b9055004cdfab07c23b787203aeea46e26fab112d3aeb02af5a906ded1b8c2cd
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-22
  short_excerpt: 'from fastapi import FastAPI from fastapi.responses import HTMLResponse
    app = FastAPI () @app . get ( "/items/" , response_class = HTMLResponse ) async
    def read_items (): return """ <html> <head> <title>Some HTML in here</title> </head>
    <body> <h1>Look ma! HTML!</h1> </body> </html> """'
  quote_hash: sha256:1a0e7cc89f9e8438f9e12953b7477ed2dd2f6703cfd9edd735766c3ff6312584
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-23
  short_excerpt: The parameter response_class will also be used to define the "media
    type" of the response.
  quote_hash: sha256:2f163108a8afc517dab71ef2012f7ae727c54310cb9cc911a7e8f4b21bb0d124
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-27
  short_excerpt: As seen in Return a Response directly , you can also override the
    response directly in your path operation , by returning it.
  quote_hash: sha256:386b775c1a2be5f47b322a00ba4a4c8a4c72b9c3f69c485b5b2d3725e6b3da83
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-28
  short_excerpt: 'The same example from above, returning an HTMLResponse , could look
    like:'
  quote_hash: sha256:efaa7558b4cab4cfd0274c3f3b172c28feaf0e2ac163999aa36f1900bed6f5e4
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-29
  short_excerpt: 'from fastapi import FastAPI from fastapi.responses import HTMLResponse
    app = FastAPI () @app . get ( "/items/" ) async def read_items (): html_content
    = """ <html> <head> <title>Some HTML in here</title> </head> <body> <h1>Look ma!
    HTML!</h1> </body> </html> """ return HTMLResponse ( content = html_content ,
    status_code = 200 )'
  quote_hash: sha256:7a10b3a79f1004d9c39222ea385ed2fa514446c282d418e5e740cd8a31f85013
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-34
  short_excerpt: If you want to override the response from inside of the function
    but at the same time document the "media type" in OpenAPI, you can use the response_class
    parameter AND return a Response object.
  quote_hash: sha256:283b5e8f87d352fea05d9eb45f8646ac5b86084db5a9a9cac40b992f26963d19
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-35
  short_excerpt: The response_class will then be used only to document the OpenAPI
    path operation , but your Response will be used as is.
  quote_hash: sha256:fa91e7fcee47af9203d7ba3b6f511d849e86d84d39ea887a26b6dcddc26297f3
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-36
  short_excerpt: HTMLResponse
  quote_hash: sha256:b3d207fb388f3cf7251d624af9897398f4f52bc3e32d3a1dbb1385a60424be10
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-38
  short_excerpt: 'from fastapi import FastAPI from fastapi.responses import HTMLResponse
    app = FastAPI () def generate_html_response (): html_content = """ <html> <head>
    <title>Some HTML in here</title> </head> <body> <h1>Look ma! HTML!</h1> </body>
    </html> """ return HTMLResponse ( content = html_content , status_code = 200 )
    @app . get ( "/items/" , response_class = HTMLResponse ) async def read_items
    (): return generate_html_response ()'
  quote_hash: sha256:455a1f89cde8d2a88bbaaf2f4fd8e103c0c452a011113ed36e3aeaafada986e4
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-41
  short_excerpt: 'But as you passed the HTMLResponse in the response_class too, FastAPI
    will know how to document it in OpenAPI and the interactive docs as HTML with
    text/html :'
  quote_hash: sha256:bcbe5fc72bfee98620bf3ee1c4ca9982c9e6de3c1f3d3642ed64562fe872a5b2
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-46
  short_excerpt: You could also use from starlette.responses import HTMLResponse .
  quote_hash: sha256:fd4ec6ee63fa344d713bdc66f1ad2ea1e3e16cdad91569caf78c6341ca34dff6
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-58
  short_excerpt: HTMLResponse ¶
  quote_hash: sha256:064f3f59f8b491127b4c44fdc560e64b010b7f1cbce4aa95ed6974c6ed413b8d
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-60
  short_excerpt: PlainTextResponse ¶
  quote_hash: sha256:b75eb2cfecbec989fedf110141f35023b0205dd6595ee03ca02c625913cb1999
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-62
  short_excerpt: 'from fastapi import FastAPI from fastapi.responses import PlainTextResponse
    app = FastAPI () @app . get ( "/" , response_class = PlainTextResponse ) async
    def main (): return "Hello World"'
  quote_hash: sha256:5f1bd2f0100f00d8ed6fd9bc1e18b852a9ed64735f5bde46cee54b8b5f3ecd5e
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-63
  short_excerpt: JSONResponse ¶
  quote_hash: sha256:c91ce98fdf08cb33274ecdd86ae4d8a296044a51bd14f5e15bf758f7fe6ee192
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-66
  short_excerpt: But if you declare a response model or return type, that will be
    used directly to serialize the data to JSON, and a response with the right media
    type for JSON will be returned directly, without using the JSONResponse class.
  quote_hash: sha256:13abb294c9d695bfed2a8af6f3bf49f60e2ff1d5e6a423b8b1a8e7caa88db99e
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-70
  short_excerpt: 'You can return a RedirectResponse directly:'
  quote_hash: sha256:298a131cd0687a5be33114bbd10c28088a52d9bd826af7209d6972c3662ac85e
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-72
  short_excerpt: 'Or you can use it in the response_class parameter:'
  quote_hash: sha256:f73d230a9e179dd96502ef442ae6265432404bd353c41ff3493a1ea33bfec5f4
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-73
  short_excerpt: 'from fastapi import FastAPI from fastapi.responses import RedirectResponse
    app = FastAPI () @app . get ( "/fastapi" , response_class = RedirectResponse )
    async def redirect_fastapi (): return "https://fastapi.tiangolo.com"'
  quote_hash: sha256:88a9ab9e2899642ccd90290cd2dcbe513337874912cf0ff057ffd3ed4b3cd102
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-76
  short_excerpt: 'You can also use the status_code parameter combined with the response_class
    parameter:'
  quote_hash: sha256:08af27c2a15e80c497481fe505251b4f7f8e61991499d3e50474167dae728f9a
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-77
  short_excerpt: 'from fastapi import FastAPI from fastapi.responses import RedirectResponse
    app = FastAPI () @app . get ( "/pydantic" , response_class = RedirectResponse
    , status_code = 302 ) async def redirect_pydantic (): return "https://docs.pydantic.dev/"'
  quote_hash: sha256:3abc874f4dbb4a7b8e5e441d9c3545e87be6ec89789bedb8884cc5c1265d1423
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-78
  short_excerpt: StreamingResponse ¶
  quote_hash: sha256:79c192695f2ec979bf438697d97a1c204717e57233e09673b5729aac99ae9e76
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-80
  short_excerpt: 'import anyio from fastapi import FastAPI from fastapi.responses
    import StreamingResponse app = FastAPI () async def fake_video_streamer (): for
    i in range ( 10 ): yield b "some fake video bytes" await anyio . sleep ( 0 ) @app
    . get ( "/" ) async def main (): return StreamingResponse ( fake_video_streamer
    ())'
  quote_hash: sha256:a291a3582ba2813e1256f036b4bca0556a3d52bd3004dcdd669f6dc2063dfc4a
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-85
  short_excerpt: Instead of returning a StreamingResponse directly, you should probably
    follow the style in Stream Data , it's much more convenient and handles cancellation
    behind the scenes for you.
  quote_hash: sha256:0e37ef25136ff9474d2c08ba10d6f0c4a34902f336a3212d4d8f1aa75d709302
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-87
  short_excerpt: FileResponse ¶
  quote_hash: sha256:e5c0ab604d8a689a440daf681b6874093b64bcc147f631a16e6e82c2427b05d4
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-95
  short_excerpt: 'from fastapi import FastAPI from fastapi.responses import FileResponse
    some_file_path = "large-video-file.mp4" app = FastAPI () @app . get ( "/" ) async
    def main (): return FileResponse ( some_file_path )'
  quote_hash: sha256:b009d803b32d6a89af120c05173ccedc5a07279077b4a998f33c95a6f40cea1f
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-96
  short_excerpt: 'You can also use the response_class parameter:'
  quote_hash: sha256:f8a1d5b441a52acb6fc745f1fa8844edf8ce0f4027e24fd1d2f338361a0eec21
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-97
  short_excerpt: 'from fastapi import FastAPI from fastapi.responses import FileResponse
    some_file_path = "large-video-file.mp4" app = FastAPI () @app . get ( "/" , response_class
    = FileResponse ) async def main (): return some_file_path'
  quote_hash: sha256:3f22142a61d479b7910374e5dbd9e873b495279c507aafdace4eedbe1d973e20
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-104
  short_excerpt: 'You could create a CustomORJSONResponse . The main thing you have
    to do is create a Response.render(content) method that returns the content as
    bytes :'
  quote_hash: sha256:5ff6c61328ddcec3df0c8599cac575f6eb5fec2b78df76dbabe883ab2ae7ffeb
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-105
  short_excerpt: 'from typing import Any import orjson from fastapi import FastAPI
    , Response app = FastAPI () class CustomORJSONResponse ( Response ): media_type
    = "application/json" def render ( self , content : Any ) -> bytes : assert orjson
    is not None , "orjson must be installed" return orjson . dumps ( content , option
    = orjson . OPT_INDENT_2 ) @app . get ( "/" , response_class = CustomORJSONResponse
    ) async def main (): return { "message" : "Hello World" }'
  quote_hash: sha256:32c1e92c4036f05763e37c794a5e78b7b8f07aca9a630c6886063550ce3b4ea0
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-116
  short_excerpt: The parameter that defines this is default_response_class .
  quote_hash: sha256:78bb37bf178d564217f5f6409a713e82ca1907f18b06ae7c018be957182fd2cd
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-117
  short_excerpt: In the example below, FastAPI will use HTMLResponse by default, in
    all path operations , instead of JSON.
  quote_hash: sha256:0757ac83784fb6193b84596d15e17b502a38ee0293ce868ad982ae50f1084f27
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-118
  short_excerpt: 'from fastapi import FastAPI from fastapi.responses import HTMLResponse
    app = FastAPI ( default_response_class = HTMLResponse ) @app . get ( "/items/"
    ) async def read_items (): return "<h1>Items</h1><p>This is a list of items.</p>"'
  quote_hash: sha256:04f2e070f9d16fdd00fd900e0286e387c743f40821267fac3126d4423c968bef
- source_id: fastapi-custom-response
  url: https://fastapi.tiangolo.com/advanced/custom-response/
  final_url: https://fastapi.tiangolo.com/advanced/custom-response/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-custom-response-119
  short_excerpt: You can still override response_class in path operations as before.
  quote_hash: sha256:eef93a516de13d5be2aa6ad8248fe923e797d82725032fe9be22b3f72e989558
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# fastapi-wrong-response-class

## Failure Class
fastapi/response-format

## Symptoms
- FastAPI returns unexpected Content-Type or data format because wrong Response subclass is used

## Fingerprints
- HTMLResponse
- PlainTextResponse
- JSONResponse
- StreamingResponse
- FileResponse
- response_class

## First Checks
- Check the response_class parameter on the path operation decorator
- Check whether returning a Response subclass directly bypasses response_model serialization
- Check whether the correct Content-Type is expected by the consuming client

## Do Not Patch Yet
- Do not return a JSONResponse directly when a response_model is declared unless you want to bypass Pydantic serialization
- Do not use StreamingResponse for data that fits in memory as a plain JSONResponse

## Evidence Needed
- Capture the HTTP response Content-Type header
- Identify whether the response was returned directly or via response_class

## Minimal Fix Scope
- The path operation decorator response_class parameter
- The return type annotation or direct Response subclass returned

## Validation Ladder
- Inspect the response Content-Type header in development
- Verify the response body matches the documented schema
- Run the endpoint test for the affected route

## Regression Guard
- Add an endpoint test that asserts Content-Type and response shape

## Reviewer Notes
