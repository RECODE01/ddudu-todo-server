"""add challenge && shcedule models

Revision ID: 605519cd2d4a
Revises: 4ad2f9a39810
Create Date: 2022-06-10 10:10:59.187878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '605519cd2d4a'
down_revision = '4ad2f9a39810'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('challenge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('contents', sa.String(), nullable=True),
    sa.Column('start_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_challenge_id'), 'challenge', ['id'], unique=False)
    op.create_index(op.f('ix_challenge_name'), 'challenge', ['name'], unique=False)
    op.create_table('challengescheduledetail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('challenge_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('contents', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenge.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_challengescheduledetail_id'), 'challengescheduledetail', ['id'], unique=False)
    op.create_table('challengeuserdetail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_master', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('challenge_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenge.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_challengeuserdetail_id'), 'challengeuserdetail', ['id'], unique=False)
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('contents', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedule_id'), 'schedule', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_schedule_id'), table_name='schedule')
    op.drop_table('schedule')
    op.drop_index(op.f('ix_challengeuserdetail_id'), table_name='challengeuserdetail')
    op.drop_table('challengeuserdetail')
    op.drop_index(op.f('ix_challengescheduledetail_id'), table_name='challengescheduledetail')
    op.drop_table('challengescheduledetail')
    op.drop_index(op.f('ix_challenge_name'), table_name='challenge')
    op.drop_index(op.f('ix_challenge_id'), table_name='challenge')
    op.drop_table('challenge')
    # ### end Alembic commands ###
