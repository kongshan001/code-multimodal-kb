"""文档答案质量评测（task 3.2/3.3）：graphify 文档检索 vs naive grep，BigModel 当 LLM judge。

三维：
  - faithfulness（graphify 答案是否被参考答案支持）
  - relevancy（是否切题）
  - head-to-head（graphify vs naive grep，谁更全面）—— 复刻 MS GraphRAG LLM grader 思路
复用 BigModel key（eval/llm.py），免装 deepeval。target = Godot 渲染文档图。
用法：python -m eval.run_doc_quality
"""
from __future__ import annotations

import json
import pathlib
import subprocess

from eval.llm import complete

GRAPH = "/Users/ks_128/Documents/godot-render-docs/graphify-out/graph.json"
DOCS_DIR = pathlib.Path("/Users/ks_128/Documents/godot-render-docs")

# gold Q&A（Godot 渲染，取自 render-docs 实际内容）
QA: list[tuple[str, str]] = [
    ("Godot 有哪几种渲染器？", "Forward+、Mobile、Compatibility 三种渲染器"),
    ("渲染底层用了哪些图形 API 或驱动？", "通过 RenderingDevice 抽象层，支持 Vulkan、Direct3D 12、Metal、OpenGL"),
    ("用户如何扩展渲染管线？", "用 CompositorEffect，挂到 Compositor 资源上，设回调类型和回调函数，把 Compositor 赋给 WorldEnvironment/Camera3D/Viewport"),
    ("Compositor 和 CompositorEffect 是什么关系？", "Compositor 持有一组 CompositorEffect；每个 CompositorEffect 在渲染管线某阶段通过回调被调用"),
    ("哪些节点或资源可以挂 Compositor？", "WorldEnvironment、Camera3D、Viewport"),
]


def graphify_answer(q: str) -> str:
    r = subprocess.run(["graphify", "query", q, "--graph", GRAPH, "--budget", "800"],
                       capture_output=True, text=True, timeout=90)
    lines = [l for l in r.stdout.splitlines() if l.startswith(("NODE ", "EDGE "))]
    return "\n".join(lines[:12]) or "(空)"


def naive_answer(q: str) -> str:
    """naive 基线：在 .rst 里 grep 问题关键词，返回命中行。"""
    import re
    kws = [w for w in re.findall(r"[A-Za-z一-龥]{2,}", q) if len(w) >= 2][:4]
    pat = "|".join(kws)
    r = subprocess.run(["grep", "-riE", pat, *DOCS_DIR.glob("*.rst")],
                       capture_output=True, text=True, timeout=30)
    hits = [l.strip() for l in r.stdout.splitlines() if l.strip()][:6]
    return "\n".join(hits) or "(空)"


def judge_yn(criterion: str) -> bool:
    return criterion.strip().upper().startswith("Y")


def run() -> dict:
    rows = []
    for q, ref in QA:
        g_ans, n_ans = graphify_answer(q), naive_answer(q)

        faith = complete(
            f"参考答案：{ref}\n待判答案：{g_ans}\n问：待判答案是否被参考答案支持、无编造？只回 YES 或 NO。")
        rel = complete(
            f"问题：{q}\n答案：{g_ans}\n问：答案是否切题回答了问题？只回 YES 或 NO。")
        h2h = complete(
            f"问题：{q}\n答案A（图检索）：{g_ans}\n答案B（关键词grep）：{n_ans}\n问：哪个更全面(comprehensive)？只回 A 或 B。")

        rows.append({"q": q, "ref": ref,
                     "faithful": judge_yn(faith), "relevant": judge_yn(rel),
                     "h2h_winner": "A" if h2h.strip().upper().startswith("A") else ("B" if h2h.strip().upper().startswith("B") else "?"),
                     "graphify_ans_head": g_ans[:80]})

    n = len(rows)
    return {"subject": "doc answer quality (graphify vs naive, BigModel judge)", "n": n,
            "faithfulness": round(sum(r["faithful"] for r in rows) / n, 3),
            "relevancy": round(sum(r["relevant"] for r in rows) / n, 3),
            "graphify_win_rate": round(sum(1 for r in rows if r["h2h_winner"] == "A") / n, 3),
            "per_query": rows}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
