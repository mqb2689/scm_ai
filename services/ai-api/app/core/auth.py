import secrets
from fastapi import Header, HTTPException, status

from app.core.config import get_settings


async def require_api_key(authorization: str | None = Header(default=None)) -> None:
    """Protect API endpoints with a shared bearer token when API_KEY is configured.

    An empty API_KEY disables authentication for local development only.
    Production deployments should use proper user identity and authorization.
    """
    expected = get_settings().api_key
    if not expected:
        return

    scheme, _, supplied = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
