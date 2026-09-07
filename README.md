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

An AI agent that acts as a digital twin of a person, allowing website visitors to learn about their career, background, and experience through conversation. The agent uses tool calling to let visitors leave messages that are delivered via email.

## Features

- Answers questions about career, background, skills, and experience
- Draws context from LinkedIn profile, resume, and GitHub projects
- Visitors can leave a message — the agent collects their details and sends it via email

## Stack

- [Gradio](https://gradio.app) — UI
- [OpenAI](https://openai.com) — language model with tool calling
- [Resend](https://resend.com) — email delivery

## Local development

Create a `.env` file with the required secrets (see `CLAUDE.md`), add your `linkedin.pdf`, `resume.pdf`, and `summary.txt` to the project root, then:

```bash
uv sync
uv run python app.py
```
