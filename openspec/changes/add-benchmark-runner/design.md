## Context

现有 benchmark = 4 个散装 `python -m eval.run_*` 脚本：各自 `print(json)` 到 stdout、靠手动 `>` 落盘、重跑即覆盖、文件名不统一、无历史留底；`eval/tests/`（4 文件 / 129 行）只测 metrics 纯函数 + harness roundtrip，端到端与归档零固化。但 `run_*.py` 已暴露可导入 `run()` 函数且 code/cross 侧零 LLM——是良好起点。`evaluation` capability 已定义指标 / gold / 阈值，本变更不重定义，只加运行外壳。约束：纯标准库（不引三方）、测试零外部依赖（不依赖真 Godot/cmm）、CN 网络 / 凭据门控不变。

## Goals / Non-Goals

**Goals:**
- 统一 `bench` 子命令入口，替代散装 `python -m eval.run_*`
- 每次报告自动归档留底（不覆盖 + `index.json` 清单）
- 完整 benchmark runbook（装 / 跑 / 读 / 复现 / 归档查询）
- 固化测试：端到端 smoke + 留底机制 + gold 回归门禁
- 报告结构化 JSON（前端预留）

**Non-Goals:**
- 前端 UI / HTTP API（后续 change）
- 交互菜单 TUI
- 评测方法论 / 指标 / gold 变更（归 `evaluation`）
- 真实 Godot/cmm 端到端测试入 CI（用 mock subject 保持零外部依赖）

## Decisions

### 决策 1：CLI = 子命令式（非交互菜单）

`bench run code|doc|cross|quality` + `list-reports` / `show <id>` / `compare <id1> <id2>`。

- **选子命令**：可脚本化、可管道、前端可复用同一入口（与"后续支持前端"对齐）
- **否决交互菜单 TUI**：难脚本化、前端用不上、实现量翻倍
- 现有 `run_*.py` 已有 `run()`，CLI 只是 argparse 子命令薄壳 → 调 `run()` → 归档

### 决策 2：报告归档 = `archive/<ts>-<subject>-<variant>.json` + `index.json`，不覆盖

- 文件名：`<UTC-ts>-<subject>-<variant>.json`（如 `20260711T1430Z-code-godot-bm25.json`）
- ts 用 UTC ISO8601 基本格式（紧凑、文件名安全、跨时区可比）
- `index.json`：追加式清单，每条 `{id, ts, subject, variant, target, lockfile, aggregate 摘要, path}`
- **不覆盖**：留底语义即"每次都留"，同 subject+variant 重跑也产新文件
- **否决"覆盖 + git 版本"**：git 不在运行时路径，非每次跑都提交
- **否决"数据库"**：YAGNI，JSON 文件 + index 足够

### 决策 3：前端预留 = 仅结构化 JSON + 可导入核心（Non-Goal HTTP）

- 报告统一 schema：`{subject, target, n, aggregate, per_query, lockfile, archive_meta}`
- 核心逻辑保持可导入纯函数（`run_*` / `archive` / `metrics`），CLI 是薄壳
- 前端到时：直接吃 `archive/*.json` + `index.json`，或另起 change 加薄 HTTP
- **否决"现在留 HTTP 占位"**：YAGNI，前端时间未定，占位端点是死代码

### 决策 4：测试固化 = 三层，零外部依赖

- **L1 纯函数**（已有，保留）：metrics / repro 纯函数
- **L2 端到端 smoke**（新）：mock subject（返回固定检索结果）→ 跑 `run()` → 断言 aggregate 在预期区间 + 归档文件生成。不依赖真 cmm / graphify / Godot
- **L3 留底机制**（新）：跑两次 → 断言两个归档文件 + index 两条 + 不覆盖
- **gold 回归**（新）：`gold_*.py` 的 GOLD 集快照断言（长度 + 首条），防意外漂移
- **否决"真 Godot 端到端入 CI"**：依赖百万行库索引，CI 不可复现；真库基线靠手动 run + 留底

### 决策 5：与 `evaluation` 的边界

`benchmark-runner` 消费 `evaluation` 的 metrics / gold / 阈值，不重定义。`evaluation` 的 "Reproducible evaluation harness" 关注"锁版本可复现 + 一 harness 测三 subject"（方法论）；`benchmark-runner` 关注"统一入口 + 留底 + 文档 + 测试固化"（工程外壳）。二者互补不重叠。

## Risks / Trade-offs

- **[归档膨胀]** 每次 run 留文件 → 长期堆积。→ 缓解：JSON 小（~10KB/份）；清理策略留作痛点触发（Non-Goal 现在）
- **[mock subject 与真实行为偏差]** L2 smoke 用 mock，不反映真 cmm 检索质量。→ 缓解：smoke 只测"管线跑通 + 归档正确"，不测检索分数；真库分数靠手动 run 留底 + 报告对比
- **[ts 用 UTC]** 用户本地时间 ≠ 文件名 ts。→ 缓解：index 同时记 UTC ts 与可读时间；runbook 说明
- **[现有 `reports/*.json` 不入 archive]** 历史报告留原处。→ 缓解：runbook 注明"archive 仅含 CLI 时代产物；历史快照在 `reports/` 根"

## Open Questions

1. `compare` 子命令的 diff 维度：仅 aggregate 对比，还是 per_query 对齐？——倾向仅 aggregate（够用，per_query 对齐复杂）
2. archive 清理策略：按数量 / 时间保留 N 份？——现在不定，痛点触发再说
