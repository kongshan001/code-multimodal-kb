"""task 3.1 端到端 smoke + 3.2 留底机制测试。

零外部依赖：mock 检索与 lockfile，不依赖真 cmm / graphify / Godot。
"""
from eval.repro import Lockfile


def _isolate(monkeypatch, tmp_path):
    """把 archive 路径隔离到 tmp_path，不污染真 eval/reports/archive/。"""
    import eval.archive as A
    monkeypatch.setattr(A, "_REPO_ROOT", tmp_path)
    monkeypatch.setattr(A, "ARCHIVE_DIR", tmp_path / "eval" / "reports" / "archive")
    monkeypatch.setattr(A, "INDEX_PATH", tmp_path / "eval" / "reports" / "archive" / "index.json")
    return A


def test_code_baseline_end_to_end_smoke(monkeypatch, tmp_path):
    """L2: mock 检索 → 跑 run() → aggregate 预期区间 + 归档文件生成。"""
    import eval.run_code_baseline as rc
    A = _isolate(monkeypatch, tmp_path)

    monkeypatch.setattr(rc, "load_gold", lambda target: ("proj", [("color", {"Color"})]))
    monkeypatch.setattr(rc, "_retrieve",
                        lambda method, project, query: [{"node": "Color", "file": "color.cpp"}])
    monkeypatch.setattr(rc, "detect_lockfile", lambda: Lockfile(cmm_version="test"))

    report = rc.run(target="code", method="bm25")
    assert report["n"] == 1
    assert report["aggregate"]["mean_broad_recall@5"] == 1.0      # Color 命中
    assert report["aggregate"]["mean_recall@5"] == 1.0             # strict 也命中
    assert report["lockfile"]["cmm_version"] == "test"

    res = A.archive_report(report, variant="test")
    assert (tmp_path / "eval" / "reports" / "archive" / f"{res['id']}.json").exists()
    g = A.get_report(res["id"])
    assert g["aggregate"]["mean_broad_recall@5"] == 1.0


def test_archive_no_overwrite(monkeypatch, tmp_path):
    """L3: 同 subject+variant 连续归档两次 → 两文件 + index 两条 + 不覆盖。"""
    A = _isolate(monkeypatch, tmp_path)
    fake = {"subject": "cmm.bm25", "target": "godot", "n": 1,
            "aggregate": {"mean_broad_recall@5": 0.846}, "per_query": []}
    r1 = A.archive_report(fake, variant="v")
    r2 = A.archive_report(fake, variant="v")
    assert r1["id"] != r2["id"]                                   # 不覆盖
    reports = [f for f in A.ARCHIVE_DIR.glob("*.json") if f.name != "index.json"]
    assert len(reports) == 2
    assert len(A.list_reports()) == 2
    assert (A.ARCHIVE_DIR / f"{r1['id']}.json").exists()          # 既有文件仍在


def test_normalize_cross_tool_fills_lockfile_and_aggregate():
    """cross-tool report 无 lockfile / aggregate → normalize 补齐。"""
    from eval.archive import normalize_report
    fake = {"subject": "cross-tool", "n": 8, "graphify_hit_rate": 1.0,
            "cmm_hit_rate@5": 1.0, "crosstool_success_rate": 1.0, "per_query": []}
    norm = normalize_report(fake, variant="godot")
    assert "lockfile" in norm
    assert norm["aggregate"]["crosstool_success_rate"] == 1.0
    assert norm["n"] == 8
