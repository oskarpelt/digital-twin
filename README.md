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
- Auto-deployed to Hugging Face Spaces via GitHub Actions

## Stack

- [Gradio](https://gradio.app) — UI
- [OpenAI](https://openai.com) — language model with tool calling
- [Resend](https://resend.com) — email delivery

## Local development

Copy `.env.example` to `.env` and fill in the required secrets, add your `linkedin.pdf`, `resume.pdf`, and `summary.txt` to the project root, then:

```bash
uv sync
uv run python app.py
```

To regenerate GitHub project context:

```bash
uv run python scripts/fetch_github.py
```

## Deployment

Pushes to `master` are automatically deployed to Hugging Face Spaces via GitHub Actions. Persona data (`LINKEDIN`, `RESUME`, `SUMMARY`, `GITHUB`) and API keys are stored as HF Spaces secrets.
