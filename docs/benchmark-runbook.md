# Benchmark Runbook

> 统一 `bench` CLI + 报告自动归档留底。消费 `evaluation` capability 的指标 / gold，
> 不重定义。规格见 `openspec/changes/add-benchmark-runner/`。

## 1. 装

| 依赖 | 用途 | 必需 |
|---|---|---|
| Python 3.12+ | 运行 CLI / 测试 | 是 |
| pytest | 跑测试套件 | 跑测试时 |
| codebase-memory-mcp（cmm） | 代码侧真评测 | 跑 `bench run code/cross` 时 |
| graphify | 文档侧真评测 | 跑 `bench run doc` 时 |
| BigModel/GLM key | 文档建图 / 答案质量 | 跑 `doc/quality` 时 |

> 测试套件零外部依赖（mock subject），无 cmm/graphify 也能 `pytest eval/tests/`。

## 2. 跑（`bench` CLI）

建议加 alias：`alias bench='python -m eval.cli'`。下文用 `bench` 代指。

### `bench run <subject>` —— 跑评测并归档

```bash
bench run code  --target godot --method bm25   # 代码侧（cmm）：grep/bm25/semantic
bench run doc                                   # 文档侧（graphify query，BFS）
bench run cross                                 # 跨工具 anchoring（文档概念→代码）
bench run quality                               # 文档答案质量（凭据门控，可能 429）
```

每次 `run`：
1. 调对应 `run_*.py` 的 `run()` 产出报告
2. `normalize_report()` 规范成统一 schema
3. `archive_report()` 落盘到 `eval/reports/archive/<UTC-ts>-<subject>-<variant>.json`（**不覆盖**）
4. 追加 `archive/index.json` 一条记录
5. stdout 打印归档 id / 路径 / aggregate 摘要

### `bench list-reports` —— 列历史归档

输出 `archive/index.json` 全部报告（id / subject/variant / ts / 主指标摘要）。

### `bench show <id>` —— 看单份报告

打印完整归档 JSON（含 `per_query` 与 `lockfile`）。

### `bench compare <id1> <id2>` —— 两份报告对比

仅 `aggregate` 维度 diff（metric / left / right / delta）。用于横向对比"换 method / 换 gold / 调 prompt"前后的指标变化。

## 3. 读报告

统一 schema（所有 subject 顶层一致）：

```
{
  "subject":      "cmm.bm25" | "graphify.query" | "cross-tool anchoring (graphify→cmm)" | ...,
  "variant":      "godot-bm25" | "godot" | ...,
  "target":       "godot" | "godot-docs-subset" | ...,
  "n":            查询条数,
  "aggregate":    { 主指标: 值, ... },
  "per_query":    [ { query, gold, retrieved_top5, recall@k, ... }, ... ],
  "lockfile":     { temperature, llm_model, cmm_version, graphify_version, mem0_version },
  "archive_meta": { id, ts, readable_ts, path }
}
```

**指标释义**：

| 指标 | 含义 |
|---|---|
| `recall@k`（strict） | top-k 节点短名精确匹配 gold 的比例 |
| `broad_recall@k` | 归一化匹配：gold 出现在 `node / qualified_name / file` 任一即算命中 |
| `crosstool_success_rate` | 文档概念 → cmm 代码定位的端到端成功率 |
| `graphify_hit_rate` / `cmm_hit_rate@5` | 跨工具链路两段各自命中率 |

> **Godot 级大 C++ 用 broad**：cmm `search_code` 把类埋在方法下，strict 在大库结构性失效（Godot strict@5=0.0）；broad + 归一化才是公平刻度。

## 4. 复现

`lockfile` 锁三项：`temp=0` + 固定 LLM 模型 + 工具版本（cmm/graphify/mem0）。

- 同 lockfile → 跨设备 / 跨时间分数可比
- 代码侧结构指标天然确定（不调 LLM），lockfile 主要记版本便于追溯
- 文档侧 / 记忆侧依赖 LLM 抽取（非确定），lockfile 是可比性前提

## 5. 归档查询

```
eval/reports/archive/
  ├─ <ts>-<subject>-<variant>.json    # 每次跑一份，不覆盖
  ├─ <ts>-<subject>-variant>-2.json   # 秒级冲突加后缀
  └─ index.json                       # 全量清单（追加式）
```

- `ts` = UTC ISO8601 基本格式（`20260711T1430Z`），跨时区可比、文件名安全
- `index.json` 每条含 `readable_ts`（本地可读时间）
- 历史 `eval/reports/*.json`（CLI 时代前的手动落盘）保留在 `reports/` 根，**不**入 archive

## 6. 测试

```bash
python -m pytest eval/tests/ -v
```

四层（23 测试）：

| 层 | 文件 | 测什么 |
|---|---|---|
| L1 纯函数 | `test_retrieval_metrics` / `test_graph_metrics` / `test_repro` / `test_harness_roundtrip` | metrics / repro / harness 纯函数 |
| L2 端到端 smoke | `test_archive::test_code_baseline_end_to_end_smoke` | mock 检索 → run() → aggregate + 归档 |
| L3 留底机制 | `test_archive::test_archive_no_overwrite` | 跑两次 → 两文件 + index 两条 + 不覆盖 |
| gold 回归 | `test_gold_regression` | gold_*.py 长度 + 首条快照，防漂移 |

## 7. 遗留用法

散装 `python -m eval.run_code_baseline --target godot --method bm25` 仍可用（直接 `print` JSON 到 stdout，**不归档**）。新用法一律走 `bench`。

## 8. 前端预留

报告 = 结构化 JSON（统一 schema），`archive/index.json` 是清单。前端（后续 change）可直接消费这两个数据源，无需解析 stdout。本变更**不**引入 HTTP / UI。
