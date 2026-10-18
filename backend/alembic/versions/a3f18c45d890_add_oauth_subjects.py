"""add OAuth provider subjects to users

Revision ID: a3f18c45d890
Revises: 6f8379b0c75a
Create Date: 2026-10-18

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a3f18c45d890"
down_revision: Union[str, None] = "6f8379b0c75a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("google_subject", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("github_subject", sa.String(length=255), nullable=True))
    op.create_unique_constraint("uq_users_google_subject", "users", ["google_subject"])
    op.create_unique_constraint("uq_users_github_subject", "users", ["github_subject"])


def downgrade() -> None:
    op.drop_constraint("uq_users_github_subject", "users", type_="unique")
    op.drop_constraint("uq_users_google_subject", "users", type_="unique")
    op.drop_column("users", "github_subject")
    op.drop_column("users", "google_subject")
