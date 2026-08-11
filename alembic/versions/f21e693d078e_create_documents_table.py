"""create documents table

Revision ID: f21e693d078e
Revises: 
Create Date: 2026-08-11 11:00:31.743258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f21e693d078e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("file_name", sa.String()),
        sa.Column("upload_date", sa.Date()),
        sa.Column("department", sa.String())
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(
        "documents"
    )
