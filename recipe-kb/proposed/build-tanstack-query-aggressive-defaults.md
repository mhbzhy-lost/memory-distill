---
id: build-tanstack-query-aggressive-defaults
kind: build-recipe
status: proposed
stack:
- react
- tanstack-query
trigger:
  file_pattern: ''
  code_signals: []
  description: 代码可能触发 tanstack-query/cache-defaults 类故障（Queries refetch or retry unexpectedly
    because TanStack Query defaults are active）
correct_pattern: []
decision_context: []
constraints:
- Do not disable all refetching globally before identifying the surprising default
- Do not treat repeated failed requests as duplicate component mounts until retry
  is checked
do_not:
- Do not disable all refetching globally before identifying the surprising default
- Do not treat repeated failed requests as duplicate component mounts until retry
  is checked
defaults: []
validation:
- Reproduce the refetch/retry trigger with query devtools or logs
- Adjust the smallest relevant query option
- Run the component/query integration test
related_debug_recipes:
- tanstack-query-aggressive-defaults
evidence_refs:
- source_id: tanstack-query-important-defaults
  url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-important-defaults-2
  short_excerpt: Query instances via useQuery or useInfiniteQuery by default consider
    cached data as stale .
  quote_hash: sha256:aeb5a98a13d87a447ff574ad14e0babd2b1c4f9dd6e38ba1e14656b09d79b40f
- source_id: tanstack-query-important-defaults
  url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-important-defaults-8
  short_excerpt: '''static'' and Infinity both prevent staleness-based refetches,
    but ''static'' is stricter: queryClient.invalidateQueries() can invalidate a query
    with staleTime: Infinity , but has no effect on staleTime: ''static'' . refetchOnMount
    , refetchOnWindowFocus , and refetchOnReconnect set to "always" are also blocked
    by ''static'' . Use ''static'' for data that cannot change while the app is running:
    feature flags fetched at boot, user permissions loaded at login, static reference
    tables. Use Infinity when you still want manual invalidation to work.'
  quote_hash: sha256:9beb1478a3a0141820e6d33cd0a8506d44cf838dd2328dabe8f07568791c5c63
- source_id: tanstack-query-important-defaults
  url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-important-defaults-13
  short_excerpt: Setting staleTime is the recommended way to avoid excessive refetches,
    but you can also customize the points in time for refetches by setting options
    like refetchOnMount , refetchOnWindowFocus and refetchOnReconnect .
  quote_hash: sha256:28677021280ddcbf1babb39f1536374d9421f5bd2346457ca1743dd8e1bf6132
- source_id: tanstack-query-important-defaults
  url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-important-defaults-19
  short_excerpt: Queries that fail are silently retried 3 times, with exponential
    backoff delay before capturing and displaying an error to the UI. To change this,
    you can alter the default retry and retryDelay options for queries to something
    other than 3 and the default exponential backoff function.
  quote_hash: sha256:781ab13a687062cf5b9c18f98333cf40d1e64160fe18ec8e4dc1c9d5a34a38f9
- source_id: tanstack-query-important-defaults
  url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-important-defaults-20
  short_excerpt: Queries that fail are silently retried 3 times, with exponential
    backoff delay before capturing and displaying an error to the UI.
  quote_hash: sha256:a11833a35095cf37a91430d0ff8525bf8162eefbb465c7da1fa029c19ecd0062
- source_id: tanstack-query-important-defaults
  url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-important-defaults-21
  short_excerpt: To change this, you can alter the default retry and retryDelay options
    for queries to something other than 3 and the default exponential backoff function.
  quote_hash: sha256:8550f42c35fd1124ca5566a2e5c67ab7a952b13675997d92818f6b2907797d9a
review: []
maintenance:
  state: proposed
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# build-tanstack-query-aggressive-defaults

## Trigger
**代码可能触发 tanstack-query/cache-defaults 类故障（Queries refetch or retry unexpectedly because TanStack Query defaults are active）**

## Correct Pattern


## Constraints
- Do not disable all refetching globally before identifying the surprising default
- Do not treat repeated failed requests as duplicate component mounts until retry is checked

## Do Not
- Do not disable all refetching globally before identifying the surprising default
- Do not treat repeated failed requests as duplicate component mounts until retry is checked

## Validation
- Reproduce the refetch/retry trigger with query devtools or logs
- Adjust the smallest relevant query option
- Run the component/query integration test

## Related Debug Recipes
- tanstack-query-aggressive-defaults

## Reviewer Notes
