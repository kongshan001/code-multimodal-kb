"""Stage 1 runner（task 6.3 实施）：gold_godot × {baseline, kb} × N run → agent episode → 判分 → 聚合。

测三件事（用户诉求）：① token 用量（input+output）② 准确度（gold ∈ 终答）③ 效率（步数 + token-per-correct）。
判分零 LLM judge（gold 符号 broad 子串）。两臂差异 = 发现工具（grep vs cmm KB），都给 read_file。

用法：
  python -m eval.run_ab_agent [--subset N] [--runs R]
  bench run ab-agent
"""
from __future__ import annotations

import argparse
import json
import statistics

from eval.ab_agent import load_creds, make_client, run_episode
from eval.repro import detect_lockfile, stamp
from eval.targets import load_problems, load_target


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


def _problem_goldset(problem: dict) -> set[str]:
    """code_retrieval→symbols；bug_fix→symbols+files；broad match 统一判分用。"""
    g = problem.get("gold", {})
    return set(g.get("symbols", [])) | set(g.get("files", []))


# ── agent-compare：4 臂（KB×skills）多题对比 ──────────────────────────────
def _mock_episode(question: str, arm: str, goldset: set[str], qi: int) -> dict:
    """确定性 mock episode（smoke 模式用，不调 LLM）。产出结构完整的假 trace。

    让无凭据环境也能跑通报告写器 + 流水线。命中模式：qi 偶数命中、奇数不中；
    skills 臂多几步（模拟 SOP 更费步）。
    """
    hit = (qi % 2 == 0)
    sym = sorted(goldset)[0] if goldset else "Unknown"
    answer = f"The answer involves `{sym}`." if hit else "I could not locate it."
    is_skill = "+" in arm
    base_tools = ["cmm_search"] if arm.startswith("kb") else ["grep_code"]
    tool_calls = (base_tools + ["read_file"]) if is_skill else base_tools
    steps = 3 if is_skill else 2
    in_tok, out_tok = 100 + qi * 8 + (10 if is_skill else 0), 20 + qi * 3
    return {
        "answer": answer, "input_tokens": in_tok, "output_tokens": out_tok,
        "total_tokens": in_tok + out_tok, "steps": steps, "llm_calls": steps,
        "tool_calls": tool_calls, "tool_steps": len(tool_calls),
        "tool_texts": ["(mock result)"] * len(tool_calls),
        "truncated": False, "wall_clock_s": round(0.5 + qi * 0.07 + (0.3 if is_skill else 0), 2),
        "cost_$": 0.0001,
        "session": [{"role": "user", "content": question},
                    {"role": "assistant", "content": [{"type": "text", "text": answer}]}],
        "thinking": [f"[mock] reasoning for q{qi} on arm {arm}: hypothesize → check → answer"],
    }


def run_compare(target_id: str = "godot-core",
                arms: tuple[str, ...] = ("no-kb", "kb", "kb+superpowers", "kb+openspec"),
                runs: int = 1, subset: int | None = None, smoke: bool = False) -> dict:
    """4 臂 agent-compare：对 code_retrieval + bug_fix 题跑多臂，捕 trace + 指标。

    smoke=True（或无凭据）→ 用 _mock_episode 产出假 trace，跑通写器/流水线。
    返 {target_id, target, arms, episodes_by_arm, n_questions, runs, model, smoke}，
    交 agent_compare_report.write_compare_report 写目录。
    """
    target = load_target(target_id)
    problems = [p for p in load_problems(target_id)
                if p["type"] in ("code_retrieval", "bug_fix")]
    questions = problems[:subset] if subset else problems

    client = None
    model = "mock"
    if not smoke:
        client = make_client()
        _, _, model = load_creds()

    episodes_by_arm: dict[str, list[dict]] = {a: [] for a in arms}
    for qi, p in enumerate(questions):
        goldset = _problem_goldset(p)
        for arm in arms:
            for r in range(runs):
                if smoke:
                    ep = _mock_episode(p["query"], arm, goldset, qi)
                else:
                    ep = run_episode(client, p["query"], arm, target=target, model=model)
                ep.update({"query": p["query"], "type": p["type"], "gold": sorted(goldset),
                           "arm": arm, "run": r, "qid": f"q{qi + 1:02d}",
                           "correct": _judge(ep["answer"], goldset)})
                episodes_by_arm[arm].append(ep)
        print(f"  [{qi + 1}/{len(questions)}] {p['type']:14} {p['query'][:30]:30} "
              + " ".join(f"{a}={'✓' if episodes_by_arm[a][-1]['correct'] else '✗'}" for a in arms),
              flush=True)

    return {"target_id": target_id, "target": target, "arms": list(arms),
            "episodes_by_arm": episodes_by_arm, "n_questions": len(questions),
            "runs": runs, "model": model, "smoke": smoke}


def run(target_id: str = "godot-core", runs: int = 1, subset: int | None = None,
        arms: tuple[str, ...] = ("baseline", "kb", "doc")) -> dict:
    problems = [p for p in load_problems(target_id) if p["type"] == "code_retrieval"]
    questions = problems[:subset] if subset else problems
    client = make_client()
    _, _, model = load_creds()

    rows = []
    for qi, p in enumerate(questions):
        query, goldset = p["query"], set(p["gold"]["symbols"])
        results_this_q = {}
        for arm in arms:
            for r in range(runs):
                ep = run_episode(client, query, arm)
                ep.update({"query": query, "gold": sorted(goldset), "arm": arm, "run": r,
                           "correct": _judge(ep["answer"], goldset),
                           "correct_retrieval": _judge_retrieval(ep["answer"], ep.get("tool_texts", []), goldset)})
                rows.append(ep)
                results_this_q[arm] = ep
        status = " ".join(f"{a}={'✓' if results_this_q[a]['correct'] else '✗'}" for a in arms)
        print(f"  [{qi + 1}/{len(questions)}] {query[:36]:36} {status}", flush=True)

    # 聚合各臂
    agg: dict = {}
    for arm in arms:
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
    def _delta(a, b, key):
        if a in agg and b in agg:
            return round(agg[a][key] - agg[b][key], 3 if "accuracy" in key else 1)
        return None
    agg["delta_accuracy_kb_minus_baseline"] = _delta("kb", "baseline", "accuracy")
    agg["delta_total_tokens_kb_minus_baseline"] = _delta("kb", "baseline", "mean_total_tokens")
    agg["delta_accuracy_doc_minus_baseline"] = _delta("doc", "baseline", "accuracy")
    agg["delta_total_tokens_doc_minus_baseline"] = _delta("doc", "baseline", "mean_total_tokens")

    report = stamp(
        {"subject": "ab-agent-stage1", "target": target_id,
         "project": load_target(target_id)["code"]["cmm_project"],
         "n_questions": len(questions), "runs": runs, "arms": list(arms), "llm_model": model,
         "aggregate": agg, "per_query": rows, "stage": 1,
         "note": "Stage 1 agent A/B：真跑 agent loop（temp=0），测答对率 + 端到端 token + 步数"},
        detect_lockfile(),
    )
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="agent A/B Stage 1：真跑 agent 准确度 + token 对照")
    ap.add_argument("--target", default="godot-core")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--subset", type=int, default=None, help="只跑前 N 题（pilot 用）")
    ap.add_argument("--arms", default="baseline,kb,doc", help="逗号分隔的臂（baseline/kb/doc）")
    args = ap.parse_args()
    arms = tuple(a.strip() for a in args.arms.split(",") if a.strip())
    print(json.dumps(run(args.target, args.runs, args.subset, arms), ensure_ascii=False, indent=2))
