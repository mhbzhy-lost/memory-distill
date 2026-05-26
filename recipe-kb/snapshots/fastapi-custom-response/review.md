# 快照人审：fastapi-custom-response

## 快照质量检查
- 来源 URL: https://fastapi.tiangolo.com/advanced/custom-response/
- 最终 URL: https://fastapi.tiangolo.com/advanced/custom-response/
- 来源类型: official_doc
- 采集时间: 2026-05-26T08:42:53.083772Z
- HTTP 状态: 200
- 内容哈希: sha256:d43495c964c96e15fdd16b754c22a3b126585bc42887a3f6eea7ad9537446a8c
- 技术栈: fastapi
- 抽取段落数: 121

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 121
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 5/5 条 expected_failure_hints

## 预期线索命中
- `HTMLResponse`
  - [fastapi-custom-response-19] To return a response with HTML directly from FastAPI , use HTMLResponse .
  - [fastapi-custom-response-20] Import HTMLResponse .
  - [fastapi-custom-response-21] Pass HTMLResponse as the parameter response_class of your path operation decorator .
- `PlainTextResponse`
  - [fastapi-custom-response-60] PlainTextResponse ¶
  - [fastapi-custom-response-62] from fastapi import FastAPI from fastapi.responses import PlainTextResponse app = FastAPI () @app . get ( "/" , response_class = PlainTextResponse ) async def main (): return "Hello World"
- `JSONResponse`
  - [fastapi-custom-response-4] But if you return a Response directly (or any subclass, like JSONResponse ), the data won't be automatically converted (even if you declare a response_model ), and the documentation won't be automatically generated (f...
  - [fastapi-custom-response-12] If you don't declare a response model, FastAPI will use the jsonable_encoder explained in JSON Compatible Encoder and put it in a JSONResponse .
  - [fastapi-custom-response-13] If you declare a response_class with a JSON media type ( application/json ), like is the case with the JSONResponse , the data you return will be automatically converted (and filtered) with any Pydantic response_model...
- `StreamingResponse`
  - [fastapi-custom-response-78] StreamingResponse ¶
  - [fastapi-custom-response-80] import anyio from fastapi import FastAPI from fastapi.responses import StreamingResponse app = FastAPI () async def fake_video_streamer (): for i in range ( 10 ): yield b "some fake video bytes" await anyio . sleep (...
  - [fastapi-custom-response-85] Instead of returning a StreamingResponse directly, you should probably follow the style in Stream Data , it's much more convenient and handles cancellation behind the scenes for you.
- `FileResponse`
  - [fastapi-custom-response-87] FileResponse ¶
  - [fastapi-custom-response-95] from fastapi import FastAPI from fastapi.responses import FileResponse some_file_path = "large-video-file.mp4" app = FastAPI () @app . get ( "/" ) async def main (): return FileResponse ( some_file_path )
  - [fastapi-custom-response-97] from fastapi import FastAPI from fastapi.responses import FileResponse some_file_path = "large-video-file.mp4" app = FastAPI () @app . get ( "/" , response_class = FileResponse ) async def main (): return some_file_path

## 段落样例
- [fastapi-custom-response-1] Custom Response - HTML, Stream, File, others ¶
- [fastapi-custom-response-2] By default, FastAPI will return JSON responses.
- [fastapi-custom-response-3] You can override it by returning a Response directly as seen in Return a Response directly .
- [fastapi-custom-response-4] But if you return a Response directly (or any subclass, like JSONResponse ), the data won't be automatically converted (even if you declare a response_model ), and the documentation won't be automatically generated (f...
- [fastapi-custom-response-5] But you can also declare the Response that you want to be used (e.g. any Response subclass), in the path operation decorator using the response_class parameter.
- [fastapi-custom-response-6] The contents that you return from your path operation function will be put inside of that Response .
- [fastapi-custom-response-7] Note
- [fastapi-custom-response-8] If you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
