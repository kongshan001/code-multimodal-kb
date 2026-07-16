"""全引擎可调项单一来源：bench.yaml（本地配置，gitignored）+ 内置默认值。

PyYAML 必装（见 requirements.txt）。`cp bench.yaml.example bench.yaml` 后改模型/价格/上限/端口/
api_key，不改代码。bench.yaml 不入库（各自本地改不冲突）；缺失时用 _DEFAULTS 兜底。

覆盖优先级：bench.yaml > 内置默认（本文件 _DEFAULTS），深合并。
凭据（api_key）优先级（在 ab_agent.load_creds）：env AB_API_KEY > bench.yaml(llm.api_key) > config.toml。
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_CONFIG_PATH = REPO / "bench.yaml"   # gitignored 本地配置（由 bench.yaml.example 复制；含 api_key）

# 内置默认（bench.yaml 缺失或某键未填时用）
_DEFAULTS = {
    "llm": {
        "base_url": "https://open.bigmodel.cn/api/anthropic",        # agent + judge 共用（anthropic 兼容端点）
        "model": "glm-5.1",
        # $/Mtoken；未知模型 → cost null（占位价，勿当真实成本）
        "prices": {"glm-5.1": {"in": 0.70, "out": 0.70},
                   "glm-5.2": {"in": 0.70, "out": 0.70}},
    },
    "agent": {
        "max_steps": 30,          # run-until-answer 的 backstop（防死循环；正常题远在此之前自然收敛）
        "skill_max_steps": 30,    # 同上（skills 臂不再单独收紧——30 轮足够 SOP 展开）
        "tool_result_cap": 2000,  # tool_result 序列化截断（防 session.jsonl 膨胀）
        "read_cap": 2000,         # read_file 截断 chars（两臂公平）
    },
    "server": {"port": 8765},
    "timeouts": {"probe": 10, "tool": 30, "long": 120, "run": 600},
}

_cached: dict | None = None


def _deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in over.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load() -> dict:
    """加载配置：bench.yaml 覆盖 _DEFAULTS（深合并）。缓存。"""
    global _cached
    if _cached is not None:
        return _cached
    cfg = dict(_DEFAULTS)
    try:
        import yaml  # 惰性：只在 bench.yaml 存在时 import
        if _CONFIG_PATH.is_file():
            user = yaml.safe_load(_CONFIG_PATH.read_text(encoding="utf-8")) or {}
            cfg = _deep_merge(cfg, user)
    except ImportError:
        pass  # 无 pyyaml → 用默认值（不阻断）
    except yaml.YAMLError as e:
        raise RuntimeError(f"bench.yaml 解析失败: {e}")
    _cached = cfg
    return cfg


def llm() -> dict:
    return load()["llm"]


def agent() -> dict:
    return load()["agent"]


def server() -> dict:
    return load()["server"]


def timeouts() -> dict:
    return load()["timeouts"]
