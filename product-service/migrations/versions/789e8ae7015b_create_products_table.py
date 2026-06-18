"""create products table

Revision ID: 789e8ae7015b
Revises:
Create Date: ...
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "789e8ae7015b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("stock_quantity", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("products")