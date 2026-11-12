from tools import tools, handle_tool_calls

MAX_TOOL_ROUNDS = 3


def run_agent(client, model, messages):
    """Stream a reply, running tool calls as needed.

    Each model call is streamed once: text is yielded as it arrives, and tool
    call deltas are assembled so no second "regenerate" call is needed.
    Yields the accumulated reply text so far (the Gradio streaming contract).
    """
    for _ in range(MAX_TOOL_ROUNDS + 1):
        stream = client.chat.completions.create(
            model=model, messages=messages, tools=tools, stream=True
        )
        text = ""
        calls: dict[int, dict] = {}

        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta.content:
                text += delta.content
                yield text
            for tc in delta.tool_calls or []:
                call = calls.setdefault(
                    tc.index, {"id": "", "type": "function", "function": {"name": "", "arguments": ""}}
                )
                if tc.id:
                    call["id"] = tc.id
                if tc.function:
                    if tc.function.name:
                        call["function"]["name"] += tc.function.name
                    if tc.function.arguments:
                        call["function"]["arguments"] += tc.function.arguments

        if not calls:
            return

        tool_calls = [calls[i] for i in sorted(calls)]
        messages.append(
            {"role": "assistant", "content": text or None, "tool_calls": tool_calls}
        )
        messages.extend(handle_tool_calls(tool_calls))

    yield "Sorry, I got stuck handling that request. Please try again."
