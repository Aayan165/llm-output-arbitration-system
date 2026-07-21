from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.client import supabase

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        token = credentials.credentials

        user = supabase.auth.get_user(token)

        return user.user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )