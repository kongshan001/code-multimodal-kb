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
        report = run_doc(args.target)
        variant = args.target
    elif args.subject == "cross":
        from eval.run_crosstool_baseline import run as run_cross
        report = run_cross(args.target)
        variant = args.target
    elif args.subject == "quality":
        from eval.run_doc_quality import run as run_q  # 凭据门控，可能 429
        report = run_q()
        variant = "godot-render"
    elif args.subject == "memory":
        from eval.run_memory_baseline import run as run_mem  # MemPalace 召回 + D1 路由
        report = run_mem(args.target)
        variant = args.target
    elif args.subject == "ab":
        from eval.run_ab_value import run as run_ab  # agent A/B Stage 0 token 代理
        report = run_ab(args.target)
        variant = f"{args.target}-stage0"
    elif args.subject == "ab-agent":
        from eval.run_ab_agent import run as run_ab1  # agent A/B Stage 1 真跑 agent
        report = run_ab1(args.target, args.runs, args.subset)
        variant = f"{args.target}-stage1-r{args.runs}" + (f"-n{args.subset}" if args.subset else "")
    elif args.subject == "agent-compare":
        from eval.run_ab_agent import run_compare
        from eval.agent_compare_report import write_compare_report
        import datetime
        arms = tuple(a.strip() for a in args.arms.split(",") if a.strip())
        result = run_compare(args.target, arms, args.runs, args.subset, smoke=args.smoke)
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        mode = "-smoke" if args.smoke else ""
        out = write_compare_report(result, f"eval/reports/agent-compare/{ts}-{args.target}{mode}")
        print(f"agent-compare 报告: {out}")
        print(f"  结果:   {out}/result.md     （结论 + 指标说明 + 对比矩阵 + 诚实边界）")
        print(f"  逐题:   {out}/questions.md  （每题各臂得分对照）")
        print(f"  矩阵:   {out}/summary.json  （程序消费用）")
        print(f"  提示:   session.jsonl/thinking.md 是本地文件（.gitignore），结果/指标类已入库")
        return 0
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
    """agent 挖符号 + LLM 拟题 → 候选（status: pending）追加进 problems.json。"""
    from eval.goldgen import generate, seeds_from_dir
    from eval.ab_agent import load_creds, make_client
    from eval.targets import load_target

    root = load_target(args.target)["code"]["codegraph_root"]
    seeds = list(args.seeds)
    if args.dir:
        seeds += seeds_from_dir(args.dir, root)
    seeds = list(dict.fromkeys(seeds))  # 去重保序
    if not seeds:
        print("需给至少一个 seed 词 或 --dir <目录>", file=sys.stderr)
        return 2
    client = make_client()
    _, _, model = load_creds()
    res = generate(seeds, args.target, client, model, args.n)
    print(f"枚举 {res['symbols']} 符号 → LLM 拟 {res['candidates']} 新候选（status: pending）")
    print(f"→ targets/{args.target}/problems.json")
    print(f"人审（前端 approve/删）或先跑: bench goldgen-verify --target {args.target}")
    return 0


def _cmd_goldgen_verify(args) -> int:
    """实证验收：在 pending 候选原地标 verdict/reason（幂等）。"""
    from eval.goldgen import verify
    res = verify(args.target)
    print(f"验收 {res['n']} pending 候选：pass {res['pass']} / 需人审 {res['review']}")
    print(f"已标 verdict/reason → targets/{args.target}/problems.json")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bench", description="engineer_demo benchmark 运行器")
    sub = ap.add_subparsers(dest="cmd", required=True)

    # run <subject> [opts]
    run_p = sub.add_parser("run", help="跑评测并归档")
    run_sub = run_p.add_subparsers(dest="subject", required=True)
    code_p = run_sub.add_parser("code", help="代码侧（cmm）")
    code_p.add_argument("--target", default="godot-core", help="target id（如 godot-core / graphify-pkg）")
    code_p.add_argument("--method", default="grep", choices=["grep", "bm25", "semantic"])
    doc_p = run_sub.add_parser("doc", help="文档侧（graphify query）")
    doc_p.add_argument("--target", default="godot-docs", help="target id")
    cross_p = run_sub.add_parser("cross", help="跨工具 anchoring")
    cross_p.add_argument("--target", default="godot-cross", help="target id")
    run_sub.add_parser("quality", help="文档答案质量（凭据门控，可能 429）")
    mem_p = run_sub.add_parser("memory", help="记忆侧（MemPalace 召回 + D1 路由）")
    mem_p.add_argument("--target", default="engineer-demo-memory", help="target id")
    dr_p = run_sub.add_parser("doc-ragas", help="文档答案质量（Ragas 协议 faithfulness+context_precision，LLM judge）")
    dr_p.add_argument("--target", default="docs")
    dr_p.add_argument("--subset", type=int, default=None)
    mr_p = run_sub.add_parser("memory-quality", help="记忆答案质量（Ragas 协议，mempalace drawer 做 context）")
    mr_p.add_argument("--target", default="engineer-demo-memory", help="target id")
    mr_p.add_argument("--subset", type=int, default=None)
    mr_p.add_argument("--k", type=int, default=5)
    ab_p = run_sub.add_parser("ab", help="agent A/B Stage 0（KB vs 朴素 grep token 代理）")
    ab_p.add_argument("--target", default="godot-core", help="target id")
    ag_p = run_sub.add_parser("ab-agent", help="agent A/B Stage 1（真跑 agent，准确度+token+步数）")
    ag_p.add_argument("--target", default="godot-core")
    ag_p.add_argument("--runs", type=int, default=1)
    ag_p.add_argument("--subset", type=int, default=None, help="只跑前 N 题（pilot）")
    ac_p = run_sub.add_parser("agent-compare", help="4 臂(KB×skills) 对比 → 目录报告（含会话+思考）")
    ac_p.add_argument("--target", default="godot-core")
    ac_p.add_argument("--arms", default="no-kb,kb,kb+superpowers,kb+openspec", help="逗号分隔的臂")
    ac_p.add_argument("--runs", type=int, default=1)
    ac_p.add_argument("--subset", type=int, default=None)
    ac_p.add_argument("--smoke", action="store_true", help="mock 模式（无凭据跑通写器/流水线）")

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
    gg = sub.add_parser("goldgen", help="agent 挖符号 + LLM 拟题 → pending 候选进 problems.json")
    gg.add_argument("seeds", nargs="*", help="搜索 seed 词，指一片代码（如 Vector color）")
    gg.add_argument("--target", required=True, help="target id（如 godot-core）")
    gg.add_argument("--dir", help="目录（派生文件名 seed 兜底）")
    gg.add_argument("--n", type=int, default=20)

    # goldgen-verify --target X：实证验收，在 pending 候选原地标 verdict/reason
    gv = sub.add_parser("goldgen-verify", help="实证验收：在 pending 候选原地标 verdict/reason")
    gv.add_argument("--target", required=True, help="target id")

    # web：起前端可视化服务
    gw = sub.add_parser("web", help="起 bench 前端可视化（localhost，零依赖）")
    gw.add_argument("--port", type=int, default=8765)

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
    if args.cmd == "goldgen-verify":
        return _cmd_goldgen_verify(args)
    if args.cmd == "web":
        from eval.server import main as serve
        serve(["--port", str(args.port)])
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
