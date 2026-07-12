"""Agent 脚手架 · catalog + detect + recommend + install/uninstall。

每个能力带 install_cmd / uninstall_cmd（在 catalog.json 里配置），后端真执行。
detect() 扫目标项目 → recommend() → install_status()。
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = Path.home() / ".claude" / "skills"
PLUGINS_CACHE = Path.home() / ".claude" / "plugins" / "cache"
SETTINGS_JSON = Path.home() / ".claude" / "settings.json"
CATALOG_FILE = REPO / "scaffold" / "catalog.json"
LOCAL_FILE = REPO / "scaffold" / "catalog.local.json"


def load_catalog() -> list:
    cats = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))["categories"]
    if LOCAL_FILE.exists():
        local = json.loads(LOCAL_FILE.read_text(encoding="utf-8")).get("categories", [])
        cats = _merge_catalogs(cats, local)
    return cats


def _merge_catalogs(builtin: list, local: list) -> list:
    by_id = {c["id"]: c for c in builtin}
    for lc in local:
        if lc["id"] in by_id:
            base_caps = {c["id"]: c for c in by_id[lc["id"]]["capabilities"]}
            for cap in lc.get("capabilities", []):
                base_caps[cap["id"]] = cap
            by_id[lc["id"]]["capabilities"] = list(base_caps.values())
        else:
            by_id[lc["id"]] = lc
    return list(by_id.values())


CATALOG = load_catalog()


# ── 安装/卸载命令映射 ─────────────────────────────────────────────────────
# install_cmd / uninstall_cmd 里的 {id} {source} {skills_dir} 会被替换
_INSTALL_CMDS = {
    # skill-dir: git clone 到 ~/.claude/skills/<id>/
    "karpathy-guidelines": {
        "install": "git clone --depth 1 {source} {skills_dir}/{id}",
        "uninstall": "rm -rf {skills_dir}/{id}",
    },
    "deep-research": {
        "install": "git clone --depth 1 {source} {skills_dir}/{id}",
        "uninstall": "rm -rf {skills_dir}/{id}",
    },
    "fireworks-tech-graph": {
        "install": "git clone --depth 1 {source} {skills_dir}/{id}",
        "uninstall": "rm -rf {skills_dir}/{id}",
    },
    # plugin: toggle settings.json
    "superpowers": {
        "install": "_plugin_toggle superpowers@superpowers-marketplace true",
        "uninstall": "_plugin_toggle superpowers@superpowers-marketplace false",
    },
    "frontend-design": {
        "install": "_plugin_toggle frontend-design@claude-plugins-official true",
        "uninstall": "_plugin_toggle frontend-design@claude-plugins-official false",
    },
    # npm
    "openspec": {
        "install": "npm install -g @fission-ai/openspec",
        "uninstall": "npm uninstall -g @fission-ai/openspec",
    },
    "codegraph": {
        "install": "npm install -g @colbymchenry/codegraph",
        "uninstall": "npm uninstall -g @colbymchenry/codegraph",
    },
    # uv tool
    "graphify": {
        "install": "uv tool install graphifyy",
        "uninstall": "uv tool uninstall graphifyy",
    },
    "mempalace": {
        "install": "uv tool install --python 3.11 mempalace",
        "uninstall": "uv tool uninstall mempalace",
    },
    # binary
    "cmm": {
        "install": "_cmm_install",
        "uninstall": "rm -f ~/.local/bin/codebase-memory-mcp",
    },
    # pip venv
    "headroom": {
        "install": "_headroom_install",
        "uninstall": "rm -rf ~/.headroom",
    },
}


def _plugin_toggle(plugin_key: str, enable: bool) -> tuple[int, str]:
    """toggle settings.json plugins[key] = true/false."""
    try:
        settings = json.loads(SETTINGS_JSON.read_text(encoding="utf-8"))
    except Exception:
        return 1, "settings.json 读失败"
    plugins = settings.setdefault("plugins", {})
    plugins[plugin_key] = enable
    SETTINGS_JSON.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    action = "启用" if enable else "禁用"
    return 0, f"{action} plugin {plugin_key}（重启 Claude Code 生效）"


def _cmm_install() -> tuple[int, str]:
    """cmm 是 binary download。"""
    return 1, "cmm 需从 GitHub releases 手动下载 binary。见 docs/deployment-runbook.md §A"


def _headroom_install() -> tuple[int, str]:
    """headroom 安装到 ~/.headroom/venv。"""
    out = subprocess.run(["bash", "-c", "curl -fsSL https://raw.githubusercontent.com/mgks/headroom/main/install.sh | bash"],
                         capture_output=True, text=True, timeout=120)
    return out.returncode, out.stdout[-200:] + out.stderr[-200:]


def execute_action(cap_id: str, action: str) -> dict:
    """执行 install 或 uninstall。返回 {rc, stdout}。"""
    cmds = _INSTALL_CMDS.get(cap_id)
    if not cmds:
        return {"rc": 1, "stdout": f"未配置 {action} 命令。请手动操作。"}
    cmd_template = cmds.get(action)
    if not cmd_template:
        return {"rc": 1, "stdout": f"无 {action} 命令"}

    cap = next((c for cat in CATALOG for c in cat["capabilities"] if c["id"] == cap_id), {})
    source = cap.get("source") or ""

    # 特殊处理（下划线前缀的内部函数）
    if cmd_template.startswith("_"):
        fn_name = cmd_template
        if fn_name == "_cmm_install":
            rc, msg = _cmm_install()
        elif fn_name == "_headroom_install":
            rc, msg = _headroom_install()
        elif fn_name.startswith("_plugin_toggle"):
            parts = fn_name.split()
            rc, msg = _plugin_toggle(parts[1], parts[2] == "true")
        else:
            return {"rc": 1, "stdout": f"未知内部命令: {fn_name}"}
        return {"rc": rc, "stdout": msg}

    # 模板替换 + 执行
    cmd = cmd_template.format(id=cap_id, source=source, skills_dir=str(SKILLS_DIR))
    out = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=180)
    # strip control chars
    msg = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\r]', '', out.stdout + out.stderr)
    return {"rc": out.returncode, "stdout": msg[-400:]}


# ── 检测每项装没装 ────────────────────────────────────────────────────────
def _check_skill(skill_id: str) -> bool:
    if (SKILLS_DIR / skill_id / "SKILL.md").exists():
        return True
    if PLUGINS_CACHE.exists():
        for _root, _dirs, _files in os.walk(PLUGINS_CACHE):
            if Path(_root).name == skill_id and "SKILL.md" in _files:
                return True
    return False


def _check_plugin(plugin_key: str) -> bool:
    """检查 settings.json plugins[key] == true。"""
    try:
        settings = json.loads(SETTINGS_JSON.read_text(encoding="utf-8"))
        return settings.get("plugins", {}).get(plugin_key, False) is True
    except Exception:
        return False


_VERIFY = {
    "superpowers": lambda: _check_plugin("superpowers@superpowers-marketplace"),
    "openspec": lambda: bool(shutil.which("openspec")),
    "karpathy-guidelines": lambda: _check_skill("karpathy-guidelines"),
    "frontend-design": lambda: _check_plugin("frontend-design@claude-plugins-official"),
    "deep-research": lambda: _check_skill("deep-research"),
    "cmm": lambda: bool(shutil.which("codebase-memory-mcp")),
    "codegraph": lambda: bool(shutil.which("codegraph")),
    "graphify": lambda: bool(shutil.which("graphify")),
    "mempalace": lambda: bool(shutil.which("mempalace")),
    "headroom": lambda: (Path.home() / "bin" / "headroom").exists() or bool(shutil.which("headroom")),
    "bench": lambda: (REPO / "eval" / "cli.py").exists(),
    "goldgen": lambda: (REPO / "eval" / "goldgen.py").exists(),
    "measurement-lab": lambda: (REPO / "web" / "index.html").exists(),
    "fireworks-tech-graph": lambda: _check_skill("fireworks-tech-graph"),
    # engineering practices: always "not installed" (they're methodology)
    "context-engineering": lambda: False,
    "prompt-engineering": lambda: False,
    "harness-engineering": lambda: False,
    "lint-feedback-loop": lambda: False,
}

# type mapping: catalog type → 是否可从脚手架安装/卸载
INSTALLABLE_TYPES = {"skill", "plugin", "tool", "mcp"}


# ── 项目检测 ────────────────────────────────────────────────────────────
def detect(project_path: str = None) -> dict:
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


def _should_recommend(rule: str, d: dict) -> str:
    if rule == "always": return "推荐"
    if rule == "when_code" and d.get("has_code"): return "推荐"
    if rule == "when_docs" and d.get("has_docs"): return "推荐"
    if rule == "when_frontend" and d.get("has_frontend"): return "推荐"
    if rule == "when_kb": return "可选"
    return "可选"


def merged(project_path: str = None) -> dict:
    d = detect(project_path)
    cats = []
    total_installed = total_recommended = total_caps = 0
    for cat in CATALOG:
        caps = []
        for cap in cat["capabilities"]:
            installed = _VERIFY.get(cap["id"], lambda: False)()
            rec = _should_recommend(cap["recommend"], d)
            # 标注是否可安装/卸载
            installable = cap["id"] in _INSTALL_CMDS and cap.get("type") in INSTALLABLE_TYPES
            caps.append({**cap, "installed": installed, "recommendation": rec, "installable": installable})
            total_caps += 1
            if installed: total_installed += 1
            if rec == "推荐": total_recommended += 1
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
