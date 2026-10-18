"""
==================================================
CommuteShare User Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- Current User Profile
- Update Profile
- Get User by ID
- Deactivate Account
==================================================
"""

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_active_user,
    get_db,
)

from app.models.user import User

from app.schemas.user import (
    UserPublic,
    UserResponse,
    UserUpdate,
)

from app.services.user_service import (
    deactivate_user,
    get_user_by_id,
    update_user_profile,
)
from app.core.config import settings

AVATAR_DIRECTORY = Path(__file__).resolve().parents[3] / "uploads" / "avatars"
IMAGE_SIGNATURES = {
    "image/jpeg": (b"\xff\xd8\xff", ".jpg"),
    "image/png": (b"\x89PNG\r\n\x1a\n", ".png"),
    "image/webp": (b"RIFF", ".webp"),
}

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Store a bounded, validated avatar locally for the current user."""
    limit = settings.MAX_PROFILE_IMAGE_SIZE_MB * 1024 * 1024
    content = await file.read(limit + 1)
    if not content or len(content) > limit:
        raise HTTPException(status_code=413, detail="Avatar must be non-empty and no larger than the configured limit.")

    detected = next(
        ((extension, signature) for mime, (signature, extension) in IMAGE_SIGNATURES.items()
         if file.content_type == mime and content.startswith(signature)),
        None,
    )
    if detected is None or (detected[0] == ".webp" and content[8:12] != b"WEBP"):
        raise HTTPException(status_code=415, detail="Upload a valid JPEG, PNG, or WebP image.")

    extension, _ = detected
    AVATAR_DIRECTORY.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    destination = AVATAR_DIRECTORY / filename
    old_image = current_user.profile_image
    try:
        destination.write_bytes(content)
        current_user.profile_image = f"/uploads/avatars/{filename}"
        db.commit()
        db.refresh(current_user)
    except Exception:
        db.rollback()
        destination.unlink(missing_ok=True)
        raise

    if old_image and old_image.startswith("/uploads/avatars/"):
        old_path = (AVATAR_DIRECTORY / Path(old_image).name).resolve()
        if old_path.parent == AVATAR_DIRECTORY.resolve() and old_path != destination:
            old_path.unlink(missing_ok=True)
    return current_user


# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user(
    current_user: User = Depends(get_current_active_user),
):
    """
    Return the currently authenticated user.
    """

    return current_user


# ==========================================================
# Get User By ID
# ==========================================================

@router.get(
    "/{user_id}",
    response_model=UserPublic,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_active_user),
):
    """
    Return a user by ID.
    """

    return get_user_by_id(
        db=db,
        user_id=user_id,
    )


# ==========================================================
# Update Profile
# ==========================================================

@router.put(
    "/me",
    response_model=UserResponse,
)
def update_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update current user's profile.
    """

    return update_user_profile(
        db=db,
        current_user=current_user,
        user_data=user_data,
    )


# ==========================================================
# Deactivate Account
# ==========================================================

@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Deactivate the current user's account.
    """

    deactivate_user(
        db=db,
        current_user=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
