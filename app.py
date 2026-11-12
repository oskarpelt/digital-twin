import gradio as gr
from langfuse import observe, propagate_attributes

from context import TWIN_SYSTEM_PROMPT
from guardrails import check_rate_limit, trim_history
from llm import stream_reply
from styles import CSS, JS, EXAMPLES
from tracing import langfuse

try:
    import spaces

    gpu = spaces.GPU
except ImportError:

    def gpu(fn):
        return fn


system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


@observe(name="chat-turn", as_type="agent", capture_input=False, capture_output=False)
def _traced_chat(message, history, request):
    # One trace per chat turn
    langfuse.update_current_span(input=message)

    if not check_rate_limit(request.client.host):
        reply = "Too many requests — please wait a moment before trying again."
        langfuse.update_current_span(
            output=reply, level="WARNING", status_message="rate limited"
        )
        yield reply
        return

    with propagate_attributes(
        session_id=request.session_hash, tags=["digital-twin", "chat"]
    ):
        messages = (
            system + trim_history(history) + [{"role": "user", "content": message}]
        )
        text = yield from stream_reply(messages)
        langfuse.update_current_span(output=text)


@gpu
def chat(message, history, request: gr.Request):
    # Must stay a plain generator function: Gradio detects streaming by checking
    # for one, and @observe's wrapper hides that.
    yield from _traced_chat(message, history, request)


demo = gr.ChatInterface(
    chat,
    examples=EXAMPLES,
    title="Oskari's Digital Twin",
    description=(
        "Talk to my AI twin about my career<br>"
        "<small>Conversations are logged to improve this assistant. "
        "Please don't share sensitive personal information.</small>"
    ),
    chatbot=gr.Chatbot(
        show_label=False, avatar_images=(None, "assets/me.jpg"), height=800
    ),
)

if __name__ == "__main__":
    demo.launch(css=CSS, js=JS, theme=gr.themes.Base(), server_name="0.0.0.0")
