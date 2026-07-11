"""D1 四层归属路由器（task 4.3）。

把 CLAUDE.md 的「记忆四层归属」判定实现成**规则级联**（signal-based 近似）。
D1 原文（金句）：忘了这条，agent 会不会做出用户必须纠正的事？
  - 会 → subjective（memory）   用户/工作方式/决策
  - 不会、但要被问起 → objective（KB）   代码/文档本身说了什么
  - 讲"怎么做" → procedural（skills）
  - 讲"何时发生" → episodic（git/tasks）

D1 本质按"后果/语义"判，非词面——纯规则只能近似。本实现用 lexical/structural
signal 做 cascade，准确率见 test_routing_accuracy + 报告（含"规则与标注同源"边界）。
"""
from __future__ import annotations

import re

LAYERS = ("objective", "procedural", "episodic", "subjective")

# ── signal 模式 ──
_DATE = re.compile(r"\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}|昨天|今天|上周|近日")
_SHA = re.compile(r"\b[0-9a-f]{7,40}\b")
_EVENT = re.compile(r"归档|提交了|同步了|装好|mine 了|完成了|落地|跑通|落地了|推送|push 了")
_SUBJECTIVE = re.compile(
    r"偏好|喜欢|决定|选型|走.+而非|用户|看重|工作方式|都要|每次.+都|推荐|倾向"
)
_PROCEDURAL = re.compile(
    r"部署|安装|步骤|如何|怎么|运行|用 .+ 命令|bench run|uv tool|init|--target|--method"
)
_OBJECTIVE = re.compile(
    r"返回|字段|属性|函数|接口|计算|节点|参数|类型|定义"
)


def route(fact: str) -> str:
    """对一条候选事实返回四层之一。cascade: subjective > episodic > procedural > objective(default)。

    subjective 先判：决策/偏好/工作方式（D1 首要测试）。决策 + 日期的复合事实，
    "决定/选型" 归 subjective（memory 存结论），纯事件（无决策词）归 episodic。
    """
    s = fact or ""

    # 决策/偏好/工作方式 → memory（首要）
    if _SUBJECTIVE.search(s) and not _pure_event(s):
        return "subjective"

    # 带日期/SHA 的纯事件 → git/tasks
    if _pure_event(s):
        return "episodic"

    # how-to/命令/步骤 → skills
    if _PROCEDURAL.search(s):
        return "procedural"

    # 代码/文档结构事实 → KB
    if _OBJECTIVE.search(s):
        return "objective"

    # 兜底：技术性陈述默认归客观
    return "objective"


def _pure_event(s: str) -> bool:
    """有日期/SHA 且无决策词 → 纯事件（归 episodic 而非 subjective）。"""
    if not (_DATE.search(s) or _SHA.search(s)):
        return False
    # 有决策词的带日期事实（如"7/11 决定走 X"）仍归 subjective（决策结论）
    if re.search(r"决定|选型|偏好", s):
        return False
    return bool(_EVENT.search(s)) or bool(_DATE.search(s) or _SHA.search(s))


def routing_accuracy(items: list[tuple[str, str]]) -> dict:
    """对 (fact, gold_layer) 集算逐类 + 总体准确率。返回 {overall, per_class, errors}。"""
    per_class: dict[str, list[bool]] = {l: [] for l in LAYERS}
    errors = []
    for fact, gold in items:
        pred = route(fact)
        ok = pred == gold
        per_class.setdefault(gold, []).append(ok)
        if not ok:
            errors.append({"fact": fact, "gold": gold, "pred": pred})
    overall = sum(sum(v) for v in per_class.values()) / max(1, sum(len(v) for v in per_class.values()))
    return {
        "overall": round(overall, 3),
        "per_class": {l: round(sum(v) / len(v), 3) for l, v in per_class.items() if v},
        "n": sum(len(v) for v in per_class.values()),
        "errors": errors,
    }
