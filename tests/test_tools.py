import json

import tools


class FakeEmails:
    def __init__(self):
        self.sent = []

    def send(self, params):
        self.sent.append(params)


def fake_resend(monkeypatch):
    fake = FakeEmails()
    monkeypatch.setattr(tools.resend, "Emails", fake)
    return fake


def test_escapes_html_in_email_body(monkeypatch):
    fake = fake_resend(monkeypatch)
    result = tools.leave_a_message(
        "<b>Eve</b>", "eve@example.com", "<script>alert(1)</script>\nsecond line"
    )
    assert result == "OK"
    body = fake.sent[0]["html"]
    assert "<script>" not in body and "&lt;script&gt;" in body
    assert "<b>Eve</b>" not in body
    assert "<br>" in body


def test_subject_has_no_control_characters(monkeypatch):
    fake = fake_resend(monkeypatch)
    tools.leave_a_message("Eve\r\nBcc: x@y.z", "eve@example.com", "hi")
    assert "\r" not in fake.sent[0]["subject"] and "\n" not in fake.sent[0]["subject"]


def test_rejects_invalid_input(monkeypatch):
    fake = fake_resend(monkeypatch)
    assert tools.leave_a_message("Eve", "not-an-email", "hi").startswith("Error")
    assert tools.leave_a_message("", "eve@example.com", "hi").startswith("Error")
    assert tools.leave_a_message("Eve", "eve@example.com", "x" * 5000).startswith("Error")
    assert tools.leave_a_message("Eve", "eve@example.com", 123).startswith("Error")
    assert fake.sent == []


def test_delivery_failure_does_not_raise(monkeypatch):
    class Boom:
        def send(self, params):
            raise RuntimeError("down")

    monkeypatch.setattr(tools.resend, "Emails", Boom())
    assert tools.leave_a_message("Eve", "eve@example.com", "hi").startswith("Error")


def test_handle_tool_calls_bad_arguments_and_unknown_tool():
    calls = [
        {"id": "1", "function": {"name": "leave_a_message", "arguments": "{not json"}},
        {"id": "2", "function": {"name": "leave_a_message", "arguments": '{"name": "x"}'}},
        {"id": "3", "function": {"name": "nope", "arguments": "{}"}},
    ]
    results = tools.handle_tool_calls(calls)
    assert [r["tool_call_id"] for r in results] == ["1", "2", "3"]
    assert all(json.loads(r["content"]).startswith(("Error", "Unknown")) for r in results)
