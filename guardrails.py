from collections import defaultdict
import time

RATE_LIMIT = 10   # requests per window per IP
RATE_WINDOW = 60  # seconds
MAX_HISTORY = 20  # messages (~10 turns)

_rate_store: dict = defaultdict(list)


def check_rate_limit(ip: str) -> bool:
    now = time.time()
    _rate_store[ip] = [t for t in _rate_store[ip] if now - t < RATE_WINDOW]
    if len(_rate_store[ip]) >= RATE_LIMIT:
        return False
    _rate_store[ip].append(now)
    return True


def trim_history(history: list) -> list:
    return history[-MAX_HISTORY:]
