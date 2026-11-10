from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.auth import require_authenticated_user
from app.core.database import get_db
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


class ProfileSyncRequest(BaseModel):
    preferred_locale: str = Field(default="en", pattern="^(en|hi)$")
    display_name: str | None = Field(default=None, max_length=150)


@router.post("/sync")
def sync_profile(
    payload: ProfileSyncRequest,
    identity: dict = Depends(require_authenticated_user),
    db: Session = Depends(get_db),
):
    email = identity.get("email")
    if not email or not identity.get("email_verified", False):
        raise HTTPException(status_code=400, detail="A verified email address is required")
    user = db.scalar(select(User).where(User.firebase_uid == identity["firebase_uid"]))
    if user is None:
        user = User(
            firebase_uid=identity["firebase_uid"],
            email=email.lower(),
            name=payload.display_name or identity.get("name"),
            preferred_locale=payload.preferred_locale,
        )
        db.add(user)
    else:
        if user.email != email.lower():
            user.email = email.lower()
        if payload.display_name is not None:
            user.name = payload.display_name
        user.preferred_locale = payload.preferred_locale
    db.commit()
    db.refresh(user)
    return {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "preferred_locale": user.preferred_locale,
        "status": user.status,
    }


@router.get("/me")
def get_me(
    identity: dict = Depends(require_authenticated_user),
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.firebase_uid == identity["firebase_uid"]))
    if user is None:
        raise HTTPException(status_code=404, detail="Profile not initialized; call POST /auth/sync")
    return {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "preferred_locale": user.preferred_locale,
        "status": user.status,
    }
