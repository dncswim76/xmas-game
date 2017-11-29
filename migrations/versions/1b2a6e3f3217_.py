"""empty message

Revision ID: 1b2a6e3f3217
Revises: 
Create Date: 2017-11-28 21:47:26.066174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b2a6e3f3217'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rounds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('round_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
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
    sa.Column('phone_number', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Username')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('User', sa.Integer(), nullable=True),
    sa.Column('player_role', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['User'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('round_id', sa.Integer(), nullable=True),
    sa.Column('votee_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['round_id'], ['rounds.id'], ),
    sa.ForeignKeyConstraint(['votee_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    op.drop_table('players')
    op.drop_table('users')
    op.drop_table('settings')
    op.drop_table('rounds')
    # ### end Alembic commands ###
