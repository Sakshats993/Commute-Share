"""
==================================================
CommuteShare Authentication Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- User Registration
- User Login
- Current User
- Password Change
==================================================
"""

import hmac
import secrets
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.core.deps import (
    get_current_active_user,
    get_db,
)
from app.core.config import settings
from app.core.security import create_access_token, hash_password

from app.models.user import User
from app.models.enums import UserRole

from app.schemas.auth import (
    ChangePasswordRequest,
    LoginResponse,
    PasswordResetConfirm,
    PasswordResetRequest,
)

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.services.auth_service import (
    change_password,
    login_user,
    request_password_reset,
    register_user,
    reset_password,
)
from app.services.audit_service import log_login, log_registration
from app.services.email_service import is_smtp_configured
from app.services.oauth_service import (
    OAuthProviderError,
    fetch_github_identity,
    fetch_google_identity,
)
from app.utils.logger import logger

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

OAUTH_PROVIDERS = {
    "google": {
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
    },
    "github": {
        "client_id": settings.GITHUB_OAUTH_CLIENT_ID,
        "client_secret": settings.GITHUB_OAUTH_CLIENT_SECRET,
    },
}


def _oauth_error_redirect(reason: str) -> RedirectResponse:
    query = urlencode({"oauth_error": reason})
    url = f"{settings.FRONTEND_URL.rstrip('/')}/login?{query}"
    return RedirectResponse(url, status_code=status.HTTP_302_FOUND)


def _provider_callback_url(provider: str) -> str:
    return f"{settings.BACKEND_PUBLIC_URL.rstrip('/')}/auth/oauth/{provider}/callback"


def _finish_oauth_login(provider: str, identity: dict, db: Session) -> str:
    subject_field = f"{provider}_subject"
    user = db.scalar(select(User).where(getattr(User, subject_field) == identity["subject"]))
    if user is None:
        user = db.scalar(
            select(User).where(func.lower(User.email) == identity["email"].lower())
        )
        if user is None:
            # Provider identity responses contain a verified email, but generally
            # do not contain a verified phone number. Keep OAuth signup available
            # without inventing one; users can add their phone in profile settings.
            user = User(
                full_name=(identity.get("full_name") or identity["email"].split("@", 1)[0])[:100],
                email=identity["email"].lower(),
                password_hash=hash_password(secrets.token_urlsafe(48)),
                profile_image=identity.get("profile_image"),
                role=UserRole.PASSENGER,
                **{subject_field: identity["subject"]},
            )
            db.add(user)
            try:
                db.commit()
                db.refresh(user)
            except IntegrityError:
                db.rollback()
                # Another callback may have created or linked this identity first.
                user = db.scalar(select(User).where(getattr(User, subject_field) == identity["subject"]))
                if user is None:
                    user = db.scalar(select(User).where(func.lower(User.email) == identity["email"].lower()))
                if user is None or getattr(user, subject_field) not in (None, identity["subject"]):
                    raise HTTPException(status_code=409, detail="This provider account is already linked.")
                if getattr(user, subject_field) is None:
                    setattr(user, subject_field, identity["subject"])
                    try:
                        db.commit()
                    except IntegrityError as exc:
                        db.rollback()
                        raise HTTPException(status_code=409, detail="This provider account is already linked.") from exc
            else:
                log_registration(db=db, user_id=user.id)
        elif not user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive.")
        elif getattr(user, subject_field):
            raise HTTPException(status_code=409, detail="This account is linked to a different provider identity.")
        else:
            setattr(user, subject_field, identity["subject"])
            try:
                db.commit()
            except IntegrityError as exc:
                db.rollback()
                raise HTTPException(status_code=409, detail="This provider account is already linked.") from exc

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive.")

    log_login(db=db, user_id=user.id)
    return create_access_token(subject=user.email)


def _oauth_callback(
    provider: str,
    *,
    code: str | None,
    state: str | None,
    provider_error: str | None,
    request: Request,
    db: Session,
) -> RedirectResponse:
    response: RedirectResponse
    cookie_name = f"commuteshare_oauth_state_{provider}"
    callback_path = f"/auth/oauth/{provider}/callback"
    state_cookie = request.cookies.get(cookie_name)

    if provider_error or not code or not state or not state_cookie or not hmac.compare_digest(state, state_cookie):
        response = _oauth_error_redirect("cancelled" if provider_error else "invalid_state")
    else:
        try:
            identity = (
                fetch_google_identity(code, _provider_callback_url(provider))
                if provider == "google"
                else fetch_github_identity(code, _provider_callback_url(provider))
            )
            access_token = _finish_oauth_login(provider, identity, db)
            callback = f"{settings.FRONTEND_URL.rstrip('/')}/oauth/callback#access_token={access_token}"
            response = RedirectResponse(
                callback,
                status_code=status.HTTP_302_FOUND,
                headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
            )
        except HTTPException as exc:
            reason = "account_required" if exc.status_code == 400 else "account_unavailable"
            response = _oauth_error_redirect(reason)
        except OAuthProviderError:
            response = _oauth_error_redirect("provider_error")
        except Exception:
            db.rollback()
            logger.exception("OAuth callback failed for {}", provider)
            response = _oauth_error_redirect("provider_error")

    response.delete_cookie(
        cookie_name,
        path=callback_path,
        secure=settings.BACKEND_PUBLIC_URL.lower().startswith("https://"),
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/providers")
def oauth_provider_status():
    """Expose provider availability without disclosing client secrets."""
    return {
        provider: bool(config["client_id"] and config["client_secret"])
        for provider, config in OAUTH_PROVIDERS.items()
    }


@router.get("/oauth/{provider}/start")
def oauth_start(provider: str):
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=404, detail="OAuth provider not supported.")
    config = OAUTH_PROVIDERS[provider]
    if not config["client_id"] or not config["client_secret"]:
        return _oauth_error_redirect("not_configured")
    if settings.ENVIRONMENT.strip().lower() in {"prod", "production"} and (
        not settings.BACKEND_PUBLIC_URL.lower().startswith("https://")
        or not settings.FRONTEND_URL.lower().startswith("https://")
    ):
        return _oauth_error_redirect("insecure_config")

    state = secrets.token_urlsafe(32)
    callback_url = _provider_callback_url(provider)
    if provider == "google":
        authorization_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode({
            "client_id": config["client_id"],
            "redirect_uri": callback_url,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
        })
    else:
        authorization_url = "https://github.com/login/oauth/authorize?" + urlencode({
            "client_id": config["client_id"],
            "redirect_uri": callback_url,
            "scope": "read:user user:email",
            "state": state,
        })

    redirect = RedirectResponse(authorization_url, status_code=status.HTTP_302_FOUND)
    redirect.set_cookie(
        f"commuteshare_oauth_state_{provider}",
        state,
        max_age=600,
        path=f"/auth/oauth/{provider}/callback",
        secure=settings.BACKEND_PUBLIC_URL.lower().startswith("https://"),
        httponly=True,
        samesite="lax",
    )
    return redirect


@router.get("/oauth/google/callback")
def google_oauth_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db),
):
    return _oauth_callback("google", code=code, state=state, provider_error=error, request=request, db=db)


@router.get("/oauth/github/callback")
def github_oauth_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db),
):
    return _oauth_callback("github", code=code, state=state, provider_error=error, request=request, db=db)


@router.post("/password-reset/request", status_code=status.HTTP_202_ACCEPTED)
def password_reset_request(
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    if not is_smtp_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Password reset email is not configured on this server.",
        )
    request_password_reset(db, str(reset_request.email))
    return {
        "message": "If an active account uses that email, password reset instructions will be sent.",
    }


@router.post("/password-reset/confirm", status_code=status.HTTP_204_NO_CONTENT)
def password_reset_confirmation(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    reset_password(db, reset_data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ==========================================================
# Register
# ==========================================================
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    return register_user(
        db=db,
        user_data=user_data,
    )

# ==========================================================
# Login
# ==========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_active_user,
    ),
):
    """
    Return current authenticated user.
    """

    return current_user

# ==========================================================
# Change Password
# ==========================================================

@router.put(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user,
    ),
):
    """
    Change current user's password.
    """

    change_password(
        db=db,
        current_user=current_user,
        password_data=password_data,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
