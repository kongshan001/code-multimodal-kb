"""LLM judge 调用（BigModel/GLM，OpenAI-compatible 端点）。

复用 ~/.claude.json openspace 的 key。eval 跑在 anaconda python（CA 有坑）→ 关 SSL 校验。
凭据与 graphify/Mem0 同一把（design：一把 key 解锁）。
"""
from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request

_BASE = "https://open.bigmodel.cn/api/paas/v4"
_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE  # anaconda python CA 绕过（graphify 在 uv-venv 不需要）


def _key() -> str:
    cfg = json.load(open(os.path.expanduser("~/.claude.json")))
    return cfg["mcpServers"]["openspace"]["env"]["OPENSPACE_LLM_API_KEY"]


def complete(prompt: str, model: str = "glm-4.6", temperature: float = 0,
             max_tokens: int = 400) -> str:
    """单轮补全，返回文本。429/5xx 退避重试（BigModel 并发限流）。"""
    req = urllib.request.Request(
        _BASE + "/chat/completions",
        data=json.dumps({"model": model, "temperature": temperature,
                         "max_tokens": max_tokens,
                         "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Authorization": "Bearer " + _key(), "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(4):
        try:
            resp = urllib.request.urlopen(req, timeout=90, context=_ctx)
            return json.loads(resp.read())["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(5 * (attempt + 1))  # 5s / 10s / 15s 退避
                continue
            raise
