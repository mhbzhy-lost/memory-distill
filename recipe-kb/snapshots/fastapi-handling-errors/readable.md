- [fastapi-handling-errors-1] Handling Errors ¶

- [fastapi-handling-errors-2] There are many situations in which you need to notify an error to a client that is using your API.

- [fastapi-handling-errors-3] This client could be a browser with a frontend, a code from someone else, an IoT device, etc.

- [fastapi-handling-errors-4] You could need to tell the client that:

- [fastapi-handling-errors-5] The client doesn't have enough privileges for that operation.

- [fastapi-handling-errors-6] The client doesn't have access to that resource.

- [fastapi-handling-errors-7] The item the client was trying to access doesn't exist.

- [fastapi-handling-errors-8] etc.

- [fastapi-handling-errors-9] In these cases, you would normally return an HTTP status code in the range of 400 (from 400 to 499).

- [fastapi-handling-errors-10] This is similar to the 200 HTTP status codes (from 200 to 299). Those "200" status codes mean that somehow there was a "success" in the request.

- [fastapi-handling-errors-11] The status codes in the 400 range mean that there was an error from the client.

- [fastapi-handling-errors-12] Remember all those "404 Not Found" errors (and jokes)?

- [fastapi-handling-errors-13] Use HTTPException ¶

- [fastapi-handling-errors-14] To return HTTP responses with errors to the client you use HTTPException .

- [fastapi-handling-errors-15] Import HTTPException ¶

- [fastapi-handling-errors-16] from fastapi import FastAPI , HTTPException app = FastAPI () items = { "foo" : "The Foo Wrestlers" } @app . get ( "/items/ {item_id} " ) async def read_item ( item_id : str ): if item_id not in items : raise HTTPException ( status_code = 404 , detail = "Item not found" ) return { "item" : items [ item_id ]}

- [fastapi-handling-errors-17] Raise an HTTPException in your code ¶

- [fastapi-handling-errors-18] HTTPException is a normal Python exception with additional data relevant for APIs.

- [fastapi-handling-errors-19] Because it's a Python exception, you don't return it, you raise it.

- [fastapi-handling-errors-20] This also means that if you are inside a utility function that you are calling inside of your path operation function , and you raise the HTTPException from inside of that utility function, it won't run the rest of the code in the path operation function , it will terminate that request right away and send the HTTP error from the HTTPException to the client.

- [fastapi-handling-errors-21] The benefit of raising an exception over returning a value will be more evident in the section about Dependencies and Security.

- [fastapi-handling-errors-22] In this example, when the client requests an item by an ID that doesn't exist, raise an exception with a status code of 404 :

- [fastapi-handling-errors-23] The resulting response ¶

- [fastapi-handling-errors-24] If the client requests http://example.com/items/foo (an item_id "foo" ), that client will receive an HTTP status code of 200, and a JSON response of:

- [fastapi-handling-errors-25] { "item" : "The Foo Wrestlers" }

- [fastapi-handling-errors-26] But if the client requests http://example.com/items/bar (a non-existent item_id "bar" ), that client will receive an HTTP status code of 404 (the "not found" error), and a JSON response of:

- [fastapi-handling-errors-27] { "detail" : "Item not found" }

- [fastapi-handling-errors-28] Tip

- [fastapi-handling-errors-29] When raising an HTTPException , you can pass any value that can be converted to JSON as the parameter detail , not only str .

- [fastapi-handling-errors-30] You could pass a dict , a list , etc.

- [fastapi-handling-errors-31] They are handled automatically by FastAPI and converted to JSON.

- [fastapi-handling-errors-32] Add custom headers ¶

- [fastapi-handling-errors-33] There are some situations in where it's useful to be able to add custom headers to the HTTP error. For example, for some types of security.

- [fastapi-handling-errors-34] You probably won't need to use it directly in your code.

- [fastapi-handling-errors-35] But in case you needed it for an advanced scenario, you can add custom headers:

- [fastapi-handling-errors-36] from fastapi import FastAPI , HTTPException app = FastAPI () items = { "foo" : "The Foo Wrestlers" } @app . get ( "/items-header/ {item_id} " ) async def read_item_header ( item_id : str ): if item_id not in items : raise HTTPException ( status_code = 404 , detail = "Item not found" , headers = { "X-Error" : "There goes my error" }, ) return { "item" : items [ item_id ]}

- [fastapi-handling-errors-37] Install custom exception handlers ¶

- [fastapi-handling-errors-38] You can add custom exception handlers with the same exception utilities from Starlette .

- [fastapi-handling-errors-39] Let's say you have a custom exception UnicornException that you (or a library you use) might raise .

- [fastapi-handling-errors-40] And you want to handle this exception globally with FastAPI.

- [fastapi-handling-errors-41] You could add a custom exception handler with @app.exception_handler() :

- [fastapi-handling-errors-42] from fastapi import FastAPI , Request from fastapi.responses import JSONResponse class UnicornException ( Exception ): def __init__ ( self , name : str ): self . name = name app = FastAPI () @app . exception_handler ( UnicornException ) async def unicorn_exception_handler ( request : Request , exc : UnicornException ): return JSONResponse ( status_code = 418 , content = { "message" : f "Oops! { exc . name } did something. There goes a rainbow..." }, ) @app . get ( "/unicorns/ {name} " ) async def read_unicorn ( name : str ): if name == "yolo" : raise UnicornException ( name = name ) return { "unicorn_name" : name }

- [fastapi-handling-errors-43] Here, if you request /unicorns/yolo , the path operation will raise a UnicornException .

- [fastapi-handling-errors-44] But it will be handled by the unicorn_exception_handler .

- [fastapi-handling-errors-45] So, you will receive a clean error, with an HTTP status code of 418 and a JSON content of:

- [fastapi-handling-errors-46] { "message" : "Oops! yolo did something. There goes a rainbow..." }

- [fastapi-handling-errors-47] Technical Details

- [fastapi-handling-errors-48] You could also use from starlette.requests import Request and from starlette.responses import JSONResponse .

- [fastapi-handling-errors-49] FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with Request .

- [fastapi-handling-errors-50] Override the default exception handlers ¶

- [fastapi-handling-errors-51] FastAPI has some default exception handlers.

- [fastapi-handling-errors-52] These handlers are in charge of returning the default JSON responses when you raise an HTTPException and when the request has invalid data.

- [fastapi-handling-errors-53] You can override these exception handlers with your own.

- [fastapi-handling-errors-54] Override request validation exceptions ¶

- [fastapi-handling-errors-55] When a request contains invalid data, FastAPI internally raises a RequestValidationError .

- [fastapi-handling-errors-56] And it also includes a default exception handler for it.

- [fastapi-handling-errors-57] To override it, import the RequestValidationError and use it with @app.exception_handler(RequestValidationError) to decorate the exception handler.

- [fastapi-handling-errors-58] The exception handler will receive a Request and the exception.

- [fastapi-handling-errors-59] from fastapi import FastAPI , HTTPException from fastapi.exceptions import RequestValidationError from fastapi.responses import PlainTextResponse from starlette.exceptions import HTTPException as StarletteHTTPException app = FastAPI () @app . exception_handler ( StarletteHTTPException ) async def http_exception_handler ( request , exc ): return PlainTextResponse ( str ( exc . detail ), status_code = exc . status_code ) @app . exception_handler ( RequestValidationError ) async def validation_exception_handler ( request , exc : RequestValidationError ): message = "Validation errors:" for error in exc . errors (): message += f " \n Field: { error [ 'loc' ] } , Error: { error [ 'msg' ] } " return PlainTextResponse ( message , status_code = 400 ) @app . get ( "/items/ {item_id} " ) async def read_item ( item_id : int ): if item_id == 3 : raise HTTPException ( status_code = 418 , detail = "Nope! I don't like 3." ) return { "item_id" : item_id }

- [fastapi-handling-errors-60] Now, if you go to /items/foo , instead of getting the default JSON error with:

- [fastapi-handling-errors-61] { "detail" : [ { "loc" : [ "path" , "item_id" ], "msg" : "value is not a valid integer" , "type" : "type_error.integer" } ] }

- [fastapi-handling-errors-62] you will get a text version, with:

- [fastapi-handling-errors-63] Validation errors: Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer

- [fastapi-handling-errors-64] Override the HTTPException error handler ¶

- [fastapi-handling-errors-65] The same way, you can override the HTTPException handler.

- [fastapi-handling-errors-66] For example, you could want to return a plain text response instead of JSON for these errors:

- [fastapi-handling-errors-67] You could also use from starlette.responses import PlainTextResponse .

- [fastapi-handling-errors-68] FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

- [fastapi-handling-errors-69] Warning

- [fastapi-handling-errors-70] Have in mind that the RequestValidationError contains the information of the file name and line where the validation error happens so that you can show it in your logs with the relevant information if you want to.

- [fastapi-handling-errors-71] But that means that if you just convert it to a string and return that information directly, you could be leaking a bit of information about your system, that's why here the code extracts and shows each error independently.

- [fastapi-handling-errors-72] Use the RequestValidationError body ¶

- [fastapi-handling-errors-73] The RequestValidationError contains the body it received with invalid data.

- [fastapi-handling-errors-74] You could use it while developing your app to log the body and debug it, return it to the user, etc.

- [fastapi-handling-errors-75] from fastapi import FastAPI , Request from fastapi.encoders import jsonable_encoder from fastapi.exceptions import RequestValidationError from fastapi.responses import JSONResponse from pydantic import BaseModel app = FastAPI () @app . exception_handler ( RequestValidationError ) async def validation_exception_handler ( request : Request , exc : RequestValidationError ): return JSONResponse ( status_code = 422 , content = jsonable_encoder ({ "detail" : exc . errors (), "body" : exc . body }), ) class Item ( BaseModel ): title : str size : int @app . post ( "/items/" ) async def create_item ( item : Item ): return item

- [fastapi-handling-errors-76] Now try sending an invalid item like:

- [fastapi-handling-errors-77] { "title" : "towel" , "size" : "XL" }

- [fastapi-handling-errors-78] You will receive a response telling you that the data is invalid containing the received body:

- [fastapi-handling-errors-79] { "detail" : [ { "loc" : [ "body" , "size" ], "msg" : "value is not a valid integer" , "type" : "type_error.integer" } ], "body" : { "title" : "towel" , "size" : "XL" } }

- [fastapi-handling-errors-80] HTTPException

- [fastapi-handling-errors-81] FastAPI has its own HTTPException .

- [fastapi-handling-errors-82] And FastAPI 's HTTPException error class inherits from Starlette's HTTPException error class.

- [fastapi-handling-errors-83] The only difference is that FastAPI 's HTTPException accepts any JSON-able data for the detail field, while Starlette's HTTPException only accepts strings for it.

- [fastapi-handling-errors-84] So, you can keep raising FastAPI 's HTTPException as normally in your code.

- [fastapi-handling-errors-85] But when you register an exception handler, you should register it for Starlette's HTTPException .

- [fastapi-handling-errors-86] This way, if any part of Starlette's internal code, or a Starlette extension or plug-in, raises a Starlette HTTPException , your handler will be able to catch and handle it.

- [fastapi-handling-errors-87] In this example, to be able to have both HTTPException s in the same code, Starlette's exceptions is renamed to StarletteHTTPException :

- [fastapi-handling-errors-88] from starlette.exceptions import HTTPException as StarletteHTTPException

- [fastapi-handling-errors-89] Reuse FastAPI 's exception handlers ¶

- [fastapi-handling-errors-90] If you want to use the exception along with the same default exception handlers from FastAPI , you can import and reuse the default exception handlers from fastapi.exception_handlers :

- [fastapi-handling-errors-91] from fastapi import FastAPI , HTTPException from fastapi.exception_handlers import ( http_exception_handler , request_validation_exception_handler , ) from fastapi.exceptions import RequestValidationError from starlette.exceptions import HTTPException as StarletteHTTPException app = FastAPI () @app . exception_handler ( StarletteHTTPException ) async def custom_http_exception_handler ( request , exc ): print ( f "OMG! An HTTP error!: { repr ( exc ) } " ) return await http_exception_handler ( request , exc ) @app . exception_handler ( RequestValidationError ) async def validation_exception_handler ( request , exc ): print ( f "OMG! The client sent invalid data!: { exc } " ) return await request_validation_exception_handler ( request , exc ) @app . get ( "/items/ {item_id} " ) async def read_item ( item_id : int ): if item_id == 3 : raise HTTPException ( status_code = 418 , detail = "Nope! I don't like 3." ) return { "item_id" : item_id }

- [fastapi-handling-errors-92] In this example you are just printing the error with a very expressive message, but you get the idea. You can use the exception and then just reuse the default exception handlers.
