"""add content to posts

Revision ID: c73b5956639e
Revises: e91141540148
Create Date: 2024-08-02 18:13:14.744454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c73b5956639e'
down_revision: Union[str, None] = 'e91141540148'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
