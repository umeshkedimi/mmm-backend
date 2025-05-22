import os
from fastapi import Request, HTTPException

API_KEY = os.getenv("API_KEY_HEADER")

def verify_api_key(request: Request):
    header_key = request.headers.get("X-API-KEY")
    if not header_key or header_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized access")
