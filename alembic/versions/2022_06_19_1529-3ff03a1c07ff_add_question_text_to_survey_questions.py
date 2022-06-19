"""add question_text to survey_questions

Revision ID: 3ff03a1c07ff
Revises: 415514445818
Create Date: 2022-06-19 15:29:36.479202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ff03a1c07ff'
down_revision = '415514445818'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('survey_questions', sa.Column('question_text', sa.Text, nullable=False))


def downgrade():
    op.drop_column('survey_questions', 'question_text')
