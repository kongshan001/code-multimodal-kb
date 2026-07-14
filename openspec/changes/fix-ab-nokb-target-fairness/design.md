## Context

`run_compare`（agent-compare 入口）只按 `problem.type` 过滤跑哪些题，不校验「各臂的发现工具对该 target 是否真的能用」。no-kb 臂的 `grep_code` 同时依赖 (a) `codegraph_root`（搜索根）与 (b) `--include` globs（文件类型）——两者都来自 target，但 (b) 当前硬编码为 C++ 扩展名、(a) 在 `graphify-pkg` 缺失。结果：`graphify-pkg`(Python) / `claude-gui`(TS) 的 no-kb grep 静默返空，与 kb 臂对照不公平。现约束（来自既有 spec）：

- `benchmark-targets / Portable benchmark engine`：引擎 SHALL 不含工程特定标识——`grep_code` 的硬编码 C++ 扩展名违反此条。
- `benchmark-targets / Per-target isolation`：机器特定路径 SHALL 经 `target.local.json`（gitignored）覆盖——`graphify-pkg` 的 `codegraph_root` 应走 local，非 base。
- 注册表哲学（`ab_tools.py` docstring）：工具 executor 是代码，但「臂 = 工具集」是数据；换 target = 换配置，executor 读 `_active`（`set_active` 注入），不硬编码。

`set_active` 已是 target 路径注入 `_active` 的单一入口（修过模块级 `load_target("godot-core")` 硬编码 bug，见 `ab_tools.py:31-33` 注释）。

## Goals / Non-Goals

**Goals:**
- no-kb 臂的 grep 文件类型过滤 target-aware：`code.globs` 优先、否则 `language` 推断，`godot-core` 零改兼容。
- `graphify-pkg` 的 no-kb grep 能返非空（V1：`grep_code("class")` 返 .py 文件）。
- agent-compare 对「某臂发现工具对该 target 不可用」可见——结果/报告标注，不再静默误导。
- 不破坏现有唯一可跑的 `godot-core`（V3 守门）。

**Non-Goals:**
- 不修 `claude-gui` 等 target.json 存别机路径者（③，划为对接规范，单列后续变更）。
- 不迁移 `godot-core`/`graphify-pkg` 既有机器特定字段（如 `cmm_project`）到 local——范围控制，仅补 `graphify-pkg` 的 `codegraph_root`。
- 不改 agent loop / 判分 / 归档 / CLI / token 计数。
- 不新增臂、不改 `ARMS` 结构。

## Decisions

### D1：include 来源 = `code.globs` 优先 + `language` 推断 fallback（C 方案）

`set_active` 注入 `_active["globs"]`：优先取 `target.code.globs`，无则按 `target.language` 查模块级 `LANG_GLOBS` 映射表。`grep_code` 读 `_active["globs"]` 替代硬编码。

**alternatives：**
- **A（仅 language 枚举）**：零配置自动，但映射知识藏代码、新语言须改代码、混合语言 target 不可控。
- **B（仅 code.globs）**：最纯数据驱动，但每个 target 都须配、`godot-core` 现状要补字段（破坏「零改兼容」目标）。
- **C（A 默认 + B 可选覆盖）✅**：既有 target（`godot-core` C++、`graphify-pkg` Python）零改即 work（靠 language 推断），需精控者配 `code.globs`。向后兼容 + 可扩展，且与 `_active` 注入 `codegraph_root`/`cmm_project` 同构。

### D2：globs 经 `_active` 注入，executor 单一来源

`grep_code` 只读 `_active["globs"]`，不直接读 target——与 `codegraph_root` 注入路径完全一致，保持「executor 读 `_active`、`set_active` 是唯一注入入口」的现有设计，避免再开一条 target→executor 直读通道。

### D3：`graphify-pkg` 的 `codegraph_root` 走 `target.local.json`

值 = `/Users/ks_128/.local/share/uv/tools/graphifyy/lib/python3.13/site-packages/graphify`（已实测存在）。放 local 而非 base：

**alternatives：**
- **写 base `target.json`**：入库可复现，但违反 `Per-target isolation`「机器特定路径走 local」约定，且与 `godot-core` 把绝对路径写 base 的同类遗留叠加。
- **写 `target.local.json` ✅**：遵循 spec；路径本就是机器特定（含 `ks_128`），local 是其正确归属。trade-off：gitignored 不入库，他人 fork 须自配——但 spec 本就如此设计，验证用本机跑（V1/V2）。

### D4：启动检查 = 探测 + 标注，**不中断**

`run_compare` 跑题前探各臂发现工具可用性：no-kb 看 `codegraph_root` 存在 + `globs` 非空；kb 看 `cmm_project` 索引可用。不可用 → 在 `result` 与报告标注（不可用臂的 `config.md`/`aggregate` + `result.md` 顶部 warning），**不跳过、不报错中断**。

**alternatives：**
- **不可用则跳过该臂**：会丢对照维度，且静默跳过本身就是另一种误导。
- **不可用则报错中断**：破坏 `godot-core` 等既有可跑 target 的现有流程（如 `cmm` 探测假阳）。
- **仅标注 ✅**：让失败可见（解决「静默误导」根因）同时零破坏。`Low-credential degradation`（mock 降级）与 `Honest comparison boundaries`（诚实边界）是同类精神。

### D5：`LANG_GLOBS` = `ab_tools.py` 模块级常量 dict

`{"C++": ["*.h","*.cpp","*.hpp"], "Python": ["*.py"], "TypeScript": ["*.ts","*.tsx"], ...}`。未知 `language` → globs 空 → grep 不加 `--include`（全文件，可能略噪但可用，且启动检查会标注「language 未映射」）。

**alternatives：** 放 target.json 枚举。否决：语言→扩展名是稳定通用知识，非 target 属性；每 target 重复配属冗余。新语言加一行常量即可。

## Risks / Trade-offs

- **[language 推断不准 / 混合语言 target]** → `code.globs` 可显式覆盖；未知 language fallback 全文件 grep + 启动检查标注「未映射」，不静默。
- **[kb 臂 cmm 可用性探测假阳/假阴]** → 探测实现保守（试查 `cmm_bm25` 或检查索引存在），探测失败只标注不阻断；首版宁可漏标不可用也不误中断。
- **[`graphify-pkg` local 不入库 → 他人需自配]** → spec 本就如此；README/dock 文档注明 no-kb 需本机 `codegraph_root`。验证证据（V1/V2）留本机输出。
- **[C 方案破坏 `godot-core` 回归]** → V3 守门断言：`godot-core` 推断 globs == 现硬编码值 `["*.h","*.cpp","*.hpp"]`，行为不变。
- **[启动检查增加跑前开销]** → 探测是轻量本地检查（路径存在 / 索引在），非 LLM 调用，开销可忽略。

## Migration Plan

纯增强 + 数据补充，无破坏性变更：
1. 加 `LANG_GLOBS` 常量 + `set_active` 注入 `globs` + `grep_code` 读 `_active["globs"]`。
2. 新建 `graphify-pkg/target.local.json`（本机）。
3. `run_compare` 加启动检查 + 标注透传；报告渲染标注。
4. 跑 V1/V2/V3 守门。

**回滚**：还原 `grep_code` include 硬编码 + 删 `graphify-pkg/target.local.json` + 删启动检查。无数据迁移、无 schema 破坏。

## Open Questions

- `LANG_GLOBS` 初始覆盖集：C++/Python/TypeScript/Go/Rust/Java 够用？未知 fallback 已定义，可后续按需补。（实现时定，不阻塞）
- kb 臂 cmm 可用性探测的具体实现（`cmm_bm25` 试查 vs 索引文件存在性）：实现时择简，保守优先。
- 不可用标注在报告的落点（`result.md` 顶部 warning + `summary.json` 每臂 `availability` 字段）：实现时定，须同时进人读与程序消费两个出口。
