# CLAUDE.md — LLM Chatbot V1

Local LLM chatbot using LM Studio as the model backend.

## Architecture

- LM Studio hosts an open-source LLM locally with an OpenAI-compatible API
- Python chat client connects to the local LM Studio endpoint
- Conversation memory and cache management included

## Running

```bash
# 1. Install and start LM Studio, load a model, start the local server
# 2. Run the chatbot
pip install openai
python chatbot.py
```

The chat client connects to LM Studio's local API endpoint (default: `http://localhost:1234/v1`).
