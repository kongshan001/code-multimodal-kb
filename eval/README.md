# 评测 harness（`add-evaluation-baseline`）

代码侧评测的零凭据地基。指标纯函数 + cmm round-trip + 可复现 lockfile。

## 统一 CLI（`bench`）

`python -m eval.cli`（建议 `alias bench='python -m eval.cli'`）跑评测并自动归档留底：
`run code|doc|cross|quality|memory|ab` / `list-reports` / `show <id>` / `compare <id1> <id2>`。

详见 [docs/benchmark-runbook.md](../docs/benchmark-runbook.md)。
散装 `python -m eval.run_*` 为遗留用法（直接 print JSON，不归档）。

## 跑

```bash
pip install -r eval/requirements.txt
python -m pytest eval/ -v
```

## 结构

| 模块 | 任务 | 内容 |
|---|---|---|
| `metrics.py` | 2.2 / 2.3 | recall@k、hit_rate、nDCG@k + Symbol Hit@k、Call-Chain Edge Recall、Path Precision@k（纯函数） |
| `subjects.py` | 1.1 | cmm CLI 适配器（list_projects / search / trace_path） |
| `harness.py` | 1.1 | EvalRecord / EvalRun / run_dataset（subject-agnostic 收集） |
| `repro.py` | 1.2 | Lockfile + 版本探测 + 报告盖印 |
| `subjects_memory.py` | 4.2 | MemPalace CLI 适配器（search + 文本输出解析） |
| `routing.py` | 4.3 | D1 四层归属路由器（subjective/episodic/procedural/objective cascade） |
| `gold_memory.py` | 4.2 / 4.3 | RECALL_GOLD（15 query）+ ROUTING_GOLD（13 候选事实，4 类） |
| `run_memory_baseline.py` | 4.2 / 4.3 | 记忆侧 runner：召回 recall@k + 路由准确率 + 去重 + 体积 |
| `run_ab_value.py` | 6.1 / 6.2 | agent A/B Stage 0：KB vs 朴素 grep 的 context token 压缩比 + 注入命中 |
| `tests/` | — | 合成样本验证（指标手算期望值）+ cmm round-trip smoke + 记忆侧 + A/B Stage 0 |

## 已完成 / 待办

- ✅ 1.1 harness 骨架（cmm round-trip smoke 通过）
- ✅ 1.2 可复现 lockfile（报告盖印 + 版本探测）
- ✅ 2.2 检索指标（recall@k / hit_rate / nDCG@k，合成验证）+ **双指标（strict / broad+归一化）**
- ✅ 2.3 图指标（Symbol Hit@k / Call-Chain Edge Recall / Path Precision@k，合成验证）
- ✅ 真基线：graphify（strict@5=0.762）+ **Godot core/**（strict@5=0.0 / broad@5=0.692）→ 报告 `reports/`
- ⏳ 2.1 RepoBench/SWE-Lancer 全量（HF 需 token + 范式不对口，留作 scale-up）
- ⏳ 2.4 PR 反挖 gold（比类名 gold 更硬，留作 gold 硬化）
- ⏳ 2.5 CoIR 向量基线对照 —— TODO
- 🔬 三路检索已进 harness（grep/bm25/semantic）：**Godot broad@5 grep 0.692 → BM25 0.846（+22%），strict@5 0.0→0.5**，实证修正 design 决策4（BM25 主路）。报告 `reports/retrieval-comparison-godot.md`
- ✅ **文档侧（凭据解锁）**：graphify+BigModel 建 Godot 17-doc 子集图（72 节点/32 边）→ `query` 跨文档检索 recall@5=**0.70**；漏点=方法节点↔概念节点连边弱。报告 `reports/doc-baseline-godot-findings.md`
- ✅ **跨工具 anchoring**：graphify 文档概念 → cmm 代码定位，8/8 = **100%** 端到端（design 核心差异化：文档↔代码双向定位，整条 KB 链路验证）。`reports/crosstool-baseline-godot.json`
- ✅ **记忆侧召回 + 路由（零 LLM）**：MemPalace 主观记忆召回 hit@5=**0.933** / hit@1=0.80；D1 四层路由准确率 **1.0**（13 候选事实）；去重 unique@5=0.613（偏弱，会话碎片）。报告 `reports/memory-baseline-2026-07.md`
- ✅ **agent A/B Stage 0（零 LLM token 代理）**：配 cmm 代码 KB vs 朴素 grep，同 26 题代码定位——KB 注入 **~195 token**（kb_hit@5=0.846）vs 朴素 grep+读 **~1750 token**（**压缩 12.71×**）+ grep 对 27% 概念题打空白（KB 救回 5/7）。报告 `reports/ab-value-baseline-2026-07.md`。Stage 1（agent 答对率+端到端 token）卡 LLM key，design §F 就绪

> 文档侧(§3) 答案质量 + 记忆侧(§4) 答案质量评测卡 LLM judge，与 doc-side KB 共享凭据解锁；记忆召回/路由已零凭据跑出（见上）。
