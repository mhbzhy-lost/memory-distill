- [fastapi-events-1] Lifespan Events ¶

- [fastapi-events-2] You can define logic (code) that should be executed before the application starts up . This means that this code will be executed once , before the application starts receiving requests .

- [fastapi-events-3] The same way, you can define logic (code) that should be executed when the application is shutting down . In this case, this code will be executed once , after having handled possibly many requests .

- [fastapi-events-4] Because this code is executed before the application starts taking requests, and right after it finishes handling requests, it covers the whole application lifespan (the word "lifespan" will be important in a second 😉).

- [fastapi-events-5] This can be very useful for setting up resources that you need to use for the whole app, and that are shared among requests, and/or that you need to clean up afterwards. For example, a database connection pool, or loading a shared machine learning model.

- [fastapi-events-6] Use Case ¶

- [fastapi-events-7] Let's start with an example use case and then see how to solve it with this.

- [fastapi-events-8] Let's imagine that you have some machine learning models that you want to use to handle requests. 🤖

- [fastapi-events-9] The same models are shared among requests, so, it's not one model per request, or one per user or something similar.

- [fastapi-events-10] Let's imagine that loading the model can take quite some time , because it has to read a lot of data from disk . So you don't want to do it for every request.

- [fastapi-events-11] You could load it at the top level of the module/file, but that would also mean that it would load the model even if you are just running a simple automated test, then that test would be slow because it would have to wait for the model to load before being able to run an independent part of the code.

- [fastapi-events-12] That's what we'll solve, let's load the model before the requests are handled, but only right before the application starts receiving requests, not while the code is being loaded.

- [fastapi-events-13] Lifespan ¶

- [fastapi-events-14] You can define this startup and shutdown logic using the lifespan parameter of the FastAPI app, and a "context manager" (I'll show you what that is in a second).

- [fastapi-events-15] Let's start with an example and then see it in detail.

- [fastapi-events-16] We create an async function lifespan() with yield like this:

- [fastapi-events-17] from contextlib import asynccontextmanager from fastapi import FastAPI def fake_answer_to_everything_ml_model ( x : float ): return x * 42 ml_models = {} @asynccontextmanager async def lifespan ( app : FastAPI ): # Load the ML model ml_models [ "answer_to_everything" ] = fake_answer_to_everything_ml_model yield # Clean up the ML models and release the resources ml_models . clear () app = FastAPI ( lifespan = lifespan ) @app . get ( "/predict" ) async def predict ( x : float ): result = ml_models [ "answer_to_everything" ]( x ) return { "result" : result }

- [fastapi-events-18] Here we are simulating the expensive startup operation of loading the model by putting the (fake) model function in the dictionary with machine learning models before the yield . This code will be executed before the application starts taking requests , during the startup .

- [fastapi-events-19] And then, right after the yield , we unload the model. This code will be executed after the application finishes handling requests , right before the shutdown . This could, for example, release resources like memory or a GPU.

- [fastapi-events-20] Tip

- [fastapi-events-21] The shutdown would happen when you are stopping the application.

- [fastapi-events-22] Maybe you need to start a new version, or you just got tired of running it. 🤷

- [fastapi-events-23] Lifespan function ¶

- [fastapi-events-24] The first thing to notice, is that we are defining an async function with yield . This is very similar to Dependencies with yield .

- [fastapi-events-25] The first part of the function, before the yield , will be executed before the application starts.

- [fastapi-events-26] And the part after the yield will be executed after the application has finished.

- [fastapi-events-27] Async Context Manager ¶

- [fastapi-events-28] If you check, the function is decorated with an @asynccontextmanager .

- [fastapi-events-29] That converts the function into something called an " async context manager ".

- [fastapi-events-30] A context manager in Python is something that you can use in a with statement, for example, open() can be used as a context manager:

- [fastapi-events-31] with open ( "file.txt" ) as file : file . read ()

- [fastapi-events-32] In recent versions of Python, there's also an async context manager . You would use it with async with :

- [fastapi-events-33] async with lifespan ( app ): await do_stuff ()

- [fastapi-events-34] When you create a context manager or an async context manager like above, what it does is that, before entering the with block, it will execute the code before the yield , and after exiting the with block, it will execute the code after the yield .

- [fastapi-events-35] In our code example above, we don't use it directly, but we pass it to FastAPI for it to use it.

- [fastapi-events-36] The lifespan parameter of the FastAPI app takes an async context manager , so we can pass our new lifespan async context manager to it.

- [fastapi-events-37] Alternative Events (deprecated) ¶

- [fastapi-events-38] Warning

- [fastapi-events-39] The recommended way to handle the startup and shutdown is using the lifespan parameter of the FastAPI app as described above. If you provide a lifespan parameter, startup and shutdown event handlers will no longer be called. It's all lifespan or all events, not both.

- [fastapi-events-40] You can probably skip this part.

- [fastapi-events-41] There's an alternative way to define this logic to be executed during startup and during shutdown .

- [fastapi-events-42] You can define event handlers (functions) that need to be executed before the application starts up, or when the application is shutting down.

- [fastapi-events-43] These functions can be declared with async def or normal def .

- [fastapi-events-44] startup event ¶

- [fastapi-events-45] To add a function that should be run before the application starts, declare it with the event "startup" :

- [fastapi-events-46] from fastapi import FastAPI app = FastAPI () items = {} @app . on_event ( "startup" ) async def startup_event (): items [ "foo" ] = { "name" : "Fighters" } items [ "bar" ] = { "name" : "Tenders" } @app . get ( "/items/ {item_id} " ) async def read_items ( item_id : str ): return items [ item_id ]

- [fastapi-events-47] In this case, the startup event handler function will initialize the items "database" (just a dict ) with some values.

- [fastapi-events-48] You can add more than one event handler function.

- [fastapi-events-49] And your application won't start receiving requests until all the startup event handlers have completed.

- [fastapi-events-50] shutdown event ¶

- [fastapi-events-51] To add a function that should be run when the application is shutting down, declare it with the event "shutdown" :

- [fastapi-events-52] from fastapi import FastAPI app = FastAPI () @app . on_event ( "shutdown" ) def shutdown_event (): with open ( "log.txt" , mode = "a" ) as log : log . write ( "Application shutdown" ) @app . get ( "/items/" ) async def read_items (): return [{ "name" : "Foo" }]

- [fastapi-events-53] Here, the shutdown event handler function will write a text line "Application shutdown" to a file log.txt .

- [fastapi-events-54] Note

- [fastapi-events-55] In the open() function, the mode="a" means "append", so, the line will be added after whatever is on that file, without overwriting the previous contents.

- [fastapi-events-56] Notice that in this case we are using a standard Python open() function that interacts with a file.

- [fastapi-events-57] So, it involves I/O (input/output), that requires "waiting" for things to be written to disk.

- [fastapi-events-58] But open() doesn't use async and await .

- [fastapi-events-59] So, we declare the event handler function with standard def instead of async def .

- [fastapi-events-60] startup and shutdown together ¶

- [fastapi-events-61] There's a high chance that the logic for your startup and shutdown is connected, you might want to start something and then finish it, acquire a resource and then release it, etc.

- [fastapi-events-62] Doing that in separated functions that don't share logic or variables together is more difficult as you would need to store values in global variables or similar tricks.

- [fastapi-events-63] Because of that, it's now recommended to instead use the lifespan as explained above.

- [fastapi-events-64] Technical Details ¶

- [fastapi-events-65] Just a technical detail for the curious nerds. 🤓

- [fastapi-events-66] Underneath, in the ASGI technical specification, this is part of the Lifespan Protocol , and it defines events called startup and shutdown .

- [fastapi-events-67] You can read more about the Starlette lifespan handlers in Starlette's Lifespan' docs .

- [fastapi-events-68] Including how to handle lifespan state that can be used in other areas of your code.

- [fastapi-events-69] Sub Applications ¶

- [fastapi-events-70] 🚨 Keep in mind that these lifespan events (startup and shutdown) will only be executed for the main application, not for Sub Applications - Mounts .
