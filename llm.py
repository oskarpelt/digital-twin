from types import SimpleNamespace

import tracing  # initialises Langfuse with masking before the OpenAI client
from langfuse.openai import OpenAI  # drop-in, traced OpenAI client

from tools import tools, handle_tool_calls

MODEL_NAME = "gpt-5.4-mini"

client = OpenAI()


def _stream_round(messages):
    """Make one streaming model call.

    Yields the reply text so far; returns (text, tool_calls), where tool_calls
    is empty when the model answered in plain text.
    """
    stream = client.chat.completions.create(
        name="generate-response",
        model=MODEL_NAME,
        messages=messages,
        tools=tools,
        stream=True,
        stream_options={"include_usage": True},  # usage/cost on streams
    )
    text = ""
    fragments = {}  # tool calls arrive in pieces keyed by index
    for chunk in stream:
        if not chunk.choices:  # final usage-only chunk
            continue
        delta = chunk.choices[0].delta
        if delta.content:
            text += delta.content
            yield text
        for tc in delta.tool_calls or []:
            f = fragments.setdefault(tc.index, {"id": "", "name": "", "args": ""})
            f["id"] = tc.id or f["id"]
            if tc.function:
                f["name"] += tc.function.name or ""
                f["args"] += tc.function.arguments or ""

    tool_calls = [
        SimpleNamespace(
            id=f["id"],
            function=SimpleNamespace(name=f["name"], arguments=f["args"]),
        )
        for _, f in sorted(fragments.items())
    ]
    return text, tool_calls


def _assistant_message(text, tool_calls):
    return {
        "role": "assistant",
        "content": text or None,
        "tool_calls": [
            {
                "id": t.id,
                "type": "function",
                "function": {
                    "name": t.function.name,
                    "arguments": t.function.arguments,
                },
            }
            for t in tool_calls
        ],
    }


def stream_reply(messages):
    """Run the model/tool loop, streaming the reply text. Returns the final text."""
    while True:
        text, tool_calls = yield from _stream_round(messages)
        if not tool_calls:
            return text
        messages.append(_assistant_message(text, tool_calls))
        messages.extend(handle_tool_calls(tool_calls))
