from app.core.security import create_access_token
from app.models.enums import UserRole
from app.models.user import User
import app.api.routes.users as users_routes


def _auth_header(db, email="avatar@example.com"):
    user = User(
        full_name="Avatar User",
        email=email,
        password_hash="test-hash",
        role=UserRole.PASSENGER,
    )
    db.add(user)
    db.commit()
    return {"Authorization": f"Bearer {create_access_token(email)}"}


def test_upload_avatar_saves_local_image_and_updates_profile(client, db, tmp_path, monkeypatch):
    monkeypatch.setattr(users_routes, "AVATAR_DIRECTORY", tmp_path)
    response = client.post(
        "/users/me/avatar",
        headers=_auth_header(db),
        files={"file": ("avatar.png", b"\x89PNG\r\n\x1a\nimage-data", "image/png")},
    )

    assert response.status_code == 200, response.text
    avatar = response.json()["profile_image"]
    assert avatar.startswith("/uploads/avatars/")
    assert len(list(tmp_path.iterdir())) == 1


def test_upload_avatar_rejects_mismatched_image_content(client, db, tmp_path, monkeypatch):
    monkeypatch.setattr(users_routes, "AVATAR_DIRECTORY", tmp_path)
    response = client.post(
        "/users/me/avatar",
        headers=_auth_header(db, "invalid-avatar@example.com"),
        files={"file": ("avatar.png", b"not an image", "image/png")},
    )

    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []
