"""Initial migration

Revision ID: 82994cf9c23d
Revises: 
Create Date: 2023-12-12 19:11:18.702558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82994cf9c23d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('first_name', sa.Text(), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('location', sa.Text(), nullable=True),
    sa.Column('user_gender', sa.Integer(), nullable=False),
    sa.Column('preferred_genders', sa.Integer(), nullable=False),
    sa.Column('passions', sa.Integer(), nullable=False),
    sa.Column('additional', sa.Text(), nullable=True),
    sa.Column('receive_email', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
