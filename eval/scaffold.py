"""Agent 脚手架 · catalog + detect + recommend + install_status。

策展清单从 scaffold/catalog.json 加载（用户可编辑）。
scaffold/catalog.local.json 可选——用户自研工具覆盖/追加（按 id 合并）。
detect() 扫目标项目 → recommend() 按 catalog 规则推荐 → install_status() 检查每项装没装。
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = Path.home() / ".claude" / "skills"
CATALOG_FILE = REPO / "scaffold" / "catalog.json"
LOCAL_FILE = REPO / "scaffold" / "catalog.local.json"


def load_catalog() -> list:
    """从 catalog.json 加载策展清单 + 合并 catalog.local.json（用户自研覆盖/追加）。"""
    cats = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))["categories"]
    if LOCAL_FILE.exists():
        local = json.loads(LOCAL_FILE.read_text(encoding="utf-8")).get("categories", [])
        cats = _merge_catalogs(cats, local)
    return cats


def _merge_catalogs(builtin: list, local: list) -> list:
    """按 category id 合并；同 id capability 以 local 覆盖。"""
    by_id = {c["id"]: c for c in builtin}
    for lc in local:
        if lc["id"] in by_id:
            # 合并 capabilities（local 覆盖同 id）
            base_caps = {c["id"]: c for c in by_id[lc["id"]]["capabilities"]}
            for cap in lc.get("capabilities", []):
                base_caps[cap["id"]] = cap
            by_id[lc["id"]]["capabilities"] = list(base_caps.values())
        else:
            by_id[lc["id"]] = lc
    return list(by_id.values())


CATALOG = load_catalog()

PLUGINS_CACHE = Path.home() / ".claude" / "plugins" / "cache"


def _check_skill(skill_id: str) -> bool:
    """检查 skill 是否安装——先查 ~/.claude/skills/，再查 plugins cache。"""
    if (SKILLS_DIR / skill_id / "SKILL.md").exists():
        return True
    # 插件式 skill：~/.claude/plugins/cache/<marketplace>/<plugin>/<ver>/skills/<skill_id>/SKILL.md
    if PLUGINS_CACHE.exists():
        for _root, _dirs, _files in os.walk(PLUGINS_CACHE):
            if Path(_root).name == skill_id and "SKILL.md" in _files:
                return True
    return False


# ── 检测每项装没装 ────────────────────────────────────────────────────────
_VERIFY = {
    "superpowers": lambda: _check_skill("using-superpowers") or _check_skill("superpowers"),
    "openspec": lambda: _check_skill("openspec-explore"),
    "karpathy-guidelines": lambda: _check_skill("karpathy-guidelines"),
    "frontend-design": lambda: _check_skill("frontend-design"),
    "deep-research": lambda: _check_skill("deep-research"),
    "cmm": lambda: bool(shutil.which("codebase-memory-mcp")),
    "codegraph": lambda: bool(shutil.which("codegraph")),
    "graphify": lambda: bool(shutil.which("graphify")),
    "mempalace": lambda: bool(shutil.which("mempalace")),
    "headroom": lambda: bool(shutil.which("headroom")) or (Path.home() / ".claude" / "settings.json").exists(),
    "bench": lambda: (REPO / "eval" / "cli.py").exists(),
    "goldgen": lambda: (REPO / "eval" / "goldgen.py").exists(),
    "measurement-lab": lambda: (REPO / "web" / "index.html").exists(),
    "fireworks-tech-graph": lambda: _check_skill("fireworks-tech-graph"),
}

# ── 项目检测 ────────────────────────────────────────────────────────────
def detect(project_path: str = None) -> dict:
    """扫目标项目 → 语言/docs/tests/frontend。"""
    p = Path(project_path) if project_path else REPO
    exts = {}
    for f in p.rglob("*"):
        if f.is_file() and ".git" not in str(f) and "node_modules" not in str(f):
            ext = f.suffix.lower()
            if ext in (".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".cpp", ".c", ".h"):
                exts[ext] = exts.get(ext, 0) + 1
    lang = "unknown"
    if exts:
        lang = {".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript/React", ".go": "Go",
                ".rs": "Rust", ".java": "Java", ".cpp": "C++", ".c": "C"}.get(max(exts, key=exts.get), "unknown")
    return {
        "language": lang,
        "has_code": bool(exts),
        "has_docs": (p / "docs").is_dir() or bool(list(p.glob("*.md"))),
        "has_tests": (p / "tests").is_dir() or (p / "eval" / "tests").is_dir() or bool(list(p.glob("**/test_*.py"))),
        "has_frontend": (p / "package.json").exists() or (p / "web").is_dir(),
        "size_files": sum(exts.values()),
        "path": str(p),
    }

# ── 推荐引擎 ────────────────────────────────────────────────────────────
def _should_recommend(rule: str, d: dict) -> str:
    """recommend rule → '推荐' / '可选' / '不推荐'。"""
    if rule == "always":
        return "推荐"
    if rule == "when_code" and d.get("has_code"):
        return "推荐"
    if rule == "when_docs" and d.get("has_docs"):
        return "推荐"
    if rule == "when_frontend" and d.get("has_frontend"):
        return "推荐"
    if rule == "when_kb":
        return "可选"  # 简化：有 KB 才推荐，MVP 不深查
    return "可选"

# ── 合并：catalog + detect + status + recommend → 前端用一个 dict ──────────
def merged(project_path: str = None) -> dict:
    d = detect(project_path)
    cats = []
    total_installed = total_recommended = total_caps = 0
    for cat in CATALOG:
        caps = []
        for cap in cat["capabilities"]:
            installed = _VERIFY.get(cap["id"], lambda: False)()
            rec = _should_recommend(cap["recommend"], d)
            caps.append({**cap, "installed": installed, "recommendation": rec})
            total_caps += 1
            if installed:
                total_installed += 1
            if rec == "推荐":
                total_recommended += 1
        cats.append({**cat, "capabilities": caps})
    return {
        "detection": d,
        "categories": cats,
        "summary": {
            "total": total_caps,
            "installed": total_installed,
            "recommended": total_recommended,
            "not_installed_recommended": total_recommended - sum(
                1 for cat in cats for cap in cat["capabilities"]
                if cap["installed"] and cap["recommendation"] == "推荐"
            ),
        },
    }
