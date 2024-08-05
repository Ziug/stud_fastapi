"""add users table

Revision ID: 1b0480a1bc51
Revises: c73b5956639e
Create Date: 2024-08-02 18:18:23.449729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b0480a1bc51'
down_revision: Union[str, None] = 'c73b5956639e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer, nullable=False),
                    sa.Column("email",sa.String, nullable=False),
                    sa.Column("password",sa.String, nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=False), nullable = False, server_default = sa.text('now()')),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    op.drop_table(table_name="users")
    pass
