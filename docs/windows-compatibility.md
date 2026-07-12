# Windows 兼容性 · 踩坑积累

> 本工具链（`setup-kb.py` / `eval.scaffold` / `eval.server`）按跨平台设计，但 **Windows 中文系统**有特定编码与路径坑。本文积累实测发现的问题、根因、修复模式，供后续开发与排错参考。
>
> 维护原则：**每在 Win 上踩一个坑，就补一条进来。**

## 根因：cp936 (GBK) 是 Windows 中文系统的默认编码

```python
>>> import locale; locale.getpreferredencoding()
'cp936'   # = GBK
```

Python 在 Win 中文系统上，`open()` / `Path.read_text()` / `print()` / `subprocess(text=True)` 默认编码都是 cp936。而本仓库所有文件（含中文 + emoji）都是 **UTF-8**。三者相撞就崩。它有**三个独立表现面**，治法各不同。

## 修复铁律（所有新代码都要遵守）

### 1. 读写文件**永远**显式指定 encoding
```python
Path(x).read_text(encoding="utf-8")          # ✓
json.loads(Path(x).read_text())              # ✗ 默认 cp936，Win 崩
open(f, encoding="utf-8")                    # ✓
```
> f-string 内的 `read_text` 用**单引号** `encoding='utf-8'`，避免与 f-string 外层双引号冲突（Python 3.11 不允许 f-string 嵌套同引号 → `SyntaxError`）。

### 2. 程序入口加 stdout/stderr reconfigure（治 print emoji）
```python
import sys
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
```
- 治 `print("✓ 成功")` / `print("⚠ 警告")` 在 GBK 终端的 `UnicodeEncodeError`
- mac/linux 本就 utf-8，零副作用

### 3. subprocess 捕获输出加 encoding（治子进程输出解码崩）
```python
subprocess.run(cmd, capture_output=True, text=True,
               encoding="utf-8", errors="replace")   # ✓
# ✗ 否则 _readerthread 用 cp936 解码子进程 UTF-8 输出 → UnicodeDecodeError
```
> 第 2 条治不了这个——subprocess 的解码用的是 `encoding=` 参数，不是 `sys.stdout`。两者独立。

**应急（零改码）**：启动加 `PYTHONUTF8=1`（开 Python UTF-8 模式，三招全覆盖）。但每次启动都得记得加，不持久——只用于临时验证或救急。

## 已发现 + 已修清单

### 2026-07-12 · scaffold / server 编码崩（commit `d041ade`）
| 文件 | 问题 | 修复 |
|---|---|---|
| `eval/scaffold.py:23,25` | `read_text()` 无 encoding → `import` 即 `UnicodeDecodeError` | 加 `encoding='utf-8'` |
| `eval/server.py` 5 处 | 同上，读 index.json / 归档报告 / gold md 崩 | 加 `encoding='utf-8'`（f-string 内单引号）|
| `eval/server.py:198-200` | `print("…就绪 ✓…⚠…")` emoji → `main()` 在 `serve_forever` 前崩，**server 起不来** | 文件头 stdout/stderr reconfigure |

**影响**：Win 中文系统上整条前端 + scaffold 链路不可用（server 起不来、catalog/install/import 全崩）。
**验收**：默认 GBK 环境 `python -m eval.server` 正常起 + `/api/health` 200 + `/api/catalog` 返回 5 类 14 项。

### 2026-07-12 · setup-kb.py 四类 Win 问题
| 位置 | 问题 | 修复 |
|---|---|---|
| 入口 | `print` 含 ✓✗⚠→ → GBK 终端 `UnicodeEncodeError` | stdout/stderr reconfigure |
| `interactive_args` | 引用未定义变量 `mem` → 交互模式 `NameError` | `mem` → `memory_mode != 'none'` |
| `_install_cmm` Win 分支 | 提示"手动下二进制见 runbook §A"——**误导**（release 根本无 Win 预编译）| 改诚实提示：`cargo install` / 自备 `.exe` 放 PATH |
| `sh()` 等 6 处 subprocess | `text=True` 默认 cp936 解码 cmm 输出 → `_readerthread` `UnicodeDecodeError` | 加 `encoding="utf-8", errors="replace"` |

**验收**：默认 GBK 环境 `python setup-kb.py --status` 三段完整输出（代码 KB / 文档 KB / MCP 注册），无崩溃。

## Windows 平台差异（非 bug，开发/部署注意）

| 项 | 说明 |
|---|---|
| **cmm 无 Win 预编译** | v0.8.1 release 仅 darwin / linux（+ ui 变体）。Win 需 `cargo install`（Rust 工具链，包名见 cmm 官网）或自备 `.exe` 放 PATH。本机 `.exe` 系另行获取。 |
| **Git Bash `/tmp` ≠ Python `/tmp`** | bash 的 `/tmp` 映射到 Git 安装目录；Windows Python 的 `/tmp` 解析为 `C:\tmp`。文件中转用绝对路径或 Windows 路径，别混用。 |
| **CLI JSON 反斜杠路径** | Git Bash 传 `{"repo_path":"D:\\path"}` 给 `.exe`，MSYS 参数转换会破坏 → `repo_path is required`。**用正斜杠 `D:/path`**，或直接用 cmm 的 MCP 工具（参数走 JSON schema，无 shell 转义）。 |
| **curl / tar** | Win10+ 自带（`curl.exe` / `bsdtar`），可用。 |
| **chmod** | Windows 无 `chmod`，`subprocess.run(["chmod",...], check=False)` 静默失败（不报错但无效）——Win 不需要它。 |

## Win 实测验证清单（改了跨平台代码必跑）

- [ ] `python -m py_compile <file>` 语法通过
- [ ] 默认环境（**不加** `PYTHONUTF8`）`python -m eval.server` 能起，`/api/health` 返回 200
- [ ] 默认环境 `python -c "from eval.scaffold import merged"` 不崩
- [ ] 默认环境 `python setup-kb.py --status` 三段完整、无 `UnicodeDecodeError`
- [ ] grep 确认：新代码无裸 `read_text()` / `text=True`（都带了 encoding）
