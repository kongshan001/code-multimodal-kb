"""Agent 脚手架 · catalog + detect + recommend + install_status（MVP）。

策展清单（builtin tap）嵌入 Python dict——避免 YAML 依赖。未来可拆 catalog.yaml + tap 多源。
detect() 扫目标项目 → recommend() 按 catalog 规则推荐 → install_status() 检查每项装没装。
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = Path.home() / ".claude" / "skills"

# ── 策展清单（builtin tap）─────────────────────────────────────────────────
CATALOG = [
    {"id": "se-workflows", "name": "🛠️ 软件工程工作流", "desc": "让 agent 按最佳实践干活",
     "capabilities": [
        {"id": "superpowers", "name": "Superpowers", "desc": "code-review / TDD / systematic-debugging 的 SOP", "type": "skill", "recommend": "always", "cost": None},
        {"id": "openspec", "name": "OpenSpec", "desc": "spec 驱动开发——先 spec 后码", "type": "skill", "recommend": "always", "cost": None},
        {"id": "karpathy-guidelines", "name": "Karpathy Guidelines", "desc": "简洁优先 / 外科手术改动 / 目标驱动", "type": "skill", "recommend": "always", "cost": None},
        {"id": "frontend-design", "name": "Frontend Design", "desc": "高质量前端设计（非 AI slop）", "type": "skill", "recommend": "when_frontend", "cost": None},
        {"id": "deep-research", "name": "Deep Research", "desc": "多源研究 + 引用追踪 + 结构化报告", "type": "skill", "recommend": "optional", "cost": None},
     ]},
    {"id": "knowledge-base", "name": "📚 知识库", "desc": "agent 知道你的代码和文档",
     "capabilities": [
        {"id": "cmm", "name": "Code KB · cmm", "desc": "代码符号/调用图检索（agent 查代码不用读文件）", "type": "tool", "recommend": "when_code", "cost": None},
        {"id": "codegraph", "name": "Code KB · codegraph", "desc": "第二代码 KB（A/B 对照 + goldgen 枚举）", "type": "tool", "recommend": "when_code", "cost": None},
        {"id": "graphify", "name": "Doc KB · graphify", "desc": "文档语义检索（NL→概念图）", "type": "tool", "recommend": "when_docs", "cost": "LLM（约 $0.3）"},
     ]},
    {"id": "context-management", "name": "🗜️ 上下文管理", "desc": "有限 context window 塞更多有效信息",
     "capabilities": [
        {"id": "mempalace", "name": "MemPalace", "desc": "跨会话记忆（local-first，核心零 LLM）", "type": "tool", "recommend": "always", "cost": None},
        {"id": "headroom", "name": "headroom", "desc": "压缩工具输出省 context token", "type": "mcp", "recommend": "optional", "cost": None},
     ]},
    {"id": "evaluation", "name": "📊 评测量化", "desc": "数字说话，不凭感觉",
     "capabilities": [
        {"id": "bench", "name": "Benchmark Harness", "desc": "召回率 / A/B 对照 / 答案质量量化", "type": "builtin", "recommend": "when_kb", "cost": None},
        {"id": "goldgen", "name": "Gold Generator", "desc": "自动给代码造测试题（agent 挖符号 + 两层验收）", "type": "builtin", "recommend": "when_code", "cost": None},
     ]},
    {"id": "visualization", "name": "🎨 可视化", "desc": "看得见才管得好",
     "capabilities": [
        {"id": "measurement-lab", "name": "Measurement Lab", "desc": "Dashboard / Run / Gold lab / Onboarding", "type": "builtin", "recommend": "always", "cost": None},
        {"id": "fireworks-tech-graph", "name": "Flow Charts", "desc": "NL → SVG+PNG 技术流程图", "type": "skill", "recommend": "optional", "cost": None},
     ]},
]

# ── 检测每项装没装 ────────────────────────────────────────────────────────
_VERIFY = {
    "superpowers": lambda: (SKILLS_DIR / "superpowers" / "SKILL.md").exists(),
    "openspec": lambda: (SKILLS_DIR / "openspec-explore" / "SKILL.md").exists(),
    "karpathy-guidelines": lambda: (SKILLS_DIR / "karpathy-guidelines" / "SKILL.md").exists(),
    "frontend-design": lambda: (SKILLS_DIR / "frontend-design" / "SKILL.md").exists(),
    "deep-research": lambda: (SKILLS_DIR / "deep-research" / "SKILL.md").exists(),
    "cmm": lambda: bool(shutil.which("codebase-memory-mcp")),
    "codegraph": lambda: bool(shutil.which("codegraph")),
    "graphify": lambda: bool(shutil.which("graphify")),
    "mempalace": lambda: bool(shutil.which("mempalace")),
    "headroom": lambda: bool(shutil.which("headroom")) or (Path.home() / ".claude" / "settings.json").exists(),
    "bench": lambda: (REPO / "eval" / "cli.py").exists(),
    "goldgen": lambda: (REPO / "eval" / "goldgen.py").exists(),
    "measurement-lab": lambda: (REPO / "web" / "index.html").exists(),
    "fireworks-tech-graph": lambda: (SKILLS_DIR / "fireworks-tech-graph" / "SKILL.md").exists(),
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
