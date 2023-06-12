"""added audiofiles

Revision ID: ed4531c2a096
Revises: 6146ac320e62
Create Date: 2023-06-12 04:22:16.223953

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ed4531c2a096'
down_revision = '6146ac320e62'
branch_labels = None
depends_on = None


def upgrade() -> None:
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
                    sa.UniqueConstraint('user_uuid'),
                    sa.UniqueConstraint('wav_file'),
                    schema='content'
                    )


def downgrade() -> None:
    op.drop_table('audiofiles', schema='content')
