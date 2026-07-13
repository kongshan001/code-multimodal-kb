## Why

benchmark 的题目（gold）当前是 `eval/gold_<target>.py` 里的 Python 字面量，前端只能读不能改；且 13 处硬编码机器/工程特定路径（`godot-src` / `ks-128` / `engineer_demo`）散布在 runner / goldgen / CLI / 前端，拿到别的工程无法低成本对接。本仓库的 `scaffold/catalog.json` + `catalog.local.json` overlay + 前端 catalog 视图已证明「配置文件 + 前端读写」范式可行——题库与目标工程治理照搬该范式，把 benchmark 从「绑定 godot/engineer_demo」解耦为「引擎 + 可拷贝的 per-target 数据目录」。

## What Changes

- **新增 per-target 目录模型**：`targets/<id>/{target.json, target.local.json, problems.json, fixtures/}`。`target.json` 描述目标工程（语言 / subject 类型 / codegraph 根 / cmm 项目名 / 文档图路径 / 跨 target 依赖）；`target.local.json`（gitignored）做机器路径 overlay，照搬 `catalog.local.json` 范式。
- **题库从 Python 字面量迁到声明式 `problems.json`**：统一 schema + `type` 判别（code_retrieval / doc_retrieval / cross_anchor / memory_recall / memory_routing 五型，gold 形状由 type 决定）；每题带稳定 id、`tags[]`（承载 `concept_query`/`known_weak_probe`/`subjective_layer` 等诚实标注）、`provenance`（来源符号/kind/文件）、`status`（pending/accepted）、`notes`。
- **goldgen 重写**：候选直接落 `problems.json` 带 `status: pending`；verify 在原地标 verdict；人审 = 前端逐条 approve 改 `status: accepted` 或删；**废除 `gold_pending_<target>.md` + 废除 fold 步骤 + 废除全量重写**。
- **移除 13 处硬编码**（`ab_tools.py:28-29` / `run_ab_value.py:27-28` / `gold_crosstool.py:8` / `run_memory_baseline.py:85` / `run_memory_quality.py:54` / `cli.py:205,215` / `goldgen.py:29,167` / `web/app.js:92,107,382`）：root / project / graph 路径全部改读 `target.json`。
- **前端 Gold lab 升级**：从「只读 markdown 队列」→ 可读写题库编辑器（列表 / 新增 / 改 / 删 / 批量打标 / approve pending）。前端只写 `problems.json` 文件不碰 git，显示「待提交」diff 指示器，用户自己 commit（同 catalog install 改 `settings.json` 模式）。
- **CLI 改造**：`--root` 参数删除（root 从 `target.json` 读）；`--target` 语义从「gold 模块名」变为「target id」（如 `godot-core`）。
- **一次性迁移**（受控 big-bang，数据量小约 93 题 / 6 文件）：6 个 `gold_*.py` → 5 个 `targets/<id>/`（godot-core / graphify-pkg / godot-docs / godot-cross / engineer-demo-memory）；快照测试同步改 pin `problems.json`。题数守恒：godot 26 / code 21 / docs 10 / cross 8 / memory recall 15 + routing 13。
- **BREAKING**：`eval/gold_*.py` 删除（importer 改走 `eval/targets.py` loader）；CLI `--root` 删除；`--target` 取值语义变更（旧 gold 模块名 → 新 target id）。

## Capabilities

### New Capabilities

- `benchmark-targets`: benchmark 的目标工程与题库数据模型——声明式题库（`problems.json`，type 判别 + 稳定 id + 元数据）、per-target 目录隔离（`targets/<id>/` + `.local` overlay）、可移植引擎（零硬编码）、配置驱动造题（goldgen 直写 + 废 pending/fold）、前端题库编辑器、迁移与回归门禁、低成本工程对接（fork 模板 + target 可拷贝）。

### Modified Capabilities

（无。`evaluation` capability 的既有 requirement 讲「测什么 / 怎么算指标」，gold 来源机制是其内部实现细节，本次变更不改 evaluation 的 requirement 语义。）

## Impact

- **删除**：`eval/gold_godot.py` / `gold_code.py` / `gold_docs.py` / `gold_crosstool.py` / `gold_memory.py` / `gold_gen.py` / `gold_godot_gen.py`。
- **新增**：`eval/targets.py`（loader：读 target.json + problems.json + 合并 .local）；`targets/<id>/{target.json, problems.json}` ×5；迁移脚本 `eval/migrate_gold.py`（一次性，迁移后可删）。
- **重写**：`eval/goldgen.py`（generate 直写 problems.json、verify 原地标、删 write_gold_module/fold/write_pending/parse_pending）。
- **改动**：`eval/run_code_baseline.py` / `run_doc_baseline.py` / `run_crosstool_baseline.py` / `run_memory_baseline.py` / `run_memory_quality.py` / `run_ab_value.py` / `ab_tools.py` / `cli.py` / `server.py`（+`GET/POST/PUT/DELETE /api/gold/<target>` 路由）；`eval/tests/test_gold_regression.py` / `test_gold_memory_snapshot`（re-pin problems.json，拔 `PROJECT` 断言）；`web/app.js`（Gold lab 编辑器）。
- **依赖**：零新增（用 stdlib `json`，不用 PyYAML——保持检索层 pytest-only，与 `catalog.json` 一致）。设计文档记录 YAML vs JSON 取舍。
- **依赖既有 change**：`add-bench-frontend`（Gold lab 视图在该 change 建造，本变更 15/16 已近完成；本变更的编辑器是其 Tier-2 interactive 需求的延伸）。
- **文档**：`docs/benchmark-runbook.md`（targets/ 模型 + 对接新工程步骤）、`README.md`（fork 模板说明）、`docs/frontend-guide.md`（Gold lab 编辑器）同步更新。
