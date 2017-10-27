"""removed_send_cta_updates_field_from_presencebrowsingdata_table

Revision ID: 69b0bfeafe08
Revises: ff5a4e3cacbf
Create Date: 2017-08-29 16:21:31.879756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69b0bfeafe08'
down_revision = 'ff5a4e3cacbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('presencebrowsingdata', 'send_cta_updates')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('presencebrowsingdata', sa.Column('send_cta_updates', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###