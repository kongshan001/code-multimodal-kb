## Why

no-kb（baseline）臂的发现工具 `grep_code` 有两个**正交**的 target 依赖——搜索根 `codegraph_root` 与文件类型 `--include` globs——任一缺失都让 grep 静默返 `(no matches)`。当前 `grep_code` 硬编码 `*.h/*.cpp/*.hpp`（只认 C++），且 `graphify-pkg` 缺 `codegraph_root`，导致 3 个会被 `run_compare` 实跑的 target 中**只有 `godot-core` 的 no-kb 臂能工作**；`graphify-pkg`（Python）与 `claude-gui`（TS）的 no-kb 系统性失效。这使得 no-kb vs kb 的对照在这些 target 上**不公平**：no-kb 输在「工具不认识该 target」而非「没有语义 KB」，污染了「KB 值不值」的量化结论。默认一直跑 `godot-core`，故该缺陷从未暴露。

## What Changes

- **①（核心）`grep_code` 文件类型过滤改 target-aware**：从 `target.code.globs`（新增可选字段）优先取，否则按 `target.language` 推断（C++→`.h/.cpp/.hpp`、Python→`.py`、TypeScript→`.ts/.tsx` …），不再硬编码 C++ 扩展名。`godot-core`（language=C++）零改兼容，推断结果 = 现硬编码值。
- **②（核心）`graphify-pkg` 补 `codegraph_root`**：经 `target.local.json`（gitignored）注入本机路径 `/Users/ks_128/.local/share/uv/tools/graphifyy/lib/python3.13/site-packages/graphify`（已实测存在；`graphifyy` 双 y 是真实目录名），遵循现有 spec「机器特定路径走 local overlay」约定。
- **④（增强）`run_compare` 跑题前探各臂发现工具可用性**：no-kb 看 `codegraph_root` 存在 + globs 非空，kb 看 `cmm_project` 索引在；不可用臂 SHALL 在结果与报告标注（防误导性对照报告）。
- **③（划出，仅标注）`claude-gui` 的 `target.json` 存的是别机 Windows 路径**（本机不存在）——本变更仅在 proposal/design 记为「已知前置条件」；真修法（路径须本机存在 / 支持 env 占位的对接规范）单列，不纳入本变更代码。
- **不改**：`ARMS` 注册表结构、agent loop、判分、归档、CLI 参数、token 计数（保持注册表「臂变数据 / loop 零改」哲学）。

## Capabilities

### New Capabilities

（无——本变更强化两个现有能力，不引入新能力。）

### Modified Capabilities

- `benchmark-targets`:
  - 强化 `Portable benchmark engine`：工具的文件类型过滤（grep `--include`）SHALL target-aware（从 `code.globs` 或 `language` 解析），SHALL NOT 硬编码特定语言扩展名——补全「引擎零工程特定假设」对文件类型这一维度的覆盖。
  - 扩展 `Per-target isolation`：`target.json` MAY 声明可选 `code.globs`（`list[str]`，覆盖 `language` 推断的文件类型）；机器特定的 `codegraph_root` SHALL 经 `target.local.json` 覆盖（重申既有约定，并为 graphify-pkg 落地）。
- `benchmark-agent-compare`:
  - 新增 `Arm availability precheck` requirement：`run_compare` SHALL 在跑题前探各臂发现工具对该 target 是否可用，不可用臂 SHALL 在结果与报告标注，避免产出静默误导的对照。

## Impact

- **代码**：`eval/ab_tools.py`（`grep_code` 的 include 逻辑 + `set_active` 注入 `globs`）、`eval/run_ab_agent.py`（`run_compare` 启动检查 + 不可用标注透传）、`eval/agent_compare_report.py`（报告渲染不可用标注）。
- **数据**：`eval/targets/graphify-pkg/target.local.json`（新增，gitignored，本机 `codegraph_root`）。
- **不变**：`ARMS` 臂定义、`run_episode` agent loop、判分（`_judge`/`_judge_retrieval`）、报告目录结构、CLI `--target`/`--arms`/`--subset` 语义、token/cost 统计。
- **回归风险**：`godot-core` 的 no-kb 行为须不变（V3 守门）；新增启动检查不得阻断既有可跑 target（仅标注，不跳过/不报错中断）。
- **已知前置条件（不在本变更修）**：`claude-gui` 等 target.json 存别机绝对路径者，需用户自配 `target.local.json` 覆盖本机路径后 no-kb 方可用——属 dock-target 对接规范，单列后续变更。
