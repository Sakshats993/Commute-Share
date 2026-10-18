"""
==================================================
CommuteShare Test Configuration

Backend Internship Project
Bermer Software Private Limited

Shared pytest fixtures for the backend test suite.

Provides:
- Test database
- Test client
- Database session
==================================================
"""

from __future__ import annotations

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.core.deps import get_db
from app.database.session import Base
from main import app


# ==========================================================
# Test Database
# ==========================================================

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ==========================================================
# Database Fixture
# ==========================================================

@pytest.fixture(scope="function")
def db():
    """
    Create a fresh database
    for every test.
    """

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:

        yield session

    finally:

        session.close()

        Base.metadata.drop_all(bind=engine)


# ==========================================================
# Dependency Override
# ==========================================================

@pytest.fixture(scope="function")
def client(db):
    """
    FastAPI test client.
    """

    def override_get_db():

        try:

            yield db

        finally:

            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:

        yield test_client

    app.dependency_overrides.clear()
