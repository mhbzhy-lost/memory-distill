# Bug: build_agent_skill wrapper 在 uv offline 模式下因 lxml wheel 缺失失败

## 现象

`tests/test_build_agent_skill.py::test_generated_skill_wrapper_runs_against_bundled_kb` 一直失败。

```
AssertionError:
  × Failed to download `lxml==6.1.1`
  ╰─▶ Network connectivity is disabled, but the
      requested data wasn't found in the cache for:
      `https://files.pythonhosted.org/packages/.../lxml-6.1.1-cp314-cp314-macosx_10_15_universal2.whl`
  help: `lxml` (v6.1.1) was included because `recipe-importer` (v0.1.0)
        depends on `lxml`
```

测试流程：打包出一个 standalone skill 目录 → 在 tmp venv 里用 `UV_OFFLINE=1` 跑 `scripts/recipe-importer version` → wrapper 调用 `uv run --frozen --project <bundle_dir>` → 失败。

## 调用链

1. 测试：`subprocess.run([wrapper, "version"], env={UV_OFFLINE=1, UV_PROJECT_ENVIRONMENT=tmp_venv})`
2. wrapper（`scripts/build_agent_skill.py:101-120`）：
   ```bash
   exec uv run --frozen --project "${bundle_dir}" recipe-importer "$@"
   ```
3. `uv run` 决定解释器：无 `--python` 参数 → 扫描系统可用 Python
4. 系统最高可用：Python 3.14.4（`/opt/homebrew/bin/python3.14` 或 uv 安装）
5. uv 创建 `tmp_venv` 用 3.14.4，需要安装 `lxml==6.1.1`
6. 离线模式 + uv cache 仅有 cp313 wheel（项目 `.venv` 用 3.13.1 创建）
7. cp314 wheel 不在缓存 → 尝试下载 → `UV_OFFLINE=1` 阻止 → 失败

## 根因假设

1. **wrapper 没 pin Python 版本**（主因）
   - `uv run` 无 `--python` 时会选系统最高 Python，而最高 Python 是 3.14.4
   - uv.lock 是 3.13 环境下生成的，wheel 是 cp313
   - 3.14.x 不在 lockfile 的 Python 版本覆盖范围内
2. **缺少项目级 `.python-version` 文件**
   - repo root 没有 `.python-version`，uv 没有默认版本提示
   - 跨机器/跨环境行为变得不可预测
3. **pyproject.toml 的 `requires-python = ">=3.12"` 上限开放**
   - uv 看到 `>=3.12` 就接受 3.14.x
   - 但 lockfile 实际只对 3.12-3.13 有 wheel

## 验证方式

```bash
# 确认 cp314 lxml wheel 不在缓存
ls ~/.cache/uv/wheels-v*/lxml*cp314* 2>/dev/null || echo "no cp314 lxml"

# 确认项目 .venv 用的是 3.13
cat .venv/pyvenv.cfg | grep version

# 重现：手动让 wrapper 用系统 Python
uv run --frozen --project <bundle_dir> python -c "import sys; print(sys.version)"
```

## 根因确认

**wrapper 没 pin Python 版本 + missing `.python-version` file**。

uv 在没有 pin 的情况下选了系统最高 Python (3.14.4)，但 uv.lock 没有 cp314 的 wheel。离线模式无法补救。

## 影响范围

1. **Standalone skill 在其他机器上无法使用**
   - 用户机器默认 Python 可能也是 3.14+
   - wrapper 会失败，skill 不可用
2. **CI 环境**
   - CI 通常有系统 Python，wrapper 行为不可预测
3. **未来 Python 版本升级**
   - 每出一个新的 Python 版本，wrapper 在新机器上都会踩同一个坑
4. **其他使用 `uv run --frozen` 的打包场景**
   - 当前项目只有这一处，但未来如有类似打包逻辑会复现

## 修复方案

**方案：添加项目级 `.python-version` 文件 + packager 把它打包进 bundle**

理由：
- `.python-version` 是 uv 的标准约定（`uv run` 默认读它）
- 文件放 repo root，开发者环境一致
- packager 把它复制进 bundle，wrapper 无需改 shell 脚本
- 版本 pin 到 `3.13`（当前项目 .venv 实际使用的版本）

**不会引入新问题的原因：**
- `.python-version` 只影响 `uv run` 的 Python 选择，不改变任何 Python 代码行为
- 项目 `requires-python = ">=3.12"` 仍允许 3.13/3.14 作为"可运行版本"，但 uv 在 `.python-version` 存在时优先用它
- 开发者手动 `uv venv` 仍可选择 3.12 创建新环境，`.python-version` 只是默认值

**替代方案（放弃）：**
- wrapper 脚本加 `--python 3.13`：hard-code 在 shell，未来升级需改两处
- `pyproject.toml` 加 `<3.14` 上限：过严，限制项目未来支持范围

## 测试覆盖

- 现有测试 `test_generated_skill_wrapper_runs_against_bundled_kb` 覆盖修复后的主路径
- 不额外加新测试（bug 已覆盖）

## 修复路径

1. repo root 创建 `.python-version`，内容 `3.13`
2. `scripts/build_agent_skill.py` 的 `COPY_ENTRIES` 增加 `.python-version`
3. 更新 `is_excluded` 不把它过滤掉（当前逻辑无副作用）
4. 跑全量测试验证修复
5. 跑 `scripts/build_agent_skill.py` + wrapper 跑通 smoke test
