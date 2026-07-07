"""评测 harness：对 subject 跑数据集，收集 (query, result, gold) 记录（task 1.1）。

数据集与 gold 来源按 subject 切换（代码侧 PR 反挖 / 文档侧借标 / 记忆侧标注），
harness 本身 subject-agnostic。本轮骨架；真数据集接入见 task 2.1（TODO）。
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable


@dataclass
class EvalRecord:
    query: Any
    result: Any
    gold: Any
    meta: dict = field(default_factory=dict)


@dataclass
class EvalRun:
    subject: str
    records: list[EvalRecord] = field(default_factory=list)

    def add(self, rec: EvalRecord) -> None:
        self.records.append(rec)

    def to_json(self) -> str:
        return json.dumps(
            {"subject": self.subject, "n": len(self.records),
             "records": [r.__dict__ for r in self.records]},
            ensure_ascii=False, indent=2, default=str,
        )


def run_dataset(
    subject_fn: Callable[[Any], Any],
    dataset: Iterable[dict],
    subject_name: str = "subject",
) -> EvalRun:
    """subject_fn(query) -> result；dataset 每项含 'query' 与 'gold'。"""
    run = EvalRun(subject=subject_name)
    for item in dataset:
        result = subject_fn(item["query"])
        run.add(EvalRecord(query=item["query"], result=result, gold=item["gold"], meta=item.get("meta", {})))
    return run
