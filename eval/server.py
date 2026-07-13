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
import sys
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from eval._subproc import run_text
from eval.targets import (TargetError, list_targets, load_problems,
                          load_target, save_problems)

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
        out = run_text([p, "--version"], timeout=8)
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
            try:
                pending = [x for x in load_problems(tgt) if x.get("status") == "pending"]
            except Exception as e:
                return self._send_json(200, {"exists": False, "count": 0,
                                             "content": f"(target 不存在或无 problems.json: {e})"})
            lines = [f"# pending 候选 · target={tgt}（来自 problems.json，前端 approve/删）", ""]
            for x in pending:
                lines.append(f"## {x['id']}")
                lines.append(f"- query: {x.get('query') or x.get('fact')}")
                lines.append(f"- gold: {x.get('gold', {})}")
                if x.get("verdict"):
                    lines.append(f"- verdict: {x['verdict']}")
                if x.get("reason"):
                    lines.append(f"- reason: {x['reason']}")
                lines.append("")
            return self._send_json(200, {"exists": bool(pending), "count": len(pending),
                                         "content": "\n".join(lines)})
        if p == "/api/targets":
            out = []
            for tid in list_targets():
                try:
                    t = load_target(tid)
                    out.append({"id": tid, "subjects": t.get("subjects", []),
                                "language": t.get("language", "")})
                except Exception:
                    out.append({"id": tid})
            return self._send_json(200, {"targets": out})
        if p.startswith("/api/gold/"):
            tgt = p[len("/api/gold/"):]
            if not tgt or "/" in tgt:
                return self._send_json(400, {"error": "GET /api/gold/<target>"})
            try:
                return self._send_json(200, {"target": load_target(tgt),
                                             "problems": load_problems(tgt)})
            except TargetError as e:
                return self._send_json(404, {"error": str(e)})
        return self._send(404, b"not found", "text/plain")

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        try:
            if u.path == "/api/run":
                subj = body.get("subject", "code")
                args = ["run", subj]
                # 只有 code 接受 --method；其它 subject 的 argparse 不认
                if subj == "code" and body.get("method"):
                    args += ["--method", body["method"]]
                # --target 各 subject 接受，但默认值不同
                if body.get("target"):
                    args += ["--target", body["target"]]
                out = run_text(["python", "-m", "eval.cli", *args], timeout=600, cwd=str(REPO))
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-2000:], "stderr": out.stderr[-500:]})
            if u.path == "/api/goldgen":
                seeds = body.get("seeds", [])
                args = ["goldgen", *seeds, "--target", body.get("target", "gen")]
                out = run_text(["python", "-m", "eval.cli", *args], timeout=300, cwd=str(REPO))
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-2000:]})
            if u.path == "/api/install":
                cap_id = body.get("id", "")
                from eval.scaffold import execute_action
                return self._send_json(200, execute_action(cap_id, "install"))
            if u.path == "/api/uninstall":
                cap_id = body.get("id", "")
                from eval.scaffold import execute_action
                return self._send_json(200, execute_action(cap_id, "uninstall"))
            if u.path == "/api/onboard":
                act = body.get("action")
                path = body.get("path", "")
                cmds = {
                    "codegraph": ["codegraph", "init", path],
                    "docgraph": ["graphify", "build", path],
                    "mine": ["mempalace", "mine", path, "--mode", "convos"],
                }
                cmd = cmds.get(act, ["echo", f"unknown action {act}"])
                out = run_text(cmd, timeout=300, cwd=str(REPO))
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-2000:], "stderr": out.stderr[-500:]})
            if u.path == "/api/goldgen-verify":
                tgt = body.get("target", "gen")
                out = run_text(["python", "-m", "eval.cli", "goldgen-verify", "--target", tgt],
                               timeout=120, cwd=str(REPO))
                return self._send_json(200, {"rc": out.returncode, "stdout": out.stdout[-1500:]})
            if u.path.startswith("/api/gold/"):
                # 新增一道题：POST /api/gold/<target>（body = 新题目，无需 id，save_problems 分配）
                tgt = u.path[len("/api/gold/"):]
                if not tgt or "/" in tgt:
                    return self._send_json(400, {"error": "POST /api/gold/<target>"})
                try:
                    problems = load_problems(tgt)
                    new = dict(body)
                    new.pop("id", None)  # id 由 save_problems 分配
                    new.setdefault("status", "accepted")
                    problems.append(new)
                    save_problems(tgt, problems)
                    return self._send_json(200, {"ok": True, "id": new["id"],
                                                 "problems": load_problems(tgt)})
                except TargetError as e:
                    return self._send_json(400, {"error": str(e)})
        except Exception as e:
            return self._send_json(500, {"error": str(e)})
        return self._send_json(404, {"error": "unknown route"})

    def _gold_write(self, method: str, path: str, body: dict):
        """PUT/DELETE /api/gold/<target>/<id> 的共用处理。"""
        rest = path[len("/api/gold/"):]
        parts = rest.split("/", 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return self._send_json(400, {"error": f"{method} /api/gold/<target>/<id>"})
        tgt, pid = parts
        try:
            problems = load_problems(tgt)
            if method == "DELETE":
                new = [p for p in problems if p["id"] != pid]
                if len(new) == len(problems):
                    return self._send_json(404, {"error": f"题目 {pid} 不存在"})
                save_problems(tgt, new, assign=False)
                return self._send_json(200, {"ok": True, "problems": new})
            # PUT：替换单题（id 以 URL 为准）
            body = dict(body)
            body["id"] = pid
            for i, p in enumerate(problems):
                if p["id"] == pid:
                    problems[i] = body
                    save_problems(tgt, problems, assign=False)
                    return self._send_json(200, {"ok": True, "problems": load_problems(tgt)})
            return self._send_json(404, {"error": f"题目 {pid} 不存在"})
        except TargetError as e:
            return self._send_json(400, {"error": str(e)})

    def do_PUT(self):
        u = urllib.parse.urlparse(self.path)
        if u.path.startswith("/api/gold/"):
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            return self._gold_write("PUT", u.path, body)
        return self._send_json(404, {"error": "unknown route"})

    def do_DELETE(self):
        u = urllib.parse.urlparse(self.path)
        if u.path.startswith("/api/gold/"):
            return self._gold_write("DELETE", u.path, {})
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
    print(f"  报告 {len(json.loads((ARCHIVE/'index.json').read_text(encoding='utf-8'))['reports']) if (ARCHIVE/'index.json').exists() else 0} 份归档")
    print("  Ctrl-C 停")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n停。")


if __name__ == "__main__":
    main()
