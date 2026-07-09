#!/usr/bin/env python3
"""setup-kb.py — KB + Memory 便捷接入（跨平台：macOS / Linux / Windows）。

把知识库(codebase-memory-mcp + graphify) + 记忆(Mem0, 可选) + agent MCP 注册
封装成一条命令。Python 实现，工具链本身即 Python，Win/Mac/Linux 原生运行。

用法:
  python3 setup-kb.py --code <代码目录> --docs <文档目录> --name <项目名>
                      [--cmm-mode fast|moderate|full] [--no-memory] [--dry-run]
                      [--llm-key X --llm-base Y --llm-model Z]

新设备: git clone <engineer_demo> && python3 setup-kb.py ...
新项目: 换 --code/--docs 指向新项目目录。详见 docs/deployment-runbook.md。
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
MEM0_DIR = HERE / "deploy" / "mem0"
BIGMODEL_ANTHROPIC_BASE = "https://open.bigmodel.cn/api/anthropic"
BIGMODEL_OPENAI_BASE = "https://open.bigmodel.cn/api/paas/v4"
DEFAULT_MODEL = "glm-4.6"


def sh(cmd: list[str], *, dry: bool, cwd: str | None = None, check: bool = True,
       capture: bool = False, env: dict | None = None) -> str:
    print(f"▶ {' '.join(cmd)}")
    if dry:
        return ""
    r = subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True,
                       env={**os.environ, **(env or {})})
    if check and r.returncode != 0:
        if capture:
            sys.stderr.write(r.stderr or "")
        raise SystemExit(f"✗ 命令失败 (rc={r.returncode}): {' '.join(cmd)}")
    return r.stdout if capture else ""


def need(tool: str) -> str:
    p = shutil.which(tool)
    if not p:
        sys.exit(f"✗ 缺依赖: {tool}（见 docs/deployment-runbook.md 安装）")
    return p


def step_precheck(a: argparse.Namespace) -> None:
    print("=== [1/6] precheck ===")
    need("codebase-memory-mcp")
    if a.docs:
        need("graphify")
    if not a.no_memory and not shutil.which("docker"):
        print("  ⚠ 未找到 docker —— Mem0 Docker 阶段将自动跳过（Win 无 Docker 常见；无 Docker 路线见 runbook §D，或 --no-memory）")
    print("  ✓ 工具就位")


def step_llm(a: argparse.Namespace) -> dict:
    """解析 LLM 凭据，默认复用 ~/.claude.json openspace 的 BigModel key。返回 env 片段。"""
    print("=== [2/6] LLM backend ===")
    key, base, model = a.llm_key, a.llm_base, a.llm_model
    if not key:
        try:
            cfg = json.load(open(os.path.expanduser("~/.claude.json")))
            key = cfg["mcpServers"]["openspace"]["env"]["OPENSPACE_LLM_API_KEY"]
            base = base or BIGMODEL_ANTHROPIC_BASE
            model = model or DEFAULT_MODEL
            print(f"  ℹ 复用环境 BigModel key ({model})")
        except Exception:
            sys.exit("✗ 无 LLM key（用 --llm-key 传，或配 ~/.claude.json openspace）")
    base = base or BIGMODEL_ANTHROPIC_BASE
    model = model or DEFAULT_MODEL
    # graphify 用 Anthropic-compat；Mem0 用 OpenAI-compat（同一把 key，BigModel 两端点都支持）
    env = {"ANTHROPIC_API_KEY": key, "ANTHROPIC_BASE_URL": base, "ANTHROPIC_MODEL": model,
           "OPENAI_API_KEY": key, "OPENAI_BASE_URL": BIGMODEL_OPENAI_BASE, "OPENAI_MODEL": model}
    for k, v in env.items():
        os.environ[k] = v
    print(f"  ✓ backend={base} model={model}")
    return env


def step_cmm(a: argparse.Namespace) -> None:
    print(f"=== [3/6] 代码 KB (cmm index, mode={a.cmm_mode}) ===")
    cmm = need("codebase-memory-mcp")
    sh([cmm, "cli", "index_repository", json.dumps({"repo_path": str(a.code), "mode": a.cmm_mode})],
       dry=a.dry_run)


def step_graphify(a: argparse.Namespace) -> None:
    print("=== [4/6] 文档 KB (graphify, docs-only) ===")
    gf = need("graphify")
    sh([gf, "."], dry=a.dry_run, cwd=str(a.docs))


def step_memory(a: argparse.Namespace) -> None:
    print("=== [5/6] 记忆层 (Mem0) ===")
    if not shutil.which("docker"):
        print("  ⚠ 无 Docker（Win 常见）→ 跳过 Docker 路线，不报错。")
        print("  ℹ 无 Docker 路线（pip + 本地向量库）：pip install mem0-open-mcp，配 local Qdrant(path)/Chroma")
        print("    + BigModel(via litellm)；详见 docs/deployment-runbook.md §D。或 --no-memory 先跳过。")
        return
    compose = MEM0_DIR / "docker-compose.yml"
    if not compose.exists():
        print(f"  ⚠ 缺 {compose}（见 docs/deployment-runbook.md §D）")
        return
    docker = "docker"
    try:
        sh([docker, "compose", "-f", str(compose), "up", "-d", "--build"], dry=a.dry_run, check=False)
    except Exception as e:
        print(f"  ⚠ Mem0 启动失败: {e}（首次拉镜像 ~500MB，重试；详见 runbook）")
        return
    if not a.dry_run:
        print("  …等待 Mem0 API 就绪（最长 120s，Neo4j 首启慢）")
        for _ in range(24):
            try:
                import urllib.request
                urllib.request.urlopen("http://localhost:8888/docs", timeout=3)
                print("  ✓ Mem0 API 就绪 @ :8888/docs")
                break
            except Exception:
                time.sleep(5)
        else:
            print("  ⚠ Mem0 API 未在 120s 内就绪；查 docker compose logs")
    # 注意：Mem0 self-host 暴露的是 REST API（:8888/docs），非 MCP。
    # agent MCP 接入需另装 OpenMemory MCP / mem0-mcp 指向本 backend（见 runbook §Mem0），此处不伪注册。
    print("  ℹ Mem0 REST @ http://localhost:8888/docs | agent MCP 接入见 docs/deployment-runbook.md §Mem0")


def step_register(a: argparse.Namespace) -> None:
    print("=== [6/6] agent MCP 注册 ===")
    cmm = shutil.which("codebase-memory-mcp")
    claude = shutil.which("claude")
    # cmm install 每设备一次（有副作用）；已注册则跳过
    if claude and "codebase-memory-mcp" in sh([claude, "mcp", "list"], dry=a.dry_run,
                                              capture=True, check=False):
        print("  ℹ cmm 已注册到 agent，跳过 install（每设备一次）")
    elif cmm:
        sh([cmm, "install", "-y"], dry=a.dry_run, check=False)
    if a.docs and claude:
        graph_json = a.docs / "graphify-out" / "graph.json"
        if graph_json.exists():
            gmcp = shutil.which("graphify-mcp")
            if gmcp:
                sh([claude, "mcp", "add", "-s", "user", f"graphify-{a.name}", "--", gmcp, str(graph_json)],
                   dry=a.dry_run, check=False) or \
                    print("  ℹ graphify-mcp 注册失败（venv 需 mcp extra：uv tool install --force graphifyy --with mcp）")


def step_status() -> None:
    """查看当前 KB 状态：cmm 已索引项目 / graphify 已建文档图 / agent MCP 注册。"""
    import glob
    print("=== KB 当前状态 ===\n")
    print("[代码 KB · cmm 已索引项目]")
    cmm = shutil.which("codebase-memory-mcp")
    if cmm:
        try:
            r = subprocess.run([cmm, "cli", "list_projects", "{}"], capture_output=True, text=True, timeout=30)
            out = r.stdout.strip()
            projects = json.loads(out[out.find("{"):]).get("projects", []) if "{" in out else []
            for p in projects:
                print(f"  ✓ {p.get('name')}  ({p.get('nodes', '?')} 节点)  @ {p.get('root_path', '')}")
            print(f"  共 {len(projects)} 个项目")
        except Exception as e:
            print(f"  ✗ 读取失败: {e}")
    else:
        print("  ✗ codebase-memory-mcp 未安装")

    print("\n[文档 KB · graphify 已建图]")
    home = os.path.expanduser("~/Documents")
    graphs = sorted(set(glob.glob(home + "/*/graphify-out/graph.json") + glob.glob(home + "/*/*/graphify-out/graph.json")))[:20]
    if not graphs:
        print("  （无）")
    for g in graphs:
        try:
            n = len(json.load(open(g)).get("nodes", []))
            print(f"  ✓ {g.replace(home + '/', '')}  ({n} 节点)")
        except Exception:
            print(f"  ? {g}")

    print("\n[agent MCP 注册]")
    claude = shutil.which("claude")
    if claude:
        r = subprocess.run([claude, "mcp", "list"], capture_output=True, text=True, timeout=30)
        for line in r.stdout.splitlines():
            if any(k in line for k in ("codebase-memory", "graphify", "mem0", "Connected", "Failed")):
                print(f"  {line.strip()}")
    else:
        print("  ✗ claude CLI 未安装")


def _ask(prompt: str, default: str = "", required: bool = False, validate=None) -> str:
    """交互式单项录入。回车=用 default；required/validate 校验。"""
    while True:
        suffix = f" [{default}]" if default != "" else ""
        try:
            val = input(f"{prompt}{suffix}: ").strip()
        except EOFError:
            val = default
        if not val:
            val = default
        if required and not val:
            print("  x 必填"); continue
        if validate and val and not validate(val):
            print("  x 无效或路径不存在"); continue
        return val


def interactive_args(dry_run: bool) -> argparse.Namespace:
    print("=== KB+Memory 交互式接入（回车=采用方括号默认）===")
    code = _ask("[1/6] 代码目录（必填）", required=True,
                validate=lambda p: pathlib.Path(p).is_dir())
    name = _ask("[2/6] 项目名", default=pathlib.Path(code).name, required=True)
    docs = _ask("[3/6] 文档目录（可选，回车跳过）", default="",
                validate=lambda p: not p or pathlib.Path(p).is_dir())
    mem = _ask("[4/6] 启用记忆层 Mem0？需 Docker [y/N]", default="n").lower().startswith("y")
    key = _ask("[5/6] LLM key（回车=复用环境 BigModel 默认）", default="")
    mode = _ask("[6/6] cmm 模式 fast/moderate/full", default="moderate")
    if mode not in ("fast", "moderate", "full"):
        mode = "moderate"
    a = argparse.Namespace(
        code=pathlib.Path(code),
        docs=pathlib.Path(docs) if docs else None,
        name=name, cmm_mode=mode, no_memory=not mem, dry_run=dry_run,
        llm_key=key or None, llm_base=None, llm_model=None)
    print(f"\n-> 确认: code={a.code} docs={a.docs or '<无>'} name={a.name} "
          f"memory={'on' if mem else 'off'} mode={mode}")
    if input("  开始接入？[Y/n]: ").strip().lower().startswith("n"):
        sys.exit("已取消")
    return a


def cmm_projects() -> list:
    cmm = shutil.which("codebase-memory-mcp")
    if not cmm:
        return []
    try:
        r = subprocess.run([cmm, "cli", "list_projects", "{}"], capture_output=True, text=True, timeout=30)
        out = r.stdout.strip()
        return json.loads(out[out.find("{"):]).get("projects", []) if "{" in out else []
    except Exception:
        return []


def _pick_project() -> str | None:
    projects = cmm_projects()
    if not projects:
        print("  （cmm 还没有已索引项目，先选 [1] 接入）"); return None
    for i, p in enumerate(projects, 1):
        print(f"  [{i}] {p.get('name')}  ({p.get('nodes', '?')} 节点)  @ {p.get('root_path', '')}")
    sel = input("选项目序号（回车取消）: ").strip()
    try:
        return projects[int(sel) - 1]["name"]
    except (ValueError, IndexError):
        return None


def interactive_query() -> None:
    print("\n--- 查询项目代码 ---")
    project = _pick_project()
    if not project:
        return
    pattern = input("查什么（关键词/符号名）: ").strip()
    if not pattern:
        return
    cmm = shutil.which("codebase-memory-mcp")
    r = subprocess.run([cmm, "cli", "search_code",
                        json.dumps({"project": project, "pattern": pattern, "limit": 8})],
                       capture_output=True, text=True, timeout=60)
    out = r.stdout.strip()
    results = json.loads(out[out.find("{"):]).get("results", []) if "{" in out else []
    if not results:
        print("  （无结果）"); return
    for res in results:
        print(f"  - {res.get('node')}  [{res.get('file')}:{res.get('start_line', '?')}]  in_degree={res.get('in_degree', '?')}")


def interactive_delete() -> None:
    print("\n--- 删除项目 ---")
    project = _pick_project()
    if not project:
        return
    if input(f"  确认删除 {project}？[y/N]: ").strip().lower() != "y":
        return
    cmm = shutil.which("codebase-memory-mcp")
    subprocess.run([cmm, "cli", "delete_project", json.dumps({"project": project})],
                   capture_output=True, text=True, timeout=30)
    print(f"  => 已删除 {project}")


def run_pipeline(a: argparse.Namespace) -> None:
    print(f"=== KB+Memory 接入: {a.name} (code={a.code} docs={a.docs or '<无>'}) ===")
    step_precheck(a)
    step_llm(a)
    step_cmm(a)
    if a.docs:
        step_graphify(a)
    if not a.no_memory:
        step_memory(a)
    else:
        print("=== [5/6] 跳过记忆层（--no-memory）===")
    step_register(a)


def interactive_menu() -> None:
    while True:
        print("\n=== KB 管理（交互式）===")
        print("  [1] 接入 / 初始化项目")
        print("  [2] 查看已接入项目（状态）")
        print("  [3] 查询某项目代码")
        print("  [4] 删除某项目")
        print("  [5] 退出")
        c = input("选择 [1-5]: ").strip()
        if c == "1":
            a = interactive_args(dry_run=False)
            run_pipeline(a)
            print(f"  => 接入完成: {a.name}（用 [2] 查看 / [3] 查询）")
        elif c == "2":
            step_status()
        elif c == "3":
            interactive_query()
        elif c == "4":
            interactive_delete()
        elif c == "5":
            print("再见"); break
        else:
            print("  无效选项")
        if c in ("1", "2", "3", "4"):
            try:
                input("\n(回车返回菜单)")
            except EOFError:
                break


def main() -> None:
    ap = argparse.ArgumentParser(description="KB+Memory 便捷接入（跨平台，支持 --interactive）")
    ap.add_argument("-i", "--interactive", action="store_true", help="交互式逐项录入（Win .bat 入口）")
    ap.add_argument("-s", "--status", action="store_true", help="查看当前 KB 状态（已索引项目/文档图/注册）")
    ap.add_argument("--code", type=pathlib.Path)
    ap.add_argument("--docs", type=pathlib.Path)
    ap.add_argument("--name")
    ap.add_argument("--cmm-mode", default="moderate", choices=["fast", "moderate", "full"])
    ap.add_argument("--no-memory", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--llm-key"); ap.add_argument("--llm-base"); ap.add_argument("--llm-model")
    a = ap.parse_args()
    if a.status:
        step_status(); return
    if a.interactive:
        interactive_menu()
        return
    if not a.code or not a.name:
        ap.error("非交互模式需 --code <目录> --name <项目名>（或用 --interactive / setup-kb.bat 进菜单）")

    if not a.code.is_dir():
        sys.exit(f"✗ 代码目录不存在: {a.code}")
    if a.docs and not a.docs.is_dir():
        sys.exit(f"✗ 文档目录不存在: {a.docs}")

    run_pipeline(a)

    print(f"=== ✅ 接入完成: {a.name} ===")
    print("验证: claude mcp list   |   重启 Claude Code 后 mcp__* 工具可用")
    if a.docs:
        print(f"文档检索示例: graphify query \"<问题>\" --graph {a.docs}/graphify-out/graph.json")


if __name__ == "__main__":
    main()
