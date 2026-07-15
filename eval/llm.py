"""LLM judge 调用（统一走 anthropic 兼容端点，与 agent 共用同一把 base_url+key）。

迁移自 OpenAI 兼容 /chat/completions（judge_base_url 已废弃）—— judge 现与 agent 共用
config.llm()['base_url']（BigModel anthropic 端点），经 ab_agent.make_client() 构造 anthropic
客户端。judge 是单轮补全（无工具无 loop），用 messages.create 即可。
凭据与 agent 同源（load_creds），一把 key/一个端点解锁全部。
"""
from __future__ import annotations

import time

from eval import config


def complete(prompt: str, model: str = "", temperature: float = 0,
             max_tokens: int = 400) -> str:
    """单轮补全，返回文本。429/5xx 退避重试（BigModel 并发限流）。
    model 默认走 config.llm()['model']（与 ab_agent 统一）。"""
    import anthropic  # 延迟导入
    from eval.ab_agent import make_client   # 避免循环导入：ab_agent 不导入 llm
    mdl = model or config.llm()["model"]
    client = make_client()
    for attempt in range(4):
        try:
            resp = client.messages.create(
                model=mdl, max_tokens=max_tokens, temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            for b in resp.content:
                tx = getattr(b, "text", None)   # 取首个 text block（模型无关）
                if tx:
                    return tx
            return ""
        except anthropic.APIStatusError as e:
            if e.status_code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(5 * (attempt + 1))   # 5/10/15s 退避
                continue
            raise
        except anthropic.RateLimitError:
            if attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            raise
