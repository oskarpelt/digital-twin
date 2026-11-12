import html
import json
import os
import re
import resend
from dotenv import load_dotenv

load_dotenv(override=True)

resend.api_key = os.getenv("RESEND_API_KEY")
MY_EMAIL = os.getenv("MY_EMAIL")

MAX_NAME_CHARS = 100
MAX_EMAIL_CHARS = 254
MAX_MESSAGE_CHARS = 2000

_EMAIL_RE = re.compile(r"^[^@\s<>]+@[^@\s<>]+\.[^@\s<>]+$")
_CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f]")


def _validate(name, email, message) -> str | None:
    """Return an error message for the model, or None if the input is fine."""
    if not all(isinstance(v, str) for v in (name, email, message)):
        return "Error: name, email and message must all be text."
    if not name.strip() or not message.strip():
        return "Error: name and message must not be empty."
    if len(name) > MAX_NAME_CHARS:
        return f"Error: name is too long (max {MAX_NAME_CHARS} characters)."
    if len(message) > MAX_MESSAGE_CHARS:
        return f"Error: message is too long (max {MAX_MESSAGE_CHARS} characters)."
    if len(email) > MAX_EMAIL_CHARS or not _EMAIL_RE.match(email):
        return "Error: the email address looks invalid. Ask the visitor to check it."
    return None


def leave_a_message(name, email, message):
    error = _validate(name, email, message)
    if error:
        return error

    # Everything here is visitor- (or injection-) controlled: escape it for the
    # HTML body and strip control characters from the subject line.
    safe_name = html.escape(name)
    safe_email = html.escape(email)
    safe_message = html.escape(message).replace("\n", "<br>")
    subject_name = _CONTROL_CHARS_RE.sub(" ", name).strip()

    try:
        resend.Emails.send({
            "from": "Digital Twin <onboarding@resend.dev>",
            "to": MY_EMAIL,
            "subject": f"Message from {subject_name} via your digital twin",
            "reply_to": email,
            "html": (
                f"<p><strong>Name:</strong> {safe_name}</p>"
                f"<p><strong>Email:</strong> {safe_email}</p>"
                f"<p><strong>Message:</strong> {safe_message}</p>"
            ),
        })
    except Exception as e:  # don't crash the chat if email delivery fails
        print(f"Failed to send email: {e}", flush=True)
        return "Error: the message could not be delivered. Apologise and suggest trying again later."
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
    """Run tool calls given as dicts: {"id", "function": {"name", "arguments"}}."""
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call["function"]["name"]
        print(f"Tool called: {tool_name}", flush=True)
        tool = tool_map.get(tool_name)
        if tool is None:
            result = "Unknown tool: " + tool_name
        else:
            try:
                arguments = json.loads(tool_call["function"]["arguments"] or "{}")
                result = tool(**arguments)
            except (json.JSONDecodeError, TypeError) as e:
                result = f"Error: invalid tool arguments ({e})."
        results.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call["id"],
            }
        )
    return results
