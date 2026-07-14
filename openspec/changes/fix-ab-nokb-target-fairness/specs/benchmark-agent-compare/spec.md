## ADDED Requirements

### Requirement: Arm availability precheck

`run_compare` SHALL 在跑题前对每个参与臂探测其发现工具对该 target 是否可用：no-kb 臂 SHALL 探 `codegraph_root` 存在且文件类型 globs 非空（`language` 已映射或声明 `code.globs`）；kb 系臂 SHALL 探 `cmm_project` 索引可用。不可用臂 SHALL 在结果对象、`summary.json`（每臂 `availability` 字段）与 `result.md`（顶部 warning）标注原因，SHALL NOT 因此跳过该臂或中断跑批。探测 SHALL 是轻量本地检查（路径 / 索引存在性），SHALL NOT 发起 LLM 调用。本要求解决「某臂发现工具对该 target 静默失效、对照不公平却不被察觉」的误导问题。

#### Scenario: no-kb 不可用被标注不中断

- **WHEN** 某 target 的 `codegraph_root` 不存在，或 `language` 未映射且无 `code.globs`
- **THEN** no-kb 臂 SHALL 被标注不可用及原因；`run_compare` SHALL 继续跑该臂（其 episode 自然失败 / 空转），不跳过、不报错中断

#### Scenario: kb 索引不可用被标注

- **WHEN** 某 target 的 `cmm_project` 索引缺失或不可查
- **THEN** kb 系臂 SHALL 被标注不可用；报告 `result.md` 顶部 SHALL 见 warning，说明该臂对该 target 的对照无意义

#### Scenario: 可用臂零破坏

- **WHEN** 某 target 各臂发现工具均可用（如 `godot-core`：root 存在 + C++ 已映射 + cmm 索引在）
- **THEN** SHALL 不产生不可用标注，输出与无本检查时一致

#### Scenario: 标注进程序与人读两出口

- **WHEN** 任一臂被标注不可用
- **THEN** `summary.json` 的对应臂 SHALL 含 `availability` 字段（含 `ok` 与 `reason`），且 `result.md` SHALL 在顶部 warning 区可读地呈现
