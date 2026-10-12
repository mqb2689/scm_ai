# Private Domain AI

A local-first AI starter for Purchasing, Logistics, Sourcing, and Warehouse workflows.

## What this starter includes

- FastAPI backend
- Local LLM inference through Ollama
- Local document retrieval (RAG) using Ollama embeddings
- Simple document ingestion for `.md` and `.txt` files
- Bearer-token protection when `API_KEY` is configured
- Basic tests, Docker Compose, security notes, and an evaluation dataset template

This is a starter codebase, not a production-certified system. Begin with synthetic or approved non-sensitive data.

## Architecture

```text
Internal user
    |
    v
FastAPI (services/ai-api)
    |-- Ollama chat model (local)
    |-- Ollama embedding model (local)
    |-- Local knowledge files (data/knowledge)
    `-- In-memory retrieval index
```

## Requirements

- Docker Desktop with Docker Compose, or Python 3.11+
- For useful local inference, enough RAM/CPU/GPU for the selected model
- No cloud AI API is required by this codebase

## Quick start with Docker Compose

1. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

   On Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env`. Set a strong `API_KEY` before exposing the service to any other device. Keep the service bound to localhost unless you have configured network controls.

3. Start the services:

   ```bash
   docker compose up -d --build
   ```

4. Pull the models into the local Ollama container:

   ```bash
   docker compose exec ollama ollama pull qwen2.5:3b
   docker compose exec ollama ollama pull nomic-embed-text
   ```

   Model availability, licensing, memory requirements, and performance vary. Review the model license before business use.

5. Check health:

   ```bash
   curl http://localhost:8000/health
   ```

6. Add approved `.md` or `.txt` documents to `data/knowledge/`, then re-index:

   ```bash
   curl -X POST http://localhost:8000/api/knowledge/reindex \
     -H "Authorization: Bearer change-me"
   ```

   Replace `change-me` with the `API_KEY` value in `.env`. If `API_KEY` is empty, authentication is disabled; do not use that setting outside local development.

7. Ask a question:

   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer change-me" \
     -d "{\"message\":\"What should be checked before approving a purchase order?\"}"
   ```

   On PowerShell, `curl` may be an alias; use `curl.exe` or `Invoke-RestMethod` if needed.

8. Open interactive API docs at `http://localhost:8000/docs`.

## Run without Docker

Run Ollama separately, then from `services/ai-api`:

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Set environment variables from `.env.example` or your shell, then run:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

When running Python directly, set `OLLAMA_BASE_URL=http://localhost:11434`.

## API endpoints

- `GET /health` — service health (does not prove the model is loaded)
- `GET /api/knowledge/status` — indexed document/chunk counts
- `POST /api/knowledge/reindex` — re-index local `.md` and `.txt` files
- `POST /api/chat` — answer a question using retrieved internal documents where available

## Repository structure

```text
apps/web/                     # Reserved for a future web UI
services/ai-api/app/
  api/                         # HTTP endpoints
  core/                        # Configuration and authentication
  llm/                         # Ollama client
  rag/                         # Local document ingestion and retrieval
  schemas/                     # Request/response models
  main.py
  tests/
data/knowledge/                # Put approved, non-sensitive starter documents here
data/evaluation/               # Example evaluation questions
docs/                          # Architecture, security, roadmap
```

## Development checks

From `services/ai-api`:

```bash
pip install -r requirements-dev.txt
pytest
ruff check app tests
```

## Security checklist before sharing or deploying

- Keep the GitHub repository private if the project or code is confidential.
- Never commit `.env`, secrets, real purchase orders, supplier quotations, contracts, database dumps, logs, or model weights.
- The `.gitignore` is not a data-loss-prevention system. Check staged files before every push.
- Configure `API_KEY`; use a long random value. This starter uses one shared token and is not a replacement for enterprise identity/RBAC.
- Keep the API bound to localhost unless network access is intentionally configured.
- Restrict outbound network access if the requirement is fully offline. Docker image/model downloads require connectivity during setup.
- Review Ollama/model telemetry and all dependencies against company policy.
- Treat retrieved documents as untrusted input. Do not let the model execute arbitrary SQL, shell commands, or write operations.
- The current retrieval index is in memory and is rebuilt on restart. It is intended for a small prototype, not a multi-user production deployment.
- Add user-level identity, role-based data filtering, audit logging, encrypted backups, rate limiting, and formal security testing before production.

## Roadmap

1. Add structured document parsers for PDF/DOCX/XLSX.
2. Add a persistent local vector store and metadata filters.
3. Integrate read-only, allowlisted business APIs.
4. Add per-user authentication and role-based authorization.
5. Add an evaluation harness for answer correctness, citations, latency, and refusal behavior.
6. Add a user interface and operational monitoring.
