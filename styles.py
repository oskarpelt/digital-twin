"""Styling constants for the digital twin Gradio app."""

EXAMPLES = [
    "Tell me about your background and experience.",
    "What have you built that you're most proud of?",
    "What are your strongest technical skills?",
    "Tell me about your personal projects.",
    "Are you open to new opportunities?",
    "How can I get in touch with you?",
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,600&display=swap');

/* ── Override Gradio theme tokens ── */
:root, .gradio-container {
  --body-background-fill:              #0a0a0a !important;
  --block-background-fill:             #111111 !important;
  --input-background-fill:             #111111 !important;
  --input-background-fill-focus:       #111111 !important;
  --border-color-primary:              #2a2a2a !important;
  --border-color-accent:               #39ff14 !important;
  --color-accent:                      #39ff14 !important;
  --body-text-color:                   #e0e0e0 !important;
  --body-text-color-subdued:           #777777 !important;
  --input-text-size:                   13px    !important;
  --button-primary-background-fill:    #111111 !important;
  --button-primary-background-fill-hover: #0f2a08 !important;
  --button-primary-border-color:       #39ff14 !important;
  --button-primary-text-color:         #39ff14 !important;
  --button-secondary-background-fill:  #111111 !important;
  --button-secondary-border-color:     #2a2a2a !important;
  --button-secondary-text-color:       #777777 !important;
  --button-secondary-background-fill-hover: #111111 !important;
  --button-secondary-border-color-hover:    #39ff14 !important;
  --button-secondary-text-color-hover:      #39ff14 !important;
  --shadow-drop:                       none    !important;
  --block-radius:                      0px     !important;
  --input-radius:                      0px     !important;
  --button-large-radius:               0px     !important;
  --button-small-radius:               0px     !important;
  --font:                              'JetBrains Mono', 'Courier New', monospace !important;
  --font-mono:                         'JetBrains Mono', 'Courier New', monospace !important;
}

/* ── Hide Gradio chrome ── */
footer, .built-with, .show-api { display: none !important; }

/* ── Page ── */
html, body, gradio-app {
  background: #0a0a0a !important;
  font-family: 'JetBrains Mono', monospace !important;
}

/* Scanline */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px,
    rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px
  );
  z-index: 9999;
}

/* ── Container ── */
.gradio-container {
  max-width: 860px !important;
  margin: 0 auto !important;
  padding: 32px 24px 48px !important;
  font-family: 'JetBrains Mono', monospace !important;
}

/* ── Title ── */
.gradio-container h1 {
  color: #39ff14 !important;
  font-size: 22px !important;
  font-weight: 600 !important;
  letter-spacing: 0.04em !important;
  margin: 0 0 4px !important;
  text-align: left !important;
  font-family: 'JetBrains Mono', monospace !important;
}
.gradio-container h1::before { content: '> '; opacity: 0.4; }

/* ── Chatbot ── */
.chatbot .label-wrap, .chatbot label { display: none !important; }
.chatbot, .chatbot.block { min-height: 600px !important; }

/* ── Message bubbles ── */
[data-testid="user"] {
  background: #181818 !important;
  color: #39ff14 !important;
  border-left: 2px solid #39ff14 !important;
  border-radius: 0 !important;
  padding: 10px 14px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 13px !important;
}
[data-testid="user"] * {
  color: #39ff14 !important;
  background: transparent !important;
  font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="bot"] {
  background: transparent !important;
  color: #e0e0e0 !important;
  border-left: 2px solid #1a7a08 !important;
  border-radius: 0 !important;
  padding: 10px 14px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 13px !important;
}
[data-testid="bot"] * {
  color: #e0e0e0 !important;
  background: transparent !important;
  font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="bot"] a { color: #39ff14 !important; }

/* Strip default bubble chrome */
.message, .message.panel-full-width {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  border-radius: 0 !important;
}

/* ── Input ── */
textarea {
  caret-color: #39ff14;
  font-family: 'JetBrains Mono', monospace !important;
}
textarea:focus {
  box-shadow: 0 0 0 1px #39ff14, 0 0 8px rgba(57,255,20,0.12) !important;
}

/* ── Examples ── */
.examples button, [data-testid="examples"] button {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 12px !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  text-align: left !important;
  padding: 8px 12px !important;
}
.examples button:hover, [data-testid="examples"] button:hover,
.examples button:hover *, [data-testid="examples"] button:hover * {
  color: #39ff14 !important;
  background: #111111 !important;
  border-color: #39ff14 !important;
}

/* ── Avatar ── */
.bot-row .avatar-container {
  width: 52px !important;
  height: 52px !important;
  min-width: 52px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: hidden !important;
}
.bot-row .avatar-container .avatar-image,
.avatar-container:not(.thumbnail-item) img {
  width: 52px !important;
  height: 52px !important;
  min-width: 52px !important;
  min-height: 52px !important;
  padding: 0 !important;
  object-fit: cover !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; }
::-webkit-scrollbar-thumb:hover { background: #39ff14; }

/* ── Selection ── */
::selection { background: #39ff14; color: #000; }

/* ── Mobile ── */
@media (max-width: 640px) {
  .gradio-container { padding: 20px 12px 36px !important; }
  .gradio-container h1 { font-size: 18px !important; }
}
"""

JS = """
() => {
  document.title = 'Digital Twin';

  const focusInput = () => {
    const areas = document.querySelectorAll('textarea');
    if (areas.length) areas[areas.length - 1].focus();
  };
  setTimeout(focusInput, 300);

  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const scan = () => document.querySelectorAll('textarea').forEach(watchTextarea);
  setTimeout(scan, 500);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""
