"""add gym tables (token table and notification table)

Revision ID: acf540f0dfcf
Revises: 4d0ee6472ce8
Create Date: 2020-02-21 14:29:35.708674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acf540f0dfcf'
down_revision = '4d0ee6472ce8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'gym_tokens',
        sa.Column('id',sa.Integer,primary_key=True),
        sa.Column('user_id',sa.Integer,sa.ForeignKey('user.id'),nullable=False),
        sa.Column('phpsessid',sa.String),
        sa.Column('csrf',sa.String),
        sa.Column('identity',sa.String),
        sa.Column('url',sa.String)
    )
    op.create_table(
        'gym_notifications',
        sa.Column('id',sa.Integer,primary_key=True),
        sa.Column('user_id',sa.Integer,sa.ForeignKey('user.id'),nullable=False),
        sa.Column('class_name',sa.String,nullable=False),
        sa.Column('class_time',sa.DateTime,nullable=False),
        sa.Column('notified',sa.Boolean,nullable=False,default=False)
    )

def downgrade():
    op.drop_table('gym_tokens')
    op.drop_table('gym_notifications')
