"""add few last columns

Revision ID: a18661640eef
Revises: 8fba258650c0
Create Date: 2024-08-02 18:36:41.201412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a18661640eef'
down_revision: Union[str, None] = '8fba258650c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE"))
    op.add_column("posts", 
                  sa.Column("created_at", sa.TIMESTAMP(timezone=False), nullable=False, server_default = sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
