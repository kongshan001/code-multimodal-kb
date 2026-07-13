"""一次性迁移：eval/gold_*.py → eval/targets/<id>/{target.json, problems.json}。

受控 big-bang（design C1）。读 6 个旧 gold 模块，生成 5 个 target 目录。
deterministic id = <target_id>-<slug(query/fact 前3词)>，撞名加 -2/-3。

用法（repo 根）：python -m eval.migrate_gold
幂等：重跑覆盖已有 target.json/problems.json。迁移完可删本脚本。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from eval import gold_code, gold_crosstool, gold_docs, gold_godot, gold_memory

TARGETS_DIR = Path(__file__).resolve().parent / "targets"
TARGETS_DIR.mkdir(parents=True, exist_ok=True)


# ── slug + 稳定 id ────────────────────────────────────────────────────────
_TOKEN = re.compile(r"[A-Za-z0-9一-鿿]+")


def _slug(text: str, n: int = 3) -> str:
    """text → lowercase kebab slug（前 n 个 token；CJK 视作 token 连串）。"""
    tokens = _TOKEN.findall(text.lower())
    return "-".join(tokens[:n]) or "q"


def _assign_ids(target_id: str, problems: list[dict]) -> None:
    """给每题分配稳定 id = <target_id>-<slug(text)>，撞名 -2/-3。就地改 problems。"""
    seen: dict[str, int] = {}
    for p in problems:
        text = p.get("fact") or p.get("query") or ""
        base = f"{target_id}-{_slug(text)}"
        if base in seen:
            seen[base] += 1
            pid = f"{base}-{seen[base]}"
        else:
            seen[base] = 1
            pid = base
        p["id"] = pid


# ── 写出 helpers ──────────────────────────────────────────────────────────
def _write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_target(target_id: str, target: dict, problems: list[dict],
                  local_example: dict) -> None:
    _assign_ids(target_id, problems)
    d = TARGETS_DIR / target_id
    _write_json(d / "target.json", target)
    _write_json(d / "problems.json", {"version": 1, "target": target_id, "problems": problems})
    _write_json(d / "target.local.example.json", local_example)


# ── 5 个 target 迁移 ──────────────────────────────────────────────────────
def migrate_godot_core() -> int:
    problems = [
        {"type": "code_retrieval", "query": q, "gold": {"symbols": sorted(s)}, "status": "accepted"}
        for q, s in gold_godot.GOLD
    ]
    target = {
        "id": "godot-core", "language": "C++", "subjects": ["code_retrieval"],
        "code": {"codegraph_root": "/Users/ks_128/Documents/godot-src/core",
                 "cmm_project": gold_godot.PROJECT},
        "notes": "Godot 4.7 core/, 13504 节点 / 38470 边（原 gold_godot）",
    }
    local = {"code": {"codegraph_root": "/your/path/to/godot-src/core",
                      "cmm_project": "your-cmm-project-name"}}
    _write_target("godot-core", target, problems, local)
    return len(problems)


def migrate_graphify_pkg() -> int:
    problems = [
        {"type": "code_retrieval", "query": q, "gold": {"symbols": sorted(s)}, "status": "accepted"}
        for q, s in gold_code.GOLD
    ]
    target = {
        "id": "graphify-pkg", "language": "Python", "subjects": ["code_retrieval"],
        "code": {"cmm_project": gold_code.PROJECT},
        "notes": "graphify 包源码，775 函数 / 4979 边（原 gold_code）",
    }
    local = {"code": {"cmm_project": "your-cmm-project-name-for-graphify"}}
    _write_target("graphify-pkg", target, problems, local)
    return len(problems)


def migrate_godot_docs() -> int:
    problems = [
        {"type": "doc_retrieval", "query": q, "gold": {"node_labels": sorted(s)}, "status": "accepted"}
        for q, s in gold_docs.GOLD
    ]
    target = {
        "id": "godot-docs", "language": "rst", "subjects": ["doc_retrieval"],
        "doc": {"graph": gold_docs.GRAPH},
        "notes": "Godot 文档子集图 17 rst → 72 节点（原 gold_docs）",
    }
    local = {"doc": {"graph": "/your/path/to/godot-docs-subset/graphify-out/graph.json"}}
    _write_target("godot-docs", target, problems, local)
    return len(problems)


def migrate_godot_cross() -> int:
    problems = [
        {"type": "cross_anchor", "query": concept,
         "gold": {"doc_node_label": doc_lbl, "cmm_identifier": cmm_id, "code_file": code_f},
         "status": "accepted"}
        for (concept, doc_lbl, cmm_id, code_f) in gold_crosstool.GOLD
    ]
    target = {
        "id": "godot-cross", "subjects": ["cross_anchor"],
        "deps": {"doc_graph": "godot-docs", "cmm": "godot-core"},
        "notes": "graphify 文档概念 → cmm 代码定位（原 gold_crosstool）",
    }
    # cross 的机器路径经 deps 间接取（godot-docs.graph + godot-core.code），local 示例留空提示
    local = {"_comment": "cross 经 deps 解析 godot-docs/godot-core 的 local overlay，本目录一般无需 local"}
    _write_target("godot-cross", target, problems, local)
    return len(problems)


# memory gold 的 2 条诚实探针（gold_memory.py 注释明示）——把注释转成 tags 数据
_MEM_PROBE_MARKERS = ("记忆四层归属判定", "文档答案质量 faithfulness")


def migrate_engineer_demo_memory() -> tuple[int, int]:
    recall = []
    for q, files in gold_memory.RECALL_GOLD:
        p = {"type": "memory_recall", "query": q,
             "gold": {"source_files": sorted(files)}, "status": "accepted"}
        if any(m in q for m in _MEM_PROBE_MARKERS):
            p["tags"] = ["known_weak_probe"]
            p["notes"] = "诚实探针：答案原文未 mine，预期召回偏弱（原 gold_memory 注释）"
        recall.append(p)
    routing = [
        {"type": "memory_routing", "fact": fact,
         "gold": {"layer": layer, "signal": signal}, "status": "accepted"}
        for (fact, layer, signal) in gold_memory.ROUTING_GOLD
    ]
    problems = recall + routing
    target = {
        "id": "engineer-demo-memory",
        "subjects": ["memory_recall", "memory_routing"],
        "memory": {"palace": "engineer_demo"},
        "notes": "自指 demo target：engineer_demo 自己的 memory 层（原 gold_memory）。"
                 "不可移植——fork 后建议删/换。recall 锚 memory 文件 + 会话 jsonl。",
    }
    local = {"memory": {"palace": "your-mempalace-project-name"}}
    _write_target("engineer-demo-memory", target, problems, local)
    return len(recall), len(routing)


def main() -> None:
    counts = {
        "godot-core (code_retrieval)": migrate_godot_core(),
        "graphify-pkg (code_retrieval)": migrate_graphify_pkg(),
        "godot-docs (doc_retrieval)": migrate_godot_docs(),
        "godot-cross (cross_anchor)": migrate_godot_cross(),
    }
    rec, rout = migrate_engineer_demo_memory()
    counts["engineer-demo-memory (recall)"] = rec
    counts["engineer-demo-memory (routing)"] = rout

    total = sum(counts.values())
    print("迁移完成 → eval/targets/")
    for k, v in counts.items():
        print(f"  {k:42} {v:>3} 题")
    print(f"  {'合计':42} {total:>3} 题")
    print("\n题数守恒对照（旧 test_gold_regression 断言）：")
    print("  godot 26 / code 21 / docs 10 / cross 8 / memory recall 15 + routing 13 = 93")


if __name__ == "__main__":
    main()
