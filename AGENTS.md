# Memory Distill 工程规则

## Project Knowledge

开工 coding / 调试 / 计划 / review 前，除宿主 memory 外，也要检查任务是否触及
项目稳定知识。

- Knowledge guide: `docs/knowledge/README.md`
- Knowledge index: `docs/knowledge/INDEX.md`
- Importer workflow: `docs/knowledge/runbooks/debug-recipe-importer-workflow.md`

当变更影响架构、契约、工作流、测试策略、集成或长期坑点时，提交前同步更新
`docs/knowledge/`。

## 人审文本语言

人审的人类可读文本必须使用中文编写。适用范围包括 snapshot `review.md`、
review checklist、CLI 中面向审阅者的提示、以及打包交付的
`debug-recipe-importer` / memory-distill skill 说明文档中的审阅规则。

源证据摘录、代码标识、命令、schema 字段名和外部专有名词保持原文，避免翻译导致证据偏移。

## Bug 处理授权

后续发现 bug 时，必须先在 `docs/bugs/` 编写独立根因分析文档；文档完成后可直接按
TDD 流程修复，不需要再等待人工审批。修复仍需覆盖根因路径、运行影响范围验证和全量测试。
