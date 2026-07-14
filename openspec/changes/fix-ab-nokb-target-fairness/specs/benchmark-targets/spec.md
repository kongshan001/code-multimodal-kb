## MODIFIED Requirements

### Requirement: Portable benchmark engine

benchmark 引擎（`eval/*.py`）SHALL 不含任何硬编码的机器路径、绝对路径或工程特定标识（`godot-src` / `ks-128` / `engineer_demo` 等）。`codegraph` 根、`cmm` 项目名、文档图路径 SHALL 全部从 `target.json`（经 local 合并）读取。CLI `--root` 参数 SHALL 不存在；`--target` SHALL 接收 target id。**工具的文件类型过滤（如 `grep` 的 `--include` globs）SHALL target-aware**：SHALL 优先从 `target.code.globs`（经 local 合并）取，否则按 `target.language` 推断，SHALL NOT 硬编码特定语言的文件扩展名。

#### Scenario: 引擎源码零硬编码

- **WHEN** 对 `eval/*.py` 与 `web/*.js` 搜索 `godot-src` / `ks-128` / `ks_128` 字面量
- **THEN** 命中 SHALL 仅出现在 `targets/*.json` 数据文件内，不得出现在引擎 `.py` / `.js` 源码

#### Scenario: 路径从 target 解析

- **WHEN** 执行 `bench run code --target <id>`
- **THEN** 引擎 SHALL 从 `targets/<id>/target.json` 解析 `codegraph_root` 与 `cmm_project`，不接受 CLI 路径参数

#### Scenario: grep 文件类型 target-aware

- **WHEN** no-kb 臂的 `grep_code` 在某 target 上执行
- **THEN** 其 `--include` globs SHALL 来自 `target.code.globs`（若声明）或 `target.language` 推断，SHALL NOT 是硬编码的 C++ 扩展名

#### Scenario: C++ 语言推断等于原硬编码值

- **WHEN** target 的 `language=C++` 且未声明 `code.globs`
- **THEN** 推断 globs SHALL 为 `["*.h", "*.cpp", "*.hpp"]`（与历史硬编码一致，零行为变更）

#### Scenario: 语言未映射 fallback

- **WHEN** target 的 `language` 不在已知映射表且未声明 `code.globs`
- **THEN** grep SHALL 不限文件类型（全文件搜），且该 target SHALL 在臂可用性启动检查中被标注「language 未映射」

### Requirement: Per-target isolation

每个目标工程 SHALL 独占一个 `targets/<id>/` 目录，内含 `target.json`（工程描述）、`problems.json`（题库）、可选 `fixtures/`。`target.json` SHALL 声明 `id`、`language`、`subjects`、以及该 target 所需的工具路径（`codegraph_root` / `cmm_project` / `graph` 按适用项）。`target.json` MAY 声明 `code.globs`（`list[str]`，覆盖按 `language` 推断的 grep 文件类型，供混合语言或非标准扩展的 target 精控）。机器特定路径 SHALL 经 `target.local.json`（gitignored）覆盖；loader SHALL 深合并 base 与 local。跨工具 target（`cross_anchor`）SHALL 经 `deps` 字段声明对其它 target 的依赖，loader SHALL 校验依赖 target 存在并解析其路径。

#### Scenario: local overlay 覆盖机器路径

- **WHEN** `target.local.json` 存在且指定 `codegraph_root`
- **THEN** loader 返回的 `codegraph_root` SHALL 来自 local，base 值被覆盖

#### Scenario: local 缺省回退 base

- **WHEN** `target.local.json` 不存在
- **THEN** loader SHALL 直接使用 `target.json` 的值

#### Scenario: 跨 target 依赖校验

- **WHEN** 加载一个声明 `deps: {doc_graph: godot-docs, cmm: godot-core}` 的 cross target
- **THEN** loader SHALL 校验 `godot-docs` 与 `godot-core` target 存在；缺失时失败

#### Scenario: code.globs 覆盖语言推断

- **WHEN** 某 target 声明 `code.globs: ["*.cs"]`
- **THEN** no-kb 臂的 grep SHALL 用 `*.cs` 过滤，而非按 `language` 推断

#### Scenario: 机器特定 codegraph_root 走 local

- **WHEN** 某 target 的 `codegraph_root` 是机器特定绝对路径
- **THEN** 该值 SHALL 经 `target.local.json` 提供（gitignored），而非入库进 base `target.json`
