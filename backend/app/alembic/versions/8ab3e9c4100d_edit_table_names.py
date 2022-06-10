"""edit table names

Revision ID: 8ab3e9c4100d
Revises: 7fa1438d1e71
Create Date: 2022-06-10 10:21:22.688084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ab3e9c4100d'
down_revision = '7fa1438d1e71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('challenge_info_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'schedule', 'challenge_schedule_detail', ['challenge_info_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_column('schedule', 'challenge_info_id')
    # ### end Alembic commands ###
