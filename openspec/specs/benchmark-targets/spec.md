# benchmark-targets Specification

## Purpose
TBD - created by archiving change add-bench-targets. Update Purpose after archive.
## Requirements
### Requirement: Declarative problem corpus

系统 SHALL 将全部 benchmark 题目以声明式 JSON（`targets/<id>/problems.json`）存储，而非 Python 源码字面量。每道题 SHALL 含：稳定 `id`（target 内唯一）、`type`（五选一：`code_retrieval` / `doc_retrieval` / `cross_anchor` / `memory_recall` / `memory_routing`）、`query` 或 `fact`、`gold`、`status`（`pending` 或 `accepted`）。`gold` 的结构 SHALL 由 `type` 决定（discriminated union）。每题 MAY 含 `tags`（承载 `concept_query` / `known_weak_probe` / `subjective_layer` 等诚实标注）、`provenance`（来源符号/kind/文件）、`notes`。loader SHALL 在加载时校验 schema，type↔gold 形状不匹配或 id 重复时失败。

#### Scenario: 加载校验 type 与 gold 形状一致

- **WHEN** loader 加载一道 `type: code_retrieval` 的题
- **THEN** SHALL 断言 `gold.symbols` 存在且为列表；`type: memory_routing` SHALL 断言 `gold.layer` 存在

#### Scenario: id 唯一

- **WHEN** 同一 target 的 `problems.json` 出现两个相同 `id`
- **THEN** loader SHALL 报错失败，拒绝加载

#### Scenario: 诚实标注是数据不是注释

- **WHEN** 一道题是已知弱探针（如答案原文未 mine）
- **THEN** 该属性 SHALL 由 `tags: ["known_weak_probe"]` 表达，而非依赖源码注释

### Requirement: Per-target isolation

每个目标工程 SHALL 独占一个 `targets/<id>/` 目录，内含 `target.json`（工程描述）、`problems.json`（题库）、可选 `fixtures/`。`target.json` SHALL 声明 `id`、`language`、`subjects`、以及该 target 所需的工具路径（`codegraph_root` / `cmm_project` / `graph` 按适用项）。机器特定路径 SHALL 经 `target.local.json`（gitignored）覆盖；loader SHALL 深合并 base 与 local。跨工具 target（`cross_anchor`）SHALL 经 `deps` 字段声明对其它 target 的依赖，loader SHALL 校验依赖 target 存在并解析其路径。

#### Scenario: local overlay 覆盖机器路径

- **WHEN** `target.local.json` 存在且指定 `codegraph_root`
- **THEN** loader 返回的 `codegraph_root` SHALL 来自 local，base 值被覆盖

#### Scenario: local 缺省回退 base

- **WHEN** `target.local.json` 不存在
- **THEN** loader SHALL 直接使用 `target.json` 的值

#### Scenario: 跨 target 依赖校验

- **WHEN** 加载一个声明 `deps: {doc_graph: godot-docs, cmm: godot-core}` 的 cross target
- **THEN** loader SHALL 校验 `godot-docs` 与 `godot-core` target 存在；缺失时失败

### Requirement: Portable benchmark engine

benchmark 引擎（`eval/*.py`）SHALL 不含任何硬编码的机器路径、绝对路径或工程特定标识（`godot-src` / `ks-128` / `engineer_demo` 等）。`codegraph` 根、`cmm` 项目名、文档图路径 SHALL 全部从 `target.json`（经 local 合并）读取。CLI `--root` 参数 SHALL 不存在；`--target` SHALL 接收 target id。

#### Scenario: 引擎源码零硬编码

- **WHEN** 对 `eval/*.py` 与 `web/*.js` 搜索 `godot-src` / `ks-128` / `ks_128` 字面量
- **THEN** 命中 SHALL 仅出现在 `targets/*.json` 数据文件内，不得出现在引擎 `.py` / `.js` 源码

#### Scenario: 路径从 target 解析

- **WHEN** 执行 `bench run code --target <id>`
- **THEN** 引擎 SHALL 从 `targets/<id>/target.json` 解析 `codegraph_root` 与 `cmm_project`，不接受 CLI 路径参数

### Requirement: Frontend problem editor

Gold lab SHALL 提供对 `problems.json` 的读写编辑：列表展示、新增、改、删、批量打标、逐条 approve pending 候选。所有写操作 SHALL 经后端 API，API SHALL 在落盘前校验 schema，非法题目（type/gold 不匹配、id 冲突）SHALL 被拒绝。前端 SHALL NOT 执行 git commit/push；SHALL 显示「待提交」改动指示器（dirty diff），由用户自行 commit。

#### Scenario: 浏览器内改题落地

- **WHEN** 用户在前端改一道题的 query 并保存
- **THEN** 后端 SHALL 校验通过后写回 `problems.json`，git 不被触碰，「待提交」指示器亮起

#### Scenario: 非法题目被拒

- **WHEN** 用户提交一道 `type: code_retrieval` 但缺 `gold.symbols` 的题
- **THEN** API SHALL 返回 schema 错误，文件不被修改

#### Scenario: approve pending 候选

- **WHEN** 用户对一道 `status: pending` 的候选点 approve
- **THEN** 该题 `status` SHALL 翻为 `accepted` 并写回文件，无需任何 fold 命令

### Requirement: Config-driven gold generation

goldgen SHALL 将生成的候选直接写入 `problems.json` 并标记 `status: pending`（携带 `provenance`）。goldgen verify SHALL 在原地（同一条目）标注 `verdict` 与 `reason`。系统 SHALL NOT 再产生 `gold_pending_<target>.md` 文件；SHALL NOT 存在 fold 步骤或全量重写题库的操作。所有人审动作（approve / 删 / 改）SHALL 以增量方式作用于 `problems.json` 单条目。

#### Scenario: 候选直写 problems.json

- **WHEN** 执行 goldgen 生成候选
- **THEN** 候选 SHALL 以 `status: pending` 落入该 target 的 `problems.json`，且无 `.md` 文件被创建

#### Scenario: verify 原地标 verdict

- **WHEN** 执行 goldgen-verify
- **THEN** 每个 pending 候选 SHALL 在原条目获得 `verdict` / `reason` 字段，不产生第二份文件

#### Scenario: 无 fold 步骤

- **WHEN** 人审完成（前端 approve / 删）
- **THEN** 题库 SHALL 已是最终态，不存在也不需要任何 fold / 入库命令

### Requirement: Problem corpus regression gate

系统 SHALL 用快照测试为每个 target 的 `problems.json` 设回归门禁（题数 + 首条 `id`），捕获无意漂移。快照 SHALL NOT 断言机器特定的 `PROJECT` 字符串或绝对路径。

#### Scenario: 题数/首条有意改动需更新快照

- **WHEN** 开发者有意增删题或改首条
- **THEN** 快照测试失败，开发者更新快照基线后通过

#### Scenario: 不 pin 机器路径

- **WHEN** 快照测试断言 target 元信息
- **THEN** SHALL 断言 `target.json` 的 `id` / `subjects` / `language`，不得断言 `codegraph_root` / `cmm_project` 的具体绝对路径字符串

### Requirement: Low-cost project onboarding

对接一个新工程 SHALL 只需：创建 `targets/<id>/` 目录 + `target.json`（+ 可选 `target.local.json`）→ onboarding 向导（索引代码库 + goldgen 造题）→ bench。仓库 SHALL 文档化「fork 模板」工作流。单个 `targets/<id>/` 目录 SHALL 自包含，可整体拷贝到另一仓库使用。memory 自指 demo target（`engineer-demo-memory`）SHALL 被明确标注为不可移植的演示数据。

#### Scenario: fork 后对接新工程

- **WHEN** 新用户 fork 本仓库并按 README 操作
- **THEN** 能删除/替换 demo targets，为自己的工程创建 `targets/<myproj>/` 并跑通 bench

#### Scenario: target 目录自包含可拷贝

- **WHEN** 将某 `targets/<id>/` 目录拷贝到另一台机器/仓库
- **THEN** 该目录内的 `target.json` + `problems.json` 足以描述该 target 的全部题库与工程绑定，无需额外引擎内信息

#### Scenario: demo target 明确标注

- **WHEN** 展示 `engineer-demo-memory` target
- **THEN** SHALL 标注其为 self-referential demo（锚 engineer_demo 自身 memory），不可移植到无等价 memory 的工程

