"""add users table

Revision ID: fb85de9b33ce
Revises: 
Create Date: 2022-06-19 09:10:37.540345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb85de9b33ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String(50), nullable=False, index=True),
        sa.Column("hashed_password", sa.String(128), nullable=False),
        sa.Column("first_name", sa.String(32), nullable=False),
        sa.Column("last_name", sa.String(32), nullable=False)
    )


def downgrade():
    #I don't know why it happens but the table is not dropped using op.drop_table("users")
    op.execute("DROP TABLE users")
