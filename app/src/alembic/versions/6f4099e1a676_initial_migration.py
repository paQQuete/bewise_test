"""initial migration

Revision ID: 6f4099e1a676
Revises: 
Create Date: 2023-06-12 23:53:13.763761

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6f4099e1a676'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('''CREATE SCHEMA IF NOT EXISTS content;
ALTER ROLE app SET search_path TO content,public;
CREATE EXTENSION "uuid-ossp";''')
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
    op.create_table('users',
                    sa.Column('username', sa.String(length=50), nullable=False),
                    sa.Column('token', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('token'),
                    schema='content'
                    )
    op.create_index(op.f('ix_content_users_username'), 'users', ['username'], unique=True, schema='content')
    op.create_table('audiofiles',
                    sa.Column('wav_file', sa.String(length=255), nullable=True),
                    sa.Column('mp3_file', sa.String(length=255), nullable=True),
                    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(['user_uuid'], ['content.users.uuid'], ),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('mp3_file'),
                    sa.UniqueConstraint('wav_file'),
                    schema='content'
                    )


def downgrade() -> None:
    op.drop_table('audiofiles', schema='content')
    op.drop_index(op.f('ix_content_users_username'), table_name='users', schema='content')
    op.drop_table('users', schema='content')
    op.drop_index(op.f('ix_content_questions_query_session'), table_name='questions', schema='content')
    op.drop_index(op.f('ix_content_questions_id'), table_name='questions', schema='content')
    op.drop_table('questions', schema='content')
    op.execute('''DROP SCHEMA content CASCADE;''')
