"""Stage 0 token 代理（task 6.1）：agent 级 A/B 的零 LLM 代理指标。

对 gold_godot 每题量两臂注入的 context 成本与命中：
  Arm B (KB)    — cmm bm25 top-5：注入 token 数 + 是否命中 gold 符号（kb_hit@5）
  Arm A (grep)  — 朴素 grep：文件名清单 token + 读 top 文件 token（naive-RAG 真实成本）
指标：context 压缩比（naive_read / kb）、kb_hit@5、mean tokens、token-per-hit、grep 盲区率。

零 LLM（cmm 检索 + grep + char/4 token 估算）。复用 gold_godot（符号 gold，零 judge 判分）。
Stage 1（全 agent 准确度 + 端到端 token）卡 LLM 凭据，见 design §F。

用法：
  python -m eval.run_ab_value
  bench run ab
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import statistics
import subprocess

from eval.repro import detect_lockfile, stamp
from eval.subjects import cmm_bm25, norm_item

PROJECT = "Users-ks_128-Documents-godot-src-core"
GODOT_CORE = "/Users/ks_128/Documents/godot-src/core"
KS = (1, 3, 5)
NAIVE_MAX_FILES = 3      # 朴素 agent 读 top-3 grep 命中文件
NAIVE_PER_FILE_CAP = 4000  # 每文件截断 chars（~1000 token）


def _tok(s: str) -> int:
    """char/4 粗估 token（Stage 1 用 API usage 精确替代）。"""
    return max(1, len(s) // 4)


def _broad_text(it: dict) -> str:
    """同 run_code_baseline.broad 口径：node+qualified_name+file 去非字母数字小写化。"""
    return "".join(c.lower() for c in
                   str(it.get("node", "") + it.get("qualified_name", "") + it.get("file", ""))
                   if c.isalnum())


def _grep_files(query: str) -> list[str]:
    """朴素 grep -rl <query>（大小写不敏感，.h/.cpp/.hpp）。返回命中文件路径。"""
    try:
        out = subprocess.run(
            ["grep", "-rli", query, GODOT_CORE, "--include=*.h", "--include=*.cpp",
             "--include=*.hpp"],
            capture_output=True, text=True, timeout=60,
        ).stdout.strip()
        return [ln for ln in out.splitlines() if ln]
    except Exception:
        return []


def _read_capped(paths: list[str]) -> str:
    """读 top-NAIVE_MAX_FILES 个文件，每文件截断 NAIVE_PER_FILE_CAP chars。"""
    out = []
    for p in paths[:NAIVE_MAX_FILES]:
        try:
            out.append(open(p, errors="ignore").read(NAIVE_PER_FILE_CAP))
        except Exception:
            continue
    return "\n".join(out)


def _grep_read_cost(query: str) -> dict:
    """Arm A 朴素 grep 的注入成本：文件名清单 + 读文件内容。"""
    files = _grep_files(query)
    list_ctx = "\n".join(files)
    read_ctx = _read_capped(files)
    return {
        "file_count": len(files),
        "list_tokens": _tok(list_ctx),
        "read_tokens": _tok(read_ctx),   # naive agent 真要答问题得读到的内容量
        "grep_miss": len(files) == 0,
    }


def run(target: str = "godot") -> dict:
    gold_mod = importlib.import_module(f"eval.gold_{target}")
    gold = gold_mod.GOLD

    rows = []
    for query, goldset in gold:
        # Arm B: KB
        kb_raw = [r for r in cmm_bm25(PROJECT, query, 5) if isinstance(r, dict)]
        kb_items = [norm_item(r) for r in kb_raw]
        kb_ctx = json.dumps(kb_items, ensure_ascii=False)
        kb_tokens = _tok(kb_ctx)
        kb_names = [it["node"] for it in kb_items]
        # kb_hit@k：gold 是否在 top-k 返回项的 broad 文本里（node+qualified_name+file，与
        # run_code_baseline.broad_recall 同口径，保证与既有 broad@5=0.846 可比）
        hit = {}
        for k in KS:
            topk_text = [_broad_text(it) for it in kb_items[:k]]
            hit[f"kb_hit@{k}"] = round(
                sum(1 for g in goldset
                    if any(_broad_text({"node": g}) in t for t in topk_text))
                / max(1, len(goldset)), 3)

        # Arm A: naive grep
        naive = _grep_read_cost(query)

        compression = round(naive["read_tokens"] / kb_tokens, 2) if kb_tokens else 0.0
        rows.append({
            "query": query,
            "gold": sorted(goldset),
            "kb_top5": kb_names[:5],
            "kb_tokens": kb_tokens,
            "kb_hit@5": hit["kb_hit@5"],
            "naive_file_count": naive["file_count"],
            "naive_list_tokens": naive["list_tokens"],
            "naive_read_tokens": naive["read_tokens"],
            "compression_read": compression,
            "grep_miss": naive["grep_miss"],
        })

    n = len(rows)
    hit_qs = [r for r in rows if not r["grep_miss"]]  # 压缩比只在 grep 有命中时有意义
    agg = {
        "n": n,
        "mean_kb_tokens": round(statistics.mean(r["kb_tokens"] for r in rows), 1),
        "mean_naive_read_tokens": round(statistics.mean(r["naive_read_tokens"] for r in rows), 1),
        "mean_compression_read": round(
            statistics.mean(r["compression_read"] for r in hit_qs), 2) if hit_qs else 0,
        "mean_kb_hit@5": round(statistics.mean(r["kb_hit@5"] for r in rows), 3),
        "grep_miss_count": sum(1 for r in rows if r["grep_miss"]),
        "naive_max_files": NAIVE_MAX_FILES,
        "naive_per_file_cap_chars": NAIVE_PER_FILE_CAP,
    }

    report = stamp(
        {"subject": "ab-value-stage0", "target": target, "project": PROJECT,
         "n": n, "aggregate": agg, "per_query": rows,
         "stage": 0,
         "note": "Stage 0 token 代理：只证 KB 省 context token + 注入命中，不证 agent 答对率（Stage 1 凭据门控）"},
        detect_lockfile(),
    )
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="agent A/B Stage 0：KB vs 朴素 grep token 代理")
    ap.add_argument("--target", default="godot")
    args = ap.parse_args()
    print(json.dumps(run(args.target), ensure_ascii=False, indent=2))
