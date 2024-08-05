"""add fkey to post table

Revision ID: 8fba258650c0
Revises: 1b0480a1bc51
Create Date: 2024-08-02 18:29:20.487195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fba258650c0'
down_revision: Union[str, None] = '1b0480a1bc51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass
