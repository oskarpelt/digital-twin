import guardrails


def setup_function():
    guardrails._rate_store.clear()
    guardrails._global_store.clear()


def test_per_ip_limit():
    for _ in range(guardrails.RATE_LIMIT):
        assert guardrails.check_rate_limit("1.1.1.1")
    assert not guardrails.check_rate_limit("1.1.1.1")
    assert guardrails.check_rate_limit("2.2.2.2")


def test_global_limit_applies_across_ips():
    for i in range(guardrails.GLOBAL_RATE_LIMIT):
        assert guardrails.check_rate_limit(f"10.0.{i // 200}.{i % 200}")
    assert not guardrails.check_rate_limit("9.9.9.9")


def test_window_expires(monkeypatch):
    now = 1000.0
    monkeypatch.setattr(guardrails.time, "time", lambda: now)
    for _ in range(guardrails.RATE_LIMIT):
        guardrails.check_rate_limit("1.1.1.1")
    assert not guardrails.check_rate_limit("1.1.1.1")
    monkeypatch.setattr(guardrails.time, "time", lambda: now + guardrails.RATE_WINDOW + 1)
    assert guardrails.check_rate_limit("1.1.1.1")


def test_trim_history_and_length():
    assert len(guardrails.trim_history(list(range(100)))) == guardrails.MAX_HISTORY
    assert guardrails.message_too_long("x" * (guardrails.MAX_MESSAGE_CHARS + 1))
    assert not guardrails.message_too_long("hello")
