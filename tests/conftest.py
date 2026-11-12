import os
import sys
from pathlib import Path

# Keep test runs out of Langfuse: set before anything imports langfuse.
os.environ["LANGFUSE_TRACING_ENABLED"] = "false"

sys.path.insert(0, str(Path(__file__).parent.parent))
