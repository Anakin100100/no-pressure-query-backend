"""add users

Revision ID: 1dd485cd6a63
Revises: 
Create Date: 2022-06-08 14:19:25.345457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1dd485cd6a63"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String(50), nullable=False, index=True),
        sa.Column("hashed_password", sa.String(128)),
        sa.Column("is_active", sa.Boolean, default=True),
    )

    op.create_table(
        "items",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("title", sa.String(100), nullable=False, index=True),
        sa.Column("description", sa.String(1000)),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id")),
    )


def downgrade():
    op.drop_table("items")
    op.drop_table("users")
