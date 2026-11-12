from openai import OpenAI
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


@gpu
def chat(message, history, request: gr.Request):
    if not check_rate_limit(request.client.host):
        yield "Too many requests — please wait a moment before trying again."
        return
    if message_too_long(message):
        yield f"That message is too long — please keep it under {MAX_MESSAGE_CHARS} characters."
        return

    messages = system + trim_history(history) + [{"role": "user", "content": message}]
    yield from run_agent(openai, MODEL_NAME, messages)


demo = gr.ChatInterface(
    chat,
    examples=EXAMPLES,
    title="Oskari's Digital Twin",
    description="Talk to my AI twin about my career",
    chatbot=gr.Chatbot(
        show_label=False, avatar_images=(None, "assets/me.jpg"), height=800
    ),
)

if __name__ == "__main__":
    demo.launch(css=CSS, js=JS, theme=gr.themes.Base())
