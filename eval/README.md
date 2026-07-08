# 评测 harness（`add-evaluation-baseline`）

代码侧评测的零凭据地基。指标纯函数 + cmm round-trip + 可复现 lockfile。

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
| `tests/` | — | 合成样本验证（指标手算期望值）+ cmm round-trip smoke |

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

> 文档侧(§3) / 记忆侧(§4) 评测卡 LLM 凭据，与 doc-side KB / Memory Stage 1 共享解锁。
