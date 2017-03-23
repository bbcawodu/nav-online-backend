"""added send_cta_updates to presencebrowsingdata table

Revision ID: 70c67b81da38
Revises: 48032ee3ef4f
Create Date: 2017-03-21 13:56:12.275329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70c67b81da38'
down_revision = '48032ee3ef4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('presencebrowsingdata', sa.Column('send_cta_updates', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('presencebrowsingdata', 'send_cta_updates')
    # ### end Alembic commands ###
