# 快照人审：fastapi-handling-errors

## 快照质量检查
- 来源 URL: https://fastapi.tiangolo.com/tutorial/handling-errors/
- 最终 URL: https://fastapi.tiangolo.com/tutorial/handling-errors/
- 来源类型: official_doc
- 采集时间: 2026-05-26T08:42:53.083772Z
- HTTP 状态: 200
- 内容哈希: sha256:dff1e84da0bc48101f4b0c82880c0a189f39f822761931bfd2e24d67c4d52dbd
- 技术栈: fastapi
- 抽取段落数: 92

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 92
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 4/4 条 expected_failure_hints

## 预期线索命中
- `HTTPException`
  - [fastapi-handling-errors-13] Use HTTPException ¶
  - [fastapi-handling-errors-14] To return HTTP responses with errors to the client you use HTTPException .
  - [fastapi-handling-errors-15] Import HTTPException ¶
- `RequestValidationError`
  - [fastapi-handling-errors-55] When a request contains invalid data, FastAPI internally raises a RequestValidationError .
  - [fastapi-handling-errors-57] To override it, import the RequestValidationError and use it with @app.exception_handler(RequestValidationError) to decorate the exception handler.
  - [fastapi-handling-errors-59] from fastapi import FastAPI , HTTPException from fastapi.exceptions import RequestValidationError from fastapi.responses import PlainTextResponse from starlette.exceptions import HTTPException as StarletteHTTPExceptio...
- `override default exception handlers`
  - [fastapi-handling-errors-50] Override the default exception handlers ¶
  - [fastapi-handling-errors-51] FastAPI has some default exception handlers.
  - [fastapi-handling-errors-53] You can override these exception handlers with your own.
- `custom exception handler`
  - [fastapi-handling-errors-37] Install custom exception handlers ¶
  - [fastapi-handling-errors-38] You can add custom exception handlers with the same exception utilities from Starlette .
  - [fastapi-handling-errors-41] You could add a custom exception handler with @app.exception_handler() :

## 段落样例
- [fastapi-handling-errors-1] Handling Errors ¶
- [fastapi-handling-errors-2] There are many situations in which you need to notify an error to a client that is using your API.
- [fastapi-handling-errors-3] This client could be a browser with a frontend, a code from someone else, an IoT device, etc.
- [fastapi-handling-errors-4] You could need to tell the client that:
- [fastapi-handling-errors-5] The client doesn't have enough privileges for that operation.
- [fastapi-handling-errors-6] The client doesn't have access to that resource.
- [fastapi-handling-errors-7] The item the client was trying to access doesn't exist.
- [fastapi-handling-errors-8] etc.

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
