from fastapi import HTTPException, status, Depends
from fastapi.security import APIKeyHeader

from config import API_KEY

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str | None = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")