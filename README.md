# Personal_Assistant
Personal assistant AI architecture for plug and play with different APIs. The goal is to create a cross compatible agent framework.

# Modular AI Agent Operating System (AI OS)

This repository is a foundation for a modular AI OS built in Python with FastAPI, SQLite, and OpenAI abstraction.

## Folder structure

- `ai-os/` - package entrypoint
- `agents/` - agent definitions and configuration
- `core/` - agent core classes, router, tools, LLM client, memory store
- `tools/` - tool implementations and helpers
- `prompts/` - prompt templates (static data)
- `db/` - SQLite DB file
- `api/` - FastAPI app
- `cli/` - interactive CLI chat script

## Quick start

1. Create a venv and install dependencies

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic openai
```

2. Run API

```powershell
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

3. Run CLI

```powershell
python cli/chat.py
```

## Notes

- `core/memory.py` initializes `db/ai_os.db` with required tables
- `api/app.py` includes endpoints:
	- `GET /agents`
	- `POST /chat`
	- `POST /tools/test`
	- `GET /memory/messages`

- The router is keyword-based for now and can be extended for LLM-based routing.
