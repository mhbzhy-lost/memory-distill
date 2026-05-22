- [tanstack-query-important-defaults-1] Out of the box, TanStack Query is configured with aggressive but sane defaults. Sometimes these defaults can catch new users off guard or make learning/debugging difficult if they are unknown by the user. Keep them in mind as you continue to learn and use TanStack Query:

- [tanstack-query-important-defaults-2] Query instances via useQuery or useInfiniteQuery by default consider cached data as stale .

- [tanstack-query-important-defaults-3] To change this behavior, you can configure your queries both globally and per-query using the staleTime option. Specifying a longer staleTime means queries will not refetch their data as often

- [tanstack-query-important-defaults-4] A Query that has a staleTime set is considered fresh until that staleTime has elapsed. set staleTime to e.g. 2 * 60 * 1000 to make sure data is read from the cache, without triggering any kinds of refetches, for 2 minutes, or until the Query is invalidated manually . set staleTime to Infinity to never trigger a refetch until the Query is invalidated manually . set staleTime to 'static' to never trigger a refetch, even if the Query is invalidated manually .

- [tanstack-query-important-defaults-5] set staleTime to e.g. 2 * 60 * 1000 to make sure data is read from the cache, without triggering any kinds of refetches, for 2 minutes, or until the Query is invalidated manually .

- [tanstack-query-important-defaults-6] set staleTime to Infinity to never trigger a refetch until the Query is invalidated manually .

- [tanstack-query-important-defaults-7] set staleTime to 'static' to never trigger a refetch, even if the Query is invalidated manually .

- [tanstack-query-important-defaults-8] 'static' and Infinity both prevent staleness-based refetches, but 'static' is stricter: queryClient.invalidateQueries() can invalidate a query with staleTime: Infinity , but has no effect on staleTime: 'static' . refetchOnMount , refetchOnWindowFocus , and refetchOnReconnect set to "always" are also blocked by 'static' . Use 'static' for data that cannot change while the app is running: feature flags fetched at boot, user permissions loaded at login, static reference tables. Use Infinity when you still want manual invalidation to work.

- [tanstack-query-important-defaults-9] Stale queries are refetched automatically in the background when: New instances of the query mount The window is refocused The network is reconnected

- [tanstack-query-important-defaults-10] New instances of the query mount

- [tanstack-query-important-defaults-11] The window is refocused

- [tanstack-query-important-defaults-12] The network is reconnected

- [tanstack-query-important-defaults-13] Setting staleTime is the recommended way to avoid excessive refetches, but you can also customize the points in time for refetches by setting options like refetchOnMount , refetchOnWindowFocus and refetchOnReconnect .

- [tanstack-query-important-defaults-14] Queries can optionally be configured with a refetchInterval to trigger refetches periodically, which is independent of the staleTime setting. See Polling for details.

- [tanstack-query-important-defaults-15] Query results that have no more active instances of useQuery , useInfiniteQuery or query observers are labeled as "inactive" and remain in the cache in case they are used again at a later time.

- [tanstack-query-important-defaults-16] By default, "inactive" queries are garbage collected after 5 minutes . To change this, you can alter the default gcTime for queries to something other than 1000 * 60 * 5 milliseconds.

- [tanstack-query-important-defaults-17] By default, "inactive" queries are garbage collected after 5 minutes .

- [tanstack-query-important-defaults-18] To change this, you can alter the default gcTime for queries to something other than 1000 * 60 * 5 milliseconds.

- [tanstack-query-important-defaults-19] Queries that fail are silently retried 3 times, with exponential backoff delay before capturing and displaying an error to the UI. To change this, you can alter the default retry and retryDelay options for queries to something other than 3 and the default exponential backoff function.

- [tanstack-query-important-defaults-20] Queries that fail are silently retried 3 times, with exponential backoff delay before capturing and displaying an error to the UI.

- [tanstack-query-important-defaults-21] To change this, you can alter the default retry and retryDelay options for queries to something other than 3 and the default exponential backoff function.

- [tanstack-query-important-defaults-22] Query results by default are structurally shared to detect if data has actually changed and if not, the data reference remains unchanged to better help with value stabilization with regards to useMemo and useCallback. If this concept sounds foreign, then don't worry about it! 99.9% of the time you will not need to disable this and it makes your app more performant at zero cost to you.

- [tanstack-query-important-defaults-23] Structural sharing only works with JSON-compatible values, any other value types will always be considered as changed. If you are seeing performance issues because of large responses for example, you can disable this feature with the config.structuralSharing flag. If you are dealing with non-JSON compatible values in your query responses and still want to detect if data has changed or not, you can provide your own custom function as config.structuralSharing to compute a value from the old and new responses, retaining references as required.

- [tanstack-query-important-defaults-24] Further Reading

- [tanstack-query-important-defaults-25] Have a look at the following articles from our Community Resources for further explanations of the defaults:

- [tanstack-query-important-defaults-26] Practical React Query

- [tanstack-query-important-defaults-27] React Query as a State Manager

- [tanstack-query-important-defaults-28] Thinking in React Query
