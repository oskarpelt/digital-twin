from langfuse import observe, propagate_attributes
from langfuse.openai import OpenAI  # drop-in, traced OpenAI client
from context import TWIN_SYSTEM_PROMPT
from agent import run_agent
from styles import CSS, JS, EXAMPLES
from guardrails import (
    MAX_MESSAGE_CHARS,
    check_rate_limit,
    message_too_long,
    trim_history,
)
from dotenv import load_dotenv
from tracing import langfuse
import gradio as gr

try:
    import spaces

    gpu = spaces.GPU
except ImportError:

    def gpu(fn):
        return fn


load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

openai = OpenAI()

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


@observe(name="chat-turn", as_type="agent", capture_input=False, capture_output=False)
def _traced_chat(message, history, request):
    # One trace per chat turn; Gradio's per-browser session hash groups a whole
    # conversation into one Langfuse session.
    langfuse.update_current_span(input=message)

    if not check_rate_limit(request.client.host):
        reply = "Too many requests — please wait a moment before trying again."
        langfuse.update_current_span(
            output=reply, level="WARNING", status_message="rate limited"
        )
        yield reply
        return
    if message_too_long(message):
        reply = f"That message is too long — please keep it under {MAX_MESSAGE_CHARS} characters."
        langfuse.update_current_span(
            output=reply, level="WARNING", status_message="message too long"
        )
        yield reply
        return

    with propagate_attributes(
        session_id=request.session_hash, tags=["digital-twin", "chat"]
    ):
        messages = (
            system + trim_history(history) + [{"role": "user", "content": message}]
        )
        text = ""
        for text in run_agent(openai, MODEL_NAME, messages):
            yield text
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
