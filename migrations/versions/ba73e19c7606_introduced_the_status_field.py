"""Introduced the status field

Revision ID: ba73e19c7606
Revises: d5ee6032984e
Create Date: 2019-04-01 03:27:00.054754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba73e19c7606'
down_revision = 'd5ee6032984e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('msg_status', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'msg_status')
    # ### end Alembic commands ###