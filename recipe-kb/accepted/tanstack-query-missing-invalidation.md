---
id: tanstack-query-missing-invalidation
kind: debug-recipe
status: accepted
stack:
- react
- tanstack-query
failure_class: tanstack-query/cache-invalidation
symptoms:
- A mutation succeeds but related query data remains stale in the UI
fingerprints:
- invalidateQueries
- mark queries as stale
- query key partial matching
- refetched in the background
first_checks:
- Check whether the mutation invalidates every affected query key
- Check partial query key matching versus exact query keys
- Check whether active queries are refetched after invalidation
do_not:
- Do not manually patch every cached list before checking invalidation coverage
- Do not invalidate a broad key without confirming the affected query key shape
evidence_needed:
- Capture the mutation success path and invalidation call
- List the affected query keys
- Show whether invalidated active queries refetch in the background
minimal_fix_scope:
- The mutation success handler or cache update path
- The query key factory or key matching options for affected data
validation_ladder:
- Run the mutation and inspect invalidated query keys
- Confirm the stale UI refetches or receives updated cache data
- Run the mutation/query integration test
regression_guard:
- Add a mutation test that asserts the related query is invalidated or refreshed
evidence_refs:
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-1
  short_excerpt: Waiting for queries to become stale before they are fetched again
    doesn't always work, especially when you know for a fact that a query's data is
    out of date because of something the user has done. For that purpose, the QueryClient
    has an invalidateQueries method that lets you intelligently mark queries as stale
    and potentially refetch them too!
  quote_hash: sha256:8675a93a5953410fb45cea4512eef8d673acb0b7f60b8a838d131a3f7936bc8c
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-2
  short_excerpt: '// Invalidate every query in the cache queryClient. invalidateQueries
    () // Invalidate every query with a key that starts with `todos` queryClient.
    invalidateQueries ({ queryKey: [ ''todos'' ] })'
  quote_hash: sha256:28f0ceed74be758c624049104a30023a03107e5a6b9b5b26df6da712328f316c
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-3
  short_excerpt: '// Invalidate every query in the cache queryClient . invalidateQueries
    () // Invalidate every query with a key that starts with `todos` queryClient .
    invalidateQueries ( { queryKey : [ '' todos '' ] } )'
  quote_hash: sha256:736c3f294786ed0d12a7476cdcf21cbbe8c5dc32a437a4ec057d1fcbf96b7d08
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-5
  short_excerpt: 'When a query is invalidated with invalidateQueries , two things
    happen:'
  quote_hash: sha256:1070df3a778e51debbeed385d7bead616099089c60b5287a46f166f824d18b23
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-6
  short_excerpt: It is marked as stale. This stale state overrides any staleTime configurations
    being used in useQuery or related hooks
  quote_hash: sha256:fcb7bc532905bc245e79fa61740bc2262f75b7a1636593750d791fe479f029a1
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-7
  short_excerpt: If the query is currently being rendered via useQuery or related
    hooks, it will also be refetched in the background
  quote_hash: sha256:8d36b9be3de1b84d9978096ef80d5fae62a02b43af825d7e295dc4412392416e
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-8
  short_excerpt: Query Matching with invalidateQueries
  quote_hash: sha256:d349ef1bae55c71f8741e9010ffc2c285f492f22b3e3d8bd3036ff2bb6a20270
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-9
  short_excerpt: When using APIs like invalidateQueries and removeQueries (and others
    that support partial query matching), you can match multiple queries by their
    prefix, or get really specific and match an exact query. For information on the
    types of filters you can use, please see Query Filters .
  quote_hash: sha256:1f7d5c52e3c9bd6327d07f22db008380c90a58fb6c1772e74b79c6a5c900b916
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-11
  short_excerpt: 'import { useQuery, useQueryClient } from ''@tanstack/react-query''
    // Get QueryClient from the context const queryClient = useQueryClient () queryClient.
    invalidateQueries ({ queryKey: [ ''todos'' ] }) // Both queries below will be
    invalidated const todoListQuery = useQuery ({ queryKey: [ ''todos'' ], queryFn:
    fetchTodoList, }) const todoListQuery = useQuery ({ queryKey: [ ''todos'' , {
    page: 1 }], queryFn: fetchTodoList, })'
  quote_hash: sha256:cb8dbedce923ff37e1bbd411431464c95c5240f865c79b9edb0bf0452d9eb695
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-12
  short_excerpt: 'import { useQuery , useQueryClient } from '' @tanstack/react-query
    '' // Get QueryClient from the context const queryClient = useQueryClient () queryClient
    . invalidateQueries ( { queryKey : [ '' todos '' ] } ) // Both queries below will
    be invalidated const todoListQuery = useQuery ( { queryKey : [ '' todos '' ] ,
    queryFn : fetchTodoList , } ) const todoListQuery = useQuery ( { queryKey : [
    '' todos '' , { page : 1 } ] , queryFn : fetchTodoList , } )'
  quote_hash: sha256:c4d68af79870bd6d53e05f464cd6a519f83f7b0cc44c356e33ce8ed7eda02bff
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-13
  short_excerpt: 'You can even invalidate queries with specific variables by passing
    a more specific query key to the invalidateQueries method:'
  quote_hash: sha256:6aa925fd2cfd3a59f61ee1a8fa595fc22ea904637de1f80bdc83ab188550eedd
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-14
  short_excerpt: 'queryClient. invalidateQueries ({ queryKey: [ ''todos'' , { type:
    ''done'' }], }) // The query below will be invalidated const todoListQuery = useQuery
    ({ queryKey: [ ''todos'' , { type: ''done'' }], queryFn: fetchTodoList, }) //
    However, the following query below will NOT be invalidated const todoListQuery
    = useQuery ({ queryKey: [ ''todos'' ], queryFn: fetchTodoList, })'
  quote_hash: sha256:23364d84dadfc65f8df4bb6a25d29e76c26371f903a828c348d4eb3124478e5f
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-15
  short_excerpt: 'queryClient . invalidateQueries ( { queryKey : [ '' todos '' , {
    type : '' done '' } ] , } ) // The query below will be invalidated const todoListQuery
    = useQuery ( { queryKey : [ '' todos '' , { type : '' done '' } ] , queryFn :
    fetchTodoList , } ) // However, the following query below will NOT be invalidated
    const todoListQuery = useQuery ( { queryKey : [ '' todos '' ] , queryFn : fetchTodoList
    , } )'
  quote_hash: sha256:d6e61f1f0743ce5f9c243b79529b423bdb980faae8afb70dc743dd415ab6783e
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-16
  short_excerpt: 'The invalidateQueries API is very flexible, so even if you want
    to only invalidate todos queries that don''t have any more variables or subkeys,
    you can pass an exact: true option to the invalidateQueries method:'
  quote_hash: sha256:9994a381804643cb3e64b964754fe3fabaa0c60647bad4bbd5cd80bbc8f7425c
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-17
  short_excerpt: 'queryClient. invalidateQueries ({ queryKey: [ ''todos'' ], exact:
    true , }) // The query below will be invalidated const todoListQuery = useQuery
    ({ queryKey: [ ''todos'' ], queryFn: fetchTodoList, }) // However, the following
    query below will NOT be invalidated const todoListQuery = useQuery ({ queryKey:
    [ ''todos'' , { type: ''done'' }], queryFn: fetchTodoList, })'
  quote_hash: sha256:221a128aeab36563608d4de0ac69e4e914c1522918377d94a151ca71141692a8
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-18
  short_excerpt: 'queryClient . invalidateQueries ( { queryKey : [ '' todos '' ] ,
    exact : true , } ) // The query below will be invalidated const todoListQuery
    = useQuery ( { queryKey : [ '' todos '' ] , queryFn : fetchTodoList , } ) // However,
    the following query below will NOT be invalidated const todoListQuery = useQuery
    ( { queryKey : [ '' todos '' , { type : '' done '' } ] , queryFn : fetchTodoList
    , } )'
  quote_hash: sha256:e35066c6c01bea7b88a655407c3d397adfb4643484899cc66902713b1ecd9a8d
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-19
  short_excerpt: 'If you find yourself wanting even more granularity, you can pass
    a predicate function to the invalidateQueries method. This function will receive
    each Query instance from the query cache and allow you to return true or false
    for whether you want to invalidate that query:'
  quote_hash: sha256:b8d9cceed4eeb0d43db2421e88731f710a2af13ef3e7916eb3b7a9000d7e769b
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-20
  short_excerpt: 'queryClient. invalidateQueries ({ predicate : ( query ) => query.queryKey[
    0 ] === ''todos'' && query.queryKey[ 1 ]?.version >= 10 , }) // The query below
    will be invalidated const todoListQuery = useQuery ({ queryKey: [ ''todos'' ,
    { version: 20 }], queryFn: fetchTodoList, }) // The query below will be invalidated
    const todoListQuery = useQuery ({ queryKey: [ ''todos'' , { version: 10 }], queryFn:
    fetchTodoList, }) // However, the following query below will NOT be invalidated
    const todoListQuery = useQuery ({ queryKey: [ ''todos'' , { version: 5 }], queryFn:
    fetchTodoList, })'
  quote_hash: sha256:240250231946d745633eb83f1e4f78c3a076b9a2fb294750ac1710fa97d0dc17
- source_id: tanstack-query-invalidation
  url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  final_url: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: tanstack-query-invalidation-21
  short_excerpt: 'queryClient . invalidateQueries ( { predicate : ( query ) => query
    . queryKey [ 0 ] === '' todos '' && query . queryKey [ 1 ] ?. version >= 10 ,
    } ) // The query below will be invalidated const todoListQuery = useQuery ( {
    queryKey : [ '' todos '' , { version : 20 } ] , queryFn : fetchTodoList , } )
    // The query below will be invalidated const todoListQuery = useQuery ( { queryKey
    : [ '' todos '' , { version : 10 } ] , queryFn : fetchTodoList , } ) // However,
    the following query below will NOT be invalidated const todoListQuery = useQuery
    ( { queryKey : [ '' todos '' , { version : 5 } ] , queryFn : f'
  quote_hash: sha256:027214bcd5b6e22a0b8b4fae68c90bb9efb920a6dd3d195d333f778fba3d897c
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# tanstack-query-missing-invalidation

## Failure Class
tanstack-query/cache-invalidation

## Symptoms
- A mutation succeeds but related query data remains stale in the UI

## Fingerprints
- invalidateQueries
- mark queries as stale
- query key partial matching
- refetched in the background

## First Checks
- Check whether the mutation invalidates every affected query key
- Check partial query key matching versus exact query keys
- Check whether active queries are refetched after invalidation

## Do Not Patch Yet
- Do not manually patch every cached list before checking invalidation coverage
- Do not invalidate a broad key without confirming the affected query key shape

## Evidence Needed
- Capture the mutation success path and invalidation call
- List the affected query keys
- Show whether invalidated active queries refetch in the background

## Minimal Fix Scope
- The mutation success handler or cache update path
- The query key factory or key matching options for affected data

## Validation Ladder
- Run the mutation and inspect invalidated query keys
- Confirm the stale UI refetches or receives updated cache data
- Run the mutation/query integration test

## Regression Guard
- Add a mutation test that asserts the related query is invalidated or refreshed

## Reviewer Notes
