---
title: Digital Twin
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "6.26.0"
app_file: app.py
pinned: false
---

# Digital Twin

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/oskarpelt/digital-twin)

An AI agent that acts as a digital twin of a person, allowing website visitors to learn about their career, background, and experience through conversation. The agent uses tool calling to let visitors leave messages that are delivered via email.

## Features

- Answers questions about career, background, skills, and experience
- Draws context from LinkedIn profile, resume, and personal GitHub projects
- Visitors can leave a message — the agent collects their name, email, and message and delivers it via email
- Every chat turn is traced with Langfuse (model calls, tool calls, token usage, cost), grouped into sessions per conversation
- Auto-deployed to Hugging Face Spaces via GitHub Actions

## Stack

- [Gradio](https://gradio.app) — UI
- [OpenAI](https://openai.com) — language model with tool calling
- [Resend](https://resend.com) — email delivery
- [Langfuse](https://langfuse.com) — tracing and observability

## Local development

Copy `.env.example` to `.env` and fill in the required secrets, add your `linkedin.pdf`, `resume.pdf`, and `summary.txt` to the project root, then:

```bash
uv sync
uv run python app.py
```

### Tracing (Langfuse)

Tracing is optional. Without Langfuse credentials the app runs normally and tracing is disabled. To enable it, create a project in [Langfuse](https://langfuse.com) and set these in `.env`:

- `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` — from Settings → API Keys
- `LANGFUSE_BASE_URL` — your region, e.g. `https://cloud.langfuse.com` (EU) or `https://us.cloud.langfuse.com` (US)
- `LANGFUSE_TRACING_ENVIRONMENT` — `development` locally, `production` on the Space, so traces stay separated

Each chat turn is one trace (`chat-turn`) containing the model calls (`generate-response`) and tool calls (e.g. `leave_a_message`). Conversations are grouped into sessions. Email addresses are redacted before traces are sent; other message content, including names, is stored.

To regenerate GitHub project context:

```bash
uv run python scripts/fetch_github.py
```

## Deployment

Pushes to `master` are automatically deployed to Hugging Face Spaces via GitHub Actions. Persona data (`LINKEDIN`, `RESUME`, `SUMMARY`, `GITHUB`) and API keys (including the `LANGFUSE_*` variables) are stored as HF Spaces secrets.
