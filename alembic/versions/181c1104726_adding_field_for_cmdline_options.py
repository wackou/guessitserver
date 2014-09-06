"""adding field for cmdline options

Revision ID: 181c1104726
Revises: 344c614ecf5
Create Date: 2014-09-06 11:30:52.468013

"""

# revision identifiers, used by Alembic.
revision = '181c1104726'
down_revision = '344c614ecf5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('submission', sa.Column('options', sa.String()))


def downgrade():
    op.drop_column('submission', 'options')
