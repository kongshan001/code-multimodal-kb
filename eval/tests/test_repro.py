"""task 1.2 验证：lockfile 能探测版本 + 盖进报告。"""
from eval.repro import Lockfile, detect_lockfile, stamp


def test_stamp_adds_lockfile_to_report():
    report = {"subject": "code", "recall@5": 0.7}
    stamped = stamp(report, Lockfile(temperature=0.0, cmm_version="0.8.1"))
    assert "lockfile" in stamped
    assert stamped["lockfile"]["temperature"] == 0.0
    assert stamped["lockfile"]["cmm_version"] == "0.8.1"
    # 不污染原 report
    assert "lockfile" not in report


def test_detect_lockfile_runs():
    lock = detect_lockfile()
    # 本机装了 cmm → 应测出版本号（非 unknown / not-installed）
    assert lock.cmm_version not in ("",)
    assert isinstance(lock.temperature, float)
