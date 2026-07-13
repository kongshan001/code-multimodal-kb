"""文档答案质量评测——Ragas 协议直接实现（faithfulness + context_precision）。

**为什么不用 ragas 库**：ragas 0.4.3 与 langchain_community 0.4 的 import 链冲突
（chat_models.vertexai 路径变），解依赖不划算。两个核心指标是公开的 LLM 判分协议，
直接复刻更稳，也与项目既有"复刻版"模式一致（见 design：run_doc_quality.py 复刻 DeepEval）。

**指标**（均 reference-free，不需标准答案）：
  faithfulness     答案拆 claims → 逐条判是否被 context 支撑 → supported/total（测幻觉）
  context_precision 每个 context chunk 判是否切题 → 相关比例（测检索精度）

**LLM**：cc-connect GLM（anthropic 兼容端点，glm-5.x，已验证通）。
**诚实边界**：GLM 生成 + GLM 判 = 同家族 self-preference（spec 反 LLM-judge 循环原则）。
  分数当**相对参考值**（改前后对比），非绝对回归值；与 grounded 分数分开报。

用法：bench run doc-ragas
"""
from __future__ import annotations

import json
import os
import re
import statistics

from eval._subproc import run_text
from eval.ab_agent import load_creds, make_client
from eval.repro import detect_lockfile, stamp
from eval.targets import load_problems, load_target

_MODEL = None
RST_DIR = "/Users/ks_128/Documents/godot-docs-subset"  # graphify 文档图源（17 篇 .rst）
_PER_DOC_CAP = 5000  # 每文档取前 N chars（覆盖到正文段落，非仅 intro）


def _doc_chunks(query: str, graph: str) -> list[str]:
    """graphify 定位节点（raw NODE 行，带 src=）→ 取 src 指向的 .rst 真实文本做可读 context。
    graphify 返图节点元数据（不可读），答案质量需要文档段落——故映射到源 .rst。"""
    out = run_text(["graphify", "query", query, "--graph", graph, "--budget", "800"],
                   timeout=30).stdout
    srcs = []
    for line in out.splitlines():
        if not line.startswith("NODE "):
            continue
        m = re.search(r"src=(\S+\.rst)", line)
        if m and m.group(1) not in srcs:
            srcs.append(m.group(1))
    chunks = []
    for src in srcs[:3]:  # top-3 不同文档
        p = os.path.join(RST_DIR, src)
        if os.path.exists(p):
            chunks.append(f"[{src}]\n" + open(p, errors="ignore").read(_PER_DOC_CAP))
    return chunks


def _llm_text(client, prompt: str, max_tokens: int = 512) -> str:
    """GLM 单轮文本。复用 ab_agent 的 anthropic→cc-connect 通路。"""
    global _MODEL
    if _MODEL is None:
        _, _, _MODEL = load_creds()
    r = client.messages.create(model=_MODEL, max_tokens=max_tokens, temperature=0.0,
                               messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")


def _extract_json(text: str):
    """防御：LLM 可能把 JSON 裹在 prose 里，抓首个 [...] 或 {...}。"""
    text = text.strip()
    for pat in (r"\[[\s\S]*\]", r"\{[\s\S]*\}"):
        m = re.search(pat, text)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                continue
    return None


def faithfulness(answer: str, context: str, client) -> dict:
    """Ragas faithfulness 协议：拆 claims → 逐条判是否被 context 支撑。"""
    claims = _extract_json(_llm_text(client,
        f"把下面答案拆成原子事实 claims。只输出 STRICT JSON 字符串数组，不要别的。\n答案：{answer}\nJSON:")) or []
    if not isinstance(claims, list) or not claims:
        return {"score": 1.0, "n_claims": 0, "n_supported": 0, "note": "无 claim（空答/非事实）= 视为 1.0"}
    verdicts = _extract_json(_llm_text(client,
        f"逐条判断每个 claim 是否被 context 支撑（entailment）。只输出 STRICT JSON：数组，每元素 {{\"claim\":..., \"supported\": true/false}}。\n"
        f"context：{context}\nclaims：{json.dumps(claims, ensure_ascii=False)}\nJSON:")) or []
    if isinstance(verdicts, list) and verdicts:
        n_sup = sum(1 for v in verdicts if (v.get("supported") if isinstance(v, dict) else False))
        return {"score": round(n_sup / len(verdicts), 3), "n_claims": len(verdicts), "n_supported": n_sup}
    return {"score": 0.0, "n_claims": len(claims), "n_supported": 0, "note": "判分解析失败"}


def context_precision(query: str, chunks: list[str], client) -> dict:
    """Ragas context_precision 协议：每个 chunk 判是否切题 → 相关比例。"""
    if not chunks:
        return {"score": 0.0, "n_chunks": 0}
    indexed = [{"i": i, "text": c[:300]} for i, c in enumerate(chunks)]
    verdicts = _extract_json(_llm_text(client,
        f"逐个 chunk 判断它对回答 query 是否相关（relevant）。只输出 STRICT JSON：数组，每元素 {{\"i\":..., \"relevant\": true/false}}。\n"
        f"query：{query}\nchunks：{json.dumps(indexed, ensure_ascii=False)}\nJSON:")) or []
    rel_map = {v["i"]: v["relevant"] for v in verdicts if isinstance(v, dict) and "i" in v} if isinstance(verdicts, list) else {}
    n_rel = sum(1 for i in range(len(chunks)) if rel_map.get(i, False))
    return {"score": round(n_rel / len(chunks), 3), "n_chunks": len(chunks), "n_relevant": n_rel}


def _generate_answer(query: str, context: str, client) -> str:
    """GLM 用 context 答 query（被评判的 RAG 答案）。强制尽力作答（不轻易 refusal，否则 faithfulness 空洞）。"""
    return _llm_text(client,
        f"根据下面 context **尽力回答**问题，只答 context 支撑的内容，2-4 句。不要轻易说\"context 不足\"——"
        f"只要 context 有相关信息就组织成答案。\n问题：{query}\ncontext：{context}\n答案：",
        max_tokens=320).strip()


def run(target_id: str = "godot-docs", subset: int | None = None) -> dict:
    graph = load_target(target_id)["doc"]["graph"]
    problems = [p for p in load_problems(target_id) if p["type"] == "doc_retrieval"]
    questions = problems[:subset] if subset else problems
    client = make_client()

    rows = []
    for p in questions:
        query, goldset = p["query"], set(p["gold"]["node_labels"])
        chunks = _doc_chunks(query, graph)  # graphify 定位 → .rst 可读文本
        context = "\n".join(chunks) or "(无 context)"
        answer = _generate_answer(query, context, client)
        f = faithfulness(answer, context, client)
        c = context_precision(query, chunks, client)
        rows.append({"query": query, "gold": sorted(goldset), "answer": answer[:200],
                     "n_chunks": len(chunks), "faithfulness": f["score"],
                     "context_precision": c["score"]})
        print(f"  faithful={f['score']:.2f} ctx_prec={c['score']:.2f}  n_chunks={len(chunks)}  {query[:40]}", flush=True)

    agg = {
        "n": len(rows),
        "mean_faithfulness": round(statistics.mean(r["faithfulness"] for r in rows), 3),
        "mean_context_precision": round(statistics.mean(r["context_precision"] for r in rows), 3),
        "llm_judge": "glm-5.x（self-preference 风险，相对参考值）",
    }
    report = stamp(
        {"subject": "doc-quality-ragas-protocol", "target": target_id, "graph": graph,
         "n": len(rows), "aggregate": agg, "per_query": rows,
         "metrics": "faithfulness + context_precision（reference-free，Ragas 协议直接实现）",
         "note": "LLM-judged（GLM 生成+判分，同家族 self-preference）；相对参考值，非 grounded 回归值"},
        detect_lockfile(),
    )
    return report


if __name__ == "__main__":
    import argparse, json as _json
    ap = argparse.ArgumentParser(description="文档答案质量（Ragas 协议：faithfulness + context_precision）")
    ap.add_argument("--target", default="godot-docs")
    ap.add_argument("--subset", type=int, default=None)
    a = ap.parse_args()
    print(_json.dumps(run(a.target, a.subset), ensure_ascii=False, indent=2))
