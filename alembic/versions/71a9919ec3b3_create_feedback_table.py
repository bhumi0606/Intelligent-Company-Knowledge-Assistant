"""create feedback table

Revision ID: 71a9919ec3b3
Revises: f21e693d078e
Create Date: 2026-08-11 11:06:35.978800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71a9919ec3b3'
down_revision: Union[str, Sequence[str], None] = 'f21e693d078e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.String()),
        sa.Column("question", sa.Text()),
        sa.Column("retrieved_chunks", sa.Text()),
        sa.Column("final_answer", sa.Text()),
        sa.Column("feedback", sa.String()),
        sa.Column("timestamp", sa.DateTime())
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(
        "feedback"
    )
