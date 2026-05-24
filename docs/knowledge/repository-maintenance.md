---
title: Repository Maintenance
kind: convention
status: active
applies_to:
  - git
  - github
last_verified: 2026-05-24
source: manual
---

# 仓库维护方式

本仓库为个人维护仓库。默认只在 `main` 分支上开发和提交，不需要为常规改动创建
独立分支或 PR；只有用户明确要求分支、PR 或隔离评审时才切分支并走 PR 流程。

远端仓库创建后，默认使用 GitHub public repo，并将 `origin` 指向该仓库。
