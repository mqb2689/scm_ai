# Security baseline

## Before use

- Set a strong `API_KEY`; never use `change-me` beyond a local smoke test.
- Keep host port binding on `127.0.0.1` unless a deliberate deployment review approves wider access.
- Do not put sensitive data in Git, issues, pull requests, logs, or test fixtures.
- Use synthetic data for development and evaluation.
- Review the license and provenance of every model and dependency.
- Restrict outbound network access after downloading approved images and model files if fully offline operation is required.
- Keep API and Ollama ports inaccessible from untrusted networks.
- Apply OS disk encryption and secure backups.

## Important limitations

This starter does not implement enterprise SSO, per-user RBAC, document-level ACLs, rate limiting, tamper-resistant audit logging, or production secrets management. Do not treat a shared API key as adequate multi-user security.

Retrieved document content is untrusted. The model must not be given unrestricted shell access, arbitrary SQL access, or unrestricted write tools. Any future business action should be allowlisted, permission-checked server-side, logged, and require approval when appropriate.
