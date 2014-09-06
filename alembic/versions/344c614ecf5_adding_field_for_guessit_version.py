"""adding field for guessit version

Revision ID: 344c614ecf5
Revises: 1fd7d7a76cac
Create Date: 2014-09-06 10:53:55.814622

"""

# revision identifiers, used by Alembic.
revision = '344c614ecf5'
down_revision = '1fd7d7a76cac'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('submission', sa.Column('guessit_version', sa.String(20)))


def downgrade():
    op.drop_column('submission', 'guessit_version')
