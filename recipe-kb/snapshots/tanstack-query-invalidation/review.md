# 快照人审：tanstack-query-invalidation

## 快照质量检查
- 来源 URL: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
- 最终 URL: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
- 来源类型: official_doc
- 采集时间: 2026-05-21T09:50:51.121768Z
- HTTP 状态: 200
- 内容哈希: sha256:4b0949469f245e0174884a6dc04f81449bd93fce55062cc4941094c3bc587217
- 技术栈: react, tanstack-query
- 抽取段落数: 21

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 21
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 3/4 条 expected_failure_hints

## 预期线索命中
- `mutation succeeds but list still shows stale data`：未找到直接段落命中
- `invalidateQueries`
  - [tanstack-query-invalidation-1] Waiting for queries to become stale before they are fetched again doesn't always work, especially when you know for a fact that a query's data is out of date because of something the user has done. For that purpose, t...
  - [tanstack-query-invalidation-2] // Invalidate every query in the cache queryClient. invalidateQueries () // Invalidate every query with a key that starts with `todos` queryClient. invalidateQueries ({ queryKey: [ 'todos' ] })
  - [tanstack-query-invalidation-3] // Invalidate every query in the cache queryClient . invalidateQueries () // Invalidate every query with a key that starts with `todos` queryClient . invalidateQueries ( { queryKey : [ ' todos ' ] } )
- `mark queries as stale`
  - [tanstack-query-invalidation-1] Waiting for queries to become stale before they are fetched again doesn't always work, especially when you know for a fact that a query's data is out of date because of something the user has done. For that purpose, t...
- `query key partial matching`
  - [tanstack-query-invalidation-9] When using APIs like invalidateQueries and removeQueries (and others that support partial query matching), you can match multiple queries by their prefix, or get really specific and match an exact query. For informati...

## 段落样例
- [tanstack-query-invalidation-1] Waiting for queries to become stale before they are fetched again doesn't always work, especially when you know for a fact that a query's data is out of date because of something the user has done. For that purpose, t...
- [tanstack-query-invalidation-2] // Invalidate every query in the cache queryClient. invalidateQueries () // Invalidate every query with a key that starts with `todos` queryClient. invalidateQueries ({ queryKey: [ 'todos' ] })
- [tanstack-query-invalidation-3] // Invalidate every query in the cache queryClient . invalidateQueries () // Invalidate every query with a key that starts with `todos` queryClient . invalidateQueries ( { queryKey : [ ' todos ' ] } )
- [tanstack-query-invalidation-4] Note: Where other libraries that use normalized caches would attempt to update local queries with the new data either imperatively or via schema inference, TanStack Query gives you the tools to avoid the manual labor...
- [tanstack-query-invalidation-5] When a query is invalidated with invalidateQueries , two things happen:
- [tanstack-query-invalidation-6] It is marked as stale. This stale state overrides any staleTime configurations being used in useQuery or related hooks
- [tanstack-query-invalidation-7] If the query is currently being rendered via useQuery or related hooks, it will also be refetched in the background
- [tanstack-query-invalidation-8] Query Matching with invalidateQueries

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
