"""Add position and department columns

Revision ID: a05dcd317276
Revises: f2415f3a30bc
Create Date: 2023-08-22 21:59:16.176233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a05dcd317276'
down_revision = 'f2415f3a30bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('department', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('position', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'position')
    op.drop_column('user', 'department')
    # ### end Alembic commands ###
