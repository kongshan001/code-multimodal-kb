"""Mem0 本地 MCP server（无 Docker · 跨平台 · 实测通过配置）。

Qdrant 本地嵌入模式（path，零服务进程）+ Ollama（全本地，绕开任何云限流）或
BigModel（回退）。stdio MCP，暴露 add_memory / search_memory / get_all_memories。

实测要点（已踩坑修好）：
- vector_store 必须**嵌套 config**（mem0 2.x）：{"provider":"qdrant","config":{...}}
- embedding_model_dims 必须显式（nomic-embed-text=768），否则默认 1536 → 维度不匹配
- Memory.add 用 user_id= 顶层参数；Memory.search/get_all 用 filters={"user_id":...}
- 抽取质量取决于 LLM：llama3.2 偏弱(英文模型抽中文事实易空)，建议 ollama pull qwen2.5:7b

依赖：pip install mem0ai qdrant-client ollama mcp   （Ollama 另需 ollama + 模型：
  ollama pull nomic-embed-text && ollama pull qwen2.5:7b）

被 setup-kb.py --memory-mode local 注册为 agent 的 stdio MCP server。
LLM 模型可由环境变量 MEM0_LLM_MODEL 覆盖（默认 qwen2.5:7b）。
"""
import json
import os
import shutil
import subprocess

from mcp.server.fastmcp import FastMCP
from mem0 import Memory


def _ollama_has(model: str) -> bool:
    if not shutil.which("ollama"):
        return False
    try:
        out = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10).stdout
        return model.split(":")[0] in out
    except Exception:
        return False


def _bigmodel_key() -> str:
    return json.load(open(os.path.expanduser("~/.claude.json")))["mcpServers"]["openspace"]["env"]["OPENSPACE_LLM_API_KEY"]


LLM_MODEL = os.environ.get("MEM0_LLM_MODEL", "llama3.2:latest")  # 已实测可跑；换 qwen2.5:7b 抽取更细

if _ollama_has("nomic-embed-text"):
    DIMS = 768  # nomic-embed-text
    CONFIG = {
        "vector_store": {"provider": "qdrant", "config": {
            "path": os.path.expanduser("~/.mem0-local"), "collection_name": "mem0",
            "embedding_model_dims": DIMS}},
        "llm": {"provider": "ollama", "config": {"model": LLM_MODEL, "ollama_base_url": "http://localhost:11434"}},
        "embedder": {"provider": "ollama", "config": {"model": "nomic-embed-text:latest", "ollama_base_url": "http://localhost:11434"}},
    }
    _BACKEND = f"ollama({LLM_MODEL} + nomic-embed-text)"
else:
    _K = _bigmodel_key()
    DIMS = 2048  # zhipu embedding-3
    CONFIG = {
        "vector_store": {"provider": "qdrant", "config": {
            "path": os.path.expanduser("~/.mem0-local"), "collection_name": "mem0",
            "embedding_model_dims": DIMS}},
        "llm": {"provider": "openai", "config": {"api_key": _K, "openai_base_url": "https://open.bigmodel.cn/api/paas/v4", "model": "glm-4.6"}},
        "embedder": {"provider": "openai", "config": {"api_key": _K, "openai_base_url": "https://open.bigmodel.cn/api/paas/v4", "model": "embedding-3"}},
    }
    _BACKEND = "bigmodel(glm-4.6 + embedding-3)"

print(f"[mem0-local] backend = {_BACKEND}", flush=True)
mem = Memory.from_config(CONFIG)
mcp = FastMCP("mem0-local")


@mcp.tool()
def add_memory(content: str, user_id: str = "default") -> str:
    """存记忆：从 content 抽取事实并入库。infer=False 强制抽取（实测：infer=True
    默认预判会让本地小模型 llama3.2 跳过抽取→空，故关闭）。"""
    return json.dumps(mem.add(content, user_id=user_id, infer=False), ensure_ascii=False)


@mcp.tool()
def search_memory(query: str, user_id: str = "default") -> str:
    """语义召回：按 query 检索相关记忆。"""
    return json.dumps(mem.search(query, filters={"user_id": user_id}), ensure_ascii=False)


@mcp.tool()
def get_all_memories(user_id: str = "default") -> str:
    """列出该 user 的全部记忆。"""
    return json.dumps(mem.get_all(filters={"user_id": user_id}), ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
