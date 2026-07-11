"""记忆侧评测测试（task 4.2 / 4.3）。

四项，零外部依赖（mock mempalace CLI / 不连真 palace）：
  test_mempalace_parser      — 录样锁 mempalace search 文本格式
  test_routing_accuracy      — D1 router 对 ROUTING_GOLD 的四类准确率
  test_memory_recall_smoke   — L2 端到端：mock search → run() aggregate 预期
  test_gold_memory_snapshot  — gold 集 drift 门禁
"""
from eval.gold_memory import RECALL_GOLD, ROUTING_GOLD, LAYERS
from eval.routing import route, routing_accuracy
from eval.subjects_memory import parse_search_output

# ── 录样：真实 mempalace search 输出片段（2 结果 + 分隔线），锁格式 ──
_SAMPLE = """
============================================================
  Results for: "记忆层 MemPalace 替换 Mem0"
============================================================

  [1] wing_api / technical
      Source: agent-memory-approach.md
      Match:  cosine_sim=0.529  bm25=1.185

      **Why:** 现有 5 个记忆孤岛碎片化。

  ────────────────────────────────────────────────────────
  [2] wing_api / technical
      Source: f4c1e4e6-d496-4489-a33b-a9c43b6bdac8.jsonl
      Match:  cosine_sim=0.512  bm25=0.207

      "我喜欢简洁代码") 存一条。
"""


def test_mempalace_parser():
    """锁 mempalace search 文本格式：rank/wing/room/source/sim/bm25 全解析对。"""
    res = parse_search_output(_SAMPLE)
    assert len(res) == 2
    assert res[0]["rank"] == 1
    assert res[0]["wing"] == "wing_api"
    assert res[0]["room"] == "technical"
    assert res[0]["source_file"] == "agent-memory-approach.md"
    assert res[0]["cosine_sim"] == 0.529
    assert res[0]["bm25_score"] == 1.185
    assert "记忆孤岛" in res[0]["text"]
    assert res[1]["source_file"] == "f4c1e4e6-d496-4489-a33b-a9c43b6bdac8.jsonl"
    assert res[1]["cosine_sim"] == 0.512
    # 边界：空 / 无 [N] 头 → []
    assert parse_search_output("") == []
    assert parse_search_output("Results for: x\n====\n(无结果)") == []


def test_routing_accuracy():
    """D1 router 对 ROUTING_GOLD：四类全覆盖 + 总体达标。"""
    res = routing_accuracy([(f, g) for f, g, _ in ROUTING_GOLD])
    assert res["n"] == len(ROUTING_GOLD)
    # 四类都被测到
    assert set(res["per_class"]) == set(LAYERS)
    # 总体达标（D1 规则在标注集上可操作）
    assert res["overall"] >= 0.85
    # 清晰样例逐条断言
    assert route("用户偏好工具装全局") == "subjective"
    assert route("2026-07-11 归档了 change") == "episodic"
    assert route("部署用 uv tool install") == "procedural"
    assert route("接口返回 node 和 file 字段") == "objective"


def test_memory_recall_smoke(monkeypatch):
    """L2 端到端：mock mempalace_search（命中 gold）→ run() aggregate 预期。"""
    import eval.run_memory_baseline as rm
    from eval.repro import Lockfile

    def fake_search(query, limit=10, wing=None, room=None):
        # 返回每个 gold source 各一条 → recall@k=1（含多 gold 项）
        for q, gold in rm.RECALL_GOLD:
            if q == query:
                return [{"rank": i + 1, "wing": "w", "room": "r",
                         "source_file": sf, "cosine_sim": 0.5, "bm25_score": 1.0,
                         "text": "..."} for i, sf in enumerate(gold)]
        return []

    monkeypatch.setattr(rm, "mempalace_search", fake_search)
    monkeypatch.setattr(rm, "detect_lockfile", lambda: Lockfile(mempalace_version="test"))

    report = rm.run()
    assert report["n"] == len(RECALL_GOLD)
    assert report["aggregate"]["mean_hit@5"] == 1.0           # mock 全命中
    assert report["aggregate"]["mean_recall@5"] == 1.0
    assert report["aggregate"]["mean_unique_source_ratio@5"] == 1.0  # 单条无冗余
    assert report["aggregate"]["routing_overall_accuracy"] >= 0.85
    assert report["lockfile"]["mempalace_version"] == "test"


def test_gold_memory_snapshot():
    """gold 集 drift 门禁：规模 + 首条稳定（防意外增删 gold）。"""
    assert len(RECALL_GOLD) == 15
    assert len(ROUTING_GOLD) == 13
    # 首条 query 稳定
    assert RECALL_GOLD[0][0] == "记忆层选型 MemPalace 还是 Mem0"
    assert "agent-memory-approach.md" in RECALL_GOLD[0][1]
    # 路由首条
    assert ROUTING_GOLD[0][1] == "objective"
    # 四类各至少 3 条
    counts = {l: sum(1 for _, g, _ in ROUTING_GOLD if g == l) for l in LAYERS}
    assert all(c >= 3 for c in counts.values()), counts
