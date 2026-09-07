import json
import os
import resend
from dotenv import load_dotenv

load_dotenv(override=True)

resend.api_key = os.getenv("RESEND_API_KEY")
MY_EMAIL = os.getenv("MY_EMAIL")


def leave_a_message(name, email, message):
    resend.Emails.send({
        "from": "Digital Twin <onboarding@resend.dev>",
        "to": MY_EMAIL,
        "subject": f"Message from {name} via your digital twin",
        "html": f"<p><strong>Name:</strong> {name}</p><p><strong>Email:</strong> {email}</p><p><strong>Message:</strong> {message}</p>",
    })
    return "OK"


leave_a_message_json = {
    "name": "leave_a_message",
    "description": "Send a message from the visitor to the person they are chatting about. Use this when the visitor wants to get in touch or leave a message.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "The visitor's name"},
            "email": {"type": "string", "description": "The visitor's email address"},
            "message": {"type": "string", "description": "The message the visitor wants to leave"},
        },
        "required": ["name", "email", "message"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": leave_a_message_json},
]

tool_map = {
    "leave_a_message": leave_a_message,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = tool_map.get(tool_name)
        result = tool(**arguments) if tool else "Unknown tool: " + tool_name
        results.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id,
            }
        )
    return results
