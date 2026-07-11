"""统一 benchmark CLI（task 2.1–2.5）：`python -m eval.cli <subcommand>`。

子命令：
  run code|doc|cross|quality   跑评测 → 归档留底 → 打印归档路径 + aggregate 摘要
  list-reports                 列出 archive/index.json 全部报告
  show <id>                    查看单份归档报告（含 per_query / lockfile）
  compare <id1> <id2>          两份报告 aggregate diff

设计见 openspec/changes/add-benchmark-runner/design.md 决策 1。
可加 alias：`alias bench='python -m eval.cli'`。
"""
from __future__ import annotations

import argparse
import json
import sys

from eval.archive import archive_report, compare_reports, get_report, list_reports


def _summary(agg: dict) -> str:
    """挑一个主指标作单行摘要。"""
    for k in ("crosstool_success_rate", "mean_broad_recall@5", "mean_recall@5",
              "graphify_hit_rate", "cmm_hit_rate@5"):
        if k in agg:
            return f"{k}={agg[k]}"
    return ""


def _cmd_run(args) -> int:
    if args.subject == "code":
        from eval.run_code_baseline import run as run_code
        report = run_code(args.target, args.method)
        variant = f"{args.target}-{args.method}"
    elif args.subject == "doc":
        from eval.run_doc_baseline import run as run_doc
        report = run_doc()
        variant = report.get("target", "godot-docs-subset")
    elif args.subject == "cross":
        from eval.run_crosstool_baseline import run as run_cross
        report = run_cross()
        variant = "godot"
    elif args.subject == "quality":
        from eval.run_doc_quality import run as run_q  # 凭据门控，可能 429
        report = run_q()
        variant = "godot-render"
    else:
        print(f"未知 subject: {args.subject}", file=sys.stderr)
        return 2

    res = archive_report(report, variant=variant)
    norm = get_report(res["id"]) or {}
    print(f"归档 id : {res['id']}")
    print(f"路径    : {res['path']}")
    print(f"subject : {norm.get('subject', '')} / variant={variant}")
    print(f"摘要    : {_summary(norm.get('aggregate', {}))}")
    print(f"aggregate: {json.dumps(norm.get('aggregate', {}), ensure_ascii=False)}")
    return 0


def _cmd_list(args) -> int:
    reports = list_reports()
    if not reports:
        print("(archive 无归档报告)")
        return 0
    print(f"{'id':52} {'subject/variant':36} {'ts':17} {'摘要'}")
    print("-" * 120)
    for r in reports:
        sv = f"{r['subject']}/{r['variant']}"
        print(f"{r['id']:52} {sv:36} {r['ts']:17} {_summary(r.get('aggregate', {}))}")
    print(f"\n共 {len(reports)} 份")
    return 0


def _cmd_show(args) -> int:
    r = get_report(args.id)
    if r is None:
        print(f"未找到报告: {args.id}", file=sys.stderr)
        return 1
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


def _cmd_compare(args) -> int:
    c = compare_reports(args.id1, args.id2)
    if c is None:
        print(f"找不到报告（需两个 id 都存在）: {args.id1} / {args.id2}", file=sys.stderr)
        return 1
    print(f"{c['left']}  vs  {c['right']}\n")
    print(f"{'metric':32} {'left':>10} {'right':>10} {'delta':>10}")
    print("-" * 66)
    for d in c["diff"]:
        delta = "" if d["delta"] is None else f"{d['delta']:+.4f}"
        print(f"{d['metric']:32} {str(d['left']):>10} {str(d['right']):>10} {delta:>10}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bench", description="engineer_demo benchmark 运行器")
    sub = ap.add_subparsers(dest="cmd", required=True)

    # run <subject> [opts]
    run_p = sub.add_parser("run", help="跑评测并归档")
    run_sub = run_p.add_subparsers(dest="subject", required=True)
    code_p = run_sub.add_parser("code", help="代码侧（cmm）")
    code_p.add_argument("--target", default="code", help="gold 模块名，如 godot")
    code_p.add_argument("--method", default="grep", choices=["grep", "bm25", "semantic"])
    run_sub.add_parser("doc", help="文档侧（graphify query）")
    run_sub.add_parser("cross", help="跨工具 anchoring")
    run_sub.add_parser("quality", help="文档答案质量（凭据门控，可能 429）")

    # list-reports
    sub.add_parser("list-reports", help="列出归档报告")

    # show <id>
    show_p = sub.add_parser("show", help="查看单份报告")
    show_p.add_argument("id")

    # compare <id1> <id2>
    cmp_p = sub.add_parser("compare", help="两份报告 aggregate 对比")
    cmp_p.add_argument("id1")
    cmp_p.add_argument("id2")

    args = ap.parse_args(argv)
    if args.cmd == "run":
        return _cmd_run(args)
    if args.cmd == "list-reports":
        return _cmd_list(args)
    if args.cmd == "show":
        return _cmd_show(args)
    if args.cmd == "compare":
        return _cmd_compare(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
