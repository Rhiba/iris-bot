"""create karma tables

Revision ID: 7d378242ae54
Revises: a14926545001
Create Date: 2020-02-03 14:43:05.464381

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '7d378242ae54'
down_revision = 'a14926545001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'karma',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('added', sa.DateTime, nullable=False, default=datetime.utcnow()),
        sa.Column('pluses', sa.Integer, nullable=False, default=0),
        sa.Column('minuses', sa.Integer, nullable=False, default=0),
        sa.Column('neutrals', sa.Integer, nullable=False, default=0)
    )	

    op.create_table(
        'karma_changes',
        sa.Column('id',sa.Integer,primary_key=True, nullable=False),
        sa.Column('karma_id', sa.Integer, sa.ForeignKey('karma.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('changed_at', sa.DateTime, nullable=False, default=datetime.utcnow()),
        sa.Column('reason', sa.String, nullable=True),
        sa.Column('change', sa.Integer, nullable=False),
        sa.Column('score', sa.Integer, nullable=False)
    )


def downgrade():
    op.drop_table('karma')
    op.drop_table('karma_changes')
