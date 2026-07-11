"""Stage 1 agent harness 测试（task 6.3）。零真实 LLM（mock _create_with_retry）。"""


class _Usage:
    def __init__(self, i, o):
        self.input_tokens = i
        self.output_tokens = o


class _Block:
    def __init__(self, type, **kw):
        self.type = type
        self.__dict__.update(kw)


class _Resp:
    def __init__(self, stop, content, usage):
        self.stop_reason = stop
        self.content = content
        self.usage = usage


def test_run_episode_tool_then_answer(monkeypatch):
    """tool_use → end_turn：token 累计 / 步数 / tool_calls / answer 正确。"""
    import eval.ab_agent as ag

    seq = [
        _Resp("tool_use", [_Block("tool_use", name="cmm_search", input={"query": "color"}, id="t1")], _Usage(100, 10)),
        _Resp("end_turn", [_Block("text", text="The answer is `Color`.")], _Usage(120, 20)),
    ]
    it = iter(seq)
    monkeypatch.setattr(ag, "_create_with_retry", lambda *a, **k: next(it))
    monkeypatch.setattr(ag, "load_creds", lambda: ("k", "u", "glm-test"))
    monkeypatch.setattr(ag, "_exec_tool", lambda name, inputs: "(mock result)")

    ep = ag.run_episode(client=None, question="what is color", arm="kb")
    assert ep["steps"] == 2
    assert ep["input_tokens"] == 220          # 100 + 120
    assert ep["output_tokens"] == 30          # 10 + 20
    assert ep["tool_calls"] == ["cmm_search"]
    assert "Color" in ep["answer"]
    assert not ep["truncated"]


def test_run_episode_truncation(monkeypatch):
    """一直 tool_use 到 max_steps → truncated=True。"""
    import eval.ab_agent as ag

    resp = _Resp("tool_use", [_Block("tool_use", name="grep_code", input={"pattern": "x"}, id="t")], _Usage(50, 5))
    monkeypatch.setattr(ag, "_create_with_retry", lambda *a, **k: resp)
    monkeypatch.setattr(ag, "load_creds", lambda: ("k", "u", "glm-test"))
    monkeypatch.setattr(ag, "_exec_tool", lambda name, inputs: "(mock)")

    ep = ag.run_episode(client=None, question="x", arm="baseline", max_steps=3)
    assert ep["truncated"] is True
    assert ep["steps"] == 3
    assert ep["input_tokens"] == 150          # 50 × 3


def test_judge_broad():
    """判分：gold 符号 broad alnum 子串匹配（零 judge）。"""
    from eval.run_ab_agent import _judge
    assert _judge("use the Color class", {"Color"}) == 1
    assert _judge("vformat handles formatting", {"vformat"}) == 1
    assert _judge("RandomNumberGenerator works", {"RandomNumberGenerator"}) == 1
    assert _judge("I don't know the answer", {"Color"}) == 0
    assert _judge("", {"Color"}) == 0
