"""add command table

Revision ID: 4d0ee6472ce8
Revises: 7d378242ae54
Create Date: 2020-02-04 13:26:32.267812

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '4d0ee6472ce8'
down_revision = '7d378242ae54'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'command',
        sa.Column('id',sa.Integer,primary_key=True),
        sa.Column('user_id',sa.Integer,sa.ForeignKey('user.id'),nullable=False),
        sa.Column('name',sa.String,nullable=False),
        sa.Column('description',sa.String),
        sa.Column('command_string',sa.String,nullable=False),
        sa.Column('added',sa.DateTime,nullable=False,default=datetime.utcnow()),
        sa.Column('admin',sa.Boolean,nullable=False,default=False)
    )


def downgrade():
    op.drop_table('command')
