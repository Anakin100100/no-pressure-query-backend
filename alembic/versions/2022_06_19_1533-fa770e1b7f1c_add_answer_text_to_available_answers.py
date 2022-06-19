"""add answer_text to available_answers

Revision ID: fa770e1b7f1c
Revises: 3ff03a1c07ff
Create Date: 2022-06-19 15:33:10.305792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa770e1b7f1c'
down_revision = '3ff03a1c07ff'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('available_answers', sa.Column('answer_text', sa.Text, nullable=False))


def downgrade():
    op.drop_column('available_answers', 'answer_text')
