"""empty message

Revision ID: 1fd7d7a76cac
Revises: None
Create Date: 2014-02-17 17:32:09.022261

"""

# revision identifiers, used by Alembic.
revision = '1fd7d7a76cac'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('submission',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=1000), nullable=False),
        sa.Column('submit_date', sa.DateTime(), nullable=False),
        sa.Column('resolved', sa.Boolean(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=True),

        sa.PrimaryKeyConstraint('id'),
    )



def downgrade():
    op.drop_table('submission')
