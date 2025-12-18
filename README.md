# AI Agent Toy

Small playground for a local AI coding agent (Gemini function-calling) plus a demo calculator app.

## What’s inside
- Agent entrypoint (`main.py`) that routes tool calls (list files, read/write files, run Python) inside a sandboxed working directory.
- Tool implementations in `functions/`: file info, file content, write file, run Python file.
- Calculator demo in `calculator/`: infix evaluator with operator precedence, JSON renderer, and unit tests.

## Prerequisites
- Python 3.10+
- `pip` (or `uv` if you prefer)  
- A `GEMINI_API_KEY` in a `.env` file at the repo root

Example `.env`:
