# api/auth.py
import os
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """FastAPI dependency that validates the X-API-Key header.

    The expected key is loaded from the API_KEY environment variable.
    Returns 403 if the key is missing or invalid.
    """
    expected_key = os.getenv("API_KEY", "")
    if not api_key or api_key != expected_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API key",
        )
    return api_key
