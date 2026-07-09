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


def main() -> None:
    ap = argparse.ArgumentParser(description="KB+Memory 便捷接入（跨平台）")
    ap.add_argument("--code", type=pathlib.Path, required=True)
    ap.add_argument("--docs", type=pathlib.Path)
    ap.add_argument("--name", required=True)
    ap.add_argument("--cmm-mode", default="moderate", choices=["fast", "moderate", "full"])
    ap.add_argument("--no-memory", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--llm-key"); ap.add_argument("--llm-base"); ap.add_argument("--llm-model")
    a = ap.parse_args()

    if not a.code.is_dir():
        sys.exit(f"✗ 代码目录不存在: {a.code}")
    if a.docs and not a.docs.is_dir():
        sys.exit(f"✗ 文档目录不存在: {a.docs}")

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

    print(f"=== ✅ 接入完成: {a.name} ===")
    print("验证: claude mcp list   |   重启 Claude Code 后 mcp__* 工具可用")
    if a.docs:
        print(f"文档检索示例: graphify query \"<问题>\" --graph {a.docs}/graphify-out/graph.json")


if __name__ == "__main__":
    main()
