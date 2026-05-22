# 快照人审：vite-troubleshooting

## 快照质量检查
- 来源 URL: https://vite.dev/guide/troubleshooting.html
- 最终 URL: https://vite.dev/guide/troubleshooting.html
- 来源类型: official_doc
- 采集时间: 2026-05-21T09:50:51.121768Z
- HTTP 状态: 200
- 内容哈希: sha256:90d899d3f6654b25ddc77423174e90106969487048f14f1bd613c76b03bb187f
- 技术栈: react, vite
- 抽取段落数: 149

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 149
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 4/4 条 expected_failure_hints

## 预期线索命中
- `This package is ESM only`
  - [vite-troubleshooting-11] This package is ESM only ​
  - [vite-troubleshooting-13] Failed to resolve "foo". This package is ESM only but it was tried to load by require .
- `ERR_REQUIRE_ESM`
  - [vite-troubleshooting-14] Error [ERR_REQUIRE_ESM]: require() of ES Module /path/to/dependency.js from /path/to/vite.config.js not supported. Instead change the require of index.js in /path/to/vite.config.js to a dynamic import() which is avail...
- `tried to load by require`
  - [vite-troubleshooting-13] Failed to resolve "foo". This package is ESM only but it was tried to load by require .
- `vite config ESM`
  - [vite-troubleshooting-14] Error [ERR_REQUIRE_ESM]: require() of ES Module /path/to/dependency.js from /path/to/vite.config.js not supported. Instead change the require of index.js in /path/to/vite.config.js to a dynamic import() which is avail...
  - [vite-troubleshooting-17] While it may work using --experimental-require-module , or Node.js >22, or in other runtimes, we still recommend converting your config to ESM by either:
  - [vite-troubleshooting-20] renaming vite.config.js / vite.config.ts to vite.config.mjs / vite.config.mts

## 段落样例
- [vite-troubleshooting-1] Troubleshooting ​
- [vite-troubleshooting-2] See Rollup's troubleshooting guide for more information too.
- [vite-troubleshooting-3] If the suggestions here don't work, please try posting questions on GitHub Discussions or in the #help channel of Vite Land Discord .
- [vite-troubleshooting-4] CLI ​
- [vite-troubleshooting-5] Error: Cannot find module 'C:\foo\bar&baz\vite\bin\vite.js' ​
- [vite-troubleshooting-6] The path to your project folder may include & , which doesn't work with npm on Windows ( npm/cmd-shim#45 ).
- [vite-troubleshooting-7] You will need to either:
- [vite-troubleshooting-8] Switch to another package manager (e.g. pnpm , yarn )

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
