"""Add model Document

Revision ID: 26cb3319bd72
Revises: a05dcd317276
Create Date: 2023-08-23 09:19:32.846247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26cb3319bd72'
down_revision = 'a05dcd317276'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=128), nullable=True),
    sa.Column('path', sa.String(length=256), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document')
    # ### end Alembic commands ###
