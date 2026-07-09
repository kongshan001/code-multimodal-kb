"""Mem0 本地（Ollama 全本地）实测：add(infer=False) → search 闭环。绕开云限流。
装完 mem0ai/qdrant-client/ollama/mcp 后：python3 deploy/mem0-local/_test.py
"""
import json
import os
import shutil

from mem0 import Memory

shutil.rmtree(os.path.expanduser("~/.mem0-local-test"), ignore_errors=True)
CONFIG = {
    "vector_store": {"provider": "qdrant", "config": {
        "path": os.path.expanduser("~/.mem0-local-test"),
        "collection_name": "mem0", "embedding_model_dims": 768}},  # nomic-embed-text=768
    "llm": {"provider": "ollama", "config": {"model": "llama3.2:latest", "ollama_base_url": "http://localhost:11434"}},
    "embedder": {"provider": "ollama", "config": {"model": "nomic-embed-text:latest", "ollama_base_url": "http://localhost:11434"}},
}

m = Memory.from_config(CONFIG)
print("[add] 存对话 → llama3.2 抽取(infer=False) + nomic-embed-text 入 qdrant")
print(json.dumps(m.add("用户偏好用 Python、写简洁代码、改动一律提交 git 带 Co-Authored-By；讨厌冗余注释",
                       user_id="u1", infer=False), ensure_ascii=False)[:250])
print("\n[search] 召回 '代码风格偏好'")
print(json.dumps(m.search("用户的代码风格偏好", filters={"user_id": "u1"}), ensure_ascii=False)[:450])
