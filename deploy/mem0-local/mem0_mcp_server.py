"""Mem0 本地 MCP server（无 Docker · 实验性）。

ChromaDB 嵌入式（本地目录，零服务进程）+ BigModel（litellm zhipu 做 LLM，
OpenAI-compat 做 embedder）。stdio MCP，暴露 add/search/get_all 工具。
被 setup-kb.py --memory-mode local 注册为 agent 的 MCP server。

⚠ 实验性：embedder config schema（openai_base_url/model/dims）按 Mem0 文档推断，
未在本机实测（chromadb 重 + BigModel 曾 429）。若 embedder 报错，按 Mem0 OSS 文档
调 config（docs.mem0.ai/open-source/configuration），或换 HuggingFace 本地 embedder。

依赖：pip install mem0ai chromadb mcp
"""
import json
import os

from mcp.server.fastmcp import FastMCP
from mem0 import Memory


def _key() -> str:
    return json.load(open(os.path.expanduser("~/.claude.json")))["mcpServers"]["openspace"]["env"]["OPENSPACE_LLM_API_KEY"]


_K = _key()
CONFIG = {
    "vector_store": {"provider": "chroma",
                     "path": os.path.expanduser("~/.mem0-local"), "collection": "mem0"},
    "llm": {"provider": "litellm", "litellm_params": {"model": "zhipu/glm-4.6", "api_key": _K}},
    "embedder": {"provider": "openai", "config": {
        "api_key": _K, "openai_base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "embedding-3"}},
}

mem = Memory.from_config(CONFIG)
mcp = FastMCP("mem0-local")


@mcp.tool()
def add_memory(content: str, user_id: str = "default") -> str:
    """存记忆：从 content 抽取事实并入库（调 LLM 抽取 + embedder 入向量库）。"""
    return json.dumps(mem.add(content, user_id=user_id), ensure_ascii=False)


@mcp.tool()
def search_memory(query: str, user_id: str = "default") -> str:
    """语义召回：按 query 检索相关记忆。"""
    return json.dumps(mem.search(query, user_id=user_id), ensure_ascii=False)


@mcp.tool()
def get_all_memories(user_id: str = "default") -> str:
    """列出该 user 的全部记忆。"""
    return json.dumps(mem.get_all(user_id=user_id), ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
