from functools import lru_cache
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from fastapi import Depends, Header, HTTPException, status
from app.core.config import settings


@lru_cache(maxsize=1)
def _firebase_app():
    if not settings.firebase_project_id:
        raise RuntimeError("FIREBASE_PROJECT_ID is not configured")
    try:
        return firebase_admin.get_app()
    except ValueError:
        return firebase_admin.initialize_app(
            credentials.ApplicationDefault(),
            {"projectId": settings.firebase_project_id},
        )


def require_authenticated_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        claims = firebase_auth.verify_id_token(token, app=_firebase_app(), check_revoked=True)
        return {
            "firebase_uid": claims["uid"],
            "email": claims.get("email"),
            "name": claims.get("name"),
            "email_verified": claims.get("email_verified", False),
        }
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc
