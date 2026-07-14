"""agent-compare 报告写器 + smoke 流水线测试（零真实 LLM）。"""
import json

from eval import ab_tools
from eval.agent_compare_report import write_compare_report
from eval.run_ab_agent import run_compare


def test_smoke_pipeline_produces_complete_directory(tmp_path):
    """smoke 模式（mock LLM）跑通 4 臂 → 目录报告结构完整。"""
    arms = ("no-kb", "kb", "kb+superpowers", "kb+openspec")
    result = run_compare("godot-core", arms=arms, runs=1, subset=3, smoke=True)
    assert result["smoke"] is True
    assert result["model"] == "mock"
    assert set(result["episodes_by_arm"]) == set(arms)

    out = tmp_path / "report"
    root = write_compare_report(result, str(out))

    # 顶层结论类
    for f in ("conclusion.md", "summary.json", "matrix.md"):
        assert (out / f).is_file(), f"缺 {f}"

    # 每臂：config + aggregate + episodes/*/episode.json
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert set(summary["arms"]) == set(arms)
    assert "context_compression_kb_vs_no_kb" in summary  # KB vs 无 KB 派生指标
    for arm in arms:
        ad = out / "arms" / arm
        assert (ad / "config.md").is_file()
        ag = json.loads((ad / "aggregate.json").read_text(encoding="utf-8"))
        # 指标齐全
        for k in ("accuracy", "mean_total_tokens", "mean_llm_calls",
                  "mean_tool_steps", "mean_wall_clock_s", "tool_diversity"):
            assert k in ag, f"{arm} aggregate 缺 {k}"
        # episodes：每题 episode.json
        eps = list((ad / "episodes").glob("q*/episode.json"))
        assert len(eps) == 3, f"{arm} 应有 3 个 episode"


def test_conclusion_has_honest_boundaries(tmp_path):
    """conclusion.md 必含诚实边界标注（self-preference / SOP-not-runtime / 样本量）。"""
    result = run_compare("godot-core", arms=("no-kb", "kb"), runs=1, subset=2, smoke=True)
    out = tmp_path / "r"
    write_compare_report(result, str(out))
    txt = (out / "conclusion.md").read_text(encoding="utf-8")
    assert "self-preference" in txt
    assert "非完整 Claude Code skill 运行时" in txt or "SOP" in txt
    assert "SMOKE" in txt  # smoke 模式标注


def test_skills_arm_config_shows_injected_skill():
    """skills 臂 config 含注入的 skill 名。"""
    cfg = ab_tools.arm_config("kb+superpowers")
    assert cfg["skills"] == ["superpowers"]
    assert "cmm_search" in cfg["tools"]
    cfg2 = ab_tools.arm_config("no-kb")
    assert cfg2["skills"] == []
