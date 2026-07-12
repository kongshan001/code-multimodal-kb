"""bench 前端的薄后端（stdlib http.server，零依赖）。

路由：
  GET  /                      → web/index.html（SPA）
  GET  /web/<file>            → 静态资源（css/js）
  GET  /api/reports           → eval/reports/archive/index.json
  GET  /api/report/<id>       → 单份归档 JSON
  GET  /api/health            → 依赖体检（cmm/graphify/codegraph/mempalace/python/creds 探测）
  POST /api/run               → subprocess 跑 `python -m eval.cli run <subject> ...`，返回 stdout
  POST /api/goldgen           → subprocess 跑 `python -m eval.cli goldgen ...`
  POST /api/onboard           → subprocess 跑 `codegraph init` / `cmm index` 等（按 action）

用法：python -m eval.server [--port 8765]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Windows 中文系统默认 stdout/文件编码是 GBK(cp936)：print 的 emoji(✓⚠) 和读 UTF-8
# 文件(含中文/emoji)都会 UnicodeEncode/DecodeError。统一强制 UTF-8——跨平台一致。
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "eval" / "reports" / "archive"
WEB = REPO / "web"
CRED_CONFIG = Path.home() / ".cc-connect" / "config.toml"

MIME = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8", ".png": "image/png",
        ".svg": "image/svg+xml", ".json": "application/json"}


def _probe_bin(name: str) -> str:
    p = shutil.which(name)
    if not p:
        return ""
    try:
        out = subprocess.run([p, "--version"], capture_output=True, text=True, timeout=8)
        return out.stdout.strip().split()[-1] if out.returncode == 0 else "ok"
    except Exception:
        return "ok"


def health() -> dict:
    """依赖体检（复用 setup.sh 探测逻辑）。"""
    deps = {
        "cmm": _probe_bin("codebase-memory-mcp"),
        "graphify": _probe_bin("graphify"),
        "codegraph": _probe_bin("codegraph"),
        "mempalace": _probe_bin("mempalace"),
    }
    # python deps
    try:
        import pytest, anthropic  # noqa
        deps["python"] = "pytest+anthropic"
    except ImportError:
        deps["python"] = ""
    deps["render"] = _probe_bin("rsvg-convert") or ("cairosvg" if shutil.which("python") else "")
    # creds
    creds = bool(os.environ.get("AB_API_KEY")) or CRED_CONFIG.exists()
    deps["creds"] = "glm" if creds else ""
    ready = all(deps[k] for k in ("cmm", "graphify", "mempalace", "python"))
    return {"ready": ready, "deps": deps}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # 安静
        pass

    def _send(self, code, body: bytes, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode(), "application/json")

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        p = u.path
        if p == "/" or p == "/index.html":
            return self._send(200, (WEB / "index.html").read_bytes(), "text/html; charset=utf-8")
        if p.startswith("/web/"):
            f = WEB / p[len("/web/"):]
            if f.is_file():
                return self._send(200, f.read_bytes(), MIME.get(f.suffix, "application/octet-stream"))
            return self._send(404, b"not found", "text/plain")
        if p == "/api/reports":
            idx = ARCHIVE / "index.json"
            return self._send_json(200, json.loads(idx.read_text(encoding='utf-8')) if idx.exists() else {"reports": []})
        if p.startswith("/api/report/"):
            rid = p[len("/api/report/"):]
            entry = next((r for r in json.loads((ARCHIVE / "index.json").read_text(encoding='utf-8'))["reports"]
                          if r["id"] == rid), None)
            if not entry:
                return self._send_json(404, {"error": "not found"})
            f = REPO / entry["path"]
            return self._send_json(200, json.loads(f.read_text(encoding='utf-8')))
        if p == "/api/health":
            return self._send_json(200, health())
        if p.startswith("/api/catalog"):
            from eval.scaffold import merged
            qs = urllib.parse.parse_qs(u.query)
            project = qs.get("project", [None])[0]
            return self._send_json(200, merged(project))
        if p.startswith("/api/pending/"):
            tgt = p[len("/api/pending/"):]
            f = REPO / "eval" / "reports" / f"gold_pending_{tgt}.md"
            return self._send_json(200, {"exists": f.exists(),
                                         "content": f.read_text(encoding='utf-8') if f.exists() else ""})
        return self._send(404, b"not found", "text/plain")

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        try:
            if u.path == "/api/run":
                args = ["run", body.get("subject", "code")]
                if body.get("target"): args += ["--target", body["target"]]
                if body.get("method"): args += ["--method", body["method"]]
                out = subprocess.run(["python", "-m", "eval.cli", *args],
                                     capture_output=True, text=True, cwd=str(REPO), timeout=600)
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-2000:], "stderr": out.stderr[-500:]})
            if u.path == "/api/goldgen":
                seeds = body.get("seeds", [])
                args = ["goldgen", *seeds, "--target", body.get("target", "gen")]
                out = subprocess.run(["python", "-m", "eval.cli", *args],
                                     capture_output=True, text=True, cwd=str(REPO), timeout=300)
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-2000:]})
            if u.path == "/api/install":
                cap_id = body.get("id", "")
                project = body.get("project", "")
                # MVP：按 type 分发安装命令（skill=git clone / tool=setup.sh / builtin=已有）
                from eval.scaffold import CATALOG, SKILLS_DIR
                cap = next((c for cat in CATALOG for c in cat["capabilities"] if c["id"] == cap_id), None)
                if not cap:
                    return self._send_json(200, {"rc": 1, "error": f"unknown capability: {cap_id}"})
                if cap["type"] == "builtin":
                    return self._send_json(200, {"rc": 0, "stdout": f"{cap['name']} 是内置能力（随脚手架自带），无需额外安装。"})
                if cap["type"] == "skill":
                    # 检查是否已在全局 skills
                    target = SKILLS_DIR / cap_id / "SKILL.md"
                    if target.exists():
                        return self._send_json(200, {"rc": 0, "stdout": f"{cap['name']} 已在 ~/.claude/skills/{cap_id}/"})
                    # MVP：提示安装方式（实际 git clone 后续实现）
                    return self._send_json(200, {"rc": 0, "stdout": f"{cap['name']} 安装方式：git clone <source> ~/.claude/skills/{cap_id}/\n（MVP：实际 clone 后续实现）"})
                if cap["type"] in ("tool", "mcp"):
                    bin_name = {"cmm": "codebase-memory-mcp", "codegraph": "codegraph", "graphify": "graphify",
                                "mempalace": "mempalace", "headroom": "headroom"}.get(cap_id, cap_id)
                    if shutil.which(bin_name):
                        return self._send_json(200, {"rc": 0, "stdout": f"{cap['name']} 已装：{shutil.which(bin_name)}"})
                    return self._send_json(200, {"rc": 0, "stdout": f"{cap['name']} 安装：./setup.sh tools\n（MVP：实际安装后续实现）"})
                return self._send_json(200, {"rc": 0, "stdout": "ok"})
            if u.path == "/api/onboard":
                act = body.get("action")
                path = body.get("path", "")
                cmds = {
                    "codegraph": ["codegraph", "init", path],
                    "docgraph": ["graphify", "build", path],
                    "mine": ["mempalace", "mine", path, "--mode", "convos"],
                }
                cmd = cmds.get(act, ["echo", f"unknown action {act}"])
                out = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=str(REPO))
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-2000:], "stderr": out.stderr[-500:]})
            if u.path == "/api/goldgen-verify":
                tgt = body.get("target", "gen")
                out = subprocess.run(["python", "-m", "eval.cli", "goldgen-verify", "--target", tgt],
                                     capture_output=True, text=True, timeout=120, cwd=str(REPO))
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-1500:]})
            if u.path == "/api/goldgen-fold":
                tgt = body.get("target", "gen")
                out = subprocess.run(["python", "-m", "eval.cli", "goldgen-fold", "--target", tgt],
                                     capture_output=True, text=True, timeout=60, cwd=str(REPO))
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-800:]})
        except Exception as e:
            return self._send_json(500, {"error": str(e)})
        return self._send_json(404, {"error": "unknown route"})

    # GET pending（gold lab 读审核队列）
    # （在 do_GET 里加 /api/pending/<target>）


def main(argv=None):
    ap = argparse.ArgumentParser(description="bench 前端薄后端（stdlib，零依赖）")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args(argv)
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    h = health()
    print(f"measurement lab → http://{a.host}:{a.port}")
    print(f"  环境 {'就绪 ✓' if h['ready'] else '⚠ 有缺项（/api/health 查）'}")
    print(f"  报告 {len(json.loads((ARCHIVE/'index.json').read_text(encoding='utf-8'))['reports']) if (ARCHIVE/'index.json').exists() else 0} 份归档")
    print("  Ctrl-C 停")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n停。")


if __name__ == "__main__":
    main()
