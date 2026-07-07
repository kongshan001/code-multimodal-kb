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
- ✅ 2.2 检索指标（recall@k / hit_rate / nDCG@k，合成验证）
- ✅ 2.3 图指标（Symbol Hit@k / Call-Chain Edge Recall / Path Precision@k，合成验证）
- ⏳ 2.1 数据集下载（RepoBench-R + SWE-Lancer-Loc，CN 走代理）—— 接口已留 `subjects.cmm_search`，TODO
- ⏳ 2.4 PR gold 反挖（需目标仓库 index 进 cmm）—— `harness.run_dataset` 已备，TODO
- ⏳ 2.5 CoIR 向量基线对照 —— TODO

> 文档侧(§3) / 记忆侧(§4) 评测卡 LLM 凭据，与 doc-side KB / Memory Stage 1 共享解锁。
