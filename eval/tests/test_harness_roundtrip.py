"""task 1.1 验证：harness 能调通 cmm 跑一个 round-trip。"""
import pytest

from eval.harness import EvalRecord, EvalRun, run_dataset
from eval.subjects import cmm_available, cmm_list_projects


def test_cmm_roundtrip():
    """cmm 已装则 list_projects 返回列表且含本机已索引的 graphify；未装则 skip。"""
    if not cmm_available():
        pytest.skip("cmm 未安装（非本机环境）")
    projects = cmm_list_projects()
    assert isinstance(projects, list)
    assert any("graphify" in p.get("name", "") for p in projects), "应含已索引的 graphify 项目"


def test_harness_collects_records():
    """harness 对合成数据集收集 (query,result,gold) 记录。"""
    dataset = [
        {"query": "重试逻辑", "gold": ["retry", "backoff"]},
        {"query": "认证", "gold": ["auth"]},
    ]
    subject_fn = lambda q: [q + "_sym"]  # 假 subject
    run = run_dataset(subject_fn, dataset, subject_name="fake")
    assert run.subject == "fake"
    assert len(run.records) == 2
    assert isinstance(run.records[0], EvalRecord)
    assert run.records[0].gold == ["retry", "backoff"]
    assert '"subject": "fake"' in run.to_json()


def test_evalrecord_meta_default():
    rec = EvalRecord(query="q", result="r", gold=["g"])
    assert rec.meta == {}
    run = EvalRun(subject="s")
    run.add(rec)
    assert len(run.records) == 1
