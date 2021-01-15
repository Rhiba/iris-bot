"""add reminder table


Revision ID: ae0af00faee0
Revises: acf540f0dfcf
Create Date: 2020-06-07 13:56:12.606791

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'ae0af00faee0'
down_revision = 'acf540f0dfcf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'reminder',
        sa.Column('id',sa.Integer,primary_key=True),
        sa.Column('user_id',sa.Integer,sa.ForeignKey('user.id'),nullable=False),
        sa.Column('channel_id',sa.Integer,nullable=False),
        sa.Column('trigger_time',sa.DateTime,nullable=False),
        sa.Column('content',sa.String,nullable=False),
        sa.Column('added',sa.DateTime,nullable=False,default=datetime.utcnow()),
        # if persistent, PMs user every 5 mins until they reply 'done',
        # else, tags user once in channel sent from
        sa.Column('persistent',sa.Boolean,nullable=False,default=False),
        # if first PM has been sent but no "done" yet, we are in snooze mode
        # (if persistent=false, then snooze is always false)
        sa.Column('snoozed',sa.Boolean,nullable=False,default=False),
        sa.Column('done',sa.Boolean,nullable=False,default=False)
    )


def downgrade():
    op.drop_table('reminder')
