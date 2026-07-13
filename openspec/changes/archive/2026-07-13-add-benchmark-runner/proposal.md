## Why

现有 benchmark 是 4 个散装 `python -m eval.run_*` 脚本：各自 `print(json)` 到 stdout、靠手动 `>` 落盘、重跑即覆盖、文件名不统一、无历史留底；测试只覆盖 metrics 纯函数，端到端与报告归档零固化。核心命题（BM25 broad@5=0.846 / 跨工具 anchoring 8/8=100%）已证，但「跑一次、留一次、可追溯、可复现」的工程外壳缺失——每次报告生成无留底导致横向对比无依据，新人照文档无法复现一次评测。需要把 benchmark 从"散装脚本"升级为"统一 CLI + 自动留底 + 文档 + 固化测试"的运行器，并为后续前端预留结构化产物。

## What Changes

- **统一 CLI 入口 `bench`（子命令式）**：`run code|doc|cross|quality`、`list-reports`、`show <id>`、`compare <id1> <id2>`，替代散装 `python -m eval.run_*`；可脚本化、可管道，为前端复用同一入口留口
- **报告自动归档留底**：每次 `run` 落盘到 `eval/reports/archive/<ts>-<subject>-<variant>.json`，**不覆盖**；维护 `archive/index.json` 清单（subject / variant / ts / lockfile 摘要 / 指标快照），支撑横向对比与追溯
- **完整使用文档**：`docs/benchmark-runbook.md`（装 / 跑 / 读报告 / 复现 / 归档查询）
- **测试用例固化**：端到端 smoke（mock subject，零外部依赖，不依赖真 Godot/cmm）+ 留底机制测试（归档新增文件、index 更新、不覆盖）+ gold 回归门禁（gold 集快照防漂移）
- **报告产物结构化**：统一 JSON schema（`subject/target/aggregate/per_query/lockfile/archive_meta`），为前端预留——**前端本身为 Non-Goal**

## Capabilities

### New Capabilities

- `benchmark-runner`: benchmark 的运行外壳——统一 CLI 入口、报告自动归档与留底、使用文档、测试固化；消费 `evaluation` capability 定义的指标 / gold，不重定义

### Modified Capabilities

（无——`evaluation` 的 requirements 不变；benchmark-runner 是其运行外壳，职责边界在 design.md 说明）

## Impact

- **新增代码**：`eval/cli.py`（bench 入口）+ `eval/archive.py`（归档层）+ `eval/tests/` 扩充；现有 `run_*.py` 已暴露可导入 `run()`，统一接 CLI（轻重构，不改检索逻辑）
- **新增文档**：`docs/benchmark-runbook.md`
- **报告目录**：`eval/reports/archive/`（新）；现有 `eval/reports/*.json` 保留为历史快照，不迁移
- **依赖**：纯标准库（argparse / json / pathlib / datetime），零新增三方依赖
- **不碰**：`evaluation` 的 metrics / gold 定义、cmm / graphify / Mem0 本身
- **Non-Goal**：前端 UI / HTTP API（后续 change）；交互菜单 TUI；评测方法论变更
