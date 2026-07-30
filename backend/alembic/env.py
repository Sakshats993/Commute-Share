"""
==================================================
CommuteShare Alembic Environment

Backend Internship Project
Bermer Software Private Limited

Configures Alembic for database migrations.
==================================================
"""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.core.config import settings
from app.database.base import Base

# Import all models so Alembic can detect them
import app.database.base  # noqa: F401

# ==========================================================
# Alembic Configuration
# ==========================================================

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ==========================================================
# Offline Migrations
# ==========================================================

def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


# ==========================================================
# Online Migrations
# ==========================================================

def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    connectable = engine_from_config(
        configuration=config.get_section(
            config.config_ini_section
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ==========================================================
# Entry Point
# ==========================================================

if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()