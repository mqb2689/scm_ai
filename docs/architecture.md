# Architecture

## Design principles

1. Local-first inference and retrieval.
2. Keep model weights and business documents outside Git.
3. Separate domain logic from the LLM provider.
4. Enforce authorization in the API/data layer, never through prompt instructions alone.
5. Start read-only; introduce write actions only with explicit authorization and approval.

## Current request flow

1. Client sends a question to FastAPI.
2. API checks the configured shared bearer token.
3. Retrieval embeds the question through the local Ollama embedding model.
4. The in-memory index ranks document chunks using cosine similarity.
5. FastAPI sends the question and retrieved excerpts to the local chat model.
6. API returns the answer and source filenames.

## Current limitations

- Only `.md` and `.txt` are parsed.
- Retrieval index is in memory and not persistent.
- No user-level identity, tenant isolation, document ACL filtering, or audit log yet.
- No direct ERP/WMS/TMS integration.
- The shared API token is only a prototype guard.
