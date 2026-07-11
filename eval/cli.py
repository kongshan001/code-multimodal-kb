"""统一 benchmark CLI（task 2.1–2.5）：`python -m eval.cli <subcommand>`。

子命令：
  run code|doc|cross|quality|memory|ab   跑评测 → 归档留底 → 打印归档路径 + aggregate 摘要
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
    for k in ("crosstool_success_rate", "routing_overall_accuracy",
              "mean_compression_read", "mean_faithfulness",
              "mean_broad_recall@5", "mean_recall@5", "mean_hit@5",
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
    elif args.subject == "memory":
        from eval.run_memory_baseline import run as run_mem  # MemPalace 召回 + D1 路由
        report = run_mem()
        variant = "engineer_demo"
    elif args.subject == "ab":
        from eval.run_ab_value import run as run_ab  # agent A/B Stage 0 token 代理
        report = run_ab(args.target)
        variant = f"{args.target}-stage0"
    elif args.subject == "ab-agent":
        from eval.run_ab_agent import run as run_ab1  # agent A/B Stage 1 真跑 agent
        report = run_ab1(args.target, args.runs, args.subset)
        variant = f"{args.target}-stage1-r{args.runs}" + (f"-n{args.subset}" if args.subset else "")
    elif args.subject == "doc-ragas":
        from eval.run_doc_quality_ragas import run as run_dr  # 文档答案质量（Ragas 协议，LLM judge）
        report = run_dr(args.target, args.subset)
        variant = f"{args.target}-ragas"
    elif args.subject == "memory-quality":
        from eval.run_memory_quality import run as run_mr  # 记忆答案质量（Ragas 协议，mempalace context）
        report = run_mr(args.target, args.subset, getattr(args, "k", 5))
        variant = f"{args.target}-ragas"
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


def _cmd_goldgen(args) -> int:
    """agent 挖符号 + LLM 拟题 → 审核队列文件。"""
    from eval.goldgen import generate, seeds_from_dir
    from eval.ab_agent import load_creds, make_client

    seeds = list(args.seeds)
    if args.dir:
        seeds += seeds_from_dir(args.dir, args.root)
    seeds = list(dict.fromkeys(seeds))  # 去重保序
    if not seeds:
        print("需给至少一个 seed 词 或 --dir <目录>", file=sys.stderr)
        return 2
    client = make_client()
    _, _, model = load_creds()
    res = generate(seeds, args.target, client, model, args.root, args.n)
    print(f"枚举 {res['symbols']} 符号 → LLM 拟 {res['candidates']} 题")
    print(f"审核队列: {res['pending_path']}")
    print(f"人审（删/改 query）后跑: bench goldgen-fold --target {args.target}")
    return 0


def _cmd_goldgen_fold(args) -> int:
    """把审核后的 gold_pending fold 进 gold_<target>.py。"""
    from eval.goldgen import fold
    res = fold(args.target)
    print(f"fold: +{res['added']} 题 → eval/gold_{res['target']}.py（共 {res['total']} 题）")
    return 0


def _cmd_goldgen_verify(args) -> int:
    """独立实证验收：标 verdict/reason 进 pending（人审前 vet 歧义/错配）。"""
    from eval.goldgen import verify_pending, pending_path
    res = verify_pending(args.target, args.root)
    print(f"验收 {res['n']} 题：实证 pass {res['pass']} / 需人审 {res['review']}")
    print(f"已标 verdict/reason → {pending_path(args.target)}")
    print("人审（重点看 review 的）后跑: bench goldgen-fold --target " + args.target)
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
    dr_p = run_sub.add_parser("doc-ragas", help="文档答案质量（Ragas 协议 faithfulness+context_precision，LLM judge）")
    dr_p.add_argument("--target", default="docs")
    dr_p.add_argument("--subset", type=int, default=None)
    mr_p = run_sub.add_parser("memory-quality", help="记忆答案质量（Ragas 协议，mempalace drawer 做 context）")
    mr_p.add_argument("--target", default="memory")
    mr_p.add_argument("--subset", type=int, default=None)
    mr_p.add_argument("--k", type=int, default=5)
    run_sub.add_parser("memory", help="记忆侧（MemPalace 召回 + D1 路由）")
    ab_p = run_sub.add_parser("ab", help="agent A/B Stage 0（KB vs 朴素 grep token 代理）")
    ab_p.add_argument("--target", default="godot", help="gold 模块名")
    ag_p = run_sub.add_parser("ab-agent", help="agent A/B Stage 1（真跑 agent，准确度+token+步数）")
    ag_p.add_argument("--target", default="godot")
    ag_p.add_argument("--runs", type=int, default=1)
    ag_p.add_argument("--subset", type=int, default=None, help="只跑前 N 题（pilot）")

    # list-reports
    sub.add_parser("list-reports", help="列出归档报告")

    # show <id>
    show_p = sub.add_parser("show", help="查看单份报告")
    show_p.add_argument("id")

    # compare <id1> <id2>
    cmp_p = sub.add_parser("compare", help="两份报告 aggregate 对比")
    cmp_p.add_argument("id1")
    cmp_p.add_argument("id2")

    # goldgen <seeds...> --target X [--dir D]：agent 挖符号+LLM拟题→审核队列
    gg = sub.add_parser("goldgen", help="agent 挖符号 + LLM 拟题 → 审核队列（人审后 fold 进 gold）")
    gg.add_argument("seeds", nargs="*", help="搜索 seed 词，指一片代码（如 Vector color）")
    gg.add_argument("--target", required=True, help="gold 模块名（如 godot / 新名）")
    gg.add_argument("--dir", help="目录（派生文件名 seed 兜底）")
    gg.add_argument("--root", default="/Users/ks_128/Documents/godot-src/core")
    gg.add_argument("--n", type=int, default=20)

    # goldgen-fold --target X：审核后的 candidate fold 进 gold_<target>.py
    gf = sub.add_parser("goldgen-fold", help="把审核后的 gold_pending fold 进 gold_<target>.py")
    gf.add_argument("--target", required=True)

    # goldgen-verify --target X：独立实证验收（人审前自动 vet）
    gv = sub.add_parser("goldgen-verify", help="独立实证验收：标 verdict/reason 进 pending（人审前 vet）")
    gv.add_argument("--target", required=True)
    gv.add_argument("--root", default="/Users/ks_128/Documents/godot-src/core")

    args = ap.parse_args(argv)
    if args.cmd == "run":
        return _cmd_run(args)
    if args.cmd == "list-reports":
        return _cmd_list(args)
    if args.cmd == "show":
        return _cmd_show(args)
    if args.cmd == "compare":
        return _cmd_compare(args)
    if args.cmd == "goldgen":
        return _cmd_goldgen(args)
    if args.cmd == "goldgen-fold":
        return _cmd_goldgen_fold(args)
    if args.cmd == "goldgen-verify":
        return _cmd_goldgen_verify(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
