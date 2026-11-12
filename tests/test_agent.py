import json
from types import SimpleNamespace as NS

import agent
import tools


def text_chunk(text):
    return NS(choices=[NS(delta=NS(content=text, tool_calls=None))])


def tool_chunk(index, id=None, name=None, arguments=None):
    fn = NS(name=name, arguments=arguments)
    tc = NS(index=index, id=id, function=fn)
    return NS(choices=[NS(delta=NS(content=None, tool_calls=[tc]))])


class FakeClient:
    """Returns one scripted stream per create() call."""

    def __init__(self, streams):
        self.streams = list(streams)
        self.calls = 0
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kwargs):
        self.calls += 1
        assert kwargs["stream"] is True
        return iter(self.streams.pop(0))


def test_plain_reply_uses_a_single_call():
    client = FakeClient([[text_chunk("Hel"), text_chunk("lo")]])
    out = list(agent.run_agent(client, "m", [{"role": "user", "content": "hi"}]))
    assert out == ["Hel", "Hello"]
    assert client.calls == 1


def test_tool_call_deltas_are_assembled_and_executed(monkeypatch):
    sent = []
    monkeypatch.setitem(tools.tool_map, "leave_a_message", lambda **kw: sent.append(kw) or "OK")
    args = json.dumps({"name": "Eve", "email": "eve@example.com", "message": "hi"})
    client = FakeClient([
        [
            tool_chunk(0, id="call_1", name="leave_a_message", arguments=""),
            tool_chunk(0, arguments=args[:10]),
            tool_chunk(0, arguments=args[10:]),
        ],
        [text_chunk("Sent!")],
    ])
    messages = [{"role": "user", "content": "leave a message"}]
    out = list(agent.run_agent(client, "m", messages))

    assert out == ["Sent!"]
    assert client.calls == 2
    assert sent == [{"name": "Eve", "email": "eve@example.com", "message": "hi"}]
    assert messages[-2]["tool_calls"][0]["id"] == "call_1"
    assert messages[-1]["role"] == "tool" and messages[-1]["tool_call_id"] == "call_1"


def test_tool_loop_is_bounded():
    looping = [tool_chunk(0, id="c", name="nope", arguments="{}")]
    client = FakeClient([looping] * (agent.MAX_TOOL_ROUNDS + 1))
    out = list(agent.run_agent(client, "m", [{"role": "user", "content": "x"}]))
    assert out[-1].startswith("Sorry")
    assert client.calls == agent.MAX_TOOL_ROUNDS + 1
