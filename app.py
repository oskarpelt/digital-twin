from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES
from guardrails import check_rate_limit, trim_history
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

    messages = system + trim_history(history) + [{"role": "user", "content": message}]

    response = openai.chat.completions.create(
        model=MODEL_NAME, messages=messages, tools=tools
    )
    while response.choices[0].finish_reason == "tool_calls":
        msg = response.choices[0].message
        results = handle_tool_calls(msg.tool_calls)
        messages.append(msg)
        messages.extend(results)
        response = openai.chat.completions.create(
            model=MODEL_NAME, messages=messages, tools=tools
        )

    stream = openai.chat.completions.create(
        model=MODEL_NAME, messages=messages, stream=True
    )
    text = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            text += delta
            yield text


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
