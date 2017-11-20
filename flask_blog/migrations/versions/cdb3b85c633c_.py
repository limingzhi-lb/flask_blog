"""empty message

Revision ID: cdb3b85c633c
Revises: 
Create Date: 2017-10-27 11:03:18.870891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdb3b85c633c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('icon', sa.String(length=64), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rid', sa.Integer(), nullable=True),
    sa.Column('rrid', sa.Integer(), nullable=True),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_rid'), 'posts', ['rid'], unique=False)
    op.create_index(op.f('ix_posts_rrid'), 'posts', ['rrid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_posts_rrid'), table_name='posts')
    op.drop_index(op.f('ix_posts_rid'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###
