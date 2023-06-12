"""alter user_uuid_fk audiofiles

Revision ID: e2c02f2b8f1a
Revises: ed4531c2a096
Create Date: 2023-06-12 19:10:57.262082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2c02f2b8f1a'
down_revision = 'ed4531c2a096'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('audiofiles_user_uuid_key', 'audiofiles', type_='unique')
    op.drop_constraint('audiofiles_user_uuid_fkey', 'audiofiles', type_='foreignkey')
    op.create_foreign_key(None, 'audiofiles', 'users', ['user_uuid'], ['uuid'], source_schema='content', referent_schema='content')


def downgrade() -> None:
    op.drop_constraint(None, 'audiofiles', schema='content', type_='foreignkey')
    op.create_foreign_key('audiofiles_user_uuid_fkey', 'audiofiles', 'users', ['user_uuid'], ['uuid'])
    op.create_unique_constraint('audiofiles_user_uuid_key', 'audiofiles', ['user_uuid'])
