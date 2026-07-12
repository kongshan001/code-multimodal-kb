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
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

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
            return self._send_json(200, json.loads(idx.read_text()) if idx.exists() else {"reports": []})
        if p.startswith("/api/report/"):
            rid = p[len("/api/report/"):]
            entry = next((r for r in json.loads((ARCHIVE / "index.json").read_text())["reports"]
                          if r["id"] == rid), None)
            if not entry:
                return self._send_json(404, {"error": "not found"})
            f = REPO / entry["path"]
            return self._send_json(200, json.loads(f.read_text()))
        if p == "/api/health":
            return self._send_json(200, health())
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
            if u.path == "/api/onboard":
                act = body.get("action")
                path = body.get("path", "")
                if act == "index":
                    out = subprocess.run(["codegraph", "init", path], capture_output=True, text=True, timeout=300)
                else:
                    out = subprocess.run(["echo", f"unknown action {act}"], capture_output=True, text=True)
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-2000:]})
        except Exception as e:
            return self._send_json(500, {"error": str(e)})
        return self._send_json(404, {"error": "unknown route"})


def main(argv=None):
    ap = argparse.ArgumentParser(description="bench 前端薄后端（stdlib，零依赖）")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args(argv)
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    h = health()
    print(f"measurement lab → http://{a.host}:{a.port}")
    print(f"  环境 {'就绪 ✓' if h['ready'] else '⚠ 有缺项（/api/health 查）'}")
    print(f"  报告 {len(json.loads((ARCHIVE/'index.json').read_text())['reports']) if (ARCHIVE/'index.json').exists() else 0} 份归档")
    print("  Ctrl-C 停")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n停。")


if __name__ == "__main__":
    main()
