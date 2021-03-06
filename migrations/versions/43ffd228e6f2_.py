"""empty message

Revision ID: 43ffd228e6f2
Revises: 
Create Date: 2017-12-04 20:20:14.076754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43ffd228e6f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Config_Variable', sa.Text(), nullable=True),
    sa.Column('value', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Username', sa.String(length=50), nullable=False),
    sa.Column('Password', sa.String(length=120), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Username')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_role', sa.Enum('UNASSIGNED', 'NAUGHTY', 'NICE', name='roles'), nullable=False),
    sa.Column('User', sa.Integer(), nullable=True),
    sa.Column('voted_round1', sa.Text(), nullable=True),
    sa.Column('voted_round2', sa.Text(), nullable=True),
    sa.Column('voted_round3', sa.Text(), nullable=True),
    sa.Column('voted_round4', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['User'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('round_id', sa.Integer(), nullable=True),
    sa.Column('vote_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['vote_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    op.drop_table('players')
    op.drop_table('users')
    op.drop_table('settings')
    # ### end Alembic commands ###
