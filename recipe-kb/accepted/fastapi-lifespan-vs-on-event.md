---
id: fastapi-lifespan-vs-on-event
kind: debug-recipe
status: accepted
stack:
- fastapi
failure_class: fastapi/lifecycle
symptoms:
- FastAPI app fails to initialize shared resources because startup/shutdown logic
  is missing or uses deprecated on_event
fingerprints:
- lifespan
- startup
- shutdown
- on_event
- asynccontextmanager
first_checks:
- Check whether on_event('startup') or on_event('shutdown') is used instead of the
  recommended lifespan context manager
- Check whether the lifespan async function contains a yield separating setup from
  teardown code
- Check whether the FastAPI app is constructed with lifespan= passed as a parameter
do_not:
- Do not perform long-running blocking operations in on_event or lifespan without
  awaiting
- Do not share state via globals without considering concurrent workers
evidence_needed:
- Identify whether the startup code runs before the first request is served
- Capture app startup logs to verify resource initialization
minimal_fix_scope:
- The lifespan async context manager function
- The FastAPI app constructor lifespan parameter
validation_ladder:
- Start the app and verify shared resources are initialized before request handling
- Stop the app and verify teardown runs
- Run the app lifecycle or integration test
regression_guard:
- Add a lifecycle test that asserts setup code runs before and teardown after request
  handling
evidence_refs:
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-1
  short_excerpt: Lifespan Events ¶
  quote_hash: sha256:d72b5581be1a4643393ebfcc934c851f36f211cdc0299d09857bfc50405f12ba
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-2
  short_excerpt: You can define logic (code) that should be executed before the application
    starts up . This means that this code will be executed once , before the application
    starts receiving requests .
  quote_hash: sha256:3fefd39e05270155b06807045a9216bd776c41d6594261b91978a64efc21862e
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-4
  short_excerpt: Because this code is executed before the application starts taking
    requests, and right after it finishes handling requests, it covers the whole application
    lifespan (the word "lifespan" will be important in a second 😉).
  quote_hash: sha256:321d05a3f69dc0b36e4ac5b4b9290bccd3d32341c7cf03403f96a63f64286d80
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-12
  short_excerpt: That's what we'll solve, let's load the model before the requests
    are handled, but only right before the application starts receiving requests,
    not while the code is being loaded.
  quote_hash: sha256:1c62d270b38364e5203f34e251b5391fba1061098763a44a65fed0702b12c590
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-13
  short_excerpt: Lifespan ¶
  quote_hash: sha256:849edc14e955aee4e5733d1b1e5b309ac6b34e33145541bcfa0c1522771ded11
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-14
  short_excerpt: You can define this startup and shutdown logic using the lifespan
    parameter of the FastAPI app, and a "context manager" (I'll show you what that
    is in a second).
  quote_hash: sha256:975bc4dbcffcc4e6af4202c4d6ea65766f7307634df276417a0747c57fec2f51
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-16
  short_excerpt: 'We create an async function lifespan() with yield like this:'
  quote_hash: sha256:fcabb28abe284e29b9dd2931a0e6b67075e557706e8a00876380caac4afb9dfb
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-17
  short_excerpt: 'from contextlib import asynccontextmanager from fastapi import FastAPI
    def fake_answer_to_everything_ml_model ( x : float ): return x * 42 ml_models
    = {} @asynccontextmanager async def lifespan ( app : FastAPI ): # Load the ML
    model ml_models [ "answer_to_everything" ] = fake_answer_to_everything_ml_model
    yield # Clean up the ML models and release the resources ml_models . clear ()
    app = FastAPI ( lifespan = lifespan ) @app . get ( "/predict" ) async def predict
    ( x : float ): result = ml_models [ "answer_to_everything" ]( x ) return { "result"
    : result }'
  quote_hash: sha256:43dce6559d16455a7dec504b159a7a58155f4bed60ddd9c44820d14d06211c08
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-18
  short_excerpt: Here we are simulating the expensive startup operation of loading
    the model by putting the (fake) model function in the dictionary with machine
    learning models before the yield . This code will be executed before the application
    starts taking requests , during the startup .
  quote_hash: sha256:a5e243e418b0a27836d029a4f8d1448c7e54faf64567c8cfc661905116237d69
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-19
  short_excerpt: And then, right after the yield , we unload the model. This code
    will be executed after the application finishes handling requests , right before
    the shutdown . This could, for example, release resources like memory or a GPU.
  quote_hash: sha256:898d3d7ec340b30a9a9d6ef3ce06fb940a2b851e9e16163d4ba54f814c14fa8e
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-21
  short_excerpt: The shutdown would happen when you are stopping the application.
  quote_hash: sha256:8c6ace3fa924397a1bc1b8a063832a93896fa1884b8e903730b4754f68e5dab2
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-23
  short_excerpt: Lifespan function ¶
  quote_hash: sha256:69e2fd8903f291afa65750b683cd6ed3e15e215d25803994abf714737745c2e6
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-25
  short_excerpt: The first part of the function, before the yield , will be executed
    before the application starts.
  quote_hash: sha256:b60808b09414d57dbe4cb11cf238fe049ab8db850e421f90213c933f7d5444e2
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-28
  short_excerpt: If you check, the function is decorated with an @asynccontextmanager
    .
  quote_hash: sha256:309fd0f5578a63dc113b39a9df9ee17e822ff4cb7627e7a301a0baa3b2df2ec8
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-33
  short_excerpt: 'async with lifespan ( app ): await do_stuff ()'
  quote_hash: sha256:7dd257445b62803b777a3f2c6050111e85fad8c95a6d6c1189864aceb6f393e5
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-36
  short_excerpt: The lifespan parameter of the FastAPI app takes an async context
    manager , so we can pass our new lifespan async context manager to it.
  quote_hash: sha256:cffc4a1ef3f73b42afac9ddc3c69ad8e4b52da975e80cc9c27a74ef4bbd13b1b
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-39
  short_excerpt: The recommended way to handle the startup and shutdown is using the
    lifespan parameter of the FastAPI app as described above. If you provide a lifespan
    parameter, startup and shutdown event handlers will no longer be called. It's
    all lifespan or all events, not both.
  quote_hash: sha256:96eac8bafab6dbee22e91247b469082a98152b81d9aeb6545ae142db53d95770
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-41
  short_excerpt: There's an alternative way to define this logic to be executed during
    startup and during shutdown .
  quote_hash: sha256:70212746018f2acc9bc7c800656465f175fa4cf11c460de305e5f125f83c1c46
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-42
  short_excerpt: You can define event handlers (functions) that need to be executed
    before the application starts up, or when the application is shutting down.
  quote_hash: sha256:1492175b7b5cd705e489ebd72871dd2343d8261539e9018988b905797c15dbf5
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-44
  short_excerpt: startup event ¶
  quote_hash: sha256:aee10343808d3131e969fda2e06492b542d637724dedbb352314e02ec575672d
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-45
  short_excerpt: 'To add a function that should be run before the application starts,
    declare it with the event "startup" :'
  quote_hash: sha256:8bae9b36ff53d1a6f024970f7d171445acbfac9740f26fa070ef333d2fff029f
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-46
  short_excerpt: 'from fastapi import FastAPI app = FastAPI () items = {} @app . on_event
    ( "startup" ) async def startup_event (): items [ "foo" ] = { "name" : "Fighters"
    } items [ "bar" ] = { "name" : "Tenders" } @app . get ( "/items/ {item_id} " )
    async def read_items ( item_id : str ): return items [ item_id ]'
  quote_hash: sha256:e6d187b22c3ddab883a4ce36ead531f4f12b55d472accdacb3d1ca516850b45e
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-47
  short_excerpt: In this case, the startup event handler function will initialize
    the items "database" (just a dict ) with some values.
  quote_hash: sha256:f16383854b3c061d7f42ab3a563cb499e5ae9c20827bf9249044759e1c6b8cfc
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-49
  short_excerpt: And your application won't start receiving requests until all the
    startup event handlers have completed.
  quote_hash: sha256:4d77c94416ec00dda0dc4d4da6969a687c63f9b0fc1169d5dc839871b305ced7
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-50
  short_excerpt: shutdown event ¶
  quote_hash: sha256:e56c017b4e52e439b3286b633a2b33e75a3a40f68dbe2c9e93a70ac21e432abe
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-51
  short_excerpt: 'To add a function that should be run when the application is shutting
    down, declare it with the event "shutdown" :'
  quote_hash: sha256:318ced13932de26c50d9b3a4c8830fdbb6a60cee390d9c7949958b7dc05f8bd5
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-52
  short_excerpt: 'from fastapi import FastAPI app = FastAPI () @app . on_event ( "shutdown"
    ) def shutdown_event (): with open ( "log.txt" , mode = "a" ) as log : log . write
    ( "Application shutdown" ) @app . get ( "/items/" ) async def read_items (): return
    [{ "name" : "Foo" }]'
  quote_hash: sha256:a6d17c4943563493867893f914f2245ac906e03026f9ddc66a2afbf76dadaae3
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-53
  short_excerpt: Here, the shutdown event handler function will write a text line
    "Application shutdown" to a file log.txt .
  quote_hash: sha256:822127e74308cd368b9b00b5c68d21227dbf8cbce7740bb32fd2467752534253
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-60
  short_excerpt: startup and shutdown together ¶
  quote_hash: sha256:942a4fb2d750f13c3966f5f56794779cfdb00639f7418ff82000b4637b6f9162
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-61
  short_excerpt: There's a high chance that the logic for your startup and shutdown
    is connected, you might want to start something and then finish it, acquire a
    resource and then release it, etc.
  quote_hash: sha256:644fb125c2624dfb2787f01a03f443b13221233191cb83f69355f5bb8333e636
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-63
  short_excerpt: Because of that, it's now recommended to instead use the lifespan
    as explained above.
  quote_hash: sha256:1bf4af1ef52b1421bd1de0779ebe7e181981dee21d1341261f2f92b505d6b5a8
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-66
  short_excerpt: Underneath, in the ASGI technical specification, this is part of
    the Lifespan Protocol , and it defines events called startup and shutdown .
  quote_hash: sha256:3a7c6e9d7ce1e256eeb620f496dbcd51fd73e7583627a0fc9d72c6530d888efc
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-67
  short_excerpt: You can read more about the Starlette lifespan handlers in Starlette's
    Lifespan' docs .
  quote_hash: sha256:64c0a69deeeeb5abde534b5500142a84b588135bdce21ae35c36eaab1ea549c0
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-68
  short_excerpt: Including how to handle lifespan state that can be used in other
    areas of your code.
  quote_hash: sha256:344bf46cb05f237fe1974bf1d0797543cd79c73b3ae4637f085e4e12a50e970f
- source_id: fastapi-events
  url: https://fastapi.tiangolo.com/advanced/events/
  final_url: https://fastapi.tiangolo.com/advanced/events/
  source_type: official_doc
  captured_at: '2026-05-26T08:42:53.083772Z'
  section_anchor: root
  span_id: fastapi-events-70
  short_excerpt: 🚨 Keep in mind that these lifespan events (startup and shutdown)
    will only be executed for the main application, not for Sub Applications - Mounts
    .
  quote_hash: sha256:15c17fb4f5a1da795dac15affc424af19f3ef4110a6a18be9a199d363e3fcb6d
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# fastapi-lifespan-vs-on-event

## Failure Class
fastapi/lifecycle

## Symptoms
- FastAPI app fails to initialize shared resources because startup/shutdown logic is missing or uses deprecated on_event

## Fingerprints
- lifespan
- startup
- shutdown
- on_event
- asynccontextmanager

## First Checks
- Check whether on_event('startup') or on_event('shutdown') is used instead of the recommended lifespan context manager
- Check whether the lifespan async function contains a yield separating setup from teardown code
- Check whether the FastAPI app is constructed with lifespan= passed as a parameter

## Do Not Patch Yet
- Do not perform long-running blocking operations in on_event or lifespan without awaiting
- Do not share state via globals without considering concurrent workers

## Evidence Needed
- Identify whether the startup code runs before the first request is served
- Capture app startup logs to verify resource initialization

## Minimal Fix Scope
- The lifespan async context manager function
- The FastAPI app constructor lifespan parameter

## Validation Ladder
- Start the app and verify shared resources are initialized before request handling
- Stop the app and verify teardown runs
- Run the app lifecycle or integration test

## Regression Guard
- Add a lifecycle test that asserts setup code runs before and teardown after request handling

## Reviewer Notes
