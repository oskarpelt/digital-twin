from collections import defaultdict, deque
import time

RATE_LIMIT = 10  # requests per window per IP
GLOBAL_RATE_LIMIT = 60  # requests per window across all IPs (cost backstop)
RATE_WINDOW = 60  # seconds
MAX_HISTORY = 20  # messages (~10 turns)
MAX_MESSAGE_CHARS = 2000  # per user message

_rate_store: dict[str, deque] = defaultdict(deque)
_global_store: deque = deque()


def _prune(timestamps: deque, now: float) -> None:
    while timestamps and now - timestamps[0] >= RATE_WINDOW:
        timestamps.popleft()


def check_rate_limit(ip: str) -> bool:
    """Per-IP limit plus a global limit.

    The global limit bounds total spend even if every visitor is seen as the
    same IP (e.g. behind a proxy) or an attacker rotates IPs.
    """
    now = time.time()

    _prune(_global_store, now)
    if len(_global_store) >= GLOBAL_RATE_LIMIT:
        return False

    timestamps = _rate_store[ip]
    _prune(timestamps, now)
    if len(timestamps) >= RATE_LIMIT:
        return False

    timestamps.append(now)
    _global_store.append(now)

    # Keep the store from growing forever with one-off visitors.
    if len(_rate_store) > 1000:
        for key in [k for k, v in _rate_store.items() if not v]:
            del _rate_store[key]
    return True


def trim_history(history: list) -> list:
    return history[-MAX_HISTORY:]


def message_too_long(message: str) -> bool:
    return len(message) > MAX_MESSAGE_CHARS
