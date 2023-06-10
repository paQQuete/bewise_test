"""initial migration

Revision ID: d6eeec628f8b
Revises: 
Create Date: 2023-06-10 22:12:53.614105

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd6eeec628f8b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE SCHEMA IF NOT EXISTS content;
    ALTER ROLE app SET search_path TO content,public;
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""")
    op.create_table('questions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('question', sa.String(length=255), nullable=False),
                    sa.Column('answer', sa.String(length=255), nullable=False),
                    sa.Column('question_created_at', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('query_session', sa.Integer(), nullable=False),
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    schema='content'
                    )
    op.create_index(op.f('ix_content_questions_id'), 'questions', ['id'], unique=True, schema='content')
    op.create_index(op.f('ix_content_questions_query_session'), 'questions', ['query_session'], unique=False,
                    schema='content')


def downgrade() -> None:
    op.drop_index(op.f('ix_content_questions_query_session'), table_name='questions', schema='content')
    op.drop_index(op.f('ix_content_questions_id'), table_name='questions', schema='content')
    op.drop_table('questions', schema='content')
    op.execute("""DROP SCHEMA content CASCADE;""")