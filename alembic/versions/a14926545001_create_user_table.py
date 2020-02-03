"""create user table

Revision ID: a14926545001
Revises: 
Create Date: 2020-02-03 14:28:00.374442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a14926545001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id',sa.Integer,primary_key=True),
        sa.Column('uid',sa.BigInteger,nullable=False),
        sa.Column('admin',sa.Boolean,nullable=False,default=False)
    )


def downgrade():
    op.drop_table('user')
