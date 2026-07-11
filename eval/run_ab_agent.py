"""Stage 1 runner（task 6.3 实施）：gold_godot × {baseline, kb} × N run → agent episode → 判分 → 聚合。

测三件事（用户诉求）：① token 用量（input+output）② 准确度（gold ∈ 终答）③ 效率（步数 + token-per-correct）。
判分零 LLM judge（gold 符号 broad 子串）。两臂差异 = 发现工具（grep vs cmm KB），都给 read_file。

用法：
  python -m eval.run_ab_agent [--subset N] [--runs R]
  bench run ab-agent
"""
from __future__ import annotations

import argparse
import importlib
import json
import statistics

from eval.ab_agent import load_creds, make_client, run_episode
from eval.repro import detect_lockfile, stamp


def _norm(s: str) -> str:
    return "".join(c.lower() for c in str(s) if c.isalnum())


def _judge(answer: str, goldset) -> int:
    """终答命中：gold 符号是否在终答里（broad alnum 子串，零 judge）。"""
    a = _norm(answer)
    return 1 if any(_norm(g) in a for g in goldset) else 0


def _judge_retrieval(answer: str, tool_texts: list[str], goldset) -> int:
    """检索命中：终答 OR agent 看过的任一工具结果含 gold（agent 拿到了答案信息）。
    区分"答对了"与"检索到了但没收敛作答"——后者揭示 agent 收敛瓶颈。"""
    hay = _norm(answer) + " " + _norm(" ".join(str(t) for t in tool_texts))
    return 1 if any(_norm(g) in hay for g in goldset) else 0


def run(target: str = "godot", runs: int = 1, subset: int | None = None) -> dict:
    gold = importlib.import_module(f"eval.gold_{target}").GOLD
    questions = gold[:subset] if subset else gold
    client = make_client()
    _, _, model = load_creds()

    rows = []
    for qi, (query, goldset) in enumerate(questions):
        for arm in ("baseline", "kb"):
            for r in range(runs):
                ep = run_episode(client, query, arm)
                ep.update({"query": query, "gold": sorted(goldset), "arm": arm, "run": r,
                           "correct": _judge(ep["answer"], goldset),
                           "correct_retrieval": _judge_retrieval(ep["answer"], ep.get("tool_texts", []), goldset)})
                rows.append(ep)
        bl = [x for x in rows if x["query"] == query and x["arm"] == "baseline"][-1]
        kb = [x for x in rows if x["query"] == query and x["arm"] == "kb"][-1]
        print(f"  [{qi + 1}/{len(questions)}] {query[:40]:40} "
              f"baseline={'✓' if bl['correct'] else '✗'} kb={'✓' if kb['correct'] else '✗'} "
              f"(retr: b{'✓' if bl['correct_retrieval'] else '✗'}/k{'✓' if kb['correct_retrieval'] else '✗'})",
              flush=True)

    # 聚合各臂
    agg: dict = {}
    for arm in ("baseline", "kb"):
        ar = [x for x in rows if x["arm"] == arm]
        tot = [x["input_tokens"] + x["output_tokens"] for x in ar]
        corr = sum(x["correct"] for x in ar)
        agg[arm] = {
            "accuracy": round(statistics.mean(x["correct"] for x in ar), 3),
            "accuracy_retrieval": round(statistics.mean(x["correct_retrieval"] for x in ar), 3),
            "mean_input_tokens": round(statistics.mean(x["input_tokens"] for x in ar), 1),
            "mean_output_tokens": round(statistics.mean(x["output_tokens"] for x in ar), 1),
            "mean_total_tokens": round(statistics.mean(tot), 1),
            "mean_steps": round(statistics.mean(x["steps"] for x in ar), 2),
            "truncated_count": sum(1 for x in ar if x["truncated"]),
            "token_per_correct": round(sum(tot) / corr, 1) if corr else None,
            "n_episodes": len(ar),
        }
    agg["delta_accuracy_kb_minus_baseline"] = round(
        agg["kb"]["accuracy"] - agg["baseline"]["accuracy"], 3)
    agg["delta_accuracy_retrieval_kb_minus_baseline"] = round(
        agg["kb"]["accuracy_retrieval"] - agg["baseline"]["accuracy_retrieval"], 3)
    agg["delta_total_tokens_kb_minus_baseline"] = round(
        agg["kb"]["mean_total_tokens"] - agg["baseline"]["mean_total_tokens"], 1)
    agg["delta_steps_kb_minus_baseline"] = round(
        agg["kb"]["mean_steps"] - agg["baseline"]["mean_steps"], 2)

    report = stamp(
        {"subject": "ab-agent-stage1", "target": target, "project": "godot-core",
         "n_questions": len(questions), "runs": runs, "llm_model": model,
         "aggregate": agg, "per_query": rows, "stage": 1,
         "note": "Stage 1 agent A/B：真跑 agent loop（temp=0），测答对率 + 端到端 token + 步数"},
        detect_lockfile(),
    )
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="agent A/B Stage 1：真跑 agent 准确度 + token 对照")
    ap.add_argument("--target", default="godot")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--subset", type=int, default=None, help="只跑前 N 题（pilot 用）")
    args = ap.parse_args()
    print(json.dumps(run(args.target, args.runs, args.subset), ensure_ascii=False, indent=2))
