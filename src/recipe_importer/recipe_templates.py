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
)


TEMPLATES_BY_LABEL = {template.failure_label: template for template in RECIPE_TEMPLATES}
TEMPLATES_BY_SOURCE = {template.source_id: template for template in RECIPE_TEMPLATES}
