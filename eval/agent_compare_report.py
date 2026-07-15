"""agent-compare 目录报告写器：多臂 episode 结果 → 目录化对比报告。

输入 run_ab_agent.run_compare 的结果 dict，写出：
  <root>/conclusion.md / summary.json / matrix.md
  <root>/arms/<arm>/{config.md, aggregate.json, episodes/qNN/{episode.json, episode.md, session.jsonl, thinking.md}}

入库：conclusion/summary/matrix/arms/<arm>/{config,aggregate,episodes/episode.json, episodes/episode.md}。
本地（.gitignore）：episodes/qNN/{session.jsonl, thinking.md}。
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from eval import ab_tools

# summary 里展示的指标（顺序即矩阵列序）
_METRIC_KEYS = [
    "accuracy", "mean_total_tokens", "mean_llm_calls", "mean_tool_steps",
    "mean_wall_clock_s", "mean_cost_$", "tool_diversity", "truncated_rate", "n_episodes",
]


def _aggregate(eps: list[dict]) -> dict:
    """单臂指标聚合。"""
    n = len(eps) or 1
    tot = [e["total_tokens"] for e in eps]
    return {
        "accuracy": round(statistics.mean(e["correct"] for e in eps), 3),
        "mean_input_tokens": round(statistics.mean(e["input_tokens"] for e in eps), 1),
        "mean_output_tokens": round(statistics.mean(e["output_tokens"] for e in eps), 1),
        "mean_total_tokens": round(statistics.mean(tot), 1),
        "mean_llm_calls": round(statistics.mean(e["llm_calls"] for e in eps), 2),
        "mean_tool_steps": round(statistics.mean(e["tool_steps"] for e in eps), 2),
        "mean_wall_clock_s": round(statistics.mean(e["wall_clock_s"] for e in eps), 2),
        "mean_cost_$": round(statistics.mean(e["cost_$"] or 0 for e in eps), 4),
        "tool_diversity": round(statistics.mean(len(set(e["tool_calls"])) for e in eps), 2),
        "truncated_rate": round(sum(1 for e in eps if e["truncated"]) / n, 3),
        "n_episodes": len(eps),
    }


def _summary_matrix(arms: list[str], aggregates: dict, result: dict) -> dict:
    """臂×指标矩阵 + 跨臂派生指标（context_compression）。"""
    mat = {a: {k: aggregates[a].get(k) for k in _METRIC_KEYS} for a in arms}
    # context_compression = no-kb 总 token / kb 总 token（>1 = KB 省）
    comp = None
    if "no-kb" in aggregates and "kb" in aggregates:
        kb_tok = aggregates["kb"]["mean_total_tokens"]
        if kb_tok:
            comp = round(aggregates["no-kb"]["mean_total_tokens"] / kb_tok, 2)
    return {
        "target": result["target_id"], "model": result["model"], "smoke": result["smoke"],
        "engine": result.get("engine", "sdk"),
        "n_questions": result["n_questions"], "runs": result["runs"],
        "arms": arms, "matrix": mat,
        "context_compression_kb_vs_no_kb": comp,
        "metric_keys": _METRIC_KEYS,
    }


def _winner(arms, aggregates, key, lower_better=False):
    """哪臂在该指标上最优（含并列）。返 (list_of_winners, value)。"""
    vals = [(a, aggregates[a].get(key)) for a in arms if aggregates[a].get(key) is not None]
    if not vals:
        return [], None
    best_v = min(v for _, v in vals) if lower_better else max(v for _, v in vals)
    winners = [a for a, v in vals if v == best_v]
    return winners, best_v


def _result_md(result: dict, aggregates: dict) -> str:
    """合并 结论 + 指标说明(小白版) + 对比矩阵 + 诚实边界 为人读 result.md。"""
    arms = result["arms"]
    acc_win, acc_v = _winner(arms, aggregates, "accuracy")
    tok_win, tok_v = _winner(arms, aggregates, "mean_total_tokens", lower_better=True)
    cost_win, cost_v = _winner(arms, aggregates, "mean_cost_$", lower_better=True)
    comp = _summary_matrix(arms, aggregates, result)["context_compression_kb_vs_no_kb"]
    mode = "（**SMOKE / mock**，非真实 LLM 跑）" if result["smoke"] else ""

    glossary = [  # 指标大白话
        ("accuracy", "答对率 = 答对的题 ÷ 总题数。0~1，越高越好"),
        ("mean_total_tokens", "平均每题烧多少 token（≈字数）。越少越省"),
        ("mean_llm_calls", "平均每题调几次大模型。越少越快越省"),
        ("mean_tool_steps", "平均每题用几次工具（cmm/grep/read）"),
        ("mean_wall_clock_s", "平均每题跑多久（秒）"),
        ("mean_cost_$", "平均每题花多少钱（≈ token × 单价）"),
        ("tool_diversity", "平均用了几种不同工具（高了可能在乱试）"),
        ("truncated_rate", "多少题没在步数内答完（卡住了）。0 最好"),
        ("context_compression", "有 KB 比无 KB 省几倍 token（>1=KB 省；仅 no-kb+kb 都跑时给）"),
    ]

    lines = [
        f"# agent-compare 结果 · target={result['target_id']} · model={result['model']} · engine={result.get('engine', 'sdk')}{mode}",
        f"> {result['n_questions']} 题 × {result['runs']} runs × {len(arms)} 臂。",
        ""]

    def _fmt_winners(ws, v, label, unit):
        if not ws:
            return f"- **{label}**：无数据"
        s = " / ".join(f"`{w}`" for w in ws)
        if len(ws) == len(arms):
            return f"- **{label}**：{len(ws)} 臂持平（{unit}={v}）"
        elif len(ws) > 1:
            return f"- **{label}**（{len(ws)} 臂并列）：{s}（{unit}={v}）"
        else:
            return f"- **{label}**：{s}（{unit}={v}）"

    lines += [
        "## 怎么读懂这份报告（规则，先看）",
        "",
        "**4 个臂是什么**：",
        "- `no-kb` = 只给 grep + 读文件（朴素搜索，无知识库）",
        "- `kb` = 给 cmm 代码知识库（语义检索符号）",
        "- `kb+superpowers` / `kb+openspec` = kb + 往 agent 指令里注入 superpowers/openspec 的工程纪律 SOP",
        "  （注入的是**精简 SOP 文本**，不是真 skill 运行时——见末尾诚实边界）",
        "",
        "**答对（✓）怎么判**：终答里含 gold 符号或文件名就算对（broad 子串匹配，零 LLM judge）。",
        "**gold 是什么**：每题的标准答案——来自 codegraph 挖出的真实代码符号/文件，构造即正确（不是人拍脑袋写的）。",
        "",
        "**某题被标截断（逐题表 `截断` 列 ⚠ / `truncated_rate` > 0）**：agent 跑满 backstop（**30 轮**，"
        "防死循环的安全网）仍未自然给出答案 = **真卡住**。本跑采用 run-until-answer：**不 inject 猜测答案**，"
        "那题的 `answer` 是占位（判分即错）。30 轮 backstop 远超正常收敛所需，所以截断率衡量的是 agent 真正卡死的比例，"
        "不是被步数上限人为截断。",
        "",
        "**`thinking` / 思考过程**：GLM-5.1 经这个端点不返独立 thinking block，所以思考 = agent 的推理文本（assistant 回答），"
        "不是单独的隐藏思维链——别当成完整思考链。",
        "**`cost_$`**：token × 单价；单价是**占位**（待确认 GLM 定价），勿当真实成本，看相对大小即可。",
        "**`tool_diversity` 高**：可能 agent 在乱试不同工具（没方向），未必好事。",
        "",
        "## 谁赢",
        _fmt_winners(acc_win, acc_v, "准确率最高", "accuracy"),
    ]
    if tok_win:
        lines.append(_fmt_winners(tok_win, tok_v, "最省 token", "mean_total_tokens"))
    if cost_win and cost_v:
        lines.append(_fmt_winners(cost_win, cost_v, "最省钱", "mean_cost_$"))
    if comp:
        lines.append(f"- **KB vs 无 KB token 压缩**：{comp}×（>1 = KB 省）")

    lines += ["", "## 指标怎么看（小白版）", "| 指标 | 大白话 |", "|---|---|"]
    for k, v in glossary:
        lines.append(f"| `{k}` | {v} |")

    lines += ["", "## 对比矩阵", "| 臂 | " + " | ".join(_METRIC_KEYS) + " |",
              "|---|" + "|".join(["---"] * len(_METRIC_KEYS)) + "|"]
    for a in arms:
        vals = [str(aggregates[a].get(k, "")) for k in _METRIC_KEYS]
        lines.append(f"| `{a}` | " + " | ".join(vals) + " |")

    lines += [""] + _questions_lines(result)   # 逐题得分对照（原 questions.md 并入）

    lines += ["## 各臂速览"]
    for a in arms:
        ag = aggregates[a]
        lines.append(f"- `{a}`: acc={ag['accuracy']} · tokens={ag['mean_total_tokens']} · "
                     f"llm_calls={ag['mean_llm_calls']} · steps={ag['mean_tool_steps']} · "
                     f"t={ag['mean_wall_clock_s']}s · tools={ag['tool_diversity']}")

    lines += [
        "",
        "## 诚实边界（必须看）",
        "- **accuracy 由 GLM 生成 + GLM 判分**（同家族 self-preference）→ 相对参考值，非绝对回归值。",
        "- **skills 臂注入的是 bundled 精简 SOP 文本**（`eval/arms/skills_bundled/`），**非完整 Claude Code skill 运行时**"
        "（无触发机制/hook）。是 headless 可复现近似，不等于真实 skill 效果。",
        "- **`cost_$` 依赖 MODEL_PRICES 单价**，单价未知则 0（占位）；当前价格为占位，勿当真实成本。",
        f"- 样本量小（{result['n_questions']} 题），结论显著性有限——看趋势勿绝对化。",
        "- bug_fix 题仍用 symbol/file broad match 判分（非修复质量 LLM-judge）。",
        "",
        "## 怎么看 skills 值不值",
        "对比 `kb+superpowers` / `kb+openspec` vs `kb` 的 accuracy（skills 帮没帮）+ mean_total_tokens（skills 多花多少）。"
        "**bug_fix 题上差异最可能显现**（纯 code_retrieval 上 skills 显不出价值）。",
        "",
        "详见 `summary.json`（臂×指标矩阵，程序消费用）、各臂 `arms/<arm>/`（config + aggregate + episodes）。",
    ]
    return "\n".join(lines) + "\n"


def _questions_lines(result: dict) -> list:
    """逐题得分对照段（合并进 result.md）：每题一张 臂×{答对/答案/指标} 表。"""
    arms = result["arms"]
    by_arm = result["episodes_by_arm"]
    qids = [e["qid"] for e in by_arm[arms[0]]]
    lines = [
        "## 逐题得分对照",
        "",
        f"> 每题各臂的答对 / 答案 / 指标（{len(qids)} 题 × {len(arms)} 臂）。看哪题谁答对、谁省 token、谁卡住。",
        "",
    ]
    for qid in qids:
        eps = {a: next(e for e in by_arm[a] if e["qid"] == qid) for a in arms}
        e0 = eps[arms[0]]
        lines += [
            f"### {qid} · {e0['type']}",
            f"**题**：{e0['query']}  ·  **gold**：{', '.join(e0['gold'])}",
            "",
            "| 臂 | 答对 | 答案（节选） | tokens | llm_calls | tool_steps | 耗时s | 截断 |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for a in arms:
            e = eps[a]
            ans = (e.get("answer") or "").replace("|", "/").replace("\n", " ").strip()[:48]
            mark = "✓" if e["correct"] else "✗"
            trunc = "⚠卡住" if e["truncated"] else ""
            lines.append(f"| `{a}` | {mark} | {ans} | {e['total_tokens']} | "
                         f"{e['llm_calls']} | {e['tool_steps']} | {e['wall_clock_s']} | {trunc} |")
        lines.append("")
    return lines


def _config_md(arm: str, cfg: dict) -> str:
    skills = cfg.get("skills", [])
    lines = [f"# 臂 `{arm}` 配置", "", f"**工具**：{', '.join(cfg['tools'])}",
             f"**注入 skills**：{', '.join(skills) or '（无）'}"]
    for s in skills:
        lines.append(f"\n---\n## 注入的 skill：{s}\n（详见 `eval/arms/skills_bundled/{s}.md`）")
    return "\n".join(lines) + "\n"


def _clean_episode(ep: dict) -> dict:
    """episode.json：去掉 session/thinking（单独落 jsonl/md/episode.md），留指标 + 逐步 tool。"""
    return {k: v for k, v in ep.items() if k not in ("session", "thinking")}


def _episode_md(ep: dict) -> str:
    """人可读的对话+思考 markdown（session 逐轮渲染，便于审核完整过程）。"""
    lines = [
        f"# {ep['qid']} · {ep['type']} · arm: `{ep['arm']}`",
        "",
        f"**题**：{ep['query']}  ·  **gold**：{', '.join(ep['gold'])}",
        f"**答对**：{'✓' if ep['correct'] else '✗'}  ·  **答案**：{(ep.get('answer') or '')[:120]}",
        f"**指标**：tokens={ep['total_tokens']} · llm_calls={ep['llm_calls']} · "
        f"tool_steps={ep['tool_steps']} · 耗时={ep['wall_clock_s']}s · "
        f"截断={'⚠是' if ep.get('truncated') else '否'}",
        "",
        "---",
        "",
    ]
    for turn in ep.get("session", []):
        role = turn.get("role", "")
        content = turn.get("content")
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        if not isinstance(content, list):
            content = [content]
        for b in content:
            if not isinstance(b, dict):
                lines.append(str(b)[:200])
                lines.append("")
                continue
            bt = b.get("type", "text")
            if role == "user":
                if bt == "tool_result":
                    txt = str(b.get("content", b.get("text", "")))[:600]
                    lines.append(f"**📋 工具结果**：\n```\n{txt}\n```")
                elif bt == "text":
                    lines.append(f"**👤 用户**：{b.get('text', '')[:200]}")
            elif role == "assistant":
                if bt == "thinking":
                    lines.append(f"> 💭 **思考**：{b.get('text', '')[:300]}")
                elif bt == "tool_use":
                    name = b.get("name", "?")
                    inp = json.dumps(b.get("input", {}), ensure_ascii=False)[:80]
                    lines.append(f"**🔧 `{name}`**({inp})")
                elif bt == "text":
                    txt = b.get("text", "").strip()
                    if txt:
                        lines.append(f"**🤖 Agent**：{txt[:300]}")
            lines.append("")
    return "\n".join(lines) + "\n"


def write_compare_report(result: dict, report_root: str) -> str:
    """把 run_compare 结果写成目录报告。返报告根目录。"""
    out = Path(report_root)
    out.mkdir(parents=True, exist_ok=True)
    arms = result["arms"]
    by_arm = result["episodes_by_arm"]

    aggregates = {a: _aggregate(by_arm[a]) for a in arms}
    for arm in arms:
        arm_dir = out / "arms" / arm
        arm_dir.mkdir(parents=True, exist_ok=True)
        (arm_dir / "config.md").write_text(_config_md(arm, ab_tools.arm_config(arm)), encoding="utf-8")
        (arm_dir / "aggregate.json").write_text(json.dumps(aggregates[arm], ensure_ascii=False, indent=2), encoding="utf-8")
        for ep in by_arm[arm]:
            edir = arm_dir / "episodes" / ep["qid"]
            edir.mkdir(parents=True, exist_ok=True)
            (edir / "episode.json").write_text(json.dumps(_clean_episode(ep), ensure_ascii=False, indent=2), encoding="utf-8")
            (edir / "session.jsonl").write_text(
                "\n".join(json.dumps(m, ensure_ascii=False) for m in ep["session"]) + "\n", encoding="utf-8")
            (edir / "thinking.md").write_text(
                "# thinking\n\n" + "\n\n---\n\n".join(ep["thinking"] or ["(无 thinking 捕获)"]) + "\n", encoding="utf-8")
            (edir / "episode.md").write_text(_episode_md(ep), encoding="utf-8")

    summary = _summary_matrix(arms, aggregates, result)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "result.md").write_text(_result_md(result, aggregates), encoding="utf-8")
    return str(out)
