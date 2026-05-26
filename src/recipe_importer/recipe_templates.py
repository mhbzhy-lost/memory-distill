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
)


TEMPLATES_BY_LABEL = {template.failure_label: template for template in RECIPE_TEMPLATES}
TEMPLATES_BY_SOURCE = {template.source_id: template for template in RECIPE_TEMPLATES}
