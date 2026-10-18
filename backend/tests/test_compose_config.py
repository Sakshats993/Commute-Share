import re
from pathlib import Path
from urllib.parse import urlparse


def test_compose_database_credentials_match_backend_example():
    project_root = Path(__file__).resolve().parents[2]
    compose = (project_root / "docker-compose.yml").read_text(encoding="utf-8")
    environment_example = (project_root / "backend/.env.example").read_text(encoding="utf-8")

    configured_url = re.search(r"^DATABASE_URL=(.+)$", environment_example, re.MULTILINE)
    compose_user = re.search(r"^\s+POSTGRES_USER:\s*(\S+)\s*$", compose, re.MULTILINE)
    compose_password = re.search(r"^\s+POSTGRES_PASSWORD:\s*(\S+)\s*$", compose, re.MULTILINE)

    assert configured_url and compose_user and compose_password
    database_url = urlparse(configured_url.group(1))

    assert database_url.hostname == "postgres"
    assert database_url.username == compose_user.group(1)
    assert database_url.password == compose_password.group(1)


def test_frontend_compose_build_has_a_vite_dockerfile():
    project_root = Path(__file__).resolve().parents[2]
    dockerfile = (project_root / "frontend/Dockerfile").read_text(encoding="utf-8")

    assert "FROM node:22-alpine" in dockerfile
    assert "RUN npm ci" in dockerfile
    assert "EXPOSE 5173" in dockerfile


def test_compose_allows_untracked_backend_environment_overrides():
    project_root = Path(__file__).resolve().parents[2]
    compose = (project_root / "docker-compose.yml").read_text(encoding="utf-8")

    assert "path: ./backend/.env" in compose
    assert "required: false" in compose
