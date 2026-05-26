from dataclasses import dataclass


@dataclass(frozen=True)
class RecipeTemplate:
    source_id: str
    failure_label: str
    recipe_id: str
    failure_class: str
    symptoms: list[str]
    fingerprints: list[str]
    first_checks: list[str]
    do_not: list[str]
    evidence_needed: list[str]
    minimal_fix_scope: list[str]
    validation_ladder: list[str]
    regression_guard: list[str]
    match_terms: list[str]


RECIPE_TEMPLATES: tuple[RecipeTemplate, ...] = (
    RecipeTemplate(
        source_id="react-error-418",
        failure_label="hydration mismatch",
        recipe_id="react-hydration-mismatch",
        failure_class="render/hydration",
        symptoms=["Hydration failed because the server rendered HTML didn't match the client"],
        fingerprints=[
            "Hydration failed",
            "server rendered HTML didn't match the client",
            "server rendered HTML did not match the client",
        ],
        first_checks=[
            "Check server/client branches such as typeof window in render output",
            "Check Date.now(), Math.random(), and locale formatting in render output",
            "Check invalid HTML nesting in the affected component",
        ],
        do_not=[
            "Do not disable SSR as the first fix",
            "Do not rewrite the component tree before locating the mismatched markup",
        ],
        evidence_needed=[
            "Identify the component producing different server and client markup",
            "Capture the browser console hydration warning",
        ],
        minimal_fix_scope=[
            "The component producing mismatched markup",
            "The server-to-client data snapshot used by that component",
        ],
        validation_ladder=[
            "Reproduce the page in development",
            "Check browser console for the hydration warning",
            "Run the related smoke test if one exists",
        ],
        regression_guard=["Add or update a smoke test for the affected page or component"],
        match_terms=["Hydration failed", "Date.now", "Math.random", "server rendered HTML"],
    ),
    RecipeTemplate(
        source_id="react-invalid-hook-call",
        failure_label="invalid hook call",
        recipe_id="react-invalid-hook-call",
        failure_class="react/hooks",
        symptoms=[
            "Invalid hook call: Hooks can only be called inside the body of a function component"
        ],
        fingerprints=[
            "Invalid hook call",
            "Hooks can only be called inside the body of a function component",
            "mismatching versions of React and React DOM",
            "more than one copy of React",
        ],
        first_checks=[
            "Check whether every Hook is called at the top level of a function component or custom Hook",
            "Check that react and react-dom resolve to matching versions",
            "Check whether the app bundles more than one copy of React",
        ],
        do_not=[
            "Do not call Hooks inside loops, conditions, nested functions, or event handlers",
            "Do not silence the warning before locating the invalid call site or duplicate React copy",
        ],
        evidence_needed=[
            "Identify the component or custom Hook where the invalid Hook call originates",
            "Capture dependency tree evidence for React and React DOM versions",
            "Check module resolution for duplicate React copies",
        ],
        minimal_fix_scope=[
            "The invalid Hook call site or custom Hook boundary",
            "The package dependency or bundler resolution path that duplicates React",
        ],
        validation_ladder=[
            "Run the affected component path in development and confirm the warning is gone",
            "Run dependency inspection for react and react-dom",
            "Run the related component or smoke test",
        ],
        regression_guard=[
            "Add a component or dependency-resolution test for the invalid Hook call path"
        ],
        match_terms=[
            "invalid hook call",
            "Hooks can only be called inside the body",
            "mismatching versions of React and React DOM",
            "more than one copy of React",
        ],
    ),
    RecipeTemplate(
        source_id="react-use-effect-troubleshooting",
        failure_label="effect dependency rerun loop",
        recipe_id="react-effect-dependency-rerun-loop",
        failure_class="react/effect-lifecycle",
        symptoms=["Effect keeps re-running in an infinite cycle or runs twice on mount"],
        fingerprints=[
            "Effect keeps re-running in an infinite cycle",
            "Effect runs twice when the component mounts",
            "dependency is different on every re-render",
            "missing cleanup function",
        ],
        first_checks=[
            "Check whether the Effect updates state that changes one of its dependencies",
            "Check object and function dependencies that are recreated on every render",
            "Check whether Strict Mode is exposing missing cleanup logic",
        ],
        do_not=[
            "Do not remove dependencies from the array to hide the loop",
            "Do not disable Strict Mode before proving cleanup mirrors setup",
        ],
        evidence_needed=[
            "Identify which dependency changes between renders",
            "Capture the state update that causes the dependency to change",
            "Show whether cleanup runs correctly before the next setup",
        ],
        minimal_fix_scope=[
            "The Effect and the reactive values it depends on",
            "The state update, memoization, or cleanup logic tied to that Effect",
        ],
        validation_ladder=[
            "Log or inspect dependency identity across two renders",
            "Run the component in development Strict Mode",
            "Run the focused component or hook test",
        ],
        regression_guard=[
            "Add a hook/component test that proves the Effect does not loop and cleanup runs"
        ],
        match_terms=[
            "Effect keeps re-running in an infinite cycle",
            "Effect runs twice when the component mounts",
            "dependency is different on every re-render",
            "cleanup function",
        ],
    ),
    RecipeTemplate(
        source_id="react-preserving-resetting-state",
        failure_label="state reset by position or key",
        recipe_id="react-state-reset-by-position-or-key",
        failure_class="react/state-preservation",
        symptoms=["Component state is reset unexpectedly or preserved when it should reset"],
        fingerprints=[
            "state is reset unexpectedly",
            "state is isolated between components",
            "key forces subtree reset",
            "nested component definitions reset state",
        ],
        first_checks=[
            "Check whether the component is rendered at a different position in the tree",
            "Check whether a key change is intentionally or accidentally forcing a reset",
            "Check whether a component function is nested inside another component",
        ],
        do_not=[
            "Do not move state upward before confirming whether identity or key is the cause",
            "Do not define component functions inside render when state must be preserved",
        ],
        evidence_needed=[
            "Compare the component tree position before and after the reset",
            "Capture key values for the affected subtree",
            "Identify whether a nested component definition is recreated each render",
        ],
        minimal_fix_scope=[
            "The affected component identity, position, or key",
            "The parent render branch that changes subtree identity",
        ],
        validation_ladder=[
            "Reproduce the state reset with a minimal interaction",
            "Verify the component keeps or resets state according to the chosen identity",
            "Run the focused component test for the affected branch",
        ],
        regression_guard=[
            "Add a component interaction test for the preserve/reset behavior"
        ],
        match_terms=[
            "State is isolated between components",
            "force a subtree to reset its state",
            "different key",
            "nested component definitions",
        ],
    ),
    RecipeTemplate(
        source_id="next-dynamic-server-error",
        failure_label="next dynamic server usage",
        recipe_id="next-dynamic-server-usage",
        failure_class="nextjs/dynamic-rendering",
        symptoms=["DynamicServerError or Dynamic Server Usage is thrown during static generation"],
        fingerprints=[
            "DynamicServerError",
            "Dynamic Server Usage",
            "cookies or headers not bound to the same call stack",
            "static generation dynamic function",
        ],
        first_checks=[
            "Check whether cookies, headers, or another dynamic function is called outside its async context",
            "Check setTimeout, setInterval, or un-awaited promise boundaries around dynamic functions",
            "Check whether the route should be dynamic instead of statically generated",
        ],
        do_not=[
            "Do not catch and swallow DynamicServerError manually",
            "Do not move cookies or headers into delayed callbacks to satisfy static generation",
        ],
        evidence_needed=[
            "Identify the dynamic function call site",
            "Trace the async call stack between the route render and the dynamic function",
            "Decide whether the route is intended to be static or dynamic",
        ],
        minimal_fix_scope=[
            "The route, server component, or helper that reads dynamic request data",
            "The async boundary that loses request context",
        ],
        validation_ladder=[
            "Build or render the affected route locally",
            "Confirm the dynamic function is called in the same async context",
            "Run the route smoke or build test",
        ],
        regression_guard=[
            "Add a route-level test or build smoke that exercises the dynamic function path"
        ],
        match_terms=[
            "DynamicServerError",
            "Dynamic Server Usage",
            "cookies or headers",
            "static generation",
            "dynamic function",
        ],
    ),
    RecipeTemplate(
        source_id="next-invalid-dynamic-suspense",
        failure_label="next invalid dynamic suspense",
        recipe_id="next-invalid-dynamic-suspense",
        failure_class="nextjs/dynamic-import",
        symptoms=["Invalid usage of suspense option of next/dynamic"],
        fingerprints=[
            "invalid usage of suspense option",
            "suspense true with ssr false",
            "suspense true with loading",
            "next dynamic React lazy",
        ],
        first_checks=[
            "Check next/dynamic options for suspense: true with ssr: false",
            "Check next/dynamic options for suspense: true with loading",
            "Check whether React 18 or newer is required for the Suspense path",
        ],
        do_not=[
            "Do not combine suspense: true with ssr: false",
            "Do not provide loading when suspense: true uses the Suspense fallback",
        ],
        evidence_needed=[
            "Find the next/dynamic call and its options object",
            "Capture the nearest Suspense boundary and fallback",
            "Confirm the React version used by the app",
        ],
        minimal_fix_scope=[
            "The next/dynamic import options for the affected component",
            "The Suspense boundary or loading fallback around that component",
        ],
        validation_ladder=[
            "Render the affected route in development",
            "Confirm the invalid next/dynamic warning is gone",
            "Run the route or component smoke test",
        ],
        regression_guard=[
            "Add a route/component test for the dynamic import loading state"
        ],
        match_terms=[
            "Invalid Usage",
            "suspense",
            "ssr: false",
            "loading",
            "React.lazy",
        ],
    ),
    RecipeTemplate(
        source_id="vite-troubleshooting",
        failure_label="vite esm-only config require",
        recipe_id="vite-esm-only-config-require",
        failure_class="vite/config-module-format",
        symptoms=["Vite fails because an ESM-only package was loaded by require"],
        fingerprints=[
            "This package is ESM only",
            "ERR_REQUIRE_ESM",
            "tried to load by require",
            "vite config ESM",
        ],
        first_checks=[
            "Check whether vite.config.* or a plugin config is loaded as CommonJS",
            "Check whether the failing dependency is ESM-only",
            "Check whether the config file extension should be .mjs or .mts",
        ],
        do_not=[
            "Do not pin an old dependency version before confirming the config module format",
            "Do not rely on experimental require support as the primary fix",
        ],
        evidence_needed=[
            "Capture the ERR_REQUIRE_ESM stack and the dependency path",
            "Identify the Vite config filename and package type",
            "Confirm how the dependency is imported from config",
        ],
        minimal_fix_scope=[
            "The Vite config module format or import statement",
            "The plugin/dependency entry loaded from config",
        ],
        validation_ladder=[
            "Run the Vite command that originally failed",
            "Confirm the config loads under ESM",
            "Run the project build or dev-server smoke",
        ],
        regression_guard=["Add a config-load smoke test or CI build check"],
        match_terms=[
            "This package is ESM only",
            "ERR_REQUIRE_ESM",
            "tried to load by require",
            "vite.config",
            "config to ESM",
        ],
    ),
    RecipeTemplate(
        source_id="tanstack-query-important-defaults",
        failure_label="tanstack query aggressive defaults",
        recipe_id="tanstack-query-aggressive-defaults",
        failure_class="tanstack-query/cache-defaults",
        symptoms=["Queries refetch or retry unexpectedly because TanStack Query defaults are active"],
        fingerprints=[
            "query data is stale by default",
            "refetch on window focus",
            "refetch on mount",
            "retry failed queries three times",
        ],
        first_checks=[
            "Check staleTime before assuming cached data should stay fresh",
            "Check refetchOnMount, refetchOnWindowFocus, and refetchOnReconnect",
            "Check retry and retryDelay when failures appear multiple times",
        ],
        do_not=[
            "Do not disable all refetching globally before identifying the surprising default",
            "Do not treat repeated failed requests as duplicate component mounts until retry is checked",
        ],
        evidence_needed=[
            "Record the query key and its options",
            "Capture whether the trigger was mount, focus, reconnect, invalidation, or retry",
            "Compare global QueryClient defaults with per-query overrides",
        ],
        minimal_fix_scope=[
            "The QueryClient default options or one affected query option set",
            "The component path that owns the surprising refetch or retry behavior",
        ],
        validation_ladder=[
            "Reproduce the refetch/retry trigger with query devtools or logs",
            "Adjust the smallest relevant query option",
            "Run the component/query integration test",
        ],
        regression_guard=[
            "Add a query behavior test for staleTime, refetch trigger, or retry count"
        ],
        match_terms=[
            "cached data as stale",
            "refetchOnWindowFocus",
            "refetchOnMount",
            "retry",
            "3 times",
        ],
    ),
    RecipeTemplate(
        source_id="tanstack-query-invalidation",
        failure_label="tanstack query missing invalidation",
        recipe_id="tanstack-query-missing-invalidation",
        failure_class="tanstack-query/cache-invalidation",
        symptoms=["A mutation succeeds but related query data remains stale in the UI"],
        fingerprints=[
            "invalidateQueries",
            "mark queries as stale",
            "query key partial matching",
            "refetched in the background",
        ],
        first_checks=[
            "Check whether the mutation invalidates every affected query key",
            "Check partial query key matching versus exact query keys",
            "Check whether active queries are refetched after invalidation",
        ],
        do_not=[
            "Do not manually patch every cached list before checking invalidation coverage",
            "Do not invalidate a broad key without confirming the affected query key shape",
        ],
        evidence_needed=[
            "Capture the mutation success path and invalidation call",
            "List the affected query keys",
            "Show whether invalidated active queries refetch in the background",
        ],
        minimal_fix_scope=[
            "The mutation success handler or cache update path",
            "The query key factory or key matching options for affected data",
        ],
        validation_ladder=[
            "Run the mutation and inspect invalidated query keys",
            "Confirm the stale UI refetches or receives updated cache data",
            "Run the mutation/query integration test",
        ],
        regression_guard=[
            "Add a mutation test that asserts the related query is invalidated or refreshed"
        ],
        match_terms=[
            "invalidateQueries",
            "marked as stale",
            "partial query matching",
            "refetched in the background",
        ],
    ),
    RecipeTemplate(
        source_id="fastapi-handling-errors",
        failure_label="fastapi httpexception custom handler",
        recipe_id="fastapi-httpexception-custom-handler",
        failure_class="fastapi/error-handling",
        symptoms=["FastAPI path operation raises HTTPException but client receives unexpected response format"],
        fingerprints=[
            "HTTPException",
            "raise HTTPException",
            "custom exception handler",
            "exception_handler",
            "detail",
        ],
        first_checks=[
            "Check the HTTPException status_code and detail parameter at the raise site",
            "Check whether a custom exception_handler overrides the default HTTPException or RequestValidationError handler",
            "Check whether headers are correctly passed via the headers parameter",
        ],
        do_not=[
            "Do not return an HTTPException as a value; it must be raised with raise",
            "Do not override RequestValidationError handler without re-raising or returning all validation errors",
        ],
        evidence_needed=[
            "Capture the HTTP response status and JSON detail returned to the client",
            "Identify whether a custom exception_handler intercepts or swallows the exception",
        ],
        minimal_fix_scope=[
            "The path operation function that raises the HTTPException",
            "The app-level exception_handler that transforms the exception to a response",
        ],
        validation_ladder=[
            "Reproduce the error endpoint with the failing request in development",
            "Inspect the HTTP response status and JSON body",
            "Run the endpoint smoke test or integration test",
        ],
        regression_guard=[
            "Add an endpoint test that asserts the correct HTTP status and detail body"
        ],
        match_terms=[
            "HTTPException",
            "raise HTTPException",
            "exception handler",
            "RequestValidationError",
            "override",
            "custom exception",
        ],
    ),
    RecipeTemplate(
        source_id="fastapi-middleware",
        failure_label="fastapi middleware call next",
        recipe_id="fastapi-middleware-call-next-order",
        failure_class="fastapi/middleware",
        symptoms=["FastAPI middleware fails silently or produces wrong response because call_next ordering is wrong"],
        fingerprints=[
            "call_next",
            "middleware",
            "process_time",
            "X-Process-Time",
            "middleware execution order",
        ],
        first_checks=[
            "Check whether call_next is awaited before or after the code that modifies the response",
            "Check whether the middleware modifies the request body before passing it to call_next",
            "Check middleware execution order when multiple middleware decorators are stacked",
        ],
        do_not=[
            "Do not skip calling call_next unless intentionally short-circuiting the request",
            "Do not access response.headers before await call_next(request) returns",
        ],
        evidence_needed=[
            "Capture the response headers to verify the custom header was added",
            "Check the timing of code before and after call_next",
        ],
        minimal_fix_scope=[
            "The middleware function and its call_next invocation",
            "The decorator ordering on the FastAPI app instance",
        ],
        validation_ladder=[
            "Reproduce the request that triggers the middleware in development",
            "Inspect the response headers and body",
            "Run the middleware integration test",
        ],
        regression_guard=[
            "Add a middleware test that asserts the custom header appears on every response"
        ],
        match_terms=[
            "call_next",
            "@app.middleware",
            "X-Process-Time",
            "add_process_time_header",
            "Starlette middleware",
        ],
    ),
    RecipeTemplate(
        source_id="fastapi-custom-response",
        failure_label="fastapi wrong response class",
        recipe_id="fastapi-wrong-response-class",
        failure_class="fastapi/response-format",
        symptoms=["FastAPI returns unexpected Content-Type or data format because wrong Response subclass is used"],
        fingerprints=[
            "HTMLResponse",
            "PlainTextResponse",
            "JSONResponse",
            "StreamingResponse",
            "FileResponse",
            "response_class",
        ],
        first_checks=[
            "Check the response_class parameter on the path operation decorator",
            "Check whether returning a Response subclass directly bypasses response_model serialization",
            "Check whether the correct Content-Type is expected by the consuming client",
        ],
        do_not=[
            "Do not return a JSONResponse directly when a response_model is declared unless you want to bypass Pydantic serialization",
            "Do not use StreamingResponse for data that fits in memory as a plain JSONResponse",
        ],
        evidence_needed=[
            "Capture the HTTP response Content-Type header",
            "Identify whether the response was returned directly or via response_class",
        ],
        minimal_fix_scope=[
            "The path operation decorator response_class parameter",
            "The return type annotation or direct Response subclass returned",
        ],
        validation_ladder=[
            "Inspect the response Content-Type header in development",
            "Verify the response body matches the documented schema",
            "Run the endpoint test for the affected route",
        ],
        regression_guard=[
            "Add an endpoint test that asserts Content-Type and response shape"
        ],
        match_terms=[
            "HTMLResponse",
            "PlainTextResponse",
            "JSONResponse",
            "StreamingResponse",
            "FileResponse",
            "response_class",
            "Response directly",
        ],
    ),
    RecipeTemplate(
        source_id="fastapi-events",
        failure_label="fastapi lifespan vs on event",
        recipe_id="fastapi-lifespan-vs-on-event",
        failure_class="fastapi/lifecycle",
        symptoms=["FastAPI app fails to initialize shared resources because startup/shutdown logic is missing or uses deprecated on_event"],
        fingerprints=[
            "lifespan",
            "startup",
            "shutdown",
            "on_event",
            "asynccontextmanager",
        ],
        first_checks=[
            "Check whether on_event('startup') or on_event('shutdown') is used instead of the recommended lifespan context manager",
            "Check whether the lifespan async function contains a yield separating setup from teardown code",
            "Check whether the FastAPI app is constructed with lifespan= passed as a parameter",
        ],
        do_not=[
            "Do not perform long-running blocking operations in on_event or lifespan without awaiting",
            "Do not share state via globals without considering concurrent workers",
        ],
        evidence_needed=[
            "Identify whether the startup code runs before the first request is served",
            "Capture app startup logs to verify resource initialization",
        ],
        minimal_fix_scope=[
            "The lifespan async context manager function",
            "The FastAPI app constructor lifespan parameter",
        ],
        validation_ladder=[
            "Start the app and verify shared resources are initialized before request handling",
            "Stop the app and verify teardown runs",
            "Run the app lifecycle or integration test",
        ],
        regression_guard=[
            "Add a lifecycle test that asserts setup code runs before and teardown after request handling"
        ],
        match_terms=[
            "lifespan",
            "on_event",
            "startup",
            "shutdown",
            "asynccontextmanager",
            "application starts",
            "before the application",
        ],
    ),
    RecipeTemplate(
        source_id="pydantic-validation-errors",
        failure_label="pydantic validation error type",
        recipe_id="pydantic-validation-error-type",
        failure_class="pydantic/validation",
        symptoms=["Pydantic raises ValidationError with an unexpected error type during model instantiation or validation"],
        fingerprints=[
            "ValidationError",
            "int_parsing",
            "bool_type",
            "missing",
            "greater_than",
            "validation error",
        ],
        first_checks=[
            "Check the error type field in exc.errors()[0]['type'] against the Pydantic validation error catalog",
            "Check the loc tuple to find which field path failed validation",
            "Check whether strict mode is enabled and affects the allowed input types",
        ],
        do_not=[
            "Do not catch ValidationError broadly without inspecting the individual error types",
            "Do not assume coercion will always succeed; check type constraints on Field definitions",
        ],
        evidence_needed=[
            "Capture exc.errors() to see all validation errors, their types, locs, and messages",
            "Identify the model field annotations and Field constraints that failed",
        ],
        minimal_fix_scope=[
            "The model field definition and type annotation",
            "The input data structure passed to model_validate or model instantiation",
        ],
        validation_ladder=[
            "Instantiate the model with failing data and inspect the ValidationError",
            "Verify the fix eliminates all errors of the same type",
            "Run the model unit test covering the affected field",
        ],
        regression_guard=[
            "Add a model test that asserts correct ValidationError.type for invalid input"
        ],
        match_terms=[
            "ValidationError",
            "int_parsing",
            "bool_type",
            "missing",
            "greater_than",
            "error type",
            "errors()",
        ],
    ),
    RecipeTemplate(
        source_id="pydantic-errors",
        failure_label="pydantic custom error messages",
        recipe_id="pydantic-custom-error-messages",
        failure_class="pydantic/error-messages",
        symptoms=["Pydantic ValidationError default messages are not suitable for the API response or client display"],
        fingerprints=[
            "customize error messages",
            "ErrorDetails",
            "error_count",
            "e.errors()",
            "ctx",
            "CUSTOM_MESSAGES",
        ],
        first_checks=[
            "Check whether the default error messages are acceptable before building a custom handler",
            "Check the error['type'] field for a match against a custom messages dictionary",
            "Check whether ctx fields are correctly substituted in custom messages",
        ],
        do_not=[
            "Do not mutate the original ValidationError object when building custom messages",
            "Do not forget to include the error['loc'] when transforming errors for API responses",
        ],
        evidence_needed=[
            "Capture the default e.errors() output before transforming",
            "Capture the custom messages dictionary and the transformed output",
        ],
        minimal_fix_scope=[
            "The custom error message mapping dictionary",
            "The error transformation function that maps ValidationError.errors() to the API response",
        ],
        validation_ladder=[
            "Trigger a validation failure and compare default vs custom error output",
            "Verify all error types present in the input are covered by the custom mapping",
            "Run the endpoint or model test that exercises the error path",
        ],
        regression_guard=[
            "Add a test that asserts custom error messages appear for the covered error types"
        ],
        match_terms=[
            "customize error messages",
            "CUSTOM_MESSAGES",
            "ErrorDetails",
            "error['type']",
            "convert_errors",
            "loc_to_dot_sep",
        ],
    ),
    RecipeTemplate(
        source_id="pydantic-usage-errors",
        failure_label="pydantic class not fully defined",
        recipe_id="pydantic-class-not-fully-defined",
        failure_class="pydantic/model-schema",
        symptoms=["PydanticUserError class-not-fully-defined raised when instantiating a model that references a forward or post-defined type"],
        fingerprints=[
            "class-not-fully-defined",
            "PydanticUserError",
            "model_rebuild",
            "ForwardRef",
            "decorator-missing-field",
        ],
        first_checks=[
            "Check whether the referenced type is defined before the model class is instantiated or validated",
            "Check whether model_rebuild() is called after the forward-referenced type is defined",
            "Check whether @field_validator field names match actual model fields",
        ],
        do_not=[
            "Do not define a BaseModel subclass with Optional['ForwardRef'] without calling model_rebuild() after the target is defined",
            "Do not suppress the class-not-fully-defined error; it means the schema is incomplete",
        ],
        evidence_needed=[
            "Capture the PydanticUserError.message and PydanticUserError.code",
            "Identify the ForwardRef or type annotation that is missing",
        ],
        minimal_fix_scope=[
            "The model class with the forward-referenced type",
            "The type definition order or model_rebuild() call site",
        ],
        validation_ladder=[
            "Instantiate the model after adding model_rebuild() and verify no PydanticUserError",
            "Verify nested model validation works with forward references",
            "Run the model unit test for the affected forward-reference path",
        ],
        regression_guard=[
            "Add a model test that validates forward-referenced nested models after model_rebuild()"
        ],
        match_terms=[
            "class-not-fully-defined",
            "PydanticUserError",
            "model_rebuild",
            "ForwardRef",
            "decorator-missing-field",
            "Optional",
        ],
    ),
    RecipeTemplate(
        source_id="langgraph-graph-recursion-limit",
        failure_label="langgraph graph recursion limit",
        recipe_id="langgraph-graph-recursion-limit",
        failure_class="langgraph/graph-execution",
        symptoms=[
            "LangGraph StateGraph raises GraphRecursionError because it reached the maximum number of steps before hitting a stop condition"
        ],
        fingerprints=[
            "GRAPH_RECURSION_LIMIT",
            "GraphRecursionError",
            "reached the maximum number of steps",
            "recursion_limit",
            "infinite loop",
        ],
        first_checks=[
            "Check whether the graph has an unintended cycle (infinite loop) by reviewing edges between nodes",
            "Check whether the default recursion_limit is too low for complex graphs that legitimately need many iterations",
            "Check whether the graph has a proper stop condition or terminal node",
        ],
        do_not=[
            "Do not blindly increase recursion_limit without first verifying there is no infinite loop",
            "Do not remove cycles by adding arbitrary stop nodes without understanding the intended graph behavior",
        ],
        evidence_needed=[
            "Capture the graph invocation config and the recursion_limit value",
            "Identify which nodes form the cycle or exceed the step limit",
        ],
        minimal_fix_scope=[
            "The graph edge definitions and conditional routing logic",
            "The config recursion_limit parameter passed to graph.invoke()",
        ],
        validation_ladder=[
            "Reproduce the GraphRecursionError in development with the failing graph invocation",
            "Inspect graph edges to confirm whether the cycle is intentional or a bug",
            "Run the graph unit test covering the affected execution path",
        ],
        regression_guard=[
            "Add a graph test that asserts the graph terminates within expected steps or raises GraphRecursionError when expected"
        ],
        match_terms=[
            "GRAPH_RECURSION_LIMIT",
            "recursion_limit",
            "maximum number of steps",
            "infinite loop",
            "StateGraph",
            "cycle",
        ],
    ),
    RecipeTemplate(
        source_id="langgraph-missing-checkpointer",
        failure_label="langgraph missing checkpointer",
        recipe_id="langgraph-missing-checkpointer",
        failure_class="langgraph/persistence",
        symptoms=[
            "LangGraph StateGraph raises an error because no checkpointer is configured for persistence-required features"
        ],
        fingerprints=[
            "MISSING_CHECKPOINTER",
            "checkpointer",
            "compile() without checkpointer",
            "InMemorySaver",
            "human-in-the-loop",
        ],
        first_checks=[
            "Check whether compile() was called with checkpointer= parameter",
            "Check whether human-in-the-loop, memory, or time-travel features require persistence",
            "Check whether @entrypoint decorator received a checkpointer argument",
        ],
        do_not=[
            "Do not use InMemorySaver in production; use PostgresSaver or another persistent checkpointer",
            "Do not skip checkpointer configuration if your graph uses interrupts, resume, or thread_id",
        ],
        evidence_needed=[
            "Identify whether the graph uses features that require persistence (human-in-the-loop, memory, time-travel)",
            "Capture the compile() call site to verify checkpointer parameter",
        ],
        minimal_fix_scope=[
            "The StateGraph.compile() call or @entrypoint decorator",
            "The checkpointer initialization (InMemorySaver, PostgresSaver, etc.)",
        ],
        validation_ladder=[
            "Instantiate the graph with a checkpointer and verify compile() succeeds",
            "Invoke the graph with a thread_id and confirm state is persisted",
            "Run the graph test covering the persistence-requiring feature",
        ],
        regression_guard=[
            "Add a graph test that asserts checkpointer is configured and state persists across invocations"
        ],
        match_terms=[
            "MISSING_CHECKPOINTER",
            "checkpointer",
            "InMemorySaver",
            "compile",
            "persistence",
            "human-in-the-loop",
        ],
    ),
    RecipeTemplate(
        source_id="langchain-output-parsing-failure",
        failure_label="langchain output parsing failure",
        recipe_id="langchain-output-parsing-failure",
        failure_class="langchain/output-parsing",
        symptoms=[
            "LangChain output parser raises OutputParserException because it was unable to handle model output"
        ],
        fingerprints=[
            "OUTPUT_PARSING_FAILURE",
            "OutputParserException",
            "output parser was unable to handle",
            "formatting instructions",
            "structured output",
        ],
        first_checks=[
            "Check whether the model output matches the expected format defined in the output parser",
            "Check whether formatting instructions in the prompt are specific enough for the model",
            "Check whether a more capable model would follow the formatting instructions reliably",
        ],
        do_not=[
            "Do not catch OutputParserException and return a default value without first improving the prompt",
            "Do not rely on output parsers when tool calling or structured_output techniques are available",
        ],
        evidence_needed=[
            "Capture the raw model output that failed to parse",
            "Capture the output parser's expected format or schema",
        ],
        minimal_fix_scope=[
            "The prompt formatting instructions",
            "The output parser class and its parsing logic",
        ],
        validation_ladder=[
            "Reproduce the parsing failure with the failing model output",
            "Improve the prompt formatting and verify the model produces parseable output",
            "Run the chain test covering the output parsing step",
        ],
        regression_guard=[
            "Add a chain test that asserts the output parser succeeds with representative model output"
        ],
        match_terms=[
            "OUTPUT_PARSING_FAILURE",
            "OutputParserException",
            "output parser",
            "formatting instructions",
            "structured output",
            "tool calling",
        ],
    ),
    RecipeTemplate(
        source_id="langgraph-invalid-concurrent-update",
        failure_label="langgraph invalid concurrent update",
        recipe_id="langgraph-invalid-concurrent-update",
        failure_class="langgraph/state-management",
        symptoms=[
            "LangGraph StateGraph raises InvalidUpdateError because multiple parallel nodes updated the same state key without a reducer"
        ],
        fingerprints=[
            "INVALID_CONCURRENT_GRAPH_UPDATE",
            "InvalidUpdateError",
            "concurrent updates",
            "reducer",
            "Annotated",
            "operator.add",
        ],
        first_checks=[
            "Check whether the state key being updated by multiple parallel nodes has a reducer function",
            "Check whether the state schema uses Annotated[list, operator.add] or similar reducer for list/accumulator keys",
            "Check whether the graph uses fanout or parallel execution that could trigger concurrent writes",
        ],
        do_not=[
            "Do not remove parallelism from the graph just to avoid concurrent update errors",
            "Do not use a reducer that silently overwrites values unless that is the intended behavior",
        ],
        evidence_needed=[
            "Identify which state keys are updated by multiple parallel nodes",
            "Capture the state schema definition and the reducer functions used",
        ],
        minimal_fix_scope=[
            "The state schema TypedDict or Pydantic model definition",
            "The reducer function annotations on state keys (e.g., Annotated[list, operator.add])",
        ],
        validation_ladder=[
            "Reproduce the InvalidUpdateError with a graph invocation that triggers parallel writes",
            "Add the appropriate reducer and verify the graph executes without error",
            "Run the graph test covering the parallel node execution path",
        ],
        regression_guard=[
            "Add a graph test that asserts parallel node execution succeeds and state is correctly merged"
        ],
        match_terms=[
            "INVALID_CONCURRENT_GRAPH_UPDATE",
            "InvalidUpdateError",
            "concurrent updates",
            "reducer",
            "Annotated",
            "operator.add",
            "fanout",
            "parallel",
        ],
    ),
    RecipeTemplate(
        source_id="react-native-troubleshooting",
        failure_label="react native metro port 8081 already in use",
        recipe_id="react-native-metro-port-8081",
        failure_class="react-native/metro-bundler",
        symptoms=[
            "Metro bundler fails to start because another process is already listening on port 8081"
        ],
        fingerprints=[
            "port 8081",
            "Port already in use",
            "Metro bundler",
            "lsof -i :8081",
        ],
        first_checks=[
            "Check whether another process is occupying port 8081 using sudo lsof -i :8081",
            "Check whether a stale Metro process is still running from a previous session",
            "Check whether you can start Metro on a different port to bypass the conflict",
        ],
        do_not=[
            "Do not reboot the machine as the first fix; terminating the occupying process is faster and safer",
            "Do not change the default port permanently without documenting the change for the team",
        ],
        evidence_needed=[
            "Capture the output of lsof -i :8081 showing the PID of the occupying process",
            "Confirm Metro actually fails on port binding, not another error",
        ],
        minimal_fix_scope=[
            "The Metro bundler process startup invocation",
            "The port configuration in the project's metro.config.js or start command",
        ],
        validation_ladder=[
            "Kill the occupying process and verify Metro starts on port 8081",
            "Verify the app connects to the Metro bundler and hot reloads",
            "Run the dev server smoke test",
        ],
        regression_guard=[
            "Add a CI pre-check script that reports stale Metro processes before builds"
        ],
        match_terms=[
            "port 8081",
            "Port already in use",
            "Metro bundler",
            "lsof",
            "npm start",
        ],
    ),
    RecipeTemplate(
        source_id="react-native-troubleshooting",
        failure_label="react native shell command unresponsive exception",
        recipe_id="react-native-shell-command-unresponsive",
        failure_class="react-native/android-build",
        symptoms=[
            "Android build fails with ShellCommandUnresponsiveException during task execution"
        ],
        fingerprints=[
            "ShellCommandUnresponsiveException",
            "Execution failed for task",
            ":app:installDebug",
            "DeviceException",
        ],
        first_checks=[
            "Check whether the ADB server is running and responsive with adb devices",
            "Check whether the ADB server needs to be restarted with adb kill-server && adb start-server",
            "Check the USB cable or emulator connection if running on a physical device",
        ],
        do_not=[
            "Do not reinstall the Android SDK before restarting the ADB server",
            "Do not increase Gradle timeout as a workaround without diagnosing the ADB unresponsiveness",
        ],
        evidence_needed=[
            "Capture the adb devices output to verify device connectivity",
            "Capture the full Gradle stack trace showing which task failed",
        ],
        minimal_fix_scope=[
            "The ADB server process",
            "The Gradle build execution environment",
        ],
        validation_ladder=[
            "Restart the ADB server and run adb devices to verify connectivity",
            "Re-attempt the Android build and verify it completes successfully",
            "Run the Android build smoke test",
        ],
        regression_guard=[
            "Add a pre-build script that restarts ADB if no devices are detected"
        ],
        match_terms=[
            "ShellCommandUnresponsiveException",
            "Execution failed for task",
            ":app:installDebug",
            "DeviceException",
            "adb kill-server",
        ],
    ),
    RecipeTemplate(
        source_id="expo-errors-and-warnings",
        failure_label="expo redbox stack trace diagnosis",
        recipe_id="expo-redbox-stack-trace",
        failure_class="expo/debugging",
        symptoms=[
            "A fatal error displays a Redbox with a stack trace that is unclear or the error location points to the wrong file"
        ],
        fingerprints=[
            "Redbox",
            "Yellowbox",
            "stack trace",
            "LogBox",
            "fatal error",
        ],
        first_checks=[
            "Check the stack trace for the file name and line number where the error occurred",
            "Check whether console.warn or console.error is the source of a Yellowbox warning versus an uncaught error",
            "Check whether a development build is showing the error or Expo Go is showing it, as stack traces differ",
        ],
        do_not=[
            "Do not ignore Yellowbox warnings; they indicate issues that may become Redbox errors after upgrade",
            "Do not suppress the error via error boundaries before identifying the root cause in the stack trace",
        ],
        evidence_needed=[
            "Capture the full stack trace from the Redbox or terminal output",
            "Identify the project file and line number mentioned in the trace",
        ],
        minimal_fix_scope=[
            "The file and line identified in the stack trace",
            "The component or function producing the fatal error",
        ],
        validation_ladder=[
            "Re-read the stack trace and navigate to the source location",
            "Fix the issue and verify the Redbox no longer appears on reload",
            "Run the component test or app smoke test",
        ],
        regression_guard=[
            "Add a component test for the error path that produced the Redbox"
        ],
        match_terms=[
            "Redbox",
            "Yellowbox",
            "stack trace",
            "fatal error",
            "HomeScreen.js",
        ],
    ),
    RecipeTemplate(
        source_id="kotlin-exceptions-language-doc",
        failure_label="kotlin null pointer java interop",
        recipe_id="kotlin-null-pointer-java-interop",
        failure_class="kotlin/null-safety",
        symptoms=[
            "Kotlin code receives NullPointerException when calling Java platform types without null checks"
        ],
        fingerprints=[
            "NullPointerException",
            "platform type",
            "Java interop",
            "!! operator",
            "null safety",
        ],
        first_checks=[
            "Check whether the value originates from a Java platform type (no nullability annotation)",
            "Check whether a non-null assertion operator !! is applied to a platform type value",
            "Check whether an explicit nullable type annotation (? suffix) is missing on the receiving side",
        ],
        do_not=[
            "Do not suppress NullPointerException with try-catch before adding null checks",
            "Do not assume Java platform types are non-null; always treat them as potentially nullable",
        ],
        evidence_needed=[
            "Identify the Java method or field that returns the platform type value",
            "Capture the stack trace showing NullPointerException at the Kotlin call site",
        ],
        minimal_fix_scope=[
            "The Kotlin receiver that consumes the Java platform type",
            "The null-safety annotation or safe call on the affected value",
        ],
        validation_ladder=[
            "Reproduce the NullPointerException with the failing input or call path",
            "Add a safe call (?.) or explicit null check and verify no exception",
            "Run the Kotlin/Java interop test for the affected call boundary",
        ],
        regression_guard=[
            "Add a test that exercises the Java interop boundary with null and non-null inputs"
        ],
        match_terms=[
            "NullPointerException",
            "platform type",
            "Java",
            "!!",
            "nullable",
            "interop",
        ],
    ),
    RecipeTemplate(
        source_id="kotlin-exceptions-language-doc",
        failure_label="kotlin require check precondition",
        recipe_id="kotlin-require-check-precondition",
        failure_class="kotlin/preconditions",
        symptoms=[
            "Kotlin require() throws IllegalArgumentException or check() throws IllegalStateException unexpectedly"
        ],
        fingerprints=[
            "require() throws",
            "IllegalArgumentException",
            "check() precondition",
            "IllegalStateException",
            "precondition",
        ],
        first_checks=[
            "Check whether require() is used for argument validation (IllegalArgumentException)",
            "Check whether check() is used for state validation (IllegalStateException)",
            "Check whether the lazyMessage lambda captures stale state when the condition evaluates late",
        ],
        do_not=[
            "Do not use require() for state checks; use check() instead",
            "Do not use check() for input validation; use require() instead",
        ],
        evidence_needed=[
            "Capture the exception message from require() or check() to identify the precondition",
            "Identify the call site where the precondition fails",
        ],
        minimal_fix_scope=[
            "The require() or check() call site and its condition expression",
            "The caller that passes the violating argument or reaches the invalid state",
        ],
        validation_ladder=[
            "Reproduce the IllegalArgumentException or IllegalStateException with the failing input",
            "Fix the caller input or state transition and verify no exception",
            "Run the unit test covering the precondition path",
        ],
        regression_guard=[
            "Add a test that asserts IllegalArgumentException from require() and IllegalStateException from check()"
        ],
        match_terms=[
            "require",
            "check",
            "IllegalArgumentException",
            "IllegalStateException",
            "precondition",
        ],
    ),
    RecipeTemplate(
        source_id="gradle-build-troubleshooting",
        failure_label="gradle java home invalid",
        recipe_id="gradle-java-home-invalid",
        failure_class="gradle/environment",
        symptoms=[
            "Gradle build fails with ERROR: JAVA_HOME is set to an invalid directory"
        ],
        fingerprints=[
            "JAVA_HOME is set to an invalid directory",
            "ERROR: JAVA_HOME",
            "please set JAVA_HOME",
            "Java Development Kit",
        ],
        first_checks=[
            "Check echo $JAVA_HOME to verify the directory exists",
            "Check whether JAVA_HOME points to the JDK root (not bin/ or jre/)",
            "Check whether the JDK version matches the Gradle project's required compatibility",
        ],
        do_not=[
            "Do not unset JAVA_HOME entirely; Gradle requires it to be set explicitly",
            "Do not point JAVA_HOME at a JRE if the project needs a full JDK",
        ],
        evidence_needed=[
            "Capture the JAVA_HOME environment variable value",
            "Capture the Gradle error message showing the invalid directory path",
        ],
        minimal_fix_scope=[
            "The JAVA_HOME environment variable configuration",
            "The shell profile or CI environment that sets JAVA_HOME",
        ],
        validation_ladder=[
            "Run echo $JAVA_HOME and verify the directory exists and contains bin/javac",
            "Run gradle --version and verify it reports the expected Java version",
            "Run the Gradle build smoke test",
        ],
        regression_guard=[
            "Add a CI check that validates JAVA_HOME before running Gradle builds"
        ],
        match_terms=[
            "JAVA_HOME",
            "invalid directory",
            "JDK",
            "JRE",
            "Java Development Kit",
        ],
    ),
    RecipeTemplate(
        source_id="gradle-build-troubleshooting",
        failure_label="gradle daemon connection failed",
        recipe_id="gradle-daemon-connection-failed",
        failure_class="gradle/daemon",
        symptoms=[
            "Gradle build fails because a new daemon was started but could not be connected to"
        ],
        fingerprints=[
            "A new daemon was started but could not be connected to",
            "Gradle Daemon",
            "could not reuse",
            "Starting a Gradle Daemon",
        ],
        first_checks=[
            "Check gradle --status to see existing daemon processes",
            "Check whether a firewall or NAT masquerade is blocking the daemon connection",
            "Check whether gradle.properties has org.gradle.jvmargs that conflict with available memory",
        ],
        do_not=[
            "Do not disable the daemon with --no-daemon as a permanent fix; diagnose the connection issue first",
            "Do not kill Gradle daemon processes without first checking whether another project is sharing them",
        ],
        evidence_needed=[
            "Capture the full Gradle daemon startup failure message",
            "Check gradle --status output for existing daemons",
        ],
        minimal_fix_scope=[
            "The Gradle daemon configuration in gradle.properties",
            "The system firewall or network settings blocking daemon connection",
        ],
        validation_ladder=[
            "Run gradle --stop and retry the build",
            "Verify gradle --status shows a healthy daemon process",
            "Run the Gradle build smoke test",
        ],
        regression_guard=[
            "Add a CI pre-build step that runs gradle --stop to clean stale daemons"
        ],
        match_terms=[
            "daemon",
            "could not be connected to",
            "Gradle Daemon",
            "gradle --status",
            "Starting a Gradle Daemon",
        ],
    ),
    RecipeTemplate(
        source_id="gradle-build-troubleshooting",
        failure_label="gradle dependency resolution conflict",
        recipe_id="gradle-dependency-resolution-conflict",
        failure_class="gradle/dependencies",
        symptoms=[
            "Gradle build fails because of conflicting transitive dependency versions that cannot be resolved"
        ],
        fingerprints=[
            "dependency resolution",
            "dependency conflict",
            "Could not resolve",
            "Conflict with dependency",
            "requested version",
        ],
        first_checks=[
            "Run gradle dependencies or the Dependencies view to see the full transitive tree",
            "Check whether a resolutionStrategy block forces a particular version",
            "Check whether the conflict is between implementation and test classpath variants",
        ],
        do_not=[
            "Do not add exclude rules globally; scope excludes to the minimum affected configuration",
            "Do not force a version without first understanding whether the forced version is API-compatible",
        ],
        evidence_needed=[
            "Capture the full dependency tree output showing the conflict",
            "Identify which module versions are incompatible and why",
        ],
        minimal_fix_scope=[
            "The build.gradle(.kts) dependency declaration or resolutionStrategy block",
            "The dependency configuration (implementation, api, testImplementation) with the conflict",
        ],
        validation_ladder=[
            "Run gradle dependencies and locate the conflicting transitive path",
            "Apply a resolutionStrategy or version pin that resolves the conflict",
            "Run the Gradle build and the affected module tests",
        ],
        regression_guard=[
            "Add a dependency-lock check or resolution strategy test to the build pipeline"
        ],
        match_terms=[
            "dependency resolution",
            "Conflict with",
            "Could not resolve",
            "requested version",
            "resolutionStrategy",
        ],
    ),
    RecipeTemplate(
        source_id="react-native-debugging",
        failure_label="react native logbox fatal error",
        recipe_id="react-native-logbox-fatal-errors",
        failure_class="react-native/debugging",
        symptoms=[
            "LogBox displays an undismissable fatal error because JavaScript cannot be executed due to a syntax or runtime error"
        ],
        fingerprints=[
            "LogBox",
            "fatal error",
            "JavaScript syntax error",
            "not dismissable",
            "Fast Refresh",
        ],
        first_checks=[
            "Check the LogBox error message for the file and line of the fatal syntax error",
            "Check whether Fast Refresh will automatically resolve the error after fixing the syntax",
            "Check whether the fatal error is coming from React Native DevTools console logs rather than app code",
        ],
        do_not=[
            "Do not use LogBox.ignoreAllLogs() to hide fatal errors; it is meant for suppressing warnings during demos",
            "Do not rely on LogBox as the sole debugging tool; open React Native DevTools Console for authoritative logs",
        ],
        evidence_needed=[
            "Capture the LogBox error message and stack trace",
            "Confirm whether React Native DevTools Console shows the same or more detail",
        ],
        minimal_fix_scope=[
            "The file and line identified by LogBox as the fatal error source",
            "The JavaScript module that fails to parse or execute",
        ],
        validation_ladder=[
            "Fix the syntax error shown in LogBox",
            "Verify the Redbox/LogBox automatically dismisses after Fast Refresh or manual reload",
            "Run the app smoke test to verify functionality",
        ],
        regression_guard=[
            "Add a build or lint check that catches the same class of syntax error before runtime"
        ],
        match_terms=[
            "LogBox",
            "fatal error",
            "syntax error",
            "Fast Refresh",
            "DevTools",
            "undismissable",
        ],
    ),
    RecipeTemplate(
        source_id="arkts-migration-guide",
        failure_label="arkts no var use let",
        recipe_id="arkts-no-var-use-let",
        failure_class="harmonyos/arkts-syntax",
        symptoms=[
            "ArkTS compiler error: arkts-no-var (10605005) — var keyword is not supported, use let instead"
        ],
        fingerprints=[
            "arkts-no-var",
            "10605005",
            "var keyword not supported",
            "ArkTS 不支持 var",
            "let 声明变量",
        ],
        first_checks=[
            "Check whether the variable declaration uses var instead of let or const",
            "Check whether the variable scope was intentionally block-scoped and convert to let",
            "Check whether the code is .ets or .ts file (var works in .ts but not .ets)",
        ],
        do_not=[
            "Do not use @ts-ignore to silence the ArkTS compiler for var usage",
            "Do not convert to const if the variable is reassigned later; use let",
        ],
        evidence_needed=[
            "Capture the compiler error message showing arkts-no-var with error code 10605005",
            "Identify the file and line where var is declared",
        ],
        minimal_fix_scope=[
            "The var declaration site",
            "The surrounding scope if the variable needs block-level scoping",
        ],
        validation_ladder=[
            "Replace var with let and verify the ArkTS compiler no longer reports 10605005",
            "Verify the variable still behaves correctly in its block scope",
            "Run the build or compile step for the affected module",
        ],
        regression_guard=[
            "Add a CI lint or type-check step that flags var usage in .ets files"
        ],
        match_terms=[
            "arkts-no-var",
            "10605005",
            "使用`let`而非`var`",
        ],
    ),
    RecipeTemplate(
        source_id="arkts-migration-guide",
        failure_label="arkts no any unknown type",
        recipe_id="arkts-no-any-unknown-type",
        failure_class="harmonyos/arkts-syntax",
        symptoms=[
            "ArkTS compiler error: arkts-no-any-unknown (10605008) — any and unknown types are not supported"
        ],
        fingerprints=[
            "arkts-no-any-unknown",
            "arkts-no-any",
            "10605008",
            "any type not supported",
            "unknown type not supported",
            "显式指定具体类型",
        ],
        first_checks=[
            "Check whether the variable or parameter is typed as any or unknown",
            "Check whether the function return type is any or unknown and replace with the actual return type",
            "Check whether an external library API returns any and the result needs to be typed with a class or interface",
        ],
        do_not=[
            "Do not replace any with Object if you need specific field access; define a class or interface",
            "Do not use ESObject as a drop-in replacement for any in .ets files without checking API version restrictions",
        ],
        evidence_needed=[
            "Capture the compiler error showing arkts-no-any-unknown with error code 10605008",
            "Identify the type declaration site where any or unknown is used",
        ],
        minimal_fix_scope=[
            "The variable, parameter, or return type annotation using any/unknown",
            "The class or interface definition that replaces the unknown type",
        ],
        validation_ladder=[
            "Replace any or unknown with a concrete type and verify no 10605008 error",
            "Verify the code still compiles and the runtime behavior is unchanged",
            "Run the module build or type-check step",
        ],
        regression_guard=[
            "Add a type-check step that flags any or unknown in .ets files"
        ],
        match_terms=[
            "arkts-no-any-unknown",
            "arkts-no-any",
            "10605008",
        ],
    ),
    RecipeTemplate(
        source_id="arkts-migration-guide",
        failure_label="arkts no untyped obj literals",
        recipe_id="arkts-no-untyped-obj-literals",
        failure_class="harmonyos/arkts-syntax",
        symptoms=[
            "ArkTS compiler error: arkts-no-untyped-obj-literals (10605038) — object literals require explicit type annotation"
        ],
        fingerprints=[
            "arkts-no-untyped-obj-literals",
            "10605038",
            "object literal type",
            "需要显式标注对象字面量的类型",
            "编译时错误",
        ],
        first_checks=[
            "Check whether an object literal is assigned to a variable without a type annotation",
            "Check whether an object literal is passed as a function argument without an explicit type interface",
            "Check whether the context type (variable annotation or parameter type) is sufficient to infer the literal type",
        ],
        do_not=[
            "Do not rely solely on contextual inference; add explicit type annotation when the context is ambiguous",
            "Do not convert object literals to class instances without checking whether an interface or class is more appropriate",
        ],
        evidence_needed=[
            "Capture the compiler error showing arkts-no-untyped-obj-literals with error code 10605038",
            "Identify the variable or parameter expecting the object literal",
        ],
        minimal_fix_scope=[
            "The object literal expression and its surrounding type context",
            "The interface or class definition used to annotate the literal type",
        ],
        validation_ladder=[
            "Add explicit type annotation to the object literal and verify no 10605038 error",
            "Verify the type annotation covers all fields in the object literal",
            "Run the build or compile step for the affected module",
        ],
        regression_guard=[
            "Add a type-check step that verifies all object literals have explicit or inferrable types"
        ],
        match_terms=[
            "arkts-no-untyped-obj-literals",
            "10605038",
            "需要显式标注对象字面量的类型",
        ],
    ),
    RecipeTemplate(
        source_id="arkts-migration-guide",
        failure_label="arkts no delete operator",
        recipe_id="arkts-no-delete-operator",
        failure_class="harmonyos/arkts-syntax",
        symptoms=[
            "ArkTS compiler error: arkts-no-delete (10605059) — delete operator is not supported"
        ],
        fingerprints=[
            "arkts-no-delete",
            "10605059",
            "delete operator",
            "delete 运算符",
            "不支持 delete",
        ],
        first_checks=[
            "Check whether the code uses the delete operator on an object property",
            "Check whether the intent is to remove a property from an object or delete an array element",
            "Check whether the target is a Map and Map.delete() should be used instead",
        ],
        do_not=[
            "Do not set the property to undefined or null as equivalent to deletion; ArkTS object layout is fixed at compile time",
            "Do not use Reflect.deleteProperty as an alternative; it is also restricted in ArkTS static mode",
        ],
        evidence_needed=[
            "Capture the compiler error showing arkts-no-delete with error code 10605059",
            "Identify the property and object that the delete operation targets",
        ],
        minimal_fix_scope=[
            "The delete expression site",
            "The data structure used to represent the object or collection",
        ],
        validation_ladder=[
            "Replace delete with an appropriate alternative (Map.delete(), array splice, or field reset) and verify no 10605059 error",
            "Verify the runtime behavior matches the original intent",
            "Run the build or compile step for the affected module",
        ],
        regression_guard=[
            "Add a type-check or lint step that flags delete operator usage in .ets files"
        ],
        match_terms=[
            "arkts-no-delete",
            "10605059",
            "不支持`delete`运算符",
        ],
    ),
    RecipeTemplate(
        source_id="arkts-migration-guide",
        failure_label="arkts no destructuring assignment",
        recipe_id="arkts-no-destruct-assignment",
        failure_class="harmonyos/arkts-syntax",
        symptoms=[
            "ArkTS compiler error: arkts-no-destruct-assignment (10605069) — destructuring assignment is not supported"
        ],
        fingerprints=[
            "arkts-no-destruct-assignment",
            "10605069",
            "destructuring assignment",
            "解构赋值",
            "不支持解构",
        ],
        first_checks=[
            "Check whether the code uses array or object destructuring in an assignment (left side is a pattern)",
            "Check whether destructuring is used for swapping variables or extracting nested fields",
            "Check whether the destructuring target is a function return value or an external data structure",
        ],
        do_not=[
            "Do not convert destructuring to indexed access ([a, b] = [x, y]) without ensuring the array is typed",
            "Do not use temporary variable assignment inside an expression to mimic destructuring; use separate statements",
        ],
        evidence_needed=[
            "Capture the compiler error showing arkts-no-destruct-assignment with error code 10605069",
            "Identify the destructuring pattern and the source value",
        ],
        minimal_fix_scope=[
            "The destructuring assignment expression",
            "The separate assignment statements used as replacement",
        ],
        validation_ladder=[
            "Replace destructuring with separate variable assignments and verify no 10605069 error",
            "Verify the replaced code produces identical values at runtime",
            "Run the build or compile step for the affected module",
        ],
        regression_guard=[
            "Add a type-check or lint step that flags destructuring patterns in .ets files"
        ],
        match_terms=[
            "arkts-no-destruct-assignment",
            "10605069",
            "不支持解构赋值",
        ],
    ),
    RecipeTemplate(
        source_id="arkts-migration-guide",
        failure_label="arkts no for in loop",
        recipe_id="arkts-no-for-in-loop",
        failure_class="harmonyos/arkts-syntax",
        symptoms=[
            "ArkTS compiler error: arkts-no-for-in (10605080) — for..in loop over object properties is not supported"
        ],
        fingerprints=[
            "arkts-no-for-in",
            "10605080",
            "for .. in",
            "for..in",
            "不支持 for..in",
        ],
        first_checks=[
            "Check whether the code uses a for..in loop to iterate over object keys",
            "Check whether the intent is to iterate over properties, array indices, or a Map's keys",
            "Check whether the object is typed and all its keys are known at compile time",
        ],
        do_not=[
            "Do not use Object.keys() as a drop-in replacement without verifying the object type is compatible",
            "Do not convert for..in to for..of on an untyped array; ensure the array is explicitly typed",
        ],
        evidence_needed=[
            "Capture the compiler error showing arkts-no-for-in with error code 10605080",
            "Identify the object being iterated and the properties accessed inside the loop",
        ],
        minimal_fix_scope=[
            "The for..in loop and its body",
            "The data structure iteration (convert to for..of on Object.keys or array iteration)",
        ],
        validation_ladder=[
            "Replace for..in with for..of on typed keys or array iteration and verify no 10605080 error",
            "Verify the iteration produces identical property access sequence",
            "Run the build or compile step for the affected module",
        ],
        regression_guard=[
            "Add a type-check or lint step that flags for..in loops in .ets files"
        ],
        match_terms=[
            "arkts-no-for-in",
            "10605080",
            "不支持`for .. in`",
        ],
    ),
    RecipeTemplate(
        source_id="arkts-migration-guide",
        failure_label="arkts no types in catch clause",
        recipe_id="arkts-no-types-in-catch",
        failure_class="harmonyos/arkts-syntax",
        symptoms=[
            "ArkTS compiler error: arkts-no-types-in-catch (10605079) — type annotation in catch clause is not supported"
        ],
        fingerprints=[
            "arkts-no-types-in-catch",
            "10605079",
            "catch type",
            "catch 语句中标注类型",
            "不支持 catch 类型标注",
        ],
        first_checks=[
            "Check whether a catch clause has a type annotation like catch(e: any) or catch(e: Error)",
            "Check whether the catch block uses e as a typed value without narrowing",
            "Check whether instanceof or as cast is used to narrow the caught value inside the block",
        ],
        do_not=[
            "Do not annotate the catch parameter with any type; omit the annotation entirely in ArkTS",
            "Do not assume the caught value is Error; always use instanceof Error before accessing .message",
        ],
        evidence_needed=[
            "Capture the compiler error showing arkts-no-types-in-catch with error code 10605079",
            "Identify the catch parameter and how it is used in the block",
        ],
        minimal_fix_scope=[
            "The catch clause parameter and its type annotation",
            "The catch block that needs instanceof narrowing",
        ],
        validation_ladder=[
            "Remove the type annotation from catch parameter and add instanceof narrowing inside the block; verify no 10605079 error",
            "Verify the error handling still works for all expected Error subtypes",
            "Run the build or compile step for the affected module",
        ],
        regression_guard=[
            "Add a type-check step that flags typed catch parameters in .ets files"
        ],
        match_terms=[
            "arkts-no-types-in-catch",
            "10605079",
            "不支持在catch语句标注类型",
        ],
    ),
    RecipeTemplate(
        source_id="arkts-migration-guide",
        failure_label="arkts no comma outside loops",
        recipe_id="arkts-no-comma-outside-loops",
        failure_class="harmonyos/arkts-syntax",
        symptoms=[
            "ArkTS compiler error: arkts-no-comma-outside-loops (10605071) — comma operator only allowed in for loop header"
        ],
        fingerprints=[
            "arkts-no-comma-outside-loops",
            "10605071",
            "comma operator",
            "逗号运算符",
            "逗号运算符仅适用于 for 循环",
        ],
        first_checks=[
            "Check whether the comma operator is used as an expression (value1, value2) not as a separator in declarations or function arguments",
            "Check whether the comma is inside a for loop header (allowed) vs. in a general expression (not allowed)",
            "Check whether the intended semantics is sequential expression evaluation or just a multi-value return",
        ],
        do_not=[
            "Do not use the comma operator to chain side effects in arbitrary expressions; use separate statements",
            "Do not confuse the comma expression operator with the comma used in variable declarations or function call arguments",
        ],
        evidence_needed=[
            "Capture the compiler error showing arkts-no-comma-outside-loops with error code 10605071",
            "Identify the comma expression site and its intended semantics",
        ],
        minimal_fix_scope=[
            "The comma expression site",
            "The surrounding statement or block where the sequential logic is split into separate statements",
        ],
        validation_ladder=[
            "Split the comma expression into separate statements or move to a for loop header; verify no 10605071 error",
            "Verify the sequential semantics is preserved after the refactor",
            "Run the build or compile step for the affected module",
        ],
        regression_guard=[
            "Add a type-check or lint step that flags comma expression usage outside for loops in .ets files"
        ],
        match_terms=[
            "arkts-no-comma-outside-loops",
            "10605071",
            "逗号运算符`,`仅用在`for`循环",
        ],
    ),
    RecipeTemplate(
        source_id="openharmony-stage-model-lifecycle",
        failure_label="arkts uiability lifecycle callback sequence error",
        recipe_id="arkts-uiability-lifecycle-callback-error",
        failure_class="harmonyos/ability-lifecycle",
        symptoms=[
            "UIAbility lifecycle callback invoked at unexpected time — onCreate, onWindowStageCreate, onForeground, onBackground, onDestroy sequence is violated"
        ],
        fingerprints=[
            "UIAbility lifecycle",
            "UIAbility onCreate",
            "UIAbility onWindowStageCreate",
            "UIAbility onForeground",
            "UIAbility onBackground",
            "UIAbility onDestroy",
            "UIAbility lifecycle onCreate",
            "UIAbility lifecycle onWindowStageCreate",
            "lifecycle callback sequence",
        ],
        first_checks=[
            "Check whether window operation code is placed in onWindowStageCreate (not onCreate), where WindowStage is not yet available",
            "Check whether global data initialization is placed in onCreate and per-window UI logic in onWindowStageCreate",
            "Check whether background-to-foreground transition logic is correctly placed in onForeground, not in onWindowStageCreate",
        ],
        do_not=[
            "Do not access WindowStage in onCreate; it is only available in onWindowStageCreate",
            "Do not perform long-running synchronous work in onWindowStageCreate; use async operations and await windowStage.loadContent",
        ],
        evidence_needed=[
            "Capture the lifecycle log sequence showing which callback fired and in what order",
            "Identify the code that depends on WindowStage or context availability",
        ],
        minimal_fix_scope=[
            "The lifecycle callback method where the misordered operation is placed",
            "The operation that depends on WindowStage or context readiness",
        ],
        validation_ladder=[
            "Move the operation to the correct lifecycle callback and verify no exception or null context",
            "Verify the lifecycle log sequence matches: onCreate → onWindowStageCreate → onForeground → onBackground → onDestroy",
            "Run the ability integration test covering the lifecycle transition",
        ],
        regression_guard=[
            "Add an ability lifecycle test asserting callback order and WindowStage availability"
        ],
        match_terms=[
            "UIAbility",
            "onCreate",
            "onWindowStageCreate",
            "onForeground",
            "onBackground",
            "lifecycle",
        ],
    ),
    RecipeTemplate(
        source_id="arkts-java-migration-guide",
        failure_label="arkts this binding context confusion",
        recipe_id="arkts-this-binding-context-confusion",
        failure_class="harmonyos/arkts-semantics",
        symptoms=[
            "ArkTS this reference points to wrong object because method passed as callback loses its context"
        ],
        fingerprints=[
            "this is undefined",
            "Cannot read properties of undefined",
            "this.bar",
            "callFunction(this.foo)",
            "ArkTS this 绑定",
        ],
        first_checks=[
            "Check whether the method is passed as a callback (callFunction(a.foo)) instead of called directly (a.foo())",
            "Check whether the method is used inside a closure or event handler where this is rebound",
            "Check whether bind(this) or an arrow function wrapper is needed to preserve context",
        ],
        do_not=[
            "Do not assume ArkTS this always points to the class instance like Java; ArkTS this is determined by the call site",
            "Do not pass class methods as naked callbacks without .bind() or arrow function wrapping",
        ],
        evidence_needed=[
            "Capture the stack trace showing this is undefined or points to wrong object",
            "Identify the call site where the method is passed as a callback versus called directly",
        ],
        minimal_fix_scope=[
            "The callback invocation site where this context is lost",
            "The method reference and its binding (bind or arrow wrapper)",
        ],
        validation_ladder=[
            "Reproduce the this binding failure with the failing call pattern",
            "Apply bind() or arrow function wrapper and verify correct this value",
            "Run the component or ability test covering the callback path",
        ],
        regression_guard=[
            "Add a test asserting the callback correctly accesses class instance properties via this"
        ],
        match_terms=[
            "this.bar",
            "this is undefined",
            "callFunction",
            "this binding",
            "bind(",
        ],
    ),
    RecipeTemplate(
        source_id="swift-error-handling-design",
        failure_label="swift throws missing try in throwing context",
        recipe_id="swift-throws-missing-try",
        failure_class="swift/error-handling",
        symptoms=[
            "Calling a throwing function without try keyword or outside do-catch block produces compile error"
        ],
        fingerprints=[
            "Call can throw",
            "try keyword required",
            "function can throw",
            "non-throwing context",
            "throws keyword",
        ],
        first_checks=[
            "Check whether the calling function is marked throws",
            "Check whether the call site wraps the throwing call in do { try ... } catch { ... }",
            "Check whether try? or try! is used where the error cannot be ignored",
        ],
        do_not=[
            "Do not use try! in production code unless the function's contract guarantees success",
            "Do not catch all errors broadly; match specific error types to avoid masking unrelated failures",
        ],
        evidence_needed=[
            "Capture the compile error message identifying the throwing function call site",
            "Identify whether the enclosing function is marked throws to propagate errors",
        ],
        minimal_fix_scope=[
            "The throwing function call site",
            "The enclosing do-catch block or the calling function's throws declaration",
        ],
        validation_ladder=[
            "Add try keyword and appropriate error handling; verify compile succeeds",
            "Test the code path with both success and failure inputs",
            "Run the unit test covering the throwing function boundary",
        ],
        regression_guard=[
            "Add a test that exercises both the throwing and success paths of the function call"
        ],
        match_terms=[
            "Call can throw",
            "try keyword",
            "throws",
            "non-throwing context",
            "do catch",
        ],
    ),
    RecipeTemplate(
        source_id="swift-existential-any-diagnostic",
        failure_label="swift any keyword required for existential types",
        recipe_id="swift-existential-any-required",
        failure_class="swift/type-system",
        symptoms=[
            "Swift 5.6+ compiler error: protocol used as a type requires any keyword before the protocol name"
        ],
        fingerprints=[
            "any",
            "existential type",
            "protocol used as a type",
            "ExistentialAny",
            "protocol as type",
        ],
        first_checks=[
            "Check whether a protocol name is used directly as a type (e.g. let x: MyProtocol) without any prefix",
            "Check whether the code targets Swift 5.6+ with ExistentialAny upcoming feature enabled",
            "Check whether a generic constraint uses protocol as type instead of where T: MyProtocol",
        ],
        do_not=[
            "Do not replace protocol existential with a struct wrapper without understanding the performance implications (existential boxes)",
            "Do not add any to generic type parameters; use <T: MyProtocol> constraint syntax instead",
        ],
        evidence_needed=[
            "Capture the compile error showing the protocol name used as a type",
            "Identify whether the type site is a variable declaration, parameter type, or return type",
        ],
        minimal_fix_scope=[
            "The protocol type annotation site needing any prefix",
            "Any generic constraint that uses the protocol as a type constraint",
        ],
        validation_ladder=[
            "Add any keyword before the protocol name and verify compile succeeds",
            "Verify runtime behavior is unchanged",
            "Run the module test covering the affected type signature",
        ],
        regression_guard=[
            "Add a compile-time test that verifies no bare protocol-as-type usage remains"
        ],
        match_terms=[
            "any",
            "existential",
            "protocol used as a type",
            "ExistentialAny",
        ],
    ),
    RecipeTemplate(
        source_id="swift-sendable-closure-captures",
        failure_label="swift sendable closure data race on captured var",
        recipe_id="swift-sendable-closure-race",
        failure_class="swift/concurrency",
        symptoms=[
            "Swift compiler error: reference to captured var in concurrently-executing code violates Sendable"
        ],
        fingerprints=[
            "reference to captured var",
            "concurrently-executing code",
            "non-Sendable type",
            "@Sendable closure",
            "data race",
        ],
        first_checks=[
            "Check whether the closure is annotated with @Sendable or passed to Task { ... } or async context",
            "Check whether a mutable var is captured by the concurrently-executing closure (data race risk)",
            "Check whether the captured type conforms to Sendable",
        ],
        do_not=[
            "Do not wrap the closure in Task { } without @Sendable; the compiler will still report the violation",
            "Do not use nonisolated(unsafe) to suppress the error without proving thread safety",
        ],
        evidence_needed=[
            "Capture the compile error identifying the captured var and the @Sendable closure",
            "Identify the concurrency context (Task, async let, async sequence, actor)",
        ],
        minimal_fix_scope=[
            "The captured variable and its mutability in the closure site",
            "The actor isolation or synchronization mechanism around the capture",
        ],
        validation_ladder=[
            "Convert the mutable var to let or add actor isolation; verify compile succeeds",
            "Verify no data race at runtime with concurrent access",
            "Run the concurrency test or TSAN check covering the affected code",
        ],
        regression_guard=[
            "Add a concurrency test asserting no data race with @Sendable closure captures"
        ],
        match_terms=[
            "reference to captured var",
            "concurrently-executing",
            "@Sendable",
            "data race",
            "Task",
        ],
    ),
    RecipeTemplate(
        source_id="swift-actor-isolated-call",
        failure_label="swift actor isolation violation on cross-context access",
        recipe_id="swift-actor-isolation-violation",
        failure_class="swift/concurrency",
        symptoms=[
            "Swift compiler error: actor-isolated property or method cannot be accessed from a non-isolated or different isolation context"
        ],
        fingerprints=[
            "actor-isolated",
            "non-isolated context",
            "MainActor-isolated",
            "actor isolation violation",
            "cannot be referenced from",
        ],
        first_checks=[
            "Check whether the access is from a nonisolated function or a different actor",
            "Check whether the accessed member is marked @MainActor or belongs to an actor struct/class",
            "Check whether await is used at the call site to cross the isolation boundary",
        ],
        do_not=[
            "Do not mark the member nonisolated unless it truly requires no synchronization",
            "Do not bypass actor isolation by calling through global functions without proving thread safety",
        ],
        evidence_needed=[
            "Capture the compile error naming the actor-isolated member and the accessing context",
            "Identify the isolation domains of both the caller and the accessed member",
        ],
        minimal_fix_scope=[
            "The cross-isolation access site needing await",
            "The isolation annotation of the affected member or the calling context",
        ],
        validation_ladder=[
            "Add await at the call site or mark the caller with the matching actor; verify compile succeeds",
            "Verify the actor's invariants are preserved at runtime",
            "Run the concurrency test covering the cross-actor access",
        ],
        regression_guard=[
            "Add a compile-time test asserting the access requires await across isolation domains"
        ],
        match_terms=[
            "actor-isolated",
            "non-isolated",
            "MainActor",
            "actor isolation",
            "await",
        ],
    ),
    RecipeTemplate(
        source_id="swift-new-diagnostic-arch",
        failure_label="swift cannot convert value of type diagnostic",
        recipe_id="swift-cannot-convert-value-of-type",
        failure_class="swift/type-checking",
        symptoms=[
            "Swift compiler reports Cannot convert value of type X to expected type Y with unclear fix-it suggestion"
        ],
        fingerprints=[
            "Cannot convert value of type",
            "binary operator cannot be applied",
            "missing argument label",
            "type has no member",
            "cannot force unwrap",
        ],
        first_checks=[
            "Check whether the mismatch is due to optional vs non-optional type (Int? vs Int)",
            "Check whether the mismatch is due to protocol conformance missing (concrete type vs protocol existential)",
            "Check whether force unwrap (!) is applied to a value that is not optional",
        ],
        do_not=[
            "Do not add as! force cast without understanding why the types do not match",
            "Do not suppress the diagnostic with @_silgen_name or @objc without fixing the underlying type mismatch",
        ],
        evidence_needed=[
            "Capture the full compile error with the expected and actual types",
            "Identify the expression or argument site where the type mismatch occurs",
        ],
        minimal_fix_scope=[
            "The expression or call site producing the type mismatch",
            "The variable or parameter type annotation that constrains the expression",
        ],
        validation_ladder=[
            "Fix the type annotation, unwrap, or convert explicitly; verify compile succeeds",
            "Verify runtime behavior matches the corrected type",
            "Run the unit test covering the affected expression",
        ],
        regression_guard=[
            "Add a compile-time test asserting the corrected type at the expression boundary"
        ],
        match_terms=[
            "Cannot convert value of type",
            "binary operator cannot",
            "missing argument",
            "has no member",
            "force unwrap",
        ],
    ),
    RecipeTemplate(
        source_id="kotlin-coroutines-exception-handling",
        failure_label="kotlin coroutine uncaught exception via handler",
        recipe_id="kotlin-coroutine-uncaught-exception",
        failure_class="kotlin/coroutines",
        symptoms=[
            "Coroutine throws uncaught exception that crashes the process instead of being handled by parent scope"
        ],
        fingerprints=[
            "CoroutineExceptionHandler got uncaught exception",
            "CoroutineExceptionHandler",
            "SupervisorJob cancellation",
            "supervisorScope",
            "coroutineScope",
        ],
        first_checks=[
            "Check whether a CoroutineExceptionHandler is installed on the root CoroutineScope or Job",
            "Check whether the failing coroutine is inside a supervisorScope (child failure does not cancel parent) vs coroutineScope (child failure propagates)",
            "Check whether a CancellationException is being swallowed instead of re-thrown",
        ],
        do_not=[
            "Do not catch CancellationException and suppress it; always re-throw after logging",
            "Do not install CoroutineExceptionHandler on a child Job; it only works on the root",
        ],
        evidence_needed=[
            "Capture the process crash log showing CoroutineExceptionHandler got uncaught exception",
            "Identify whether the failure is in a child coroutine and how it propagates to the scope",
        ],
        minimal_fix_scope=[
            "The root CoroutineScope or the supervisorScope boundary where the failure should be contained",
            "The coroutine launch block that throws the uncaught exception",
        ],
        validation_ladder=[
            "Reproduce the uncaught exception with the failing coroutine input",
            "Add a SupervisorJob or supervisorScope and verify the exception is contained",
            "Run the coroutine test covering the failure path",
        ],
        regression_guard=[
            "Add a coroutine test asserting the exception is handled and does not cancel the parent scope"
        ],
        match_terms=[
            "CoroutineExceptionHandler",
            "uncaught exception",
            "supervisorScope",
            "coroutineScope",
            "SupervisorJob",
            "CancellationException",
        ],
    ),
    RecipeTemplate(
        source_id="kotlin-flow-exception-handling",
        failure_label="kotlin flow exception transparency violation",
        recipe_id="kotlin-flow-exception-transparency",
        failure_class="kotlin/flow",
        symptoms=[
            "Flow throws Flow exception transparency violation because an exception was emitted from an unexpected place"
        ],
        fingerprints=[
            "Flow exception transparency violation",
            "Flow invariant is violated",
            "emission happened in",
            "flowOn instead",
            "catch operator",
        ],
        first_checks=[
            "Check whether the exception originated inside the flow { } builder vs upstream operators",
            "Check whether catch only catches upstream exceptions (it does not catch downstream collect failures)",
            "Check whether flowOn was used instead of withContext to change the execution context",
        ],
        do_not=[
            "Do not use withContext inside a flow { } builder; use flowOn instead",
            "Do not catch exceptions in collect {} and expect the flow to continue; use catch operator before collect",
        ],
        evidence_needed=[
            "Capture the Flow exception transparency violation stack trace",
            "Identify which flow operator or collect site threw the exception",
        ],
        minimal_fix_scope=[
            "The flow { } builder block or the operator chain",
            "The catch operator placement relative to upstream and downstream failures",
        ],
        validation_ladder=[
            "Reproduce the exception with the failing flow emission",
            "Move the catch operator upstream and verify the exception is handled",
            "Run the flow test covering the failure path",
        ],
        regression_guard=[
            "Add a flow test asserting the catch operator handles the specific error type"
        ],
        match_terms=[
            "exception transparency violation",
            "Flow invariant is violated",
            "flowOn",
            "catch operator",
            "withContext",
        ],
    ),
    RecipeTemplate(
        source_id="kotlin-serialization-basic-errors",
        failure_label="kotlin serialization missing serializable annotation",
        recipe_id="kotlin-serialization-missing-serializable",
        failure_class="kotlin/serialization",
        symptoms=[
            "Kotlin serialization fails because Serializer for class is not found; the class is not marked @Serializable"
        ],
        fingerprints=[
            "Serializer for class",
            "is not found",
            "marked as @Serializable",
            "MissingFieldException",
            "JsonDecodingException",
        ],
        first_checks=[
            "Check whether the class is annotated with @Serializable",
            "Check whether the kotlinx.serialization compiler plugin is applied in the build",
            "Check whether all non-nullable fields have values in the JSON input",
        ],
        do_not=[
            "Do not pass a class without @Serializable to Json.encodeToString or decodeFromString",
            "Do not make nullable fields non-nullable to fix MissingFieldException; handle the missing value explicitly",
        ],
        evidence_needed=[
            "Capture the compile or runtime error showing the class name that is missing @Serializable",
            "Identify the JSON input that triggers the decode failure",
        ],
        minimal_fix_scope=[
            "The class definition needing @Serializable annotation",
            "The build.gradle(.kts) serialization plugin configuration",
        ],
        validation_ladder=[
            "Add @Serializable annotation and verify compile succeeds",
            "Decode a sample JSON input and verify all fields are correctly populated",
            "Run the serialization unit test for the affected class",
        ],
        regression_guard=[
            "Add a serialization test asserting round-trip encode/decode for the affected class"
        ],
        match_terms=[
            "Serializer for class",
            "@Serializable",
            "MissingFieldException",
            "JsonDecodingException",
            "Unknown key",
        ],
    ),
    RecipeTemplate(
        source_id="openharmony-stage-model-lifecycle",
        failure_label="arkts uiability context null or invalid",
        recipe_id="arkts-uiability-context-not-ready",
        failure_class="harmonyos/ability-lifecycle",
        symptoms=[
            "Accessing UIAbilityContext returns null or throws because context is accessed before onCreate initializes it"
        ],
        fingerprints=[
            "UIAbilityContext",
            "Context is null",
            "context not ready",
            "getContext",
            "context 为空",
        ],
        first_checks=[
            "Check whether context is accessed in a member initializer, constructor, or static field before onCreate",
            "Check whether getContext() is called on a component that has not yet been attached to an AbilityStage",
            "Check whether the context is passed through a closure that captures a stale null reference",
        ],
        do_not=[
            "Do not cache UIAbilityContext in a module-level variable before onCreate completes",
            "Do not pass context to child components via property assignment before the context is initialized in onCreate",
        ],
        evidence_needed=[
            "Capture the stack trace showing context is null at the call site",
            "Identify the lifecycle stage when the null context is accessed",
        ],
        minimal_fix_scope=[
            "The context access site and the lifecycle callback it is in",
            "The state initialization order in the UIAbility subclass",
        ],
        validation_ladder=[
            "Move context access to onCreate or a later callback and verify no null reference",
            "Verify child components receive context only after it is initialized",
            "Run the ability lifecycle test covering context availability",
        ],
        regression_guard=[
            "Add an ability test asserting context is non-null from onCreate onwards"
        ],
        match_terms=[
            "UIAbilityContext",
            "context",
            "null",
            "getContext",
            "onCreate",
        ],
    ),
)


TEMPLATES_BY_LABEL = {template.failure_label: template for template in RECIPE_TEMPLATES}
_templates_by_source: dict[str, list[RecipeTemplate]] = {}
for _t in RECIPE_TEMPLATES:
    _templates_by_source.setdefault(_t.source_id, []).append(_t)
TEMPLATES_BY_SOURCE: dict[str, list[RecipeTemplate]] = _templates_by_source
