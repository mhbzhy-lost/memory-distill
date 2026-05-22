- [tanstack-query-invalidation-1] Waiting for queries to become stale before they are fetched again doesn't always work, especially when you know for a fact that a query's data is out of date because of something the user has done. For that purpose, the QueryClient has an invalidateQueries method that lets you intelligently mark queries as stale and potentially refetch them too!

- [tanstack-query-invalidation-2] // Invalidate every query in the cache queryClient. invalidateQueries () // Invalidate every query with a key that starts with `todos` queryClient. invalidateQueries ({ queryKey: [ 'todos' ] })

- [tanstack-query-invalidation-3] // Invalidate every query in the cache queryClient . invalidateQueries () // Invalidate every query with a key that starts with `todos` queryClient . invalidateQueries ( { queryKey : [ ' todos ' ] } )

- [tanstack-query-invalidation-4] Note: Where other libraries that use normalized caches would attempt to update local queries with the new data either imperatively or via schema inference, TanStack Query gives you the tools to avoid the manual labor that comes with maintaining normalized caches and instead prescribes targeted invalidation, background-refetching and ultimately atomic updates .

- [tanstack-query-invalidation-5] When a query is invalidated with invalidateQueries , two things happen:

- [tanstack-query-invalidation-6] It is marked as stale. This stale state overrides any staleTime configurations being used in useQuery or related hooks

- [tanstack-query-invalidation-7] If the query is currently being rendered via useQuery or related hooks, it will also be refetched in the background

- [tanstack-query-invalidation-8] Query Matching with invalidateQueries

- [tanstack-query-invalidation-9] When using APIs like invalidateQueries and removeQueries (and others that support partial query matching), you can match multiple queries by their prefix, or get really specific and match an exact query. For information on the types of filters you can use, please see Query Filters .

- [tanstack-query-invalidation-10] In this example, we can use the todos prefix to invalidate any queries that start with todos in their query key:

- [tanstack-query-invalidation-11] import { useQuery, useQueryClient } from '@tanstack/react-query' // Get QueryClient from the context const queryClient = useQueryClient () queryClient. invalidateQueries ({ queryKey: [ 'todos' ] }) // Both queries below will be invalidated const todoListQuery = useQuery ({ queryKey: [ 'todos' ], queryFn: fetchTodoList, }) const todoListQuery = useQuery ({ queryKey: [ 'todos' , { page: 1 }], queryFn: fetchTodoList, })

- [tanstack-query-invalidation-12] import { useQuery , useQueryClient } from ' @tanstack/react-query ' // Get QueryClient from the context const queryClient = useQueryClient () queryClient . invalidateQueries ( { queryKey : [ ' todos ' ] } ) // Both queries below will be invalidated const todoListQuery = useQuery ( { queryKey : [ ' todos ' ] , queryFn : fetchTodoList , } ) const todoListQuery = useQuery ( { queryKey : [ ' todos ' , { page : 1 } ] , queryFn : fetchTodoList , } )

- [tanstack-query-invalidation-13] You can even invalidate queries with specific variables by passing a more specific query key to the invalidateQueries method:

- [tanstack-query-invalidation-14] queryClient. invalidateQueries ({ queryKey: [ 'todos' , { type: 'done' }], }) // The query below will be invalidated const todoListQuery = useQuery ({ queryKey: [ 'todos' , { type: 'done' }], queryFn: fetchTodoList, }) // However, the following query below will NOT be invalidated const todoListQuery = useQuery ({ queryKey: [ 'todos' ], queryFn: fetchTodoList, })

- [tanstack-query-invalidation-15] queryClient . invalidateQueries ( { queryKey : [ ' todos ' , { type : ' done ' } ] , } ) // The query below will be invalidated const todoListQuery = useQuery ( { queryKey : [ ' todos ' , { type : ' done ' } ] , queryFn : fetchTodoList , } ) // However, the following query below will NOT be invalidated const todoListQuery = useQuery ( { queryKey : [ ' todos ' ] , queryFn : fetchTodoList , } )

- [tanstack-query-invalidation-16] The invalidateQueries API is very flexible, so even if you want to only invalidate todos queries that don't have any more variables or subkeys, you can pass an exact: true option to the invalidateQueries method:

- [tanstack-query-invalidation-17] queryClient. invalidateQueries ({ queryKey: [ 'todos' ], exact: true , }) // The query below will be invalidated const todoListQuery = useQuery ({ queryKey: [ 'todos' ], queryFn: fetchTodoList, }) // However, the following query below will NOT be invalidated const todoListQuery = useQuery ({ queryKey: [ 'todos' , { type: 'done' }], queryFn: fetchTodoList, })

- [tanstack-query-invalidation-18] queryClient . invalidateQueries ( { queryKey : [ ' todos ' ] , exact : true , } ) // The query below will be invalidated const todoListQuery = useQuery ( { queryKey : [ ' todos ' ] , queryFn : fetchTodoList , } ) // However, the following query below will NOT be invalidated const todoListQuery = useQuery ( { queryKey : [ ' todos ' , { type : ' done ' } ] , queryFn : fetchTodoList , } )

- [tanstack-query-invalidation-19] If you find yourself wanting even more granularity, you can pass a predicate function to the invalidateQueries method. This function will receive each Query instance from the query cache and allow you to return true or false for whether you want to invalidate that query:

- [tanstack-query-invalidation-20] queryClient. invalidateQueries ({ predicate : ( query ) => query.queryKey[ 0 ] === 'todos' && query.queryKey[ 1 ]?.version >= 10 , }) // The query below will be invalidated const todoListQuery = useQuery ({ queryKey: [ 'todos' , { version: 20 }], queryFn: fetchTodoList, }) // The query below will be invalidated const todoListQuery = useQuery ({ queryKey: [ 'todos' , { version: 10 }], queryFn: fetchTodoList, }) // However, the following query below will NOT be invalidated const todoListQuery = useQuery ({ queryKey: [ 'todos' , { version: 5 }], queryFn: fetchTodoList, })

- [tanstack-query-invalidation-21] queryClient . invalidateQueries ( { predicate : ( query ) => query . queryKey [ 0 ] === ' todos ' && query . queryKey [ 1 ] ?. version >= 10 , } ) // The query below will be invalidated const todoListQuery = useQuery ( { queryKey : [ ' todos ' , { version : 20 } ] , queryFn : fetchTodoList , } ) // The query below will be invalidated const todoListQuery = useQuery ( { queryKey : [ ' todos ' , { version : 10 } ] , queryFn : fetchTodoList , } ) // However, the following query below will NOT be invalidated const todoListQuery = useQuery ( { queryKey : [ ' todos ' , { version : 5 } ] , queryFn : fetchTodoList , } )
