- [fastapi-custom-response-1] Custom Response - HTML, Stream, File, others ¶

- [fastapi-custom-response-2] By default, FastAPI will return JSON responses.

- [fastapi-custom-response-3] You can override it by returning a Response directly as seen in Return a Response directly .

- [fastapi-custom-response-4] But if you return a Response directly (or any subclass, like JSONResponse ), the data won't be automatically converted (even if you declare a response_model ), and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header Content-Type as part of the generated OpenAPI).

- [fastapi-custom-response-5] But you can also declare the Response that you want to be used (e.g. any Response subclass), in the path operation decorator using the response_class parameter.

- [fastapi-custom-response-6] The contents that you return from your path operation function will be put inside of that Response .

- [fastapi-custom-response-7] Note

- [fastapi-custom-response-8] If you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.

- [fastapi-custom-response-9] JSON Responses ¶

- [fastapi-custom-response-10] By default FastAPI returns JSON responses.

- [fastapi-custom-response-11] If you declare a Response Model FastAPI will use it to serialize the data to JSON, using Pydantic.

- [fastapi-custom-response-12] If you don't declare a response model, FastAPI will use the jsonable_encoder explained in JSON Compatible Encoder and put it in a JSONResponse .

- [fastapi-custom-response-13] If you declare a response_class with a JSON media type ( application/json ), like is the case with the JSONResponse , the data you return will be automatically converted (and filtered) with any Pydantic response_model that you declared in the path operation decorator . But the data won't be serialized to JSON bytes with Pydantic, instead it will be converted with the jsonable_encoder and then passed to the JSONResponse class, which will serialize it to bytes using the standard JSON library in Python.

- [fastapi-custom-response-14] JSON Performance ¶

- [fastapi-custom-response-15] In short, if you want the maximum performance, use a Response Model and don't declare a response_class in the path operation decorator .

- [fastapi-custom-response-16] # Code above omitted 👆 @app . post ( "/items/" ) async def create_item ( item : Item ) -> Item : return item # Code below omitted 👇

- [fastapi-custom-response-17] from fastapi import FastAPI from pydantic import BaseModel app = FastAPI () class Item ( BaseModel ): name : str description : str | None = None price : float tax : float | None = None tags : list [ str ] = [] @app . post ( "/items/" ) async def create_item ( item : Item ) -> Item : return item @app . get ( "/items/" ) async def read_items () -> list [ Item ]: return [ Item ( name = "Portal Gun" , price = 42.0 ), Item ( name = "Plumbus" , price = 32.0 ), ]

- [fastapi-custom-response-18] HTML Response ¶

- [fastapi-custom-response-19] To return a response with HTML directly from FastAPI , use HTMLResponse .

- [fastapi-custom-response-20] Import HTMLResponse .

- [fastapi-custom-response-21] Pass HTMLResponse as the parameter response_class of your path operation decorator .

- [fastapi-custom-response-22] from fastapi import FastAPI from fastapi.responses import HTMLResponse app = FastAPI () @app . get ( "/items/" , response_class = HTMLResponse ) async def read_items (): return """ <html> <head> <title>Some HTML in here</title> </head> <body> <h1>Look ma! HTML!</h1> </body> </html> """

- [fastapi-custom-response-23] The parameter response_class will also be used to define the "media type" of the response.

- [fastapi-custom-response-24] In this case, the HTTP header Content-Type will be set to text/html .

- [fastapi-custom-response-25] And it will be documented as such in OpenAPI.

- [fastapi-custom-response-26] Return a Response ¶

- [fastapi-custom-response-27] As seen in Return a Response directly , you can also override the response directly in your path operation , by returning it.

- [fastapi-custom-response-28] The same example from above, returning an HTMLResponse , could look like:

- [fastapi-custom-response-29] from fastapi import FastAPI from fastapi.responses import HTMLResponse app = FastAPI () @app . get ( "/items/" ) async def read_items (): html_content = """ <html> <head> <title>Some HTML in here</title> </head> <body> <h1>Look ma! HTML!</h1> </body> </html> """ return HTMLResponse ( content = html_content , status_code = 200 )

- [fastapi-custom-response-30] Warning

- [fastapi-custom-response-31] A Response returned directly by your path operation function won't be documented in OpenAPI (for example, the Content-Type won't be documented) and won't be visible in the automatic interactive docs.

- [fastapi-custom-response-32] Of course, the actual Content-Type header, status code, etc, will come from the Response object you returned.

- [fastapi-custom-response-33] Document in OpenAPI and override Response ¶

- [fastapi-custom-response-34] If you want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, you can use the response_class parameter AND return a Response object.

- [fastapi-custom-response-35] The response_class will then be used only to document the OpenAPI path operation , but your Response will be used as is.

- [fastapi-custom-response-36] HTMLResponse

- [fastapi-custom-response-37] For example, it could be something like:

- [fastapi-custom-response-38] from fastapi import FastAPI from fastapi.responses import HTMLResponse app = FastAPI () def generate_html_response (): html_content = """ <html> <head> <title>Some HTML in here</title> </head> <body> <h1>Look ma! HTML!</h1> </body> </html> """ return HTMLResponse ( content = html_content , status_code = 200 ) @app . get ( "/items/" , response_class = HTMLResponse ) async def read_items (): return generate_html_response ()

- [fastapi-custom-response-39] In this example, the function generate_html_response() already generates and returns a Response instead of returning the HTML in a str .

- [fastapi-custom-response-40] By returning the result of calling generate_html_response() , you are already returning a Response that will override the default FastAPI behavior.

- [fastapi-custom-response-41] But as you passed the HTMLResponse in the response_class too, FastAPI will know how to document it in OpenAPI and the interactive docs as HTML with text/html :

- [fastapi-custom-response-42] Available responses ¶

- [fastapi-custom-response-43] Here are some of the available responses.

- [fastapi-custom-response-44] Keep in mind that you can use Response to return anything else, or even create a custom sub-class.

- [fastapi-custom-response-45] Technical Details

- [fastapi-custom-response-46] You could also use from starlette.responses import HTMLResponse .

- [fastapi-custom-response-47] FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

- [fastapi-custom-response-48] Response ¶

- [fastapi-custom-response-49] The main Response class, all the other responses inherit from it.

- [fastapi-custom-response-50] You can return it directly.

- [fastapi-custom-response-51] It accepts the following parameters:

- [fastapi-custom-response-52] content - A str or bytes .

- [fastapi-custom-response-53] status_code - An int HTTP status code.

- [fastapi-custom-response-54] headers - A dict of strings.

- [fastapi-custom-response-55] media_type - A str giving the media type. E.g. "text/html" .

- [fastapi-custom-response-56] FastAPI (actually Starlette) will automatically include a Content-Length header. It will also include a Content-Type header, based on the media_type and appending a charset for text types.

- [fastapi-custom-response-57] from fastapi import FastAPI , Response app = FastAPI () @app . get ( "/legacy/" ) def get_legacy_data (): data = """<?xml version="1.0"?> <shampoo> <Header> Apply shampoo here. </Header> <Body> You'll have to use soap here. </Body> </shampoo> """ return Response ( content = data , media_type = "application/xml" )

- [fastapi-custom-response-58] HTMLResponse ¶

- [fastapi-custom-response-59] Takes some text or bytes and returns an HTML response, as you read above.

- [fastapi-custom-response-60] PlainTextResponse ¶

- [fastapi-custom-response-61] Takes some text or bytes and returns a plain text response.

- [fastapi-custom-response-62] from fastapi import FastAPI from fastapi.responses import PlainTextResponse app = FastAPI () @app . get ( "/" , response_class = PlainTextResponse ) async def main (): return "Hello World"

- [fastapi-custom-response-63] JSONResponse ¶

- [fastapi-custom-response-64] Takes some data and returns an application/json encoded response.

- [fastapi-custom-response-65] This is the default response used in FastAPI , as you read above.

- [fastapi-custom-response-66] But if you declare a response model or return type, that will be used directly to serialize the data to JSON, and a response with the right media type for JSON will be returned directly, without using the JSONResponse class.

- [fastapi-custom-response-67] This is the ideal way to get the best performance.

- [fastapi-custom-response-68] RedirectResponse ¶

- [fastapi-custom-response-69] Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.

- [fastapi-custom-response-70] You can return a RedirectResponse directly:

- [fastapi-custom-response-71] from fastapi import FastAPI from fastapi.responses import RedirectResponse app = FastAPI () @app . get ( "/typer" ) async def redirect_typer (): return RedirectResponse ( "https://typer.tiangolo.com" )

- [fastapi-custom-response-72] Or you can use it in the response_class parameter:

- [fastapi-custom-response-73] from fastapi import FastAPI from fastapi.responses import RedirectResponse app = FastAPI () @app . get ( "/fastapi" , response_class = RedirectResponse ) async def redirect_fastapi (): return "https://fastapi.tiangolo.com"

- [fastapi-custom-response-74] If you do that, then you can return the URL directly from your path operation function.

- [fastapi-custom-response-75] In this case, the status_code used will be the default one for the RedirectResponse , which is 307 .

- [fastapi-custom-response-76] You can also use the status_code parameter combined with the response_class parameter:

- [fastapi-custom-response-77] from fastapi import FastAPI from fastapi.responses import RedirectResponse app = FastAPI () @app . get ( "/pydantic" , response_class = RedirectResponse , status_code = 302 ) async def redirect_pydantic (): return "https://docs.pydantic.dev/"

- [fastapi-custom-response-78] StreamingResponse ¶

- [fastapi-custom-response-79] Takes an async generator or a normal generator/iterator (a function with yield ) and streams the response body.

- [fastapi-custom-response-80] import anyio from fastapi import FastAPI from fastapi.responses import StreamingResponse app = FastAPI () async def fake_video_streamer (): for i in range ( 10 ): yield b "some fake video bytes" await anyio . sleep ( 0 ) @app . get ( "/" ) async def main (): return StreamingResponse ( fake_video_streamer ())

- [fastapi-custom-response-81] An async task can only be cancelled when it reaches an await . If there is no await , the generator (function with yield ) can not be cancelled properly and may keep running even after cancellation is requested.

- [fastapi-custom-response-82] Since this small example does not need any await statements, we add an await anyio.sleep(0) to give the event loop a chance to handle cancellation.

- [fastapi-custom-response-83] This would be even more important with large or infinite streams.

- [fastapi-custom-response-84] Tip

- [fastapi-custom-response-85] Instead of returning a StreamingResponse directly, you should probably follow the style in Stream Data , it's much more convenient and handles cancellation behind the scenes for you.

- [fastapi-custom-response-86] If you are streaming JSON Lines, follow the Stream JSON Lines tutorial.

- [fastapi-custom-response-87] FileResponse ¶

- [fastapi-custom-response-88] Asynchronously streams a file as the response.

- [fastapi-custom-response-89] Takes a different set of arguments to instantiate than the other response types:

- [fastapi-custom-response-90] path - The file path to the file to stream.

- [fastapi-custom-response-91] headers - Any custom headers to include, as a dictionary.

- [fastapi-custom-response-92] media_type - A string giving the media type. If unset, the filename or path will be used to infer a media type.

- [fastapi-custom-response-93] filename - If set, this will be included in the response Content-Disposition .

- [fastapi-custom-response-94] File responses will include appropriate Content-Length , Last-Modified and ETag headers.

- [fastapi-custom-response-95] from fastapi import FastAPI from fastapi.responses import FileResponse some_file_path = "large-video-file.mp4" app = FastAPI () @app . get ( "/" ) async def main (): return FileResponse ( some_file_path )

- [fastapi-custom-response-96] You can also use the response_class parameter:

- [fastapi-custom-response-97] from fastapi import FastAPI from fastapi.responses import FileResponse some_file_path = "large-video-file.mp4" app = FastAPI () @app . get ( "/" , response_class = FileResponse ) async def main (): return some_file_path

- [fastapi-custom-response-98] In this case, you can return the file path directly from your path operation function.

- [fastapi-custom-response-99] Custom response class ¶

- [fastapi-custom-response-100] You can create your own custom response class, inheriting from Response and using it.

- [fastapi-custom-response-101] For example, let's say that you want to use orjson with some settings.

- [fastapi-custom-response-102] orjson

- [fastapi-custom-response-103] Let's say you want it to return indented and formatted JSON, so you want to use the orjson option orjson.OPT_INDENT_2 .

- [fastapi-custom-response-104] You could create a CustomORJSONResponse . The main thing you have to do is create a Response.render(content) method that returns the content as bytes :

- [fastapi-custom-response-105] from typing import Any import orjson from fastapi import FastAPI , Response app = FastAPI () class CustomORJSONResponse ( Response ): media_type = "application/json" def render ( self , content : Any ) -> bytes : assert orjson is not None , "orjson must be installed" return orjson . dumps ( content , option = orjson . OPT_INDENT_2 ) @app . get ( "/" , response_class = CustomORJSONResponse ) async def main (): return { "message" : "Hello World" }

- [fastapi-custom-response-106] Now instead of returning:

- [fastapi-custom-response-107] { "message" : "Hello World" }

- [fastapi-custom-response-108] ...this response will return:

- [fastapi-custom-response-109] Of course, you will probably find much better ways to take advantage of this than formatting JSON. 😉

- [fastapi-custom-response-110] orjson or Response Model ¶

- [fastapi-custom-response-111] If what you are looking for is performance, you are probably better off using a Response Model than an orjson response.

- [fastapi-custom-response-112] With a response model, FastAPI will use Pydantic to serialize the data to JSON, without using intermediate steps, like converting it with jsonable_encoder , which would happen in any other case.

- [fastapi-custom-response-113] And under the hood, Pydantic uses the same underlying Rust mechanisms as orjson to serialize to JSON, so you will already get the best performance with a response model.

- [fastapi-custom-response-114] Default response class ¶

- [fastapi-custom-response-115] When creating a FastAPI class instance or an APIRouter you can specify which response class to use by default.

- [fastapi-custom-response-116] The parameter that defines this is default_response_class .

- [fastapi-custom-response-117] In the example below, FastAPI will use HTMLResponse by default, in all path operations , instead of JSON.

- [fastapi-custom-response-118] from fastapi import FastAPI from fastapi.responses import HTMLResponse app = FastAPI ( default_response_class = HTMLResponse ) @app . get ( "/items/" ) async def read_items (): return "<h1>Items</h1><p>This is a list of items.</p>"

- [fastapi-custom-response-119] You can still override response_class in path operations as before.

- [fastapi-custom-response-120] Additional documentation ¶

- [fastapi-custom-response-121] You can also declare the media type and many other details in OpenAPI using responses : Additional Responses in OpenAPI .
