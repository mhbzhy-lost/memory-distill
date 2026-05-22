# 快照人审：tanstack-query-important-defaults

## 快照质量检查
- 来源 URL: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
- 最终 URL: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults
- 来源类型: official_doc
- 采集时间: 2026-05-21T09:50:51.121768Z
- HTTP 状态: 200
- 内容哈希: sha256:1bbd5b7e2b29bfacbb0739210a05d0c2899bbe182d5ba503a55e697c7faed850
- 技术栈: react, tanstack-query
- 抽取段落数: 28

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 28
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 4/4 条 expected_failure_hints

## 预期线索命中
- `query data is stale by default`
  - [tanstack-query-important-defaults-2] Query instances via useQuery or useInfiniteQuery by default consider cached data as stale .
  - [tanstack-query-important-defaults-3] To change this behavior, you can configure your queries both globally and per-query using the staleTime option. Specifying a longer staleTime means queries will not refetch their data as often
  - [tanstack-query-important-defaults-4] A Query that has a staleTime set is considered fresh until that staleTime has elapsed. set staleTime to e.g. 2 * 60 * 1000 to make sure data is read from the cache, without triggering any kinds of refetches, for 2 min...
- `refetch on window focus`
  - [tanstack-query-important-defaults-8] 'static' and Infinity both prevent staleness-based refetches, but 'static' is stricter: queryClient.invalidateQueries() can invalidate a query with staleTime: Infinity , but has no effect on staleTime: 'static' . refe...
  - [tanstack-query-important-defaults-13] Setting staleTime is the recommended way to avoid excessive refetches, but you can also customize the points in time for refetches by setting options like refetchOnMount , refetchOnWindowFocus and refetchOnReconnect .
- `refetch on mount`
  - [tanstack-query-important-defaults-8] 'static' and Infinity both prevent staleness-based refetches, but 'static' is stricter: queryClient.invalidateQueries() can invalidate a query with staleTime: Infinity , but has no effect on staleTime: 'static' . refe...
  - [tanstack-query-important-defaults-13] Setting staleTime is the recommended way to avoid excessive refetches, but you can also customize the points in time for refetches by setting options like refetchOnMount , refetchOnWindowFocus and refetchOnReconnect .
- `retry failed queries three times`
  - [tanstack-query-important-defaults-19] Queries that fail are silently retried 3 times, with exponential backoff delay before capturing and displaying an error to the UI. To change this, you can alter the default retry and retryDelay options for queries to...

## 段落样例
- [tanstack-query-important-defaults-1] Out of the box, TanStack Query is configured with aggressive but sane defaults. Sometimes these defaults can catch new users off guard or make learning/debugging difficult if they are unknown by the user. Keep them in...
- [tanstack-query-important-defaults-2] Query instances via useQuery or useInfiniteQuery by default consider cached data as stale .
- [tanstack-query-important-defaults-3] To change this behavior, you can configure your queries both globally and per-query using the staleTime option. Specifying a longer staleTime means queries will not refetch their data as often
- [tanstack-query-important-defaults-4] A Query that has a staleTime set is considered fresh until that staleTime has elapsed. set staleTime to e.g. 2 * 60 * 1000 to make sure data is read from the cache, without triggering any kinds of refetches, for 2 min...
- [tanstack-query-important-defaults-5] set staleTime to e.g. 2 * 60 * 1000 to make sure data is read from the cache, without triggering any kinds of refetches, for 2 minutes, or until the Query is invalidated manually .
- [tanstack-query-important-defaults-6] set staleTime to Infinity to never trigger a refetch until the Query is invalidated manually .
- [tanstack-query-important-defaults-7] set staleTime to 'static' to never trigger a refetch, even if the Query is invalidated manually .
- [tanstack-query-important-defaults-8] 'static' and Infinity both prevent staleness-based refetches, but 'static' is stricter: queryClient.invalidateQueries() can invalidate a query with staleTime: Infinity , but has no effect on staleTime: 'static' . refe...

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
