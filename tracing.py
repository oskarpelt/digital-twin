import re

from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv(override=True)  # Langfuse reads its credentials at init

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def mask(data, **kwargs):
    """Redact email addresses (visitor contact details) before data leaves the app."""
    if isinstance(data, str):
        return _EMAIL_RE.sub("[EMAIL]", data)
    if isinstance(data, dict):
        return {k: mask(v) for k, v in data.items()}
    if isinstance(data, (list, tuple)):
        return [mask(v) for v in data]
    return data


# Global client, initialised once with masking. The environment
# (production/development) comes from LANGFUSE_TRACING_ENVIRONMENT.
langfuse = Langfuse(mask=mask)
