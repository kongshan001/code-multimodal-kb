"""Stage 1 agent harness 测试（migrate-ab-agent-to-claude-sdk）。
零真实 LLM：mock claude_agent_sdk.query 的消息流，验 trace 抽取（tokens/步数/tool_calls/answer/truncated）。
"""

import types


class TextBlock:
    """类名须 == SDK 真实 block 类名（_extract_assistant 靠 type().__name__ 判型）。"""
    def __init__(self, text):
        self.text = text


class ToolUseBlock:
    def __init__(self, name, input):
        self.name = name
        self.input = input
        self.id = id


class ThinkingBlock:
    def __init__(self, thinking):
        self.thinking = thinking


class AssistantMessage:
    """类名须 == SDK 真实消息类型名（_consume 靠 type().__name__ 判型）。content = block 列表。"""
    def __init__(self, content):
        self.content = content


class ResultMessage:
    """类名须 == SDK 真实消息类型名。result 文本 + usage + cost。"""
    def __init__(self, result="", usage=None, cost=None, num_turns=1):
        self.result = result
        self.usage = usage or {}
        self.total_cost_usd = cost
        self.num_turns = num_turns


def _stream(*msgs):
    """把一组 message 对象包成 async generator（仿 query() 返回值）。"""
    async def gen():
        for m in msgs:
            yield m
    return gen()


def test_run_episode_tool_then_answer(monkeypatch):
    """tool_use → text answer：tool_calls/steps/llm_calls/tokens/answer/truncated 正确（消息流抽取）。"""
    import eval.ab_agent as ag
    monkeypatch.setattr(ag, "load_creds", lambda: ("k", "u", "glm-test"))
    stream = _stream(
        AssistantMessage([ToolUseBlock(name="cmm_search", input={"query": "color"})]),
        AssistantMessage([TextBlock("The answer is `Color`.")]),
        ResultMessage("The answer is `Color`.", {"input_tokens": 120, "output_tokens": 20}),
    )
    monkeypatch.setattr("claude_agent_sdk.query", lambda prompt=None, options=None: stream)
    ep = ag.run_episode(question="what is color", arm="kb")
    assert ep["tool_calls"] == ["cmm_search"]
    assert ep["tool_steps"] == 1
    assert ep["llm_calls"] == 2                       # 2 个 AssistantMessage
    assert ep["input_tokens"] == 120
    assert ep["output_tokens"] == 20
    assert ep["total_tokens"] == 140
    assert "Color" in ep["answer"]
    assert not ep["truncated"]
    # trace key 契约（specs regression）
    assert {"answer", "input_tokens", "output_tokens", "total_tokens", "steps", "llm_calls",
            "tool_calls", "tool_steps", "tool_texts", "truncated", "wall_clock_s",
            "cost_$", "session", "thinking"} <= set(ep)


def test_run_episode_truncation(monkeypatch):
    """max_turns 耗尽、无自然作答 → truncated=True + force-answer（多 1 次调用，答案非空）。"""
    import eval.ab_agent as ag
    monkeypatch.setattr(ag, "load_creds", lambda: ("k", "u", "glm-test"))
    calls = []

    def fake_query(prompt=None, options=None):
        calls.append(prompt)
        if len(calls) == 1:
            # 主 query：只 tool_use，result 空 → 无答案
            return _stream(
                AssistantMessage([ToolUseBlock(name="grep_code", input={"pattern": "x"})]),
                ResultMessage("", {"input_tokens": 50, "output_tokens": 5}),
            )
        # force-answer：文本答案
        return _stream(
            AssistantMessage([TextBlock("`XClass`")]),
            ResultMessage("`XClass`", {"input_tokens": 30, "output_tokens": 8}),
        )

    monkeypatch.setattr("claude_agent_sdk.query", fake_query)
    ep = ag.run_episode(question="x", arm="baseline", max_steps=1)
    assert ep["truncated"] is True
    assert ep["answer"]                               # force-answer 不留空
    assert ep["llm_calls"] == 2                       # 1 主 + 1 force
    assert ep["input_tokens"] == 80                   # 50 + 30


def test_judge_broad():
    """判分：gold 符号 broad alnum 子串匹配（零 judge）。"""
    from eval.run_ab_agent import _judge
    assert _judge("use the Color class", {"Color"}) == 1
    assert _judge("vformat handles formatting", {"vformat"}) == 1
    assert _judge("RandomNumberGenerator works", {"RandomNumberGenerator"}) == 1
    assert _judge("I don't know the answer", {"Color"}) == 0
    assert _judge("", {"Color"}) == 0
